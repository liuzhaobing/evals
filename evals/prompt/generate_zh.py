# -*- coding:utf-8 -*-
import json
import os.path
import tarfile
import urllib.request
import zipfile

import jsonlines
import pandas as pd

import evals
from evals.prompt.generate_base import GenerateZh


class tnews(GenerateZh):
    """
    今日头条中文新闻（短文本）分类
 该数据集来自今日头条的新闻版块，共提取了15个类别的新闻，包括旅游，教育，金融，军事等
 数据量：训练集(53,360)，验证集(10,000)，测试集(10,000)
    """
    d_url = "https://storage.googleapis.com/cluebenchmark/tasks/tnews_public.zip"
    tnews_tags = {"news_story": "故事",
                  "news_culture": "文化",
                  "news_entertainment": "娱乐",
                  "news_sports": "体育",
                  "news_finance": "财经",
                  "news_house": "房产",
                  "news_car": "汽车",
                  "news_edu": "教育",
                  "news_tech": "科技",
                  "news_military": "军事",
                  "news_travel": "旅游",
                  "news_world": "国际",
                  "news_stock": "股票",
                  "news_agriculture": "农业",
                  "news_game": "游戏"}

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": ["test.json", "test1.0.json"], "train": ["train.json"], "validation": ["dev.json"]}
        for label, filename in resolve.items():
            file_content = evals.get_jsonls(os.path.join(self.this_download_path, filename[-1]))
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as jsonf:
                for content in file_content:
                    if content.__contains__("label_desc"):
                        content["label_zh"] = self.tnews_tags[content["label_desc"]]
                    jsonf.write(content)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["label_zh"])

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": f"任务：阅读新闻片段并判断新闻类别，请简要给出两个字的答案，例如：财经。新闻片段：{item['sentence']}"}]


class iflytek(GenerateZh):
    """
    该数据集共有1.7万多条关于app应用描述的长文本标注数据，包含和日常生活相关的各类应用主题，共119个类别：""打车"":0,""地图导航"":1,""免费WIFI"":2,""租车"":3,….,""女性"":115,""经营"":116,""收款"":117,""其他"":118(分别用0-118表示
 数据量：训练集(12,133)，验证集(2,599)，测试集(2,600)
    """
    d_url = "https://storage.googleapis.com/cluebenchmark/tasks/iflytek_public.zip"
    iflytek_tags = ["打车", "地图导航", "免费WIFI", "租车", "同城服务", "快递物流", "婚庆", "家政", "公共交通", "政务",
                    "社区服务", "薅羊毛", "魔幻", "仙侠", "卡牌", "飞行空战", "射击游戏", "休闲益智", "动作类",
                    "体育竞技", "棋牌中心", "经营养成", "策略", "MOBA", "辅助工具", "约会社交", "即时通讯", "工作社交",
                    "论坛圈子", "婚恋社交", "情侣社交", "社交工具", "生活社交", "微博博客", "新闻", "漫画", "小说",
                    "技术", "教辅", "问答交流", "搞笑", "杂志", "百科", "影视娱乐", "求职", "兼职", "视频", "短视频",
                    "音乐", "直播", "电台", "K歌", "成人", "中小学", "职考", "公务员", "英语", "视频教育", "高等教育",
                    "成人教育", "艺术", "语言(非英语)", "旅游资讯", "综合预定", "民航", "铁路", "酒店", "行程管理",
                    "民宿短租", "出国", "工具", "亲子儿童", "母婴", "驾校", "违章", "汽车咨询", "汽车交易", "日常养车",
                    "行车辅助", "租房", "买房", "装修家居", "电子产品", "问诊挂号", "养生保健", "医疗服务", "减肥瘦身",
                    "美妆美业", "菜谱", "餐饮店", "体育咨讯", "运动健身", "支付", "保险", "股票", "借贷", "理财",
                    "彩票", "记账", "银行", "美颜", "影像剪辑", "摄影修图", "相机", "绘画", "二手", "电商", "团购",
                    "外卖", "电影票务", "社区超市", "购物咨询", "笔记", "办公", "日程管理", "女性", "经营", "收款",
                    "其他"]

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": "test.json", "train": "train.json", "validation": "dev.json"}
        for label, filename in resolve.items():
            file_content = evals.get_jsonls(os.path.join(self.this_download_path, filename))
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as jsonf:
                jsonf.write_all(file_content)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["label_des"])

    def format_chat_prompt(self, item):
        return [{"role": "system", "content": "任务：阅读应用程序描述，从给出的标签中选出一个最适合它的应用分类。"},
                {"role": "system", "content": f"标签：{'、'.join(self.iflytek_tags)}。"},
                {"role": "system", "content": f"应用程序描述：{item['sentence']}。"}]


