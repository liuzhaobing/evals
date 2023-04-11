# -*- coding:utf-8 -*-
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
                return dict(id=str(uuid.uuid4()),
                            model=model.MODEL_NAME,
                            choices=[{"message": {"role": "assistant", "content": model.create(*args, **kwargs)}}])
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
        payload = {"input": kwargs["prompt"]}
        resp = requests.request(method="POST", url=url, json=payload)
        return resp.json()


class OpenAIAPI(CloudMindsModel):
    MODEL_NAME = "openai_api"

    @classmethod
    def create(cls, *args, **kwargs):
        url = "http://172.16.32.2:31806/chatgpt/api/ask"
        payload = {
            "input": [{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": kwargs["prompt"]}],
            "conv_user_id": "cffbda0f-ea62-4549-b766-ac7356e0b5ca2"
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
        url = f'http://172.16.23.85:30592/chatglm/ask'
        resp = requests.post(url, json={
            "input": kwargs["prompt"],
            "history": [],
            "conv_user_id": str(uuid.uuid4()),
        })
        return resp.json()["body"]["message"]


class HuggingFaceSBertPq(CloudMindsModel):
    MODEL_NAME = "sbert_pq"
    model = sentence_transformers.SentenceTransformer('inkoziev/sbert_pq').to(device)

    @classmethod
    def create(cls, *args, **kwargs):
        query = kwargs["prompt"]
        sentence1 = query.split("\n")[1].replace("User: 句子1：", "")
        sentence2 = query.split("\n")[2].replace("User: 句子2：", "")
        sentences = [sentence1, sentence2]

        embeddings = cls.model.encode(sentences)

        s = sentence_transformers.util.cos_sim(a=embeddings[0], b=embeddings[1])
        line = 0.7

        return "是" if s.item() > line else "否"


def mock_trace_id():
    return str(uuid.uuid4()) + "@cloudminds-test.com.cn"


class SmartVoice(CloudMindsModel):
    MODEL_NAME = "flag_open"
    address = "172.16.23.85:30811"  # fit 86
    agent_id = 65
    is_conversation = False
    session_id = mock_trace_id()

    channel = grpc.insecure_channel(address)
    stub = talk_pb2_grpc.TalkStub(channel)

    @classmethod
    def create(cls, *args, **kwargs):
        def talk_req(payload):
            yield payload

        message = talk_pb2.TalkRequest(is_full=True,
                                       agent_id=cls.agent_id,
                                       session_id=cls.session_id if cls.is_conversation else mock_trace_id(),
                                       question_id=mock_trace_id(),
                                       event_type=0,
                                       robot_id="5C1AEC03573747D",
                                       tenant_code="cloudminds",
                                       version="v3",
                                       test_mode=False,
                                       asr=talk_pb2.Asr(lang="CH", text=kwargs["prompt"]))
        stream_response = cls.stub.StreamingTalk(talk_req(message).__iter__())
        response_json = [json.loads(json_format.MessageToJson(response)) for response in stream_response]
        tts = response_json[-1]["tts"][0]
        try:
            return tts["action"]["param"]["raw_data"]["wholeAnswer"]
        except:
            if tts.__contains__("text"):
                return tts["text"]
            return ""


if __name__ == '__main__':
    # model_name = "chatglm_api"
    # model_name = "openai_api"
    # model_name = "bloom_api"
    # model_name = "sbert_pq"
    model_name = "flag_open"
    result = ChatCompletion.create(model=model_name,
                                   prompt="任务：判断两个句子语义是否相似，回答'否'或者'是'。\nUser: 句子1：出入境的回执单可以乘机吗。\nUser: 句子2：出入境管理局开的证明可以换登记牌吗。\nAssistant: ")
    print(result)
