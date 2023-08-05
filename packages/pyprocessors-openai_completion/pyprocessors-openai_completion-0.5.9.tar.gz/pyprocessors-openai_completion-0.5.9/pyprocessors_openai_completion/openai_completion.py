import collections
import os
from enum import Enum
from functools import lru_cache
from string import Template
from typing import List, cast, Type

import openai
from pydantic import Field, BaseModel
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, AltText


class OpenAIModel(str, Enum):
    davinci_instruct_beta = "davinci-instruct-beta"
    text_davinci_003 = "text-davinci-003"
    text_curie_001 = "text-curie-001"
    text_babbage_001 = "text-babbage-001"
    text_ada_001 = "text-ada-001"


class OpenAICompletionParameters(ProcessorParameters):
    model: OpenAIModel = Field(
        OpenAIModel.davinci_instruct_beta,
        description="""The [OpenAI model](https://help.openai.com/en/articles/5832130-what-s-changed-with-engine-names-and-best-practices) used for completion. Options currently available:</br>
                        <li>`davinci-instruct-beta` - older Instruct GPT-3 model
                        <li>`text-davinci-003` - Most capable GPT-3 model. Can do any task the other models can do, often with higher quality, longer output and better instruction-following.
                        <li>`text-curie-001` - Very capable, but faster and lower cost than Davinci.
                        <li>`text-babbage-001` - Capable of straightforward tasks, very fast, and lower cost.
                        <li>`text-ada-001` - Capable of very simple tasks, usually the fastest model in the GPT-3 series, and lowest cost.
                        """,
    )
    max_tokens: int = Field(
        256,
        description="""The maximum number of tokens to generate in the completion.
    The token count of your prompt plus max_tokens cannot exceed the model's context length.
    Most models have a context length of 2048 tokens (except for the newest models, which support 4096).""",
    )
    temperature: float = Field(
        1.0,
        description="""What sampling temperature to use, between 0 and 2.
    Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    We generally recommend altering this or `top_p` but not both.""",
    )
    top_p: int = Field(
        1,
        description="""An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass.
    So 0.1 means only the tokens comprising the top 10% probability mass are considered.
    We generally recommend altering this or `temperature` but not both.""",
    )
    n: int = Field(
        1,
        description="""How many completions to generate for each prompt.
    Note: Because this parameter generates many completions, it can quickly consume your token quota.
    Use carefully and ensure that you have reasonable settings for `max_tokens`.""",
    )
    best_of: int = Field(
        1,
        description="""Generates best_of completions server-side and returns the "best" (the one with the highest log probability per token).
    Results cannot be streamed.
    When used with `n`, `best_of` controls the number of candidate completions and `n` specifies how many to return – `best_of` must be greater than `n`.
    Use carefully and ensure that you have reasonable settings for `max_tokens`.""",
    )
    presence_penalty: float = Field(
        0.0,
        description="""Number between -2.0 and 2.0.
    Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.""",
    )
    frequency_penalty: float = Field(
        0.0,
        description="""Number between -2.0 and 2.0.
    Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.""",
    )
    prompt_altText: str = Field(
        None,
        description="""<li>If defined: contains the prompt as an alternative text of the input document (can be a template string containing `$text` to be substituted by the document text),
        <li>if not takes the text of the input document as prompt.""",
    )
    completion_altText: str = Field(
        None,
        description="""<li>If defined: generates the completion as an alternative text of the input document,
    <li>if not: replace the text of the input document.""",
    )


SUPPORTED_LANGUAGES = "de,en,es,fr,it,nl,pt"


# noqa: E501
class OpenAICompletionProcessor(ProcessorBase):
    __doc__ = """Generate text using [OpenAI Text Completion](https://platform.openai.com/docs/guides/completion) API
    You input some text as a prompt, and the model will generate a text completion that attempts to match whatever context or pattern you gave it.
    #languages:""" + SUPPORTED_LANGUAGES

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)
        openai = get_openai()
        params: OpenAICompletionParameters = cast(
            OpenAICompletionParameters, parameters
        )
        try:

            for document in documents:
                lang = document_language(document, None)
                if lang is None or lang not in supported_languages:
                    raise AttributeError(
                        f"Metadata language {lang} is required and must be in {SUPPORTED_LANGUAGES}"
                    )
                altTexts = document.altTexts or []
                prompt = document.text
                if params.prompt_altText is not None and len(
                        params.prompt_altText.strip()
                ):
                    prompt_altText = next(
                        (
                            alt
                            for alt in altTexts
                            if alt.name == params.prompt_altText.strip()
                        ),
                        None,
                    )
                    if prompt_altText is not None:
                        prompt = prompt_altText.text
                        if "$" in prompt:
                            prompt_templ = Template(prompt)
                            flatten_doc = flatten(document.dict())
                            prompt = prompt_templ.safe_substitute(flatten_doc)

                response = openai.Completion.create(
                    model=params.model.value,
                    prompt=prompt,
                    max_tokens=params.max_tokens,
                    temperature=params.temperature,
                    top_p=params.top_p,
                    n=params.n,
                    frequency_penalty=params.frequency_penalty,
                    presence_penalty=params.presence_penalty,
                    best_of=params.best_of,
                )
                completion = "\n".join(r["text"] for r in response["choices"])
                if params.completion_altText is not None and len(
                        params.completion_altText
                ):
                    altTexts.append(
                        AltText(name=params.completion_altText, text=completion)
                    )
                    document.altTexts = altTexts
                else:
                    document.text = completion
                    document.sentences = []
                    document.annotations = None
                    document.categories = None
        except BaseException as err:
            raise err
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAICompletionParameters


def flatten(d, parent_key="", sep="."):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def document_language(doc: Document, default: str = None):
    if doc.metadata is not None and "language" in doc.metadata:
        return doc.metadata["language"]
    return default


@lru_cache(maxsize=None)
def get_openai():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    return openai
