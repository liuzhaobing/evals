"""
This file defines various helper functions for interacting with the OpenAI API.
"""
import logging

import backoff
import openai


def generate_dummy_chat_completion():
    return {
        "id": "dummy-id",
        "object": "chat.completion",
        "created": 12345,
        "model": "dummy-chat",
        "usage": {"prompt_tokens": 56, "completion_tokens": 6, "total_tokens": 62},
        "choices": [
            {
                "message": {"role": "assistant", "content": "This is a dummy response."},
                "finish_reason": "stop",
                "index": 0,
            }
        ],
    }


def generate_dummy_completion():
    return {
        "id": "dummy-id",
        "object": "text_completion",
        "created": 12345,
        "model": "dummy-completion",
        "choices": [
            {
                "text": "This is a dummy response.",
                "index": 0,
                "logprobs": None,
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 5, "completion_tokens": 6, "total_tokens": 11},
    }


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(
        openai.error.ServiceUnavailableError,
        openai.error.APIError,
        openai.error.RateLimitError,
        openai.error.APIConnectionError,
        openai.error.Timeout,
    ),
    max_value=60,
    factor=1.5,
)
def openai_completion_create_retrying(*args, **kwargs):
    """
    Helper function for creating a completion.
    `args` and `kwargs` match what is accepted by `openai.Completion.create`.
    """
    if kwargs["model"] == "dummy-completion":
        return generate_dummy_completion()

    result = openai.Completion.create(*args, **kwargs)
    if "error" in result:
        logging.warning(result)
        raise openai.error.APIError(result["error"])
    return result


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(
        openai.error.ServiceUnavailableError,
        openai.error.APIError,
        openai.error.RateLimitError,
        openai.error.APIConnectionError,
        openai.error.Timeout,
    ),
    max_value=60,
    factor=1.5,
)
def openai_chat_completion_create_retrying(*args, **kwargs):
    """
    Helper function for creating a chat completion.
    `args` and `kwargs` match what is accepted by `openai.ChatCompletion.create`.
    """
    if kwargs["model"] == "dummy-chat":
        return generate_dummy_chat_completion()

    return openai_chat(*args, **kwargs)

    # result = openai.ChatCompletion.create(*args, **kwargs)
    # if "error" in result:
    #     logging.warning(result)
    #     raise openai.error.APIError(result["error"])
    # return result


def openai_chat(*args, **kwargs):
    import requests
    # import json
    import uuid

    url = "http://172.16.32.2:31806/chatgpt/api/ask"
    resp = requests.post(url, json={
        "input": kwargs["messages"],
        "conv_user_id": "cffbda0f-ea62-4549-b766-ac7356e0b5ca2"
    })
    d = resp.json()
    rtn = ""
    if d["code"] == 0:
        rtn = d["body"]["message"]
    return {
        "id": str(uuid.uuid4()),
        "model": "chatgpt",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": rtn
                }
            }
        ]
    }


def cloudminds_chat_completion_create_retrying(*args, **kwargs):
    """
    Helper function for creating a chat completion for cloudminds model.
    """
    import requests
    import uuid

    if kwargs["model"] == "chatglm":
        return chatglm_api(kwargs["prompt"])
    if kwargs["model"] == "bloom":
        return bloom_api(kwargs["prompt"])

def bloom_api(query):
    import requests
    import uuid

    url = f'http://172.16.33.2:8080/bloom'
    resp = requests.post(url, json={
        "input": query,
    })
    return {
        "id": str(uuid.uuid4()),
        "model": "bloom",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": resp.json()
                }
            }
        ]
    }


def chatglm_api(query):
    import requests
    import uuid

    url = f'http://172.16.23.85:30592/chatglm/ask'
    resp = requests.post(url, json={
      "input": query,
      "history": [],
      "conv_user_id": str(uuid.uuid4()),
    })
    return {
        "id": str(uuid.uuid4()),
        "model": "chatglm",
        "choices":[
            {
                "message":{
                    "role":"assistant",
                    "content":resp.json()["body"]["message"]
                }
            }
        ]
    }