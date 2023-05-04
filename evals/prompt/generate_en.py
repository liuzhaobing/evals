# -*- coding:utf-8 -*-
import os
import json
import tarfile
import urllib.request
import zipfile

import jsonlines
import evals
import logging
import pandas as pd
from datasets import load_dataset
from xml.etree.ElementTree import parse

from evals.prompt.generate_base import Generate

logger = logging.getLogger(__name__)


class WinoGrande(Generate):
    """WinoGrande"""
    d_url = "https://storage.googleapis.com/ai2-mosaic/public/winogrande/winogrande_1.1.zip"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": "test.jsonl", "train": "train_l.jsonl", "validation": "dev.jsonl"}
        for label, filename in resolve.items():
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                for i in evals.get_jsonls(os.path.join(self.this_download_path, "winogrande_1.1", filename)):
                    f.write(i)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["answer"])

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": "TASK: Read the provided sentence with blank, then identify the correct option from given two options which can fill the blank precisely, in the format \"<answer>\". The answer should be number only."},
                {"role": "system", "content": f"sentence: {item['sentence']}"},
                {"role": "system", "content": f"option1: {item['option1']}"},
                {"role": "system", "content": f"option2: {item['option2']}"}]


class StoryCloze(Generate):
    """Story Cloze Test Winter 2018"""

    def extract_and_save_datasets(self):
        resolve = {"test": "https://goo.gl/BcTtB4", "validation": "https://goo.gl/XWjas1"}
        for label, filename in resolve.items():
            os.makedirs(self.this_download_path, exist_ok=True)
            this_download_filename = os.path.join(self.this_download_path, self.class_name + ".csv")
            urllib.request.urlretrieve(filename, this_download_filename)
            df = pd.read_csv(this_download_filename)
            head_list = list(df.columns)
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                for line in df.values:
                    f.write(dict(zip(head_list, line)))

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["AnswerRightEnding"])

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": "TASK: There are four statements of story and two possible continuation of the story, choose a possible correct ending, in the format \"<answer>\". The answer must be a number only."},
                {"role": "system", "content": f"statement 1: {item['InputSentence1']}"},
                {"role": "system", "content": f"statement 2: {item['InputSentence2']}"},
                {"role": "system", "content": f"statement 3: {item['InputSentence3']}"},
                {"role": "system", "content": f"statement 4: {item['InputSentence4']}"},
                {"role": "system", "content": f"possible continuation 1: {item['RandomFifthSentenceQuiz1']}"},
                {"role": "system", "content": f"possible continuation 2: {item['RandomFifthSentenceQuiz2']}"}]


class COPA(Generate):
    """COPA (Choice of Plausible Alternatives)
    https://people.ict.usc.edu/~gordon/copa.html
    """
    d_url = "https://people.ict.usc.edu/~gordon/downloads/COPA-resources.tgz"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".tgz")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with tarfile.open(this_download_filename, "r:gz") as tar:
            tar.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": "copa-test.xml", "validation": "copa-dev.xml"}
        for label, filename in resolve.items():
            document = parse(os.path.join(self.this_download_path, "COPA-resources", "datasets", filename))
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                for item in document.iterfind("item"):
                    f.write(dict(id=item.attrib["id"],
                                 asks_for=item.attrib["asks-for"],
                                 most_plausible_alternative=item.attrib["most-plausible-alternative"],
                                 p=item.findtext('p'),
                                 a1=item.findtext('a1'),
                                 a2=item.findtext('a2')))

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["most_plausible_alternative"])

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": f"TASK: There are a premise and two alternatives, select the alternative based on the given question that more plausibly has a causal relation with the premise, in the format \"<answer>\". The answer must be a number only."},
                {"role": "system", "content": f"premise: {item['p']}"},
                {"role": "system", "content": f"alternative 1: {item['a1']}"},
                {"role": "system", "content": f"alternative 2: {item['a2']}"},
                {"role": "user", "content": f"question: which is the {item['asks_for']} with the premise？"}]


