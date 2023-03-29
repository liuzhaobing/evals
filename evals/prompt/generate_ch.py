import jsonlines
import os
import json
import re
from evals.prompt.generate_base import Generate


class Anli(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": ["R3", "dev.jsonl"]}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename[0], filename[1]), encoding="utf-8").readlines()
            datas = datas[:5]
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                for item in datas:
                    wf.write(item)

    def format_one_json(self, item):
        item = json.loads(item)
        return dict(input=self.format_chat_prompt(item), ideal=item["label"])

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": "Evaluate the following natural language reasoning. I will first give a context, and then give a reasoning result to evaluate whether the reasoning is reasonable. The evaluation results are divided into three categories, e means that the reasoning result is reasonable, n means that it is impossible to judge whether it is correct, and c means the reasoning result and the context No, the answer you output can only be one of e, n, c, Below is the context:",
            },
            {
                "role": "system",
                "content": item["context"] + ". hypothesis:" + item["hypothesis"],
            },
        ]


class dureader_checklist(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "dev.json"}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename), encoding="utf-8") as f:
                datas = json.load(f)
                datas = datas["data"][0]["paragraphs"][:5]
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                    for item in datas:
                        wf.write(item)

    def format_one_json(self, item):
        if item["qas"][0]["answers"][0]["text"] == "":
            return dict(input=self.format_chat_prompt(item), ideal="无答案")
        else:
            return dict(input=self.format_chat_prompt(item), ideal=item["qas"][0]["answers"][0]["text"])

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": "给定一个问题q，一段篇章p，参赛系统需要根据篇章内容，判断该篇章p中是否包含给定问题的答案，如果是，则给出该问题的答案；否则输出“无答案”",
            },
            {
                "role": "system",
                "content": "p:番石榴性温,味甜、酸、涩…，最重要的是番石榴所含的脂肪热量较低,一个番石榴所含的脂肪约0.9克重或84卡路里。比起苹果,番石榴所含有的脂肪少38%,卡路里少, q: 番石榴汁热量?",
                "name": "example_user"
            },
            {
                "role": "system",
                "content": "一个番石榴所含的脂肪约0.9克重或84卡路里",
                "name": "example_assistant"
            },
            {
                "role": "system",
                "content": "p:云南省下辖8个市、8个少数民族自治州,面积39万平方千米,总人口4596万人,云南汉族人口为3062.9万人,占云南省总人口的66.63%, q: 云南文山市多少人口?",
                "name": "example_user"
            },
            {
                "role": "system",
                "content": "无答案",
                "name": "example_assistant"
            },
            {
                "role": "user",
                "content": "p: {}, q:{}".format(item["context"], item["qas"][0]["question"]),
            }
        ]


class Ape210K(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "test.ape.json"}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename), encoding="utf-8").readlines()
            datas = datas[:5]
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                for item in datas:
                    wf.write(item)

    def format_one_json(self, item):
        item = json.loads(item)
        return dict(input=self.format_chat_prompt(item), ideal=item["ans"])

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": "求解下面的问题, 只输出答案即可，问题: {}".format(item["original_text"]),
            }
        ]


class webQA(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "me_test.ann.json"}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename), encoding="utf-8") as f:
                datas = json.load(f)
                i = 0

                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                    for key, value in datas.items():
                        i += 1
                        if i > 6:
                            break
                        wf.write(value)

    def format_one_json(self, item):
        answer = ""
        for key,value in item["evidences"].items():
            if "answer" in value:
                answer += value["answer"][0]
        return dict(input=self.format_chat_prompt(item), ideal=answer)

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": item["question"],
            }
        ]


class Math23k(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "math23k_test.json"}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename), encoding="utf-8") as f:
                datas = json.load(f)
                datas = datas[:5]
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                    for item in datas:
                        wf.write(item)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["ans"])

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": item["original_text"],
            }
        ]


class MultiArith(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "MultiArith.json"}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename), encoding="utf-8") as f:
                datas = json.load(f)
                datas = datas[:5]
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                    for item in datas:
                        wf.write(item)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["lSolutions"])

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": "answer the following questions, you only need to give the answer, no need to give a step of information,question is:"+item["sQuestion"],
            }
        ]

class PKUMOD_CCKS(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": ("验证集问题.txt", "验证集答案.txt")}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename[0]), encoding="utf-8") as f:
                with open(os.path.join(self.this_download_path, filename[1]), encoding="utf-8") as f2:
                    datas = f.readlines()
                    datas2 = f2.readlines()
                    datas = datas[:5]
                    datas2 = datas2[:5]
                    with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                        for i in range(len(datas)):
                            if datas2[i].startswith('"'):
                                answer = datas2[i].replace('"', "")
                            else:
                                pattern = "<(.*?)>"
                                matches = re.findall(pattern, datas2[i], re.DOTALL)
                                answers = []
                                for match in matches:
                                    answers.append(match.split("_")[0])
                                answer = ",".join(answers)
                            wf.write({"question": datas[i], "answer": answer})

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["answer"])

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": item["question"],
            }
        ]


if __name__ == '__main__':
    # Ape210K(config=["test"])
    # dureader_checklist(config=["test"])
    # webQA(config=["test"])
    Math23k(config=["test"])
    # PKUMOD_CCKS(config=["test"])
    # MultiArith(config=["test"])
