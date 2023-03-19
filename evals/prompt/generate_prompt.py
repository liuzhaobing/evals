# -*- coding:utf-8 -*-
import os
from typing import Any

import jsonlines
import evals
import logging
import pandas as pd
from datasets import load_dataset

logger = logging.getLogger(__name__)


class Generate:
    dataset = "dataset"

    def __init__(self, jsonl_path: list, yaml_path: list, test_dataset_path: list):
        """
        jsonl_path: jsonl 输出文件名
        yaml_path： yaml 输出文件名
        test_dataset_path： 数据集输入路径
        """
        self.jsonl_path = jsonl_path
        self.yaml_path = yaml_path
        self.test_dataset_path = test_dataset_path

        # dataset的路径
        self.dataset_path = os.path.join(os.getcwd(), "..", "..", self.dataset)

        # registry路径
        self.registry_path = os.path.join(os.getcwd(), "..", "registry")

        # test case的输出路径  xxx.jsonl
        this_dataset_registry_path = os.path.join(self.registry_path, "data", jsonl_path[0].split(".")[0])
        os.makedirs(this_dataset_registry_path, exist_ok=True)
        self.this_dataset_registry_file_path = os.path.join(this_dataset_registry_path, jsonl_path[0])

        # test suite的输出路径  xxx.yaml
        self.this_yaml_file_path = os.path.join(self.registry_path, "evals", yaml_path[0])

        # 执行
        self.generate_prompt_jsonl_batch()
        self.generate_evals_yaml_batch()

    def test_data_set_file_path(self): ...  # 获取数据集源文件加载地址 或者hugging face 地址

    def read_dataset_as_list(self, dataset_file_path) -> Any: ...  # 读取数据集为嵌套字典的列表

    def format_chat_prompt(self, item) -> Any: ...  # 生成一条prompt模板

    def format_one_json(self, item) -> dict: ...  # 生成一条jsonl

    def generate_prompt_jsonl_batch(self):  # 写jsonl文件
        with jsonlines.open(self.this_dataset_registry_file_path, "w") as f:
            for item in self.read_dataset_as_list(self.test_data_set_file_path()):
                f.write(self.format_one_json(item))

    def generate_evals_yaml_batch(self):  # 写yaml文件
        with open(self.this_yaml_file_path, "w") as f:
            f.write(self.format_one_yaml())

    def format_one_yaml(self):  # 生成test case模板
        return f"""
{self.jsonl_path[0].split(".")[0]}_match:
  id: {self.jsonl_path[0].split(".")[0]}.match1.v0
  metrics: [accuracy]
{self.jsonl_path[0].split(".")[0]}.match1.v0:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: {self.jsonl_path[0].split(".")[0]}/{self.jsonl_path[0]}

{self.jsonl_path[0].split(".")[0]}_fact:
  id: {self.jsonl_path[0].split(".")[0]}.fact1.v0
  metrics: [accuracy]
{self.jsonl_path[0].split(".")[0]}.fact1.v0:
  class: evals.elsuite.modelgraded.classify:ModelBasedClassify
  args:
    samples_jsonl: {self.jsonl_path[0].split(".")[0]}/{self.jsonl_path[0]}
    eval_type: cot_classify
    modelgraded_spec_file: fact
""".strip()


class WinoGrande(Generate):
    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["answer"])

    def test_data_set_file_path(self):
        return os.path.join(self.dataset_path, self.test_dataset_path[0], self.test_dataset_path[1])

    def read_dataset_as_list(self, this_dataset_file_path):
        """dataset读取为对象"""
        return evals.get_jsonls(this_dataset_file_path)

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": "TASK: Read the provided sentence with blank, then identify the correct option from given two options which can fill the blank precisely, in the format \"<answer>\". The answer should be number only."},
                {"role": "system", "content": f"sentence: {item['sentence']}"},
                {"role": "system", "content": f"option1: {item['option1']}"},
                {"role": "system", "content": f"option2: {item['option2']}"}]


class StoryCloze(Generate):
    """story_cloze"""

    def test_data_set_file_path(self):
        return os.path.join(self.dataset_path, self.test_dataset_path[0], self.test_dataset_path[1])

    def read_dataset_as_list(self, this_dataset_file_path):
        df = pd.read_csv(this_dataset_file_path)
        head_list = list(df.columns)
        return [dict(zip(head_list, line)) for line in df.values]

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
    """COPA (Choice of Plausible Alternatives)"""

    def test_data_set_file_path(self):
        return os.path.join(self.dataset_path,
                            self.test_dataset_path[0],
                            self.test_dataset_path[1],
                            self.test_dataset_path[2])

    def read_dataset_as_list(self, dataset_file_path):
        from xml.etree.ElementTree import parse
        document = parse(dataset_file_path)
        return [dict(id=item.attrib["id"],
                     asks_for=item.attrib["asks-for"],
                     most_plausible_alternative=item.attrib["most-plausible-alternative"],
                     p=item.findtext('p'),
                     a1=item.findtext('a1'),
                     a2=item.findtext('a2')) for item in document.iterfind('item')]

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

    def test_data_set_file_path(self):
        return os.path.join(self.dataset_path, self.test_dataset_path[0], self.test_dataset_path[1])

    def read_dataset_as_list(self, dataset_file_path):
        return evals.get_jsonls(dataset_file_path)

    def format_one_json(self, item):
        return []

    def format_chat_prompt(self, item):
        return []  # TODO


