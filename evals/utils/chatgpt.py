# coding=gbk
import openai

openai.api_key = "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"

class ChatGpt(object):
    #���Ŷ�
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



content = """������Ҫ���������ͱ�׼��������һ��ģ�͵Ļظ�����Ҫ���������������һ��ģ�͵Ļظ��Ƿ���ȷ�� ����������:\n[BEGIN DATA]\n************\n[����]: ��̫��ϵ9�������У�������������һ�ţ�\n************\n[��׼��]: ľ��\n************\n[ģ���ύ�Ĵ�]: ��̫��ϵ 9 ��������,����������ľ�ǡ�ľ����̫��ϵ��������������,������ԼΪ����� 243 ��������ֱ��Ҳ�ȵ����,ԼΪ����� 173 ����ľ����̫��ϵ����������,Ҳ���������塣\n************\n[END DATA]\n\n����׼����ģ���ύ�Ĵ𰸽��бȽϡ� ���Է���﷨������ŵ��κβ��졣\n ģ���ύ�Ĵ𰸿����Ǳ�׼�𰸵��Ӽ��򳬼���Ҳ���������ͻ�� ȷ��������������� ͨ��ѡ������ѡ��֮һ�ش����⣺\n (A) ģ���ύ�Ĵ��Ǳ�׼�𰸵��Ӽ�������������ȫһ�¡�\n (B) ģ���ύ�Ĵ��Ǳ�׼�𰸵ĳ���������������ȫһ�¡�\n (C) ģ���ύ�Ĵ𰸰������׼����ͬ������ϸ�ڡ�\n (D) ģ���ύ�Ĵ����׼�𰸴��ڷ��硣\n (E) ģ���ύ�Ĵ𰸺ͱ�׼�𰸲�ͬ��������ʵ�ԵĽǶ���������Щ�����޹ؽ�Ҫ��\n\nFirst, answer by printing a single choice from \"A\" or \"B\" or \"C\" or \"D\" or \"E\" (without quotes or punctuation) corresponding to the correct answer. Then, from the next line, explain your reasonings step by step."""
cg = ChatGpt()
r, s = cg.askChatGPT(content)
print(r)