class waimai_10k(GenerateZh):
    """
    某外卖平台收集的用户评价，正向4000 条，负向约 8000 条
    """
    d_url = "https://raw.githubusercontent.com/SophonPlus/ChineseNlpCorpus/master/datasets/waimai_10k/waimai_10k.csv"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".csv")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        df = pd.read_csv(this_download_filename)
        head_list = list(df.columns)
        with jsonlines.open(os.path.join(self.this_dataset_path, "train.jsonl"), "w") as f:
            for line in df.values:
                f.write(dict(zip(head_list, line)))

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal="积极" if item["label"] else "消极")

    def format_chat_prompt(self, item):
        return [{"role": "system", "content": "任务：根据客人的评语推测他对本次用餐体验是积极还是消极态度。"},
                {"role": "system", "content": f"评语：{item['review']}"}]


class ChnSentiCorp_htl_all(GenerateZh):
    """
    7000 多条酒店评论数据，5000 多条正向评论，2000 多条负向评论
    """
    d_url = "https://raw.githubusercontent.com/SophonPlus/ChineseNlpCorpus/master/datasets/ChnSentiCorp_htl_all/ChnSentiCorp_htl_all.csv"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".csv")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        df = pd.read_csv(this_download_filename)
        head_list = list(df.columns)
        with jsonlines.open(os.path.join(self.this_dataset_path, "train.jsonl"), "w") as f:
            for line in df.values:
                f.write(dict(zip(head_list, line)))

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal="积极" if item["label"] else "消极")

    def format_chat_prompt(self, item):
        return [{"role": "system", "content": "任务：根据客人的评语推测他对本次酒店入住体验是积极还是消极态度。"},
                {"role": "system", "content": f"评语：{item['review']}"}]


class afqmc(GenerateZh):
    """
    蚂蚁金融语义相似度
    训练集（34334）验证集（4316）测试集（3861）
    """
    d_url = "https://storage.googleapis.com/cluebenchmark/tasks/afqmc_public.zip"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": "test.json", "train": "train.json", "validation": "dev.json"}
        for label, filename in resolve.items():
            file_content = evals.get_jsonls(os.path.join(self.this_download_path, filename))
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as jsonf:
                for content in file_content:
                    jsonf.write(content)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal="是" if int(item["label"]) else "否")

    def format_chat_prompt(self, item):
        return [{"role": "system", "content": "任务：判断两个句子语义是否相似，回答“否”或者“是”。"},
                {"role": "system", "content": f"句子1：{item['sentence1']}。"},
                {"role": "system", "content": f"句子2：{item['sentence2']}。"}]


class lcqmc(GenerateZh):
    """
    通用领域匹配数据集，该数据集从百度知道不同领域的用户问题中抽取构建数据。
    训练集：238766 开发集：8802  测试集：12500
    """
    d_url = "https://dataset-bj.cdn.bcebos.com/qianyan/lcqmc.zip"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": "test.tsv", "train": "train.tsv", "validation": "dev.tsv"}

        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, self.class_name, filename), "r", encoding="UTF-8") as f:
                file_content = f.readlines()
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                for content in file_content:
                    line = content.strip().split("\t")
                    f.write(dict(sentence1=line[0], sentence2=line[1], label=line[2] if len(line) > 2 else -1))

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal="是" if int(item["label"]) else "否")

    def format_chat_prompt(self, item):
        return [{"role": "system", "content": "任务：判断两个句子语义是否相似，回答“否”或者“是”。"},
                {"role": "system", "content": f"句子1：{item['sentence1']}。"},
                {"role": "system", "content": f"句子2：{item['sentence2']}。"}]


class cmrc(GenerateZh):
    """
    数据量：训练集(短文数2,403，问题数10,142)，试验集(短文数256，问题数1,002)，开发集(短文数848，问题数3,219)
    """
    d_url = "https://storage.googleapis.com/cluebenchmark/tasks/cmrc2018_public.zip"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": "test.json", "train": "train.json", "validation": "dev.json", "trial": "trial.json"}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename), "r", encoding="UTF-8") as f:
                file_content = json.load(f)["data"]
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                f.write_all(file_content)

    def format_one_json(self, item):
        template, answers = self.format_chat_prompt(item)
        return dict(input=template, ideal=answers)

    def format_chat_prompt(self, item):
        template = [{"role": "system", "content": "任务：阅读短文并按照顺序回答所有的问题，回答必须清晰简洁。"},
                    {"role": "system", "content": f"短文题目：{item['title']}。"}]
        answers = []
        for paragraphs in item["paragraphs"]:
            template.append({"role": "system", "content": f"短文内容：{paragraphs['context']}。"})
            for qas in paragraphs["qas"]:
                template.append({"role": "user", "content": f"问题：{qas['question']}"})
                answers.append([answer["text"] for answer in qas["answers"]])
        return template, answers


