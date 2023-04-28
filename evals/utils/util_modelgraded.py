# -*- coding:utf-8 -*-
from evals.elsuite.modelgraded.classify_utils import get_choice, MATCH_FNS
from evals.utils import cloudminds

PROMPT = """
现在需要你根据问题和标准答案评估另一个模型的回复。只需要答案包含即可，模型提供了额外的信息不算分歧, 下面是数据:
[BEGIN DATA]
************
[问题]: {input}
************
[标准答案]: {ideal}
************
[模型提交的答案]: {completion}
************
[END DATA]

将标准答案与模型提交的答案进行比较。 忽略风格、语法或标点符号的任何差异。
模型提交的答案可能是标准答案的子集或超集，也可能与其冲突。 确定适用哪种情况。 通过选择以下选项之一回答问题：
 (A) 模型提交的答案是标准答案的子集，并且与其完全一致。
 (B) 模型提交的答案是标准答案的超集，并且与其完全一致。
 (C) 模型提交的答案包含与标准答案相同的所有细节。
 (D) 模型提交的答案与标准答案存在分歧。
 (E) 模型提交的答案和标准答案不同，但从事实性的角度来看，这些差异无关紧要。

首先，一步步写出你的推理，并确保你的结论是正确的，避免一开始就简单地陈述正确答案。 然后只输出一个正确答案所对应的选项标签A、B、C、D、E，不带任何标点符号。 最后，在新的一行中单独重复选项标签。

推理：
""".strip()

if __name__ == '__main__':
    result = cloudminds.ChatCompletion.create(
        model="openai_api",
        prompt=PROMPT.format(input="时未寒的主要成就是什么",
                             ideal="时未寒主要成就是：发表作品两百余万字。",
                             completion="时未寒是一位中国作家，出生于 1970 年代，四川人。他是大陆新武侠四杰之一，与凤歌、王晴川、小椴合称南凤歌北晴川西未寒东小椴。时未寒的作品以金戈铁马、英雄气概和技击的阳刚之气著称，被誉为大陆新武侠扛鼎之作。他的代表作包括《碎空刀》、《偷天弓》、《换日箭》、《山河》等。时未寒已经发表了两百余万字的作品，出版有长篇小说多部。")
    )
    choice = get_choice(text=result["choices"][-1]["message"]["content"],
                        eval_type="cot_classify_zh",
                        match_fn=MATCH_FNS["starts_or_endswith"],
                        choice_strings=['A', 'B', 'C', 'D', 'E'])
    print(choice)
