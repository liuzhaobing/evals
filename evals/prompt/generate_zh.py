# -*- coding:utf-8 -*-
import json
import os.path
import tarfile
import urllib.request
import zipfile

import jsonlines
import pandas as pd

import evals
from evals.prompt.generate_base import Generate


class tnews(Generate):
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


class iflytek(Generate):
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
                {"role": "user", "content": f"应用程序描述：{item['sentence']}。"}]


class waimai_10k(Generate):
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
                {"role": "user", "content": f"评语：{item['review']}"}]


class ChnSentiCorp_htl_all(Generate):
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
                {"role": "user", "content": f"评语：{item['review']}"}]


class afqmc(Generate):
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
                {"role": "user", "content": f"句子1：{item['sentence1']}。"},
                {"role": "user", "content": f"句子2：{item['sentence2']}。"}]


class lcqmc(Generate):
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
                {"role": "user", "content": f"句子1：{item['sentence1']}。"},
                {"role": "user", "content": f"句子2：{item['sentence2']}。"}]


class cmrc(Generate):
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


class csl(Generate):
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
                {"role": "user", "content": f"关键词：{'、'.join(item['keyword'])}。"}]


class cluener2020(Generate):
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
                {"role": "user", "content": f"文本内容：{item['text']}。"}]


class cluewsc2020(Generate):
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
                {"role": "user",
                 "content": f"陈述：“{item['target']['span2_text']}”在句中指代“{item['target']['span1_text']}”。"}]


class bltc(Generate):
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


class MDCSC(Generate):
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
                {"role": "user", "content": f"句子：{item['sentence1']}"}]


class RiSAWOZ(Generate):
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


if __name__ == '__main__':
    # RiSAWOZ(config=["test"])

    MDCSC(config=["test"])  # test/train

    # bltc(config=["validation"])

    cluewsc2020(config=["validation"])  # test(无答案)/validation/train

    cluener2020(config=["validation"])  # test(无答案)/validation/train

    csl(config=["validation"])  # test(无答案)/validation/train

    cmrc(config=["validation"])  # test(无答案)/validation/train/trail

    lcqmc(config=["validation"])  # test(无答案)/validation/train

    afqmc(config=["validation"])  # test(无答案)/validation/train

    ChnSentiCorp_htl_all(config=["train"])  # train

    waimai_10k(config=["train"])  # train

    iflytek(config=["validation"])  # test(无答案)/validation/train

    tnews(config=["validation"])  # test(无答案)/validation/train
