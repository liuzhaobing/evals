import jsonlines
import os
import re
import json
from evals.prompt.generate_base import Generate


class Anli(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": ["R3", "dev.jsonl"]}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename[0], filename[1]), encoding="utf-8").readlines()
            datas = datas[:10]
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


class Arc(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "ARC-V1-Feb2018/ARC-V1-Feb2018-2/ARC-Easy/ARC-Easy-Test.jsonl"}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename), encoding="utf-8").readlines()
            datas = datas[:5]
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                for item in datas:
                    wf.write(item)

    def format_one_json(self, item):
        item = json.loads(item)
        answer = ""
        for choice in item["question"]["choices"]:
            if choice["label"] == item["answerKey"]:
                answer = choice["label"] + "." + choice["text"]
        return dict(input=self.format_chat_prompt(item), ideal=answer)

    def format_chat_prompt(self, item):
        options = []
        for choice in item["question"]["choices"]:
            options.append(choice["label"]+"."+choice["text"])

        sys_msg = """This is a multiple choice question, which of the following options better describes or achieves the goal, you Just give the answer, no need to explain why,  the following are the goal and options, Goal: {question}? Options: {options}"""
        return [
                   {
                       "role": "system",
                       "content": sys_msg.format(question=item["question"]["stem"], options=options)
                   }
               ]


class GSM8K(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "GSM8K/grade-school-math-master/grade-school-math-master/grade_school_math/data/test.jsonl"}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename), encoding="utf-8").readlines()
            datas = datas[:5]
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                for item in datas:
                    wf.write(item)

    def format_one_json(self, item):
        item = json.loads(item)
        return dict(input=self.format_chat_prompt(item), ideal=item["answer"])

    def format_chat_prompt(self, item):
        return [
                   {
                       "role": "system",
                       "content": "answer the following math questions, question: %s" % item["question"],
                   }
               ]


class Hellaswag(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "hellaswag/hellaswag_val.jsonl"}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename), encoding="utf-8").readlines()
            datas = datas[:5]
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                for item in datas:
                    wf.write(item)

    def format_one_json(self, item):
        item = json.loads(item)
        return dict(input=self.format_chat_prompt(item), ideal=item["endings"][item["label"]])

    def format_chat_prompt(self, item):
        answers = []
        for i, answer in enumerate(item["endings"]):
            answers.append(str(i + 1) + "." + answer)
        ans_str = " ".join(answers)

        return [
                   {
                       "role": "system",
                       "content": f"Read the story first, then choose your best ending from the options below to supplement the story. story is: {item['ctx_a']}, options are: {ans_str}",
                   }
               ]

class NatureQuestions(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "nq/samples.jsonl"}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename), encoding="utf-8").readlines()
            datas = datas[:5]
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                for item in datas:
                    wf.write(item)

    def get_contenct(self, html):
        from bs4 import BeautifulSoup
        # parse html content
        soup = BeautifulSoup(html, "html.parser")
        ele = soup.find("div", {"id": "bodyContent"})
        return ele.get_text()

    def format_one_json(self, item):
        item = json.loads(item)

        answers = []
        for i in item["annotations"]:
            if i["long_answer"]["candidate_index"] == -1:
                continue
            for j in i["short_answers"]:
                ass = item["document_tokens"][j["start_token"]:j["end_token"]]
                for item in ass:
                    if not item["html_token"]:
                        answers.append(item["token"])
        answer_str = " ".join(answers)
        return dict(input=self.format_chat_prompt(item), ideal=answer_str)

    def format_chat_prompt(self, item):
        d = self.get_contenct(item["document_html"])
        return [
            {
                "role": "system",
                "content": "Answer the following questions as concisely as possible After reading the following article, the question is: {question}, and then the passage is: {raw_data}".format(question=item["question_text"], raw_data=d),
            }
        ]


class PhysicalQA(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "piqa/samples.jsonl"}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename), encoding="utf-8").readlines()
            datas = datas[:5]
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                for item in datas:
                    wf.write(item)

    def generate_prompt_jsonl_batch(self):
        """写jsonl文件"""
        with jsonlines.open(self.this_dataset_registry_file_path, "w") as f:
            for index, item in enumerate(self.read_dataset_as_list(self.test_data_set_file_path())):
                f.write(self.format_single_json(item, index))

    def format_single_json(self, item, index):
        item = json.loads(item)
        answers = [0, 1, 1, 1, 0] #从
        return dict(input=self.format_chat_prompt(item), ideal=answers[index])

    def format_chat_prompt(self, item):
        options = []
        for choice in item["question"]["choices"]:
            options.append(choice["label"] + "." + choice["text"])
        sys_msg = """This is a multiple choice question, which of the following two options better describes or achieves the goal, you Just give the answer, no need to explain why,  the following are the goal and options, Goal: {question}? Options: {options}"""
        return [
            {
                "role": "system",
                "content": sys_msg.format(question=item["question"]["stem"], options=options),
            }
        ]


class TriviaQA(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "triviaqa/samples.jsonl"}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename), encoding="utf-8").readlines()
            datas = datas[:5]
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                for item in datas:
                    wf.write(item)

    def format_one_json(self, item):
        item = json.loads(item)
        return dict(input=self.format_chat_prompt(item), ideal=item["Answer"]["Value"])

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": f"Answer the following questions as concisely as possible. question is: {item['Question']}",
            }
        ]


class WebQuestions(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "web_questions/test.json"}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename), encoding="utf-8").readlines()
            datas = datas[:5]
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                for item in datas:
                    wf.write(item)

    def format_one_json(self, item):
        item = json.loads(item)
        answers = re.findall("description \"(.*?)\"", item["targetValue"])
        if answers == []:
            answers = re.findall("description (.*?)\)", item["targetValue"])
        return dict(input=self.format_chat_prompt(item), ideal=" or ".join(answers))

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": f"Answer the following questions as concisely as possible. question is: {item['utterance']}",
            }
        ]

if __name__ == '__main__':
    Anli(config=["test"])  # test(无答案)/train/validation