class csl(GenerateZh):
    """
    中文科技文献数据集(CSL)取自中文论文摘要及其关键词，论文选自部分中文社会科学和自然科学核心期刊
    数据量：训练集(20,000)，验证集(3,000)，测试集(3,000)
    """
    d_url = "https://storage.googleapis.com/cluebenchmark/tasks/csl_public.zip"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": "test.json", "train": "train.json", "validation": "dev.json"}
        for label, filename in resolve.items():
            file_content = evals.get_jsonls(os.path.join(self.this_download_path, filename))
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                f.write_all(file_content)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal="正确" if int(item["label"]) else "错误")

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": "任务：阅读论文摘要后提取关键词，判断如下提供的关键词是否正确，回答“正确”或“错误”。"},
                {"role": "system", "content": f"摘要：{item['abst']}。"},
                {"role": "system", "content": f"关键词：{'、'.join(item['keyword'])}。"}]


class cluener2020(GenerateZh):
    """
    数据分为10个标签类别，分别为: 地址（address），书名（book），公司（company），游戏（game），政府（government），电影（movie），姓名（name），组织机构（organization），职位（position），景点（scene）,
    训练集：10748, 验证集集：1343
    """
    d_url = "https://storage.googleapis.com/cluebenchmark/tasks/cluener_public.zip"
    cluener_tags = {
        "address": "地址",
        "book": "书名",
        "company": "公司",
        "game": "游戏",
        "government": "政府",
        "movie": "电影",
        "name": "姓名",
        "organization": "组织机构",
        "position": "职位",
        "scene": "景点",
    }

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": "test.json", "train": "train.json", "validation": "dev.json"}
        for label, filename in resolve.items():
            file_content = evals.get_jsonls(os.path.join(self.this_download_path, filename))
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                f.write_all(file_content)

    def format_one_json(self, item):
        ideal = []
        for category, detail in item["label"].items():
            category_zh = self.cluener_tags[category]
            for entity in detail.keys():
                ideal.append(f"{entity}({category_zh})")

        return dict(input=self.format_chat_prompt(item), ideal=ideal)

    def format_chat_prompt(self, item):
        return [{"role": "system", "content": "任务：按照实体类别提取下面这段文本的实体。"},
                {"role": "system", "content": f"备选的实体类别：{'、'.join(self.cluener_tags.values())}。"},
                {"role": "system", "content": f"文本内容：{item['text']}。"}]


class cluewsc2020(GenerateZh):
    """
    判断句子中的代词指代的是哪个名词
    训练集（1244）验证集（304）
    """
    d_url = "https://storage.googleapis.com/cluebenchmark/tasks/cluewsc2020_public.zip"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": ["test.json", "test1.0.json"], "train": ["train.json"], "validation": ["dev.json"]}
        for label, filename in resolve.items():
            file_content = evals.get_jsonls(os.path.join(self.this_download_path, filename[-1]))
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                f.write_all(file_content)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal="正确" if item["label"] == "true" else "错误")

    def format_chat_prompt(self, item):
        return [{"role": "system", "content": "任务：阅读一段文本，判断陈述句中指代是否正确，回答“正确”或“错误”。"},
                {"role": "system", "content": f"文本内容：{item['text']}"},
                {"role": "system",
                 "content": f"陈述：“{item['target']['span2_text']}”在句中指代“{item['target']['span1_text']}”。"}]


class bltc(GenerateZh):
    """低资源语言翻译,中俄平行数据，泰语单语数据"""
    d_url = "https://dataset-bj.cdn.bcebos.com/qianyan/bltc.tar.gz"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".tar.gz")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with tarfile.open(this_download_filename, "r:gz") as tar:
            tar.extractall(self.this_download_path)
        os.remove(this_download_filename)
        # TODO

    def format_one_json(self, item):
        return {}

    def format_chat_prompt(self, item):
        return []


