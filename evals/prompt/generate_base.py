# -*- coding:utf-8 -*-
import os
import random

import jsonlines
import evals
import logging

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
            all_data = evals.get_jsonls(dataset_file_path)
            if len(self.config) > 1:
                if type(self.config[1]) == int:
                    """限定此测试集的样本数"""
                    return random.sample(all_data, self.config[1])
            return all_data
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
    modelgraded_spec: fact
""".strip()


class GenerateZh(Generate):
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
    eval_type: cot_classify_zh
    modelgraded_spec: fact_zh
""".strip()
