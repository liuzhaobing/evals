(1) cloze and completion
tasks [[1](https://aclanthology.org/P16-1144.pdf),[2](https://aclanthology.org/P19-1472.pdf),[3](https://aclanthology.org/N16-1098.pdf)];

(2) Open-domain question
answering [[4](https://aclanthology.org/P17-1147.pdf),[5](https://aclanthology.org/Q19-1026.pdf),[6](https://aclanthology.org/D13-1160.pdf)];

(3) [Winograd-style](https://en.wikipedia.org/wiki/Winograd_schema_challenge)
tasks [[7](https://www.aaai.org/ocs/index.php/KR/KR12/paper/download/4492/4924),[8](https://ojs.aaai.org/index.php/AAAI/article/view/6399/6255)];

(4) commonsense
reasoning [[9](https://ojs.aaai.org/index.php/AAAI/article/view/6239/6095),[10](https://arxiv.org/pdf/1803.05457.pdf),[11](https://aclanthology.org/D18-1260.pdf)];

(5) in-context reading
comprehension [[12](https://aclanthology.org/Q19-1016.pdf),[13](https://aclanthology.org/D18-1241.pdf),[14](https://aclanthology.org/N19-1246.pdf),[15](https://aclanthology.org/P18-2124.pdf),[16](https://aclanthology.org/D17-1082.pdf)];

(6) the [SuperGLUE](https://arxiv.org/abs/1905.00537) tasks;

(7) natural language inference

reference：https://ai.googleblog.com/2021/12/more-efficient-in-context-learning-with.html

# 一、评测指标Accuracy

## story_cloze

#### 数据集格式

```json
{
  "answer_right_ending": 1,
  "input_sentence_1": "Rick grew up in a troubled household.",
  "input_sentence_2": "He never found good support in family, and turned to gangs.",
  "input_sentence_3": "It wasn't long before Rick got shot in a robbery.",
  "input_sentence_4": "The incident caused him to turn a new leaf.",
  "sentence_quiz1": "He is happy now.",
  "sentence_quiz2": "He joined a gang.",
  "story_id": "138d5bfb-05cc-41e3-bf2c-fa85ebad14e2"
}
```

#### 数据解释

The data fields are the same among all splits.

- `input_sentence_1`: The first statement in the story.
- `input_sentence_2`: The second statement in the story.
- `input_sentence_3`: The third statement in the story.
- `input_sentence_4`: The forth statement in the story.
- `sentence_quiz1`: first possible continuation of the story.
- `sentence_quiz2`: second possible continuation of the story.
- `answer_right_ending`: correct possible ending; either 1 or 2.
- `story_id`: story id.

#### 数据集下载地址

*需要先下载并解压到本地*

Story Cloze Test Winter 2018 (recommended) set:

\* val set: https://goo.gl/XWjas1

\* test set: https://goo.gl/BcTtB4

Story Cloze Test Spring 2016 set:

\* val set: https://goo.gl/cDmS6I

\* test set: https://goo.gl/iE31Qm

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("story_cloze", "2018", data_dir=r"C:\Users\liuzhaobing\PycharmProjects\Train\data\story_cloze")
```

原文地址：https://huggingface.co/datasets/story_cloze

## winogrande

#### 数据集格式

| sentence (string)                                                                        | option1 (string) | option2 (string) | answer (string) |
|:-----------------------------------------------------------------------------------------|:-----------------|:-----------------|:----------------|
| "Sarah was a much better surgeon than Maria so _ always got the easier cases."           | "Sarah"          | "Maria"          | "2"             |
| "Sarah was a much better surgeon than Maria so _ always got the harder cases."           | "Sarah"          | "Maria"          | "1"             |
| "They were worried the wine would ruin the bed and the blanket, but the _ was't ruined." | "blanket"        | "bed"            | "2"             |
| "Terry tried to bake the eggplant in the toaster oven but the _ was too big."            | "eggplant"       | "toaster"        | "1"             |

#### 子类目

winogrande_debiased

winogrande_l

winogrande_m

winogrande_s

winogrande_xl

winogrande_xs

#### 数据集类型

test、train、validation

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("winogrande", "winogrande_xs")

dataset_test = dataset["test"]
```

原文地址：https://huggingface.co/datasets/winogrande

## ·Winograd-Style Tasks

论文地址：https://www.researchgate.net/publication/348342786_An_Analysis_of_Dataset_Overlap_on_Winograd-Style_Tasks

## COPA (Choice of Plausible Alternatives)

a tool for assessing progress in open-domain commonsense causal reasoning.

#### 数据集格式

```xml

<copa-corpus version="1.0">

    <item id="503" asks-for="effect" most-plausible-alternative="2">
        <p>Termites invaded the house.</p>
        <a1>The termites disappeared from the house.</a1>
        <a2>The termites ate through the wood in the house.</a2>
    </item>

    <item id="504" asks-for="effect" most-plausible-alternative="1">
        <p>The travelers reached the border.</p>
        <a1>The patrol agent checked their passports.</a1>
        <a2>The patrol agent accused them of smuggling.</a2>
    </item>

</copa-corpus>
```

#### 答案格式

```
503 0 1
504 1 0
```

The format [`item_id 1 0`] indicates that the response for the item `item_id` from the dataset was selected to be the
first alternative; similarly, [`item_id 0 1`] indicates that the second alternative was selected as response for the
item `item_id`.

#### 数据集下载地址

https://people.ict.usc.edu/~gordon/copa.html

#### 数据集说明

Included in this package are the following resources:

- `datasets/copa-dev.xml` : 500 questions of the development set
- `datasets/copa-test.xml` : 500 questions of the test set
- `datasets/copa-all.xml` : 1000 questions of both the development and test sets
- `datasets/copa.dtd` : The format of the XML question files
- `results/gold.*` : Correct answers for each set of questions
- `results/baselineFirst.*` : Choices where the first alternative is always selected
- `results/PMIgutenbergW5.*` : Choices made by the best-performing baseline system of Roemmele et al, 2011.
- `copa-eval.jar` : A java package for computing statistical significance of differences in answer sets
- `copa-eval.sh` : A simple shell script for using the java package

#### 使用方式

-

原文地址：https://paperswithcode.com/dataset/copa

## ·WiC (Words in Context)

原文地址：https://paperswithcode.com/dataset/wic

## WSC (Winograd Schema Challenge)

根据语境推测句子中代词的指代对象 A Winograd schema is a pair of sentences differing in one or two words with a highly
ambiguous pronoun,

#### 数据集格式

```json
{
  "label": 0,
  "options": [
    "The city councilmen",
    "The demonstrators"
  ],
  "pronoun": "they",
  "pronoun_loc": 63,
  "quote": "they feared violence",
  "quote_loc": 63,
  "source": "(Winograd 1972)",
  "text": "The city councilmen refused the demonstrators a permit because they feared violence."
}
```

#### 数据解释

- `text` (str): The text sequence
- `options` (list[str]): The two entity options that the pronoun may be referring to
- `label` (int): The index of the correct option in the `options` field
- `pronoun` (str): The pronoun in the sequence to be resolved
- `pronoun_loc` (int): The starting position of the pronoun in the sequence
- `quote` (str): The substr with the key action or context surrounding the pronoun
- `quote_loc` (int): The starting position of the quote in the sequence
- `source` (str): A description of the source who contributed the example

#### 子类目

wsc285

wsc273

#### 数据集类型

test

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("winograd_wsc", "wsc273")
dataset_test = dataset["test"]
```

原文地址：https://paperswithcode.com/dataset/wsc

## BoolQ (Boolean Questions)

阅读短文判断给出的问法是否正确

#### 数据集格式

```json
{
  "answer": false,
  "passage": "\"All biomass goes through at least some of these steps: it needs to be grown, collected, dried, fermented, distilled, and burned...",
  "question": "does ethanol take more energy make that produces"
}

```

#### 数据集类型

validation、train

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("boolq")
dataset_test = dataset["validation"]
```

原文地址：https://paperswithcode.com/dataset/boolq

## **·Reading Comprehension with Commonsense Reasoning Dataset** (ReCoRD)

原文地址：https://paperswithcode.com/dataset/record

## ·RTE (Recognizing Textual Entailment)

原文地址：https://paperswithcode.com/dataset/rte

# 二、评测指标SummaCZS; ROUGE-1, 2, L, LSum; METEOR; BLEU

## CNN/Daily Mail

简要概况新闻内容

#### 数据集格式

```json
{
  "id": "0054d6d30dbcad772e20b22771153a2a9cbeaf62",
  "article": "(CNN) -- An American woman died aboard a cruise ship that docked at Rio de Janeiro on Tuesday, the same ship on which 86 passengers previously fell ill, according to the state-run Brazilian news agency, Agencia Brasil. The American tourist died aboard the MS Veendam, owned by cruise operator Holland America. Federal Police told Agencia Brasil that forensic doctors were investigating her death. The ship's doctors told police that the woman was elderly and suffered from diabetes and hypertension, according the agency. The other passengers came down with diarrhea prior to her death during an earlier part of the trip, the ship's doctors said. The Veendam left New York 36 days ago for a South America tour.",
  "highlights": "The elderly woman suffered from diabetes and hypertension, ship's doctors say .\nPreviously, 86 passengers had fallen ill on the ship, Agencia Brasil says ."
}
```

#### 数据解释

- `id`: a string containing the heximal formated SHA1 hash of the url where the story was retrieved from
- `article`: a string containing the body of the news article
- `highlights`: a string containing the highlight of the article as written by the article author

#### 数据集

(cnn_dailymail_dutch)
(cnn_dailymail)
(test2)
(citesum)
(atypical_animacy)
(asrs-aviation-reports)

#### 子类目

1.0.0/2.0.0/3.0.0

#### 数据集类型

test、train、validation

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("cnn_dailymail", "3.0.0")
```

原文地址：https://paperswithcode.com/dataset/cnn-daily-mail-1

# 三、评测指标Matthew’s correlation coefficient

解释：MCC, Its job is to gauge or measure the difference between the predicted values and actual values and is equivalent
to chi-square statistics for a 2 x 2 contingency table.

### ·axb-Broad Coverage Diagnostics

# 四、评测指标EM / F1

## MultiRC (Multi-Sentence Reading Comprehension)

#### 数据集格式

阅读一篇短文章`Fiction-stories-masc-A_Wasted_Day-2.txt`，根据问题`query`提炼出文章中的n条main topic，断言模型预测出的main
topic与数据集预期的main topic是否完全相等。

#### 数据集类型

test、train、validation

#### 数据集下载地址

*需要下载并解压到本地*

http://www.eraserbenchmark.com/zipped/multirc.tar.gz

中文/繁体测试语料可参考地址：https://blog.51cto.com/u_15064656/4274624

#### 使用方式

支持框架TensorFlow：https://www.tensorflow.org/datasets/catalog/eraser_multi_rc

```python
from datasets import load_dataset

dataset = load_dataset("eraser_multi_rc", data_dir=r"C:\Users\liuzhaobing\PycharmProjects\Train\data\multirc")

dataset_test = dataset["test"]
```

原文地址：https://paperswithcode.com/dataset/multirc

# 五、评测指标Perplexity

## ·Penn Treebank

#### 使用方法

```python
import torchtext

dataset = torchtext.datasets.PennTreebank(split="test")
```

原文地址：https://paperswithcode.com/dataset/penn-treebank

# 六、评测指标Exact Match，F1

## CoQA (Conversational Question Answering Challenge)

understand a text passage and answer a series of interconnected questions that appear in a conversation.

#### 数据集格式

```json lines
{
  "answers": "{\"answer_end\": [179, 494, 511, 545, 879, 1127, 1128, 94, 150, 412, 1009, 1046, 643, -1, 764, 724, 125, 1384, 881, 910], \"answer_...",
  "questions": "[\"When was the Vat formally opened?\", \"what is the library for?\", \"for what subjects?\", \"and?\", \"what was started in 2014?\", \"ho...",
  "source": "wikipedia",
  "story": "\"The Vatican Apostolic Library (), more commonly called the Vatican Library or simply the Vat, is the library of the Holy See, l..."
}
```

#### 数据解释

- `source`: a `string` feature.
- `story`: a `string` feature.
- `questions`: a `list` of `string` features.
- `answers`: a `dictionary` feature containing:
    - `input_text`: a `string` feature.
    - `answer_start`: a `int32` feature.
    - `answer_end`: a `int32` feature.

#### 数据集类型

validation、train

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("coqa")
```

原文地址：https://paperswithcode.com/dataset/coqa

## QuAC (Question Answering in Context)

原文地址：https://paperswithcode.com/dataset/quac