class BoolQ(Generate):
    """BoolQ (Boolean Questions)"""

    # def test_data_set_file_path(self):
    #     return os.path.join(self.dataset_path, self.test_dataset_path[0], self.test_dataset_path[1])

    # def read_dataset_as_list(self, dataset_file_path):
    #     return evals.get_jsonls(dataset_file_path)

    def test_data_set_file_path(self):
        return self.test_dataset_path

    def read_dataset_as_list(self, dataset_file_path):
        data = load_dataset(dataset_file_path[0])
        return [item for item in data['validation']]

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=str(item["answer"]))

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": "TASK: Read a short passage and judge whether the given question is correct, in the format \"<answer>\". The answer must be 'true' or 'false' only."},
                {"role": "system", "content": f"title: {item['title']}"},
                {"role": "system", "content": f"passage: {item['passage']}"},
                {"role": "user", "content": f"question: {item['question']}"}]


class WSC(Generate):
    """WSC (Winograd Schema Challenge)"""

    def test_data_set_file_path(self):
        return self.test_dataset_path

    def read_dataset_as_list(self, dataset_file_path):
        data = load_dataset(dataset_file_path[0], dataset_file_path[1])
        return [item for item in data['test']]

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

    def test_data_set_file_path(self):
        return self.test_dataset_path

    def read_dataset_as_list(self, dataset_file_path):
        data = load_dataset(dataset_file_path[0])
        return [item for item in data['validation']]

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
{self.jsonl_path[0].split(".")[0]}_match:
  id: {self.jsonl_path[0].split(".")[0]}.match1.v0
  metrics: [f1_score]
{self.jsonl_path[0].split(".")[0]}.match1.v0:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: {self.jsonl_path[0].split(".")[0]}/{self.jsonl_path[0]}

{self.jsonl_path[0].split(".")[0]}_fact:
  id: {self.jsonl_path[0].split(".")[0]}.fact1.v0
  metrics: [f1_score]
{self.jsonl_path[0].split(".")[0]}.fact1.v0:
  class: evals.elsuite.modelgraded.classify:ModelBasedClassify
  args:
    samples_jsonl: {self.jsonl_path[0].split(".")[0]}/{self.jsonl_path[0]}
    eval_type: cot_classify
    modelgraded_spec_file: fact
""".strip()


class CNNDailyMail(Generate):
    """CNN/Daily Mail"""

    def test_data_set_file_path(self):
        return self.test_dataset_path

    def read_dataset_as_list(self, dataset_file_path):
        data = load_dataset(dataset_file_path[0], dataset_file_path[1])
        return [item for item in data['test']]

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["highlights"])

    def format_chat_prompt(self, item):
        return [{"role": "system", "content": f"{item['article']}"}]

    def format_one_yaml(self): ...  # TODO


if __name__ == '__main__':
    # CNNDailyMail(jsonl_path=["CNNDailyMail.jsonl"], yaml_path=["CNNDailyMail.yaml"],
    #              test_dataset_path=["cnn_dailymail", "3.0.0"])

    COQA(jsonl_path=["COQA.jsonl"], yaml_path=["COQA.yaml"], test_dataset_path=["coqa"])

    # MultiRC(jsonl_path=["multirc.jsonl"], yaml_path=["multric.yaml"], test_dataset_path=["multric", "test.jsonl"])

    WSC(jsonl_path=["WSC.jsonl"], yaml_path=["WSC.yaml"], test_dataset_path=["winograd_wsc", "wsc273"])

    BoolQ(jsonl_path=["BoolQ.jsonl"], yaml_path=["BoolQ.yaml"], test_dataset_path=["boolq"])

    COPA(jsonl_path=["COPA.jsonl"], yaml_path=["COPA.yaml"],
         test_dataset_path=["COPA-resources", "datasets", "copa-dev.xml"])

    StoryCloze(jsonl_path=["story_cloze.jsonl"], yaml_path=["story_cloze.yaml"],
               test_dataset_path=["story_cloze", "cloze_test_val__winter2018-cloze_test_ALL_val - 1 - 1.csv"])

    WinoGrande(jsonl_path=["winogrande.jsonl"], yaml_path=["winogrande.yaml"],
               test_dataset_path=["winogrande", "dev.jsonl"])
