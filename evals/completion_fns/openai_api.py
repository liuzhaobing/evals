# -*- coding:utf-8 -*-
import logging
import concurrent.futures
from typing import Any, Optional, Union

import openai
import requests

from evals.api import CompletionFn, CompletionResult

from evals.prompt.base import (
    CompletionPrompt,
    OpenAICreateChatPrompt,
    OpenAICreatePrompt,
    Prompt,
)
from evals.record import record_sampling

_EVALS_THREAD_TIMEOUT = 300


def openai_api_http(*args, **kwargs):
    _headers = {
        "ApiName": "robotGptApiProxy",
        "Content-Type": "application/json",
        "Authorization": kwargs.pop("api_key", "")
    }
    if model := kwargs.pop("model", ""):
        _headers["model"] = model

    prompt = kwargs.pop("prompt", "")
    if prompt and isinstance(prompt, str):
        prompt = [{"role": "user", "content": prompt}]

    payload = {
        "input": prompt,
        "conv_user_id": "cffbda0f-ea62-4549-b766-ac7356e0b5ca2@cloudminds-test.com.cn",
        "temperature": 0
    }
    resp = requests.request(method="POST", url=kwargs.pop("host"), headers=_headers, json=payload)
    return resp.json()


def request_with_timeout(func, *args, timeout=_EVALS_THREAD_TIMEOUT, **kwargs):
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                result = future.result(timeout=timeout)
                if result.get("code") == 0 and result.get("message") == "Success":
                    return result
                logging.warning(result)

            except concurrent.futures.TimeoutError as e:
                continue


def openai_completion_create_retrying(*args, **kwargs):
    return request_with_timeout(openai_api_http, *args, **kwargs)


class OpenAIBaseCompletionResult(CompletionResult):
    def __init__(self, raw_data: Any, prompt: Any):
        self.raw_data = raw_data
        self.prompt = prompt

    def get_completions(self) -> list[str]:
        raise NotImplementedError


class OpenAICompletionResult(OpenAIBaseCompletionResult):
    def get_completions(self) -> list[str]:
        completions = []
        if self.raw_data and "body" in self.raw_data:
            completions.append(self.raw_data["body"]["message"])
        return completions


class OpenAICompletionFn(CompletionFn):
    def __init__(
            self,
            host: Optional[str] = None,
            model: Optional[str] = None,
            api_key: Optional[str] = None,
            n_ctx: Optional[int] = None,
            extra_options: Optional[dict] = {},
            **kwargs,
    ):
        self.host = host
        self.model = model
        self.api_key = api_key
        self.n_ctx = n_ctx
        self.extra_options = extra_options

    def __call__(
            self,
            prompt: Union[str, OpenAICreateChatPrompt],
            **kwargs,
    ) -> OpenAICompletionResult:
        if not isinstance(prompt, Prompt):
            assert (
                    isinstance(prompt, str)
                    or (isinstance(prompt, list) and all(isinstance(token, int) for token in prompt))
                    or (isinstance(prompt, list) and all(isinstance(token, str) for token in prompt))
                    or (isinstance(prompt, list) and all(isinstance(msg, dict) for msg in prompt))
            ), f"Got type {type(prompt)}, with val {type(prompt[0])} for prompt, expected str or list[int] or list[str] or list[dict[str, str]]"

            prompt = CompletionPrompt(
                raw_prompt=prompt,
            )

        openai_create_prompt: OpenAICreatePrompt = prompt.to_formatted_prompt()

        result = openai_completion_create_retrying(
            host=self.host,
            model=self.model,
            api_key=self.api_key,
            prompt=openai_create_prompt,
            **{**kwargs, **self.extra_options},
        )
        result = OpenAICompletionResult(raw_data=result, prompt=openai_create_prompt)
        record_sampling(prompt=result.prompt, sampled=result.get_completions())
        return result