class MultiRC(Generate):
    """MultiRC (Multi-Sentence Reading Comprehension)"""
    d_url = "http://www.eraserbenchmark.com/zipped/multirc.tar.gz"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".tgz")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with tarfile.open(this_download_filename, "r:gz") as tar:
            tar.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": "test.jsonl", "validation": "val.jsonl", "train": "train.jsonl"}
        for label, filename in resolve.items():
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                for i in evals.get_jsonls(os.path.join(self.this_download_path, "multirc", filename)):
                    # 把文章内容读取出来 存放到 story_content
                    with open(
                            os.path.join(self.this_download_path, "multirc", "docs", i["annotation_id"].split(":")[0]),
                            "r", encoding="UTF-8") as story:
                        i["story_content"] = story.read()
                    f.write(i)

    def format_one_json(self, item):
        # TODO
        return {}

    def format_chat_prompt(self, item):
        # TODO
        return []


class BoolQ(Generate):
    """BoolQ (Boolean Questions)"""

    # def test_data_set_file_path(self):
    #     return os.path.join(self.dataset_path, self.config[0], self.config[1])

    # def read_dataset_as_list(self, dataset_file_path):
    #     return evals.get_jsonls(dataset_file_path)

    def extract_and_save_datasets(self):
        dataset = load_dataset("boolq")
        for label in self.labels:
            if dataset.__contains__(label):
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                    for item in dataset[label]:
                        f.write(item)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=str(item["answer"]))

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": "TASK: Read a short passage and judge whether the given question is correct, in the format \"<answer>\". The answer must be 'true' or 'false' only."},
                {"role": "system", "content": f"passage: {item['passage']}"},
                {"role": "user", "content": f"question: {item['question']}"}]


class WSC(Generate):
    """WSC (Winograd Schema Challenge)"""

    def extract_and_save_datasets(self):
        dataset = load_dataset("winograd_wsc", "wsc285")
        for label in self.labels:
            if dataset.__contains__(label):
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                    for item in dataset[label]:
                        f.write(item)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=str(item["label"]))

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": "TASK: Read text and determine which, from given two options, the pronoun refer to in the text, in the format \"<answer>\". The answer must be number only."},
                {"role": "system", "content": f"text: {item['text']}"},
                {"role": "system", "content": f"option 0: {item['options'][0]}"},
                {"role": "system", "content": f"option 1: {item['options'][1]}"},
                {"role": "user", "content": f"pronoun: {item['pronoun']}"}]


class COQA(Generate):
    """CoQA (Conversational Question Answering Challenge)"""

    def extract_and_save_datasets(self):
        dataset = load_dataset("coqa")
        for label in self.labels:
            if dataset.__contains__(label):
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                    for item in dataset[label]:
                        f.write(item)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=[item['answers']['input_text'][-1]])

    def format_chat_prompt(self, item):
        """Match"""
        story = item["story"]
        prompt = [{
            "role": "system",
            "content": f"TASK: Read the provided passage, then identify the correct answer to the questions below, in the format \"<answer> || <quote>\". The quote should be succinct and come directly from either the passage and/or previous question-answer pairs. If the passage does not provide enough information to answer the question, answer with \"unknown || unknown\".\n---\n{story}"
        }]
        for index in range(len(item["questions"])):
            if item["questions"][index] == item["questions"][-1]:
                prompt.append({
                    "role": "user",
                    "content": f"Q: {item['questions'][index]}"
                })
                return prompt
            prompt.append({
                "role": "system",
                "content": f"Q: {item['questions'][index]}",
                "name": "example_user"
            })
            prompt.append({
                "role": "system",
                "content": f"A: {item['answers']['input_text'][index]} || {story[item['answers']['answer_start'][index]:item['answers']['answer_end'][index]]}",
                "name": "example_assistant"
            })

    def format_one_yaml(self):  # 生成test case模板
        return f"""
{self.class_name}_match:
  id: {self.class_name}.match1.v0
  metrics: [f1_score]
{self.class_name}.match1.v0:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: {self.class_name}/{self.class_name + ".jsonl"}

{self.class_name}_fact:
  id: {self.class_name}.fact1.v0
  metrics: [f1_score]
{self.class_name}.fact1.v0:
  class: evals.elsuite.modelgraded.classify:ModelBasedClassify
  args:
    samples_jsonl: {self.class_name}/{self.class_name + ".jsonl"}
    eval_type: cot_classify
    modelgraded_spec: fact
""".strip()