class MDCSC(GenerateZh):
    """
    人工标注了8000多条中文多领域拼写错误及正确的句子对
    """
    d_url = "https://dataset-bj.cdn.bcebos.com/qianyan/MD-CSC.zip"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": ["law.test", "med.test", "odw.test"], "train": ["law.train", "med.train", "odw.train"]}
        for label, filename in resolve.items():
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as jsonf:
                for file in filename:
                    with open(os.path.join(self.this_download_path, "MD-CSC", file), "r", encoding="UTF-8") as f:
                        file_content = f.readlines()
                        for content in file_content:
                            content_list = content.strip().split("\t")
                            jsonf.write(dict(label=content_list[0],
                                             sentence1=content_list[1],
                                             sentence2=content_list[2]))

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["sentence2"])

    def format_chat_prompt(self, item):
        return [{"role": "system",
                 "content": "任务：指出句中的错字并给出纠正后的句子，只回答纠正后的句子，如果句子没有错误就回答句子本身。"},
                {"role": "system", "content": f"句子：{item['sentence1']}"}]


class RiSAWOZ(GenerateZh):
    """
    具有丰富语义信息标注的大规模中文多领域任务型对话数据集，它包含1.12万个已标注的人-人多轮对话，总对话轮数超过15万轮，覆盖12个领域
    """
    d_url = "https://dataset-bj.cdn.bcebos.com/qianyan/RiSAWOZ.zip"

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".zip")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with zipfile.ZipFile(this_download_filename) as zip_ref:
            zip_ref.extractall(self.this_download_path)
        os.remove(this_download_filename)
        resolve = {"test": "test.json", "train": "train.json", "validation": "dev.json"}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, self.class_name, filename), "r", encoding="UTF-8") as f:
                file_content = json.load(f)
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                f.write_all(file_content)

    def format_one_json(self, item):
        # TODO
        return {}

    def format_chat_prompt(self, item):
        # TODO
        return []


class xfinal(GenerateZh):
    """机器翻译 """
    d_url = "https://storage.googleapis.com/paws/pawsx/x-final.tar.gz"
    lang = {
        "de": "德语",
        "en": "英语",
        "es": "西班牙语",
        "fr": "法语",
        "ja": "日语",
        "ko": "韩语",
        "zh": "中文"
    }

    def extract_and_save_datasets(self):
        os.makedirs(self.this_download_path, exist_ok=True)
        this_download_filename = os.path.join(self.this_download_path, self.class_name + ".tar.gz")
        urllib.request.urlretrieve(self.d_url, this_download_filename)
        with tarfile.open(this_download_filename, "r:gz") as tar:
            tar.extractall(self.this_download_path)
        os.remove(this_download_filename)

        resolve = {"test": "test_2k.tsv", "validation": "dev_2k.tsv", "train": "translated_train.tsv"}
        for label, filename in resolve.items():
            with jsonlines.open(os.path.join(self.this_dataset_path, f"{label}.jsonl"), "w") as f:
                tmp_list = []
                for lang_en, lang_zh in self.lang.items():
                    now_file = os.path.join(self.this_download_path, "x-final", lang_en, filename)
                    df = pd.read_csv(now_file, sep="\t", header=0, encoding="UTF-8")
                    head_list = list(df.columns)
                    values = df.values

                    if len(tmp_list) > 0:
                        for index in range(len(values)):
                            value = dict(zip(head_list, values[index]))
                            tmp_list[index]["sentence1_" + lang_en] = value["sentence1"]
                            tmp_list[index]["sentence2_" + lang_en] = value["sentence2"]

                    else:
                        for line in values:
                            value = dict(zip(head_list, line))
                            tmp_list.append({"id": value["id"],
                                             "sentence1_" + lang_en: value["sentence1"],
                                             "sentence2_" + lang_en: value["sentence2"],
                                             "label": value["label"]})
                # TODO
                f.write_all(tmp_list)


class semantic_similarity(GenerateZh):
    """
    本地qqsim测试数据
    """

    def extract_and_save_datasets(self):
        resolve = {"test": "semantic_similarity.xlsx"}
        for label, filename in resolve.items():
            df = pd.read_excel(io=os.path.join(self.this_download_path, filename), sheet_name="Sheet1")
            head_list = list(df.columns)
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as f:
                for line in df.values:
                    f.write(dict(zip(head_list, line)))

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal="是" if int(item["label"]) else "否")

    def format_chat_prompt(self, item):
        return [{"role": "system", "content": "任务：判断两个句子语义是否相似，回答“否”或者“是”。"},
                {"role": "system", "content": f"句子1：{item['sentence1']}。"},
                {"role": "system", "content": f"句子2：{item['sentence2']}。"}]


class dureader_checklist(GenerateZh):
    """
    refer: https://github.com/zhoujx4/DuReader-Checklist-BASELINE
    """

    def extract_and_save_datasets(self):
        resolve = {"test": "test1.json", "train": "train.json", "validation": "dev.json"}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename), encoding="utf-8") as f:
                datas = json.load(f)
                datas = datas["data"][0]["paragraphs"]
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


