# coding=gbk
import openai

openai.api_key = "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"

class ChatGpt(object):
    #云团队
    url = "http://172.16.32.2:31806/chatgpt/api/ask"
    def __init__(self):
        self.index = 0

    def askChatGPT(self, question):
        import requests
        import json
        resp = requests.post(self.url, json={
            "input": [{"role": "user", "content": f"{question}"}],
            "conv_user_id": "cffbda0f-ea62-4549-b766-ac7356e0b5ca2"
        })
        d = json.loads(resp.text)
        if d["code"] != 0:
            return "", False
        return d["body"]["message"], True



content = """现在需要你根据问题和标准答案评估另一个模型的回复。你要结合着问题评估另一个模型的回复是否正确， 下面是数据:\n[BEGIN DATA]\n************\n[问题]: 在太阳系9大行星中，最大的行星是哪一颗？\n************\n[标准答案]: 木星\n************\n[模型提交的答案]: 在太阳系 9 大行星中,最大的行星是木星。木星是太阳系中质量最大的行星,其质量约为地球的 243 倍。它的直径也比地球大,约为地球的 173 倍。木星是太阳系中最大的行星,也是最大的天体。\n************\n[END DATA]\n\n将标准答案与模型提交的答案进行比较。 忽略风格、语法或标点符号的任何差异。\n 模型提交的答案可能是标准答案的子集或超集，也可能与其冲突。 确定适用哪种情况。 通过选择以下选项之一回答问题：\n (A) 模型提交的答案是标准答案的子集，并且与其完全一致。\n (B) 模型提交的答案是标准答案的超集，并且与其完全一致。\n (C) 模型提交的答案包含与标准答案相同的所有细节。\n (D) 模型提交的答案与标准答案存在分歧。\n (E) 模型提交的答案和标准答案不同，但从事实性的角度来看，这些差异无关紧要。\n\nFirst, answer by printing a single choice from \"A\" or \"B\" or \"C\" or \"D\" or \"E\" (without quotes or punctuation) corresponding to the correct answer. Then, from the next line, explain your reasonings step by step."""
cg = ChatGpt()
r, s = cg.askChatGPT(content)
print(r)