class CNNDailyMail(Generate):
    """CNN/Daily Mail"""

    def extract_and_save_datasets(self):
        dataset = load_dataset("cnn_dailymail", "3.0.0")
        for label in self.labels:
            if dataset.__contains__(label):
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                    for item in dataset[label]:
                        f.write(item)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["highlights"])

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": f"TASK: Read article and prompt a bref summary. article: ```{item['article']}```"}]


class SQuAD(Generate):
    """SQuAD (Stanford Question Answering Dataset)"""

    def extract_and_save_datasets(self):
        resolve = {"train": "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json",
                   "validation": "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json"}
        for label, filename in resolve.items():
            os.makedirs(self.this_download_path, exist_ok=True)
            this_download_filename = os.path.join(self.this_download_path, label + ".json")
            urllib.request.urlretrieve(filename, this_download_filename)
            with open(this_download_filename, "r") as f:
                file_content = json.load(f)
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                for i in file_content["data"]:
                    for j in i["paragraphs"]:
                        for k in j["qas"]:
                            k["context"] = j["context"]
                            k["title"] = i["title"]
                            f.write(k)

    def format_one_json(self, item):
        if not item["is_impossible"]:
            return dict(input=self.format_chat_prompt(item), ideal=[answer["text"] for answer in item['answers']])
        return dict(input=self.format_chat_prompt(item), ideal=[answer["text"] for answer in item['plausible_answers']])

    def format_chat_prompt(self, item):
        return [
            {"role": "system",
             "content": "TASK: Read passage and answer question, where the answer to question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable."},
            {"role": "system", "content": f"Title: {item['title']}"},
            {"role": "system", "content": f"Passage: {item['context']}"},
            {"role": "user", "content": f"Question: {item['question']}"}
        ]


class RACE(Generate):
    """RACE (ReAding Comprehension dataset from Examinations)"""
    d_url = "http://www.cs.cmu.edu/~glai1/data/race/RACE.tar.gz"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".tar.gz")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with tarfile.open(this_download_filename, "r:gz") as tar:
            tar.extractall(self.this_download_path)
        os.remove(this_download_filename)
        dataset = load_dataset(self.this_download_path)
        for label in self.labels:
            if dataset.__contains__(label):
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                    for item in dataset[label]:
                        f.write(json.loads(item["text"]))

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item['answers'])

    def format_chat_prompt(self, item):
        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H"]
        template = [{"role": "system",
                     "content": "TASK: There is an article followed by some questions. For each of them there are some choices marked A, B, C, etc. You should decide on the best choice one by one after reading the article."},
                    {"role": "system", "content": f"Article: {item['article']}"}]
        for index in range(len(item["questions"])):
            content = f"Question {index + 1}: {item['questions'][index]} \nOptions: "
            for option in item["options"][index]:
                content += "\n"
                content += alphabet[item["options"][index].index(option)]
                content += ". "
                content += option
            template.append({"role": "user", "content": content})
        return template


class DROP(Generate):
    """DROP (Discrete Reasoning Over Paragraphs)"""

    def extract_and_save_datasets(self):
        dataset = load_dataset("drop")
        for label in self.labels:
            if dataset.__contains__(label):
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                    for item in dataset[label]:
                        f.write(item)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["answers_spans"]["spans"])

    def format_chat_prompt(self, item):
        return [{"role": "system", "content": "TASK: Read a passage and answer the following question concisely."},
                {"role": "system", "content": f"Passage: {item['passage']}"},
                {"role": "user", "content": f"Question: {item['question']}"}]


class QuAC(Generate):
    """QuAC (Question Answering in Context)"""

    def extract_and_save_datasets(self):
        dataset = load_dataset("quac")
        for label in self.labels:
            if dataset.__contains__(label):
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                    for item in dataset[label]:
                        f.write(item)

    def format_one_json(self, item):
        # TODO
        return {}

    def format_chat_prompt(self, item):
        # TODO
        return []