class Ape210K(GenerateZh):
    def extract_and_save_datasets(self):
        resolve = {"test": "test.ape.json", "train": "train.ape.json", "validation": "valid.ape.json"}
        for label, filename in resolve.items():
            datas = open(os.path.join(self.this_download_path, filename), encoding="utf-8").readlines()
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                wf.write_all(datas)

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


class WebQA(GenerateZh):
    def extract_and_save_datasets(self):
        resolve = {"test": "me_test.ann.json", "train": "me_train.json", "validation": "me_validation.ann.json"}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename), encoding="utf-8") as f:
                datas = json.load(f)
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                    for key, value in datas.items():
                        wf.write(value)

    def format_one_json(self, item):
        answer = ""
        for key, value in item["evidences"].items():
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


class Math23k(GenerateZh):
    def extract_and_save_datasets(self):
        resolve = {"test": "math23k_test.json"}
        for label, filename in resolve.items():
            datas = json.load(open(os.path.join(self.this_download_path, filename), encoding="utf-8"))
            with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                wf.write_all(datas)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["ans"])

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": item["original_text"],
            }
        ]


class MultiArith(GenerateZh):
    """MultiArith数学计算
    test: 600

    refer: https://github.com/wangxr14/Algebraic-Word-Problem-Solver
    """

    def extract_and_save_datasets(self):
        resolve = {"test": "MultiArith.json"}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename), encoding="utf-8") as f:
                datas = json.load(f)
                with jsonlines.open(os.path.join(self.this_dataset_path, label + ".jsonl"), "w") as wf:
                    for item in datas:
                        wf.write(item)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["lSolutions"])

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": "answer the following questions, you only need to give the answer, no need to give a step of information,question is:" +
                           item["sQuestion"],
            }
        ]


# 基本常识
class JBCS(GenerateZh):
    def extract_and_save_datasets(self):
        questions = [{
            "question": "中国的首都是哪里？",
            "answer": "北京"
        }, {
            "question": "在太阳系9大行星中，最大的行星是哪一颗？",
            "answer": "木星"
        }, {
            "question": "为中国赢得第一块澳运会金牌的项目是？",
            "answer": "射击"
        }, {
            "question": "世界最高峰是什么峰？",
            "answer": "珠穆朗玛峰"
        }, {
            "question": "世界上面积最大的国家是哪个国家？",
            "answer": "俄罗斯"
        }
        ]
        with jsonlines.open(os.path.join(self.this_dataset_path, "test.jsonl"), "w") as wf:
            for item in questions:
                wf.write(item)

    def format_one_json(self, item):
        return dict(input=self.format_chat_prompt(item), ideal=item["answer"])

    def format_chat_prompt(self, item):
        return [
            {
                "role": "system",
                "content": item["question"],
            }
        ]


class PKUMOD_CCKS(GenerateZh):
    def extract_and_save_datasets(self):
        resolve = {"test": ("验证集问题.txt", "验证集答案.txt")}
        for label, filename in resolve.items():
            with open(os.path.join(self.this_download_path, filename[0]), encoding="utf-8") as f:
                with open(os.path.join(self.this_download_path, filename[1]), encoding="utf-8") as f2:
                    datas = f.readlines()
                    datas2 = f2.readlines()
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
    sample = 100

    # semantic_similarity(config=["test"])

    # xfinal(config=["test"])

    # RiSAWOZ(config=["test"])

    MDCSC(config=["test"])  # test/train

    # bltc(config=["validation"])

    cluewsc2020(config=["validation", sample])  # test(无答案)/validation/train

    cluener2020(config=["validation", sample])  # test(无答案)/validation/train

    csl(config=["validation", sample])  # test(无答案)/validation/train

    cmrc(config=["validation", sample])  # test(无答案)/validation/train/trail

    lcqmc(config=["validation", sample])  # test(无答案)/validation/train

    afqmc(config=["validation", sample])  # test(无答案)/validation/train

    ChnSentiCorp_htl_all(config=["train", sample])  # train

    waimai_10k(config=["train", sample])  # train

    iflytek(config=["validation", sample])  # test(无答案)/validation/train

    tnews(config=["validation", sample])  # test(无答案)/validation/train

    Ape210K(config=["test", sample])  # test/train/validation

    dureader_checklist(config=["validation", sample])  # test(无答案)/train/validation

    WebQA(config=["test", sample])  # test/train/validation

    Math23k(config=["test", sample])  # test

    PKUMOD_CCKS(config=["test", sample])  # test

    MultiArith(config=["test", sample])  # test
