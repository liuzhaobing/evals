# -*- coding:utf-8 -*-
from evals.elsuite.modelgraded.classify_utils import get_choice, MATCH_FNS
from evals.utils import cloudminds

PROMPT = """
现在需要你根据问题对比两个模型的回答，请从综合角度评判哪个模型的回答效果最好。以下是数据：
    [问题]: {input}
    [模型回答A]：{completionA}
    [模型回答B]：{completionB}

首先，一步步写出你的推理，并确保你的结论是客观的，避免一开始就简单地陈述正确答案。 然后只输出一个模型回答所对应的选项标签A、B，不带任何标点符号。 最后，在新的一行中单独重复选项标签。
推理：
""".strip()

if __name__ == '__main__':
    result = cloudminds.ChatCompletion.create(
        model="openai_api",
        prompt=PROMPT.format(input="[Round 0]\n问：春望的作者是谁\n答：《春望》是唐代诗人杜甫所作的诗歌。这首诗描绘了春天的景色，表现了诗人对自然的热爱和对生命的感悟。诗中通过描写春天的美景和生命的短暂，表达了诗人的感慨和思考，被誉为唐代诗歌中的经典之作。\n[Round 1]\n问：是什么题材的\n答：",
                             completionA="春望是五言律诗，是中国传统诗歌的一种体裁，简称五律，属于近体诗范畴。此体发源于南朝齐永明时期，其雏型是沈约等讲究声律、对偶的新体诗，至初唐沈佺期、宋之问时基本定型，成熟于盛唐时期。",
                             completionB="《春望》属于写景抒情的诗歌，主要题材是爱情、人生与自然。\n\n诗中写道：“国破山河在，城春草木深。感时花溅泪，恨别鸟惊心。”表达了诗人对国家破败、山河失陷的悲痛之情；“烽火连三月，家书抵万金”。")
    )
    print(result)
    choice = get_choice(text=result["choices"][-1]["message"]["content"],
                        eval_type="cot_classify_zh",
                        match_fn=MATCH_FNS["starts_or_endswith"],
                        choice_strings=['A', 'B'])
    print(choice)