class ReCoRD(Generate):
    """ReCoRD (Reading Comprehension with Commonsense Reasoning Dataset)"""
    d_url = "https://raw.githubusercontent.com/liuzhaobing/NLP/main/datasets/ReCoRD.zip"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"train": "train.json", "validation": "dev.json"}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename), "r", encoding="UTF-8") as f:
                file_content = json.load(f)
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as jsonf:
                for content in file_content["data"]:
                    jsonf.write(content)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item),
                    ideal=[[answer["text"] for answer in q["answers"]] for q in item["qas"]])

    def format_chat_prompt(self, item):
        template = [
            {"role": "system", "content": "TASK: Read a news and answer the following questions one by one concisely."},
            {"role": "system", "content": f"News: {item['passage']['text']}"}]
        for q in item["qas"]:
            template.append({"role": "user", "content": f"Question: {q['query']}"})
        return template


class WiC(Generate):
    """WiC (Words in Context)"""
    d_url = "https://pilehvar.github.io/wic/package/WiC_dataset.zip"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"train": ["train", ["train.data.txt", "train.gold.txt"]],
                   "validation": ["dev", ["dev.data.txt", "dev.gold.txt"]],
                   "test": ["test", ["test.data.txt", "test.gold.txt"]]}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename[0], filename[1][1]), "r", encoding="UTF-8") as f:
                answer_content = f.readlines()

            with open(os.path.join(self.this_download_path, filename[0], filename[1][0]), "r", encoding="UTF-8") as f:
                question_content = f.readlines()

            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as jsonf:
                for q in question_content:
                    q_content = q.strip().split("\t")
                    jsonf.write(dict(
                        lemma=q_content[0],  # 需要消歧的词的原型
                        pos=q_content[1],  # 需要消歧的词的词性
                        start1_start2=q_content[2],  # 0-2 其中0代表词在第一个句子中的单词索引 2代表词在第二个句子中的单词索引
                        setence1=q_content[3],  # 第一个句子
                        setence2=q_content[4],  # 第二个句子
                        label=answer_content[question_content.index(q)].strip(),  # 词在两个句子中的意思是否相同 取值为True或False
                    ))

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=True if item["label"] == 'T' else False)

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": "TASK: Whether two sentences containing the same verb or noun have the same meaning? Please answer with a single word 'True' or 'False' only."},
                {"role": "system", "content": f"Sentence 1: {item['setence1']}"},
                {"role": "system", "content": f"Sentence 2: {item['setence2']}"},
                {"role": "system", "content": f"Lemma: {item['lemma']}."},
                {"role": "system", "content": f"Pos: {'Verb' if item['pos'] == 'V' else 'Noun'}."}]


class HumanEval(Generate):
    """HumanEval"""

    def extract_and_save_datasets(self):
        dataset = load_dataset("openai_humaneval")
        for label in self.labels:
            if dataset.__contains__(label):
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                    for item in dataset[label]:
                        f.write(item)

    def format_one_json(self, item):
        return {}

    def format_chat_prompt(self, item):
        return []


class Anli(Generate):
    """ANLI (Adversarial NLI)
    https://paperswithcode.com/dataset/anli
    """

    def extract_and_save_datasets(self):
        resolve = {"test": ["R3", "dev.jsonl"], "validation": ["R3", "dev.jsonl"], "train": ["R3", "train.jsonl"]}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename[0], filename[1]), encoding="utf-8").readlines()
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
    """ARC (AI2 Reasoning Challenge)
    https://paperswithcode.com/dataset/arc
    """
    d_url = "https://ai2-public-datasets.s3.amazonaws.com/arc/ARC-V1-Feb2018.zip"

    def extract_and_save_datasets(self):

        resolve = {"test": [("ARC-Easy", "ARC-Easy-Test.jsonl"), ("ARC-Challenge", "ARC-Challenge-Test.jsonl")],
                   "train": [("ARC-Easy", "ARC-Easy-Train.jsonl"), ("ARC-Challenge", "ARC-Challenge-Train.jsonl")],
                   "validation": [("ARC-Easy", "ARC-Easy-Dev.jsonl"), ("ARC-Challenge", "ARC-Challenge-Dev.jsonl")]}
        for label, filename in resolve.items():
            datas = []
            for file in filename:
                datas += open(os.path.join(self.this_download_path, "ARC-V1-Feb2018-2", file[0], file[1]),
                              encoding="utf-8").readlines()
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                wf.write_all(datas)

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
            options.append(choice["label"] + "." + choice["text"])

        sys_msg = """This is a multiple choice question, which of the following options better describes or achieves the goal, you Just give the answer, no need to explain why,  the following are the goal and options, Goal: {question}? Options: {options}"""
        return [
            {
                "role": "system",
                "content": sys_msg.format(question=item["question"]["stem"], options=options)
            }
        ]


