# -*- coding:utf-8 -*-
import json
import logging
import concurrent.futures
from typing import Any, Optional, Union

import requests
from evals.api import CompletionFn, CompletionResult
from evals.record import record_sampling
from evals.prompt.base import (
    CompletionPrompt,
    OpenAICreateChatPrompt,
    OpenAICreatePrompt,
    Prompt,
)

_EVALS_THREAD_TIMEOUT = 300


def cloudminds_api_http(*args, **kwargs):
    prompt = kwargs.pop("prompt")
    payload = {
        "model": "vicuna",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_new_tokens": 2048,
        "stream": False
    }
    print(json.dumps(payload))
    resp = requests.request(method="POST", url=kwargs.pop("host"), json=payload)
    return resp.json()


def request_with_timeout(func, *args, timeout=_EVALS_THREAD_TIMEOUT, **kwargs):
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                result = future.result(timeout=timeout)
                if "error" not in result:
                    return result
                logging.warning(result)

            except concurrent.futures.TimeoutError as e:
                continue


def cloudminds_completion_create_retrying(*args, **kwargs):
    return request_with_timeout(cloudminds_api_http, *args, **kwargs)


class CloudMindsBaseCompletionResult(CompletionResult):
    def __init__(self, raw_data: Any, prompt: Any):
        self.raw_data = raw_data
        self.prompt = prompt

    def get_completions(self) -> list[str]:
        raise NotImplementedError


class CloudMindsCompletionResult(CloudMindsBaseCompletionResult):
    def get_completions(self) -> list[str]:
        completions = []
        if self.raw_data and "choices" in self.raw_data:
            for choice in self.raw_data["choices"]:
                if "message" in choice:
                    completions.append(choice["message"]["content"])
        return completions


class CloudMindsCompletionFn(CompletionFn):
    def __init__(
            self,
            host: Optional[str] = None,
            n_ctx: Optional[int] = None,
            extra_options: Optional[dict] = {},
            **kwargs,
    ):
        self.host = host
        self.n_ctx = n_ctx
        self.extra_options = extra_options

    def __call__(
            self,
            prompt: Union[str, OpenAICreateChatPrompt],
            **kwargs,
    ) -> CloudMindsCompletionResult:
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

        cloudminds_create_prompt: OpenAICreatePrompt = prompt.to_formatted_prompt()

        result = cloudminds_completion_create_retrying(
            host=self.host,
            prompt=cloudminds_create_prompt,
            **{**kwargs, **self.extra_options},
        )
        result = CloudMindsCompletionResult(raw_data=result, prompt=cloudminds_create_prompt)
        record_sampling(prompt=result.prompt, sampled=result.get_completions())
        return result
