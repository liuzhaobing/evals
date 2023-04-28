# -*- coding:utf-8 -*-
import os

import evals
from evals.utils import util


def read_files(dir_name: str, allow_suffix: str = ".jsonl"):
    files = []
    for dir_path, dir_names, filenames in os.walk(dir_name):
        for filepath in filenames:
            file_full_path = os.path.join(dir_path, filepath)
            if file_full_path.endswith(allow_suffix):
                files.append(file_full_path)
    return files


def convert_jsonl_to_excel(filename):
    datas = evals.get_jsonls(filename)
    result = {"data": {}}
    for data in datas:
        if data.__contains__("spec"):
            result["model_name"] = data["spec"]["model_name"]
            result["eval_name"] = data["spec"]["base_eval"]
            result["run_id"] = data["spec"]["run_id"]
        if data.__contains__("type"):
            sample_id = data["sample_id"]
            if data["type"] == "sampling":
                res = {
                    "edg_cost_" + data["data"]["metadata"]["model"]: data["data"]["metadata"]["edg_cost"],
                    "prompt_" + data["data"]["metadata"]["model"]: data["data"]["prompt"],
                    "sampled_" + data["data"]["metadata"]["model"]: data["data"]["sampled"]
                }
            elif data["type"] == "metrics":
                res = {"choice": data["data"]["choice"]}
            elif data["type"] == "raw_sample":
                res = {"ideal": data["data"]["ideal"]}
            else:
                res = {}
            if result["data"].__contains__(sample_id):
                result["data"][sample_id] = dict(result["data"][sample_id], **res)
            else:
                result["data"][sample_id] = res
        continue
    excel_result = [value for _, value in result["data"].items()]
    util.save_data_to_xlsx(excel_result,
                           os.path.join(os.path.dirname(filename),
                                        f"{result['model_name']}_{result['eval_name']}_{result['run_id']}.xlsx"))


if __name__ == '__main__':
    all_files = read_files(f"/tmp/evallogs")
    for f in all_files:
        try:
            convert_jsonl_to_excel(f)
            print(f"[SUCCESS] - {f}")
        except:
            print(f"[FAILED] - {f}")
            continue