class GSM8K(Generate):
    def extract_and_save_datasets(self):
        dataset = load_dataset("gsm8k", "main")  # ['main', 'socratic']
        for label in self.labels:
            if dataset.__contains__(label):
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                    for item in dataset[label]:
                        wf.write(item)

    def format_one_json(self, item):
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
        dataset = load_dataset("hellaswag")
        for label in self.labels:
            if dataset.__contains__(label):
                datas = dataset[label]
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                    wf.write_all(datas)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["endings"][int(item["label"])])

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
    d_url = "https://storage.cloud.google.com/natural_questions/v1.0-simplified/nq-dev-all.jsonl.gz"

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
                "content": "Answer the following questions as concisely as possible After reading the following article, the question is: {question}, and then the passage is: {raw_data}".format(
                    question=item["question_text"], raw_data=d),
            }
        ]


class PhysicalQA(Generate):
    """物理常识
    test: 3084
    train: 16113
    validation: 1838

    refer: https://huggingface.co/datasets/piqa
    """

    def extract_and_save_datasets(self):
        dataset = load_dataset("piqa")
        for label in self.labels:
            if dataset.__contains__(label):
                datas = dataset[label]
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                    wf.write_all(datas)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=int(item["label"] + 1))

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": "TASK: Answer the following question which requires physical commonsense. You must choose the most appropriate solution, of which exactly one is correct, in the format \"<answer>\". The answer should be number only.",
            },
            {
                "role": "user",
                "content": f"Question: {item['goal']}\nSolution 1: {item['sol1']}\nSolution 2: {item['sol2']}"
            }
        ]


class TriviaQA(Generate):
    """TriviaQA: A Large Scale Dataset for Reading Comprehension and Question Answering
    """

    d_url = "http://nlp.cs.washington.edu/triviaqa/data/triviaqa-rc.tar.gz"

    def extract_and_save_datasets(self):
        dataset = load_dataset("trivia_qa", "rc")
        for label in self.labels:
            if dataset.__contains__(label):
                datas = dataset[label]
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                    wf.write_all(datas)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["Answer"]["Value"])

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": f"Answer the following questions as concisely as possible. question is: {item['Question']}",
            }
        ]


class WebQuestions(Generate):
    """
    refer: https://worksheets.codalab.org/worksheets/0xba659fe363cb46e7a505c5b6a774dc8a
    """

    def extract_and_save_datasets(self):
        resolve = {"test": "test.json", "train": "train.json"}
        for label, filename in resolve.items():
            datas = json.load(open(os.path.join(self.this_download_path, filename), encoding="utf-8"))
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                wf.write_all(datas)

    def format_one_json(self, item):
        answers = re.findall("description \"(.*?)\"", item["targetValue"])
        if not answers:
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
    sample = 100

    # HumanEval(config=["test"])  # test

    WiC(config=["test", sample])  # test/train/validation

    ReCoRD(config=["validation", sample])  # train/validation

    QuAC(config=["validation", sample])  # train/validation

    DROP(config=["validation", sample])  # train/validation

    RACE(config=["test", sample])  # test/train/validation

    SQuAD(config=["validation", sample])  # train/validation

    CNNDailyMail(config=["test", sample])  # test/train/validation

    COQA(config=["validation", sample])  # train/validation

    MultiRC(config=["test", sample])  # test

    WSC(config=["test", sample])  # test

    BoolQ(config=["validation", sample])  # train/validation

    COPA(config=["test", sample])  # test/validation

    StoryCloze(config=["validation", sample])  # test(无答案)/validation

    WinoGrande(config=["validation", sample])  # test(无答案)/train/validation

    Anli(config=["validation", sample])  # test(无答案)/train/validation

    Arc(config=["validation", sample])  # test/train/validation

    GSM8K(config=["test", sample])  # test/train

    Hellaswag(config=["validation", sample])  # test(无答案)/train/validation

    PhysicalQA(config=["validation", sample])  # test(无答案)/train/validation

    # TriviaQA(config=["validation", sample])  # TODO

    # WebQuestions(config=["test", sample])  # TODO test/train
