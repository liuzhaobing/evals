# -*- coding:utf-8 -*-
import logging
import time

import requests
import sentence_transformers
import torch
import uuid
import grpc
import json
from evals.utils.api.talk import talk_pb2
from evals.utils.api.talk import talk_pb2_grpc
from google.protobuf import json_format

if torch.cuda.is_available():
    device = torch.device("cuda:0")
else:
    device = torch.device("cpu")


class CloudMindsModel:
    """
    继承此类 并重写create方法和MODEL_NAME属性
    其中:
        MODEL_NAME 为模型名称 如 bloom 、 chatglm
        create 为实际调用函数 请注意其返回值的格式为 string
    """
    MODEL_NAME: str

    @classmethod
    def create(cls, *args, **kwargs):
        for model in CloudMindsModel.__subclasses__():
            if not hasattr(model, "MODEL_NAME"):
                continue
            if model.MODEL_NAME == kwargs["model"]:
                retry = 0
                while True:
                    retry += 1
                    start_time = time.time()
                    model_output = model.create(*args, **kwargs)
                    edg_cost = int(time.time() - start_time) * 1000
                    if model_output:
                        break
                    if retry >= 3:
                        logging.info(f"model [{model.MODEL_NAME}] call failed after retry {retry}")
                        break
                    logging.info(f"model [{model.MODEL_NAME}] call failed retry {retry}")
                return dict(id=str(uuid.uuid4()),
                            model=model.MODEL_NAME,
                            choices=[{"message": {"role": "assistant", "content": model_output, "edg_cost": edg_cost}}])
        raise ValueError(f"no such model named {kwargs['model']}")


class ChatCompletion(CloudMindsModel):
    @property
    def models(self) -> set:
        return {model.MODEL_NAME for model in CloudMindsModel.__subclasses__() if hasattr(model, "MODEL_NAME")}

    @classmethod
    def create(cls, *args, **kwargs):
        return super().create(*args, **kwargs)


class BloomAPI(CloudMindsModel):
    MODEL_NAME = "bloom_api"

    @classmethod
    def create(cls, *args, **kwargs) -> str:
        url = f'http://172.16.33.2:8080/bloom'
        payload = {"input": str(kwargs["prompt"])}
        resp = requests.request(method="POST", url=url, json=payload)
        return resp.content.decode().strip()


class OpenAIAPI(CloudMindsModel):
    MODEL_NAME = "openai_api"

    @classmethod
    def create(cls, *args, **kwargs):
        is_conversation = False
        session_id = mock_trace_id()
        if kwargs.__contains__("is_conversation"):
            is_conversation = kwargs["is_conversation"]
        if kwargs.__contains__("session_id"):
            session_id = kwargs["session_id"]
        url = "http://172.16.32.2:31806/chatgpt/api/ask"
        payload = {
            "input": [{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": str(kwargs["prompt"])}],
            "conv_user_id": session_id
        }
        resp = requests.post(url, json=payload)
        d = resp.json()
        rtn = ""
        if d["code"] == 0:
            rtn = d["body"]["message"]
        return rtn


class ChatGLMAPI(CloudMindsModel):
    MODEL_NAME = "chatglm_api"

    @classmethod
    def create(cls, *args, **kwargs):
        is_conversation = False
        session_id = mock_trace_id()
        if kwargs.__contains__("is_conversation"):
            is_conversation = kwargs["is_conversation"]
        if kwargs.__contains__("session_id"):
            session_id = kwargs["session_id"]
        url = f'http://172.16.23.85:30592/chatglm/ask'
        resp = requests.post(url, json={
            "input": str(kwargs["prompt"]),
            "history": [],
            "conv_user_id": session_id,
        })
        return resp.json()["body"]["message"]


def mock_trace_id():
    return str(uuid.uuid4()) + "@cloudminds-test.com.cn"


class SmartVoice(CloudMindsModel):
    MODEL_NAME = "smartvoice"
    address = "172.16.23.85:30811"  # fit 86
    agent_id = 65
    is_conversation = False
    session_id = mock_trace_id()

    channel = grpc.insecure_channel(address)
    stub = talk_pb2_grpc.TalkStub(channel)

    @classmethod
    def create(cls, *args, **kwargs):
        if kwargs.__contains__("address"):
            cls.address = kwargs["address"]
        if kwargs.__contains__("agent_id"):
            cls.agent_id = kwargs["agent_id"]
        if kwargs.__contains__("is_conversation"):
            cls.is_conversation = kwargs["is_conversation"]
        if kwargs.__contains__("session_id"):
            cls.session_id = kwargs["session_id"]
        if not cls.is_conversation:
            cls.session_id = mock_trace_id()

        def talk_req(payload):
            yield payload

        try:
            message = talk_pb2.TalkRequest(is_full=True,
                                           agent_id=cls.agent_id,
                                           session_id=cls.session_id if cls.is_conversation else mock_trace_id(),
                                           question_id=mock_trace_id(),
                                           event_type=0,
                                           robot_id="5C1AEC03573747D",
                                           tenant_code="cloudminds",
                                           version="v3",
                                           test_mode=False,
                                           asr=talk_pb2.Asr(lang="CH", text=str(kwargs["prompt"])))
            response = cls.stub.Talk(message)
            for tts in response.tts:
                raw_data = json_format.MessageToDict(tts.action.param.raw_data)
                if raw_data:
                    if raw_data.__contains__("wholeAnswer"):
                        return raw_data["wholeAnswer"]
                if tts.text:
                    return tts.text
            return ""
        except:
            return ""


if __name__ == '__main__':
    # model_name = "chatglm_api"
    # model_name = "openai_api"
    # model_name = "bloom_api"
    model_name = "smartvoice"
    result = ChatCompletion.create(model=model_name,
                                   prompt="任务：判断两个句子语义是否相似，回答'否'或者'是'。\nUser: 句子1：出入境的回执单可以乘机吗。\nUser: 句子2：出入境管理局开的证明可以换登记牌吗。\nAssistant: ")
    print(result)
