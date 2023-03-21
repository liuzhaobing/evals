# -*- coding:utf-8 -*-
import os
import json

import jsonlines
import evals
import logging
import pandas as pd
from datasets import load_dataset
from xml.etree.ElementTree import parse

logger = logging.getLogger(__name__)


class Generate:
    datasets = "datasets"
    downloads = "downloads"

    def __init__(self, config: list):
        self.labels = ["validation", "train", "test"]
        self.class_name = self.__class__.__name__
        self.config = config

        # dataset的路径
        self.dataset_path = os.path.join(os.getcwd(), "..", "..", self.datasets)
        self.this_dataset_path = os.path.join(self.dataset_path, self.class_name)
        os.makedirs(self.this_dataset_path, exist_ok=True)

        # downloads的路径
        self.downloads_path = os.path.join(os.getcwd(), "..", "..", self.downloads)
        self.this_download_path = os.path.join(self.downloads_path, self.class_name)

        # registry路径
        self.registry_path = os.path.join(os.getcwd(), "..", "registry")

        # test case的输出路径  xxx.jsonl
        this_dataset_registry_path = os.path.join(self.registry_path, "data", self.class_name)
        os.makedirs(this_dataset_registry_path, exist_ok=True)
        self.this_dataset_registry_file_path = os.path.join(this_dataset_registry_path, self.class_name + ".jsonl")

        # test suite的输出路径  xxx.yaml
        self.this_yaml_file_path = os.path.join(self.registry_path, "evals", self.class_name + ".yaml")

        # 执行
        self.generate_prompt_jsonl_batch()
        self.generate_evals_yaml_batch()

    def extract_and_save_datasets(self):
        """将原生格式转译为jsonl格式文件并存储到本地 datasets 目录"""
        raise ValueError("no such function named extract_and_save_datasets")

    def test_data_set_file_path(self):
        """返回eval评估的数据集文件地址"""
        return os.path.join(self.this_dataset_path, self.config[0] + ".jsonl")

    def read_dataset_as_list(self, dataset_file_path):
        """读取数据集为对象"""
        if not os.path.exists(dataset_file_path):
            self.extract_and_save_datasets()
        if os.path.exists(dataset_file_path):
            return evals.get_jsonls(dataset_file_path)
        raise ValueError(f"no such subset named {self.config}]")

    def format_chat_prompt(self, item):
        """生成一条prompt模板"""
        raise ValueError("no such function named format_chat_prompt")

    def format_one_json(self, item):
        """生成一条jsonl"""
        raise ValueError("no such function named format_one_json")

    def generate_prompt_jsonl_batch(self):
        """写jsonl文件"""
        with jsonlines.open(self.this_dataset_registry_file_path, "w") as f:
            for item in self.read_dataset_as_list(self.test_data_set_file_path()):
                f.write(self.format_one_json(item))

    def generate_evals_yaml_batch(self):
        """写yaml文件"""
        with open(self.this_yaml_file_path, "w") as f:
            f.write(self.format_one_yaml())

    def format_one_yaml(self):
        """生成test case模板"""
        return f"""
{self.class_name}_match:
  id: {self.class_name}.match1.v0
  metrics: [accuracy]
{self.class_name}.match1.v0:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: {self.class_name}/{self.class_name + ".jsonl"}

{self.class_name}_fact:
  id: {self.class_name}.fact1.v0
  metrics: [accuracy]
{self.class_name}.fact1.v0:
  class: evals.elsuite.modelgraded.classify:ModelBasedClassify
  args:
    samples_jsonl: {self.class_name}/{self.class_name + ".jsonl"}
    eval_type: cot_classify
    modelgraded_spec_file: fact
""".strip()


class WinoGrande(Generate):
    """https://github.com/allenai/winogrande 先手动下载"""

    def extract_and_save_datasets(self):
        resolve = {"test": "test.jsonl", "train": "train_l.jsonl", "validation": "dev.jsonl"}
        for label, filename in resolve.items():
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                for i in evals.get_jsonls(os.path.join(self.this_download_path, filename)):
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
        resolve = {"test": "cloze_test_test__winter2018-cloze_test_ALL_test - 1.csv",
                   "validation": "cloze_test_val__winter2018-cloze_test_ALL_val - 1 - 1.csv"}
        for label, filename in resolve.items():
            df = pd.read_csv(os.path.join(self.this_download_path, filename))
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

    def extract_and_save_datasets(self):
        resolve = {"test": ["datasets", "copa-test.xml"], "validation": ["datasets", "copa-dev.xml"]}
        for label, filename in resolve.items():
            document = parse(os.path.join(self.this_download_path, filename[0], filename[1]))
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
    """MultiRC (Multi-Sentence Reading Comprehension)
    http://www.eraserbenchmark.com/zipped/multirc.tar.gz
    """

    def extract_and_save_datasets(self):
        resolve = {"test": "test.jsonl", "validation": "val.jsonl", "train": "train.jsonl"}
        for label, filename in resolve.items():
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                for i in evals.get_jsonls(os.path.join(self.this_download_path, filename)):
                    # 把文章内容读取出来 存放到 story_content
                    with open(os.path.join(self.this_download_path, "docs", i["annotation_id"].split(":")[0]),
                              "r", encoding="UTF-8") as story:
                        i["story_content"] = story.read()
                    f.write(i)

    def format_one_json(self, item):
        return {}

    def format_chat_prompt(self, item):
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
    modelgraded_spec_file: fact
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
        resolve = {"train": "train-v2.0.json", "validation": "dev-v2.0.json"}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename), "r") as f:
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

    def extract_and_save_datasets(self):
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
        return [{"role": "system",
                 "content": "TASK: Read a passage and answer the following question concisely."},
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
        return {}

    def format_chat_prompt(self, item):
        return []


if __name__ == '__main__':
    # QuAC(config=["validation"])  # train/validation

    DROP(config=["validation"])  # train/validation

    RACE(config=["test"])  # test/train/validation

    SQuAD(config=["validation"])  # train/validation

    CNNDailyMail(config=["test"])  # test/train/validation

    COQA(config=["validation"])  # train/validation

    # MultiRC(config=["test"])  # test

    WSC(config=["test"])  # test

    BoolQ(config=["validation"])  # train/validation

    COPA(config=["test"])  # test/validation

    StoryCloze(config=["validation"])  # test(无答案)/validation

    WinoGrande(config=["test"])  # test/train/validation