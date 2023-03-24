import jsonlines
import os
import json
from evals.prompt.generate_base import Generate


class Anli(Generate):
    def extract_and_save_datasets(self):
        resolve = {"test": "R3/dev.jsonl"}
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

if __name__ == '__main__':
    Anli(config=["test"])  # test(无答案)/train/validation
