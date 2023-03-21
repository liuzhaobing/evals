## story_cloze

*'Story Cloze Test' is a new commonsense reasoning framework for evaluating story understanding, story generation, and
script learning.This test requires a system to choose the correct ending to a four-sentence story.*

原文地址：https://huggingface.co/datasets/story_cloze

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

#### 格式说明

The data fields are the same among all splits.

- `input_sentence_1`: The first statement in the story.
- `input_sentence_2`: The second statement in the story.
- `input_sentence_3`: The third statement in the story.
- `input_sentence_4`: The forth statement in the story.
- `sentence_quiz1`: first possible continuation of the story.
- `sentence_quiz2`: second possible continuation of the story.
- `answer_right_ending`: correct possible ending; either 1 or 2.
- `story_id`: story id.

#### 下载地址

Story Cloze Test Winter 2018 (recommended) set:

\* val set: https://goo.gl/XWjas1

\* test set: https://goo.gl/BcTtB4

Story Cloze Test Spring 2016 set:

\* val set: https://goo.gl/cDmS6I

\* test set: https://goo.gl/iE31Qm

#### 数据集大小

| 数据集        | 大小   | 备注  |
|:-----------|:-----|:----|
| validation | 1571 | -   |
| test       | 1571 | 无答案 |

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("story_cloze", "2018", data_dir=r"C:\Train\data\story_cloze")

dataset_val = dataset["validation"]
```

## winogrande

*WinoGrande is a new collection of 44k problems, inspired by Winograd Schema Challenge (Levesque, Davis, and Morgenstern
2011), but adjusted to improve the scale and robustness against the dataset-specific bias. Formulated as a
fill-in-a-blank task with binary options, the goal is to choose the right option for a given sentence which requires
commonsense reasoning.*

原文地址：https://huggingface.co/datasets/winogrande

#### 数据集格式

| sentence (string)                                                                        | option1 (string) | option2 (string) | answer (string) |
|:-----------------------------------------------------------------------------------------|:-----------------|:-----------------|:----------------|
| "Sarah was a much better surgeon than Maria so _ always got the easier cases."           | "Sarah"          | "Maria"          | "2"             |
| "Sarah was a much better surgeon than Maria so _ always got the harder cases."           | "Sarah"          | "Maria"          | "1"             |
| "They were worried the wine would ruin the bed and the blanket, but the _ was't ruined." | "blanket"        | "bed"            | "2"             |
| "Terry tried to bake the eggplant in the toaster oven but the _ was too big."            | "eggplant"       | "toaster"        | "1"             |

#### 下载地址

https://github.com/allenai/winogrande

#### 数据集大小

| 数据集            | 大小    | 备注  | 数据源                 | 数据源说明                                                            |
|:---------------|:------|:----|---------------------|------------------------------------------------------------------|
| dev            | 1267  |     |                     | -                                                                |
| test           | 1767  | 无答案 |                     | -                                                                |
| train_debiased | 9248  |     | winogrande_debiased | 这是一个经过去偏的版本，意味着它经过特殊处理，以减少数据中的不公平和偏见。这对于研究和开发公平、无偏见的AI系统非常有用。    |
| train_l        | 10234 |     | winogrande_l        | 这是一个较大规模的数据集，包含大量的问题。它适用于在充足的计算资源下进行模型训练和验证，或者在研究和开发高性能AI系统时使用。  |
| train_m        | 2558  |     | winogrande_m        | 这是一个中等规模的数据集，包含更多的问题。这可以用于在中等计算资源上进行模型训练和验证，或用于更复杂的研究和开发任务。      |
| train_s        | 640   |     | winogrande_s        | 这是一个较小规模的数据集，包含更多的问题。它可以用于在相对较小的计算资源上进行模型训练和验证。                  |
| train_xl       | 40398 |     | winogrande_xl       | 这是最大规模的数据集，包含最多的问题。这个数据集适用于在大规模计算资源下进行模型训练和验证，或者用于研究和开发最先进的AI系统。 |
| train_xs       | 160   |     | winogrande_xs       | 这是最小的数据集，包含数量有限的问题。它适合用于快速验证模型性能，以及在计算资源有限的情况下进行实验。              |

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("winogrande", "winogrande_xs")
# winogrande_debiased/winogrande_l/winogrande_m/winogrande_s/winogrande_xl/winogrande_xs

dataset_test = dataset["test"]  # test/train/validation
```

## COPA (Choice of Plausible Alternatives)

原文地址：https://paperswithcode.com/dataset/copa

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

#### 格式说明

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

#### 下载地址

https://people.ict.usc.edu/~gordon/copa.html

#### 数据集大小

| 数据集  | 大小  | 备注  |
|:-----|:----|:----|
| dev  | 500 | -   |
| test | 500 | -   |

#### 使用方式

-

## WSC (Winograd Schema Challenge)

A Winograd schema is a pair of sentences that differ in only one or two words and that contain an ambiguity that is
resolved in opposite ways in the two sentences and requires the use of world knowledge and reasoning for its resolution.
The schema takes its name from a well-known example by Terry Winograd:

> The city councilmen refused the demonstrators a permit because they [feared/advocated] violence.

If the word is `feared'', then `they'' presumably refers to the city council; if it is `advocated'' then `they''
presumably refers to the demonstrators.

原文地址：https://paperswithcode.com/dataset/wsc

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

#### 格式说明

- `text` (str): The text sequence
- `options` (list[str]): The two entity options that the pronoun may be referring to
- `label` (int): The index of the correct option in the `options` field
- `pronoun` (str): The pronoun in the sequence to be resolved
- `pronoun_loc` (int): The starting position of the pronoun in the sequence
- `quote` (str): The substr with the key action or context surrounding the pronoun
- `quote_loc` (int): The starting position of the quote in the sequence
- `source` (str): A description of the source who contributed the example

#### 数据集大小

| 数据集  | 大小  | 备注  | 数据源    | 数据源说明                                                           |
|:-----|:----|:----|--------|-----------------------------------------------------------------|
| test | 273 | -   | wsc273 | 包含 273 个句子对，相对较少。这个数据集在某些情况下可能用于快速测试和验证算法的性能，但可能不如 WSC285 那样全面。 |
| test | 285 | -   | wsc285 | 用于评估计算机系统在处理代词消歧问题上的能力。这个数据集包括了更广泛的语言模式和场景，因此它对模型的评估可能更全面。      |

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("winograd_wsc", "wsc273")  # wsc285/wsc273
dataset_test = dataset["test"]  # test
```

## BoolQ (Boolean Questions)

*BoolQ is a question answering dataset for yes/no questions containing 15942 examples. These questions are naturally
occurring ---they are generated in unprompted and unconstrained settings. Each example is a triplet of (question,
passage, answer), with the title of the page as optional additional context. The text-pair classification setup is
similar to existing natural language inference tasks.*

阅读短文判断给出的问题是否正确

原文地址：https://paperswithcode.com/dataset/boolq

#### 数据集格式

```json
{
  "answer": false,
  "passage": "\"All biomass goes through at least some of these steps: it needs to be grown, collected, dried, fermented, distilled, and burned...",
  "question": "does ethanol take more energy make that produces"
}

```

#### 下载地址

https://github.com/google-research-datasets/boolean-questions

#### 数据集大小

| 数据集   | 大小   | 备注                                                 |
|:------|:-----|:---------------------------------------------------|
| dev   | 3270 | https://storage.cloud.google.com/boolq/dev.jsonl   |
| train | 9427 | https://storage.cloud.google.com/boolq/train.jsonl |
| test  | 3245 | https://storage.cloud.google.com/boolq/test.jsonl  |

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("boolq")
dataset_test = dataset["validation"]  # validation/train
```

## CNN/Daily Mail

*The CNN / DailyMail Dataset is an English-language dataset containing just over 300k unique news articles as written by
journalists at CNN and the Daily Mail. The current version supports both extractive and abstractive summarization,
though the original version was created for machine reading and comprehension and abstractive question answering.*

原文地址：https://paperswithcode.com/dataset/cnn-daily-mail-1

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

#### 数据集大小

| 数据集        | 大小     | 备注            |
|:-----------|:-------|:--------------|
| validation | 13368  | cnn_dailymail |
| train      | 287113 | cnn_dailymail |
| test       | 11490  | cnn_dailymail |

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("cnn_dailymail", "3.0.0")  # 1.0.0/2.0.0/3.0.0
# cnn_dailymail_dutch/cnn_dailymail/test2/citesum/atypical_animacy/asrs-aviation-reports

dataset_test = dataset["test"]  # test/validation/train
```

*Version 1.0.0 aimed to support supervised neural methodologies for machine reading and question answering with a large
amount of real natural language training data and released about 313k unique articles and nearly 1M Cloze style
questions to go with the articles. Versions 2.0.0 and 3.0.0 changed the structure of the dataset to support
summarization rather than question answering. Version 3.0.0 provided a non-anonymized version of the data, whereas both
the previous versions were preprocessed to replace named entities with unique identifier labels.*

## MultiRC (Multi-Sentence Reading Comprehension)

*Eraser Multi RC is a dataset for queries over multi-line passages, along with answers and a rationalte. Each example in
this dataset has the following 5 parts. 1. A Mutli-line Passage. 2. A Query about the passage. 3. An Answer to the
query. 4. A Classification as to whether the answer is right or wrong 5. An Explanation justifying the classification.*

原文地址：https://paperswithcode.com/dataset/multirc

#### 数据集格式

```json
{
  "annotation_id": "Fiction-stories-masc-A_Wasted_Day-2.txt:1:2",
  "classification": "False",
  "docids": null,
  "evidences": [
    [
      {
        "docid": "Fiction-stories-masc-A_Wasted_Day-2.txt",
        "end_sentence": 4,
        "end_token": 112,
        "start_sentence": 3,
        "start_token": 106,
        "text": "It was a charming morning ."
      },
      {
        "docid": "Fiction-stories-masc-A_Wasted_Day-2.txt",
        "end_sentence": 5,
        "end_token": 127,
        "start_sentence": 4,
        "start_token": 112,
        "text": "The spring was at full tide , and the air was sweet and clean ."
      }
    ]
  ],
  "query": "Why was it a charming morning ? || It was cold and grey but he was somehow happy",
  "query_type": null
}
```

#### 下载地址

http://www.eraserbenchmark.com/zipped/multirc.tar.gz

中文/繁体测试语料可参考地址：https://blog.51cto.com/u_15064656/4274624

#### 数据集大小

| 数据集        | 大小    | 备注  |
|:-----------|:------|:----|
| validation | 3214  | -   |
| train      | 24029 | -   |
| test       | 4848  | -   |

#### 使用方式

支持框架TensorFlow：https://www.tensorflow.org/datasets/catalog/eraser_multi_rc

```python
from datasets import load_dataset

dataset = load_dataset("eraser_multi_rc", data_dir=r"C:\Train\data\multirc")

dataset_test = dataset["test"]  # validation/train/test
```

## CoQA (Conversational Question Answering Challenge)

*CoQA is a large-scale dataset for building Conversational Question Answering systems. Our dataset contains 127k
questions with answers, obtained from 8k conversations about text passages from seven diverse domains. The questions are
conversational, and the answers are free-form text with their corresponding evidence highlighted in the passage.*

原文地址：https://paperswithcode.com/dataset/coqa

#### 数据集格式

```json lines
{
  "answers": "{\"answer_end\": [179, 494, 511, 545, 879, 1127, 1128, 94, 150, 412, 1009, 1046, 643, -1, 764, 724, 125, 1384, 881, 910], \"answer_...",
  "questions": "[\"When was the Vat formally opened?\", \"what is the library for?\", \"for what subjects?\", \"and?\", \"what was started in 2014?\", \"ho...",
  "source": "wikipedia",
  "story": "\"The Vatican Apostolic Library (), more commonly called the Vatican Library or simply the Vat, is the library of the Holy See, l..."
}
```

#### 格式说明

- `source`: a `string` feature.
- `story`: a `string` feature.
- `questions`: a `list` of `string` features.
- `answers`: a `dictionary` feature containing:
    - `input_text`: a `string` feature.
    - `answer_start`: a `int32` feature.
    - `answer_end`: a `int32` feature.

#### 数据集大小

| 数据集        | 大小   | 备注  |
|:-----------|:-----|:----|
| validation | 500  | -   |
| train      | 7199 | -   |

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("coqa")

dataset_val = dataset["validation"]  # validation/train
```

## SQuAD (Stanford Question Answering Dataset)

*Stanford Question Answering Dataset (SQuAD) is a reading comprehension dataset, consisting of questions posed by crowdworkers on a set of Wikipedia articles, where the answer to every question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable.*

原文地址：https://rajpurkar.github.io/SQuAD-explorer/

#### 数据集格式

```json
{
	"title": "Force",
    "paragraphs": [
        {
            "context": "Philosophers in antiquity used the concept of force in the study of stationary and moving objects and simple machines, but thinkers such as Aristotle and Archimedes retained fundamental errors in understanding force. In part this was due to an incomplete understanding of the sometimes non-obvious force of friction, and a consequently inadequate view of the nature of natural motion. A fundamental error was the belief that a force is required to maintain motion, even at a constant velocity. Most of the previous misunderstandings about motion and force were eventually corrected by Galileo Galilei and Sir Isaac Newton. With his mathematical insight, Sir Isaac Newton formulated laws of motion that were not improved-on for nearly three hundred years. By the early 20th century, Einstein developed a theory of relativity that correctly predicted the action of forces on objects with increasing momenta near the speed of light, and also provided insight into the forces produced by gravitation and inertia.",
            "qas": [
                {
                    "id": "573735e8c3c5551400e51e71",
                    "question": "What concept did philosophers in antiquity use to study simple machines?",
                    "is_impossible": false,
                    "answers": [
                        {"text": "force", "answer_start": 46},
                        {"text": "the concept of force", "answer_start": 31},
                    ]
                }
            ]
        },
        {
            "context": "",
            "qas": []
        }
    ]
}
```

#### 数据集大小

| 数据集 | 大小   | 备注                                                         |
| :----- | :----- | :----------------------------------------------------------- |
| dev    | 11873  | https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json |
| train  | 130319 | https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json |

*数据集细化后，一个question对应一条数据*

## RACE (ReAding Comprehension dataset from Examinations)

*RACE is a large-scale reading comprehension dataset with more than 28,000 passages and nearly 100,000 questions. The dataset is collected from English examinations in China, which are designed for middle school and high school students. The dataset can be served as the training and test sets for machine comprehension.*  初高中英语试卷阅读理解

原文地址：https://paperswithcode.com/dataset/race

#### 数据格式

```json
{
	"answers": ["C", "B"],
	"options": [
		[
			"his mother had no cellphone",
			"his mother wasn't at home",
			"he didn't take a cellphone with him",
			"he was too frightened to call"
		],
		[
			"call off the ban",
			"continue the ban",
			"thank the parents",
			"allow some students to use cellphones at school"
		]
	],
	"questions": [
		"A 13-year-old student was shot with a gun after school, unable to call his mother for help, because   _  .",
		"According to what the spokesman said, the school might   _  ."
	],
	"article": "New York City schoolchildren can't use cellphones at school because of Mayor Michael R. Bloomberg's ban on cellphones in schools. Many parents are opposed to Mayor Michael R. Bloomberg's ban on cellphones in schools by e-mail messages.\nThere was a 13-year-old student who was shot with a gun after school, unable to call his mother for help. There was a high school student robbed three times last year, twice in her school building. There was a girl who got a piece of glass placed in her eye during school and was saved from a possible cornea transplant   only because, having disobeyed the cellphone ban, she was able to call her mother and get an operation on time.\nThe ban has been on for years, but it set off a widespread parental outcry only in April, after some headmasters sent home letters reminding parents that cellphones are not allowed to be brought into school.\nMr Bloomberg has defended the ban, saying that cellphones are bad and often used to cheat or call in friends for fights. If something is important, he says, parents can call schools directly.\nOn the other hand, many of the e-mail messages from parents described the ban as \"cruel and heartless\", \"absurdly  wrong-headed\", \"anti-parent\", \"ridiculous\".\n\"We respect the fears that parents have,\" David Cantor, a spokesman for Schools Minister Joel I. Klein said, \"but after all the fact is that having phones in schools always leads to more problems.\"",
	"id": "high2639.txt"
}
```

#### 下载地址

http://www.cs.cmu.edu/~glai1/data/race/RACE.tar.gz

#### 数据集大小

| name   | train | validation | test |
| ------ | ----- | ---------- | ---- |
| high   | 62445 | 3451       | 3498 |
| middle | 25321 | 1436       | 1436 |
| all    | 87866 | 4887       | 4934 |

#### 使用方式

```python
from dataset import load_dataset

dataset = load_dataset(r"C:\Train\data\RACE")

dataset_test = dataset["test"]  # test/train/dev
```

## DROP (Discrete Reasoning Over Paragraphs)

*DROP: A Reading Comprehension Benchmark Requiring Discrete Reasoning Over Paragraphs. . DROP is a crowdsourced, adversarially-created, 96k-question benchmark, in which a system must resolve references in a question, perhaps to multiple input positions, and perform discrete operations over them (such as addition, counting, or sorting). These operations require a much more comprehensive understanding of the content of paragraphs than what was necessary for prior datasets.*

原文地址：https://paperswithcode.com/dataset/drop

#### 数据格式

| section_id (string) | query_id (string)                      | passage (string)                                             | question (string)                                            | answers_spans (sequence)                        |
| :------------------ | :------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :---------------------------------------------- |
| "nfl_2201"          | "f16c0ee7-f131-4a8b-a6ac-4d275ea68066" | "To start the season, the Lions traveled south to Tampa, Florida to take on the Tampa Bay Buccaneers. The Lions scored first in the first quarter with a 23-yard field goal by Jason Hanson. The Buccaneers tied it up with a 38-yard field goal by Connor Barth, then took the lead when Aqib Talib intercepted a pass from Matthew Stafford and ran it in 28 yards. The Lions responded with a 28-yard field goal. In the second quarter, Detroit took the lead with a 36-yard touchdown catch by Calvin Johnson, and later added more points when Tony Scheffler caught an 11-yard TD pass. Tampa Bay responded with a 31-yard field goal just before halftime. The second half was relatively quiet, with each team only scoring one touchdown. First, Detroit's Calvin Johnson caught a 1-yard pass in the third quarter. The game's final points came when Mike Williams of Tampa Bay caught a 5-yard pass. The Lions won their regular season opener for the first time since 2007" | "How many points did the buccaneers need to tie in the first?" | { "spans": [ "3" ], "types": [ "number" ] }     |
| "nfl_2201"          | "f703d43d-73fa-4fda-8913-d81bd5569700" | "To start the season, the Lions traveled south to Tampa, Florida to take on the Tampa Bay Buccaneers. The Lions scored first in the first quarter with a 23-yard field goal by Jason Hanson. The Buccaneers tied it up with a 38-yard field goal by Connor Barth, then took the lead when Aqib Talib intercepted a pass from Matthew Stafford and ran it in 28 yards. The Lions responded with a 28-yard field goal. In the second quarter, Detroit took the lead with a 36-yard touchdown catch by Calvin Johnson, and later added more points when Tony Scheffler caught an 11-yard TD pass. Tampa Bay responded with a 31-yard field goal just before halftime. The second half was relatively quiet, with each team only scoring one touchdown. First, Detroit's Calvin Johnson caught a 1-yard pass in the third quarter. The game's final points came when Mike Williams of Tampa Bay caught a 5-yard pass. The Lions won their regular season opener for the first time since 2007" | "How long was the Lion's longest field goal?"                | { "spans": [ "28-yard" ], "types": [ "span" ] } |

下载地址：https://ai2-public-datasets.s3.amazonaws.com/drop/drop_dataset.zip

#### 数据集大小

| 数据集     | 大小  | 备注 |
| :--------- | :---- | :--- |
| validation | 9535  | -    |
| train      | 77400 | -    |

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("drop")

dataset_val = dataset["validation"]  # train/validation
```

## QuAC (Question Answering in Context)

*Question Answering in Context is a dataset for modeling, understanding, and participating in information seeking dialog. Data instances consist of an interactive dialog between two crowd workers: (1) a student who poses a sequence of freeform questions to learn as much as possible about a hidden Wikipedia text, and (2) a teacher who answers the questions by providing short excerpts (spans) from the text. QuAC introduces challenges not found in existing machine comprehension datasets: its questions are often more open-ended, unanswerable, or only meaningful within the dialog context.*

原文地址：https://paperswithcode.com/dataset/quac

#### 数据格式

```json
{
  'dialogue_id': 'C_6abd2040a75d47168a9e4cca9ca3fed5_0',

  'wikipedia_page_title': 'Satchel Paige',

  'background': 'Leroy Robert "Satchel" Paige (July 7, 1906 - June 8, 1982) was an American Negro league baseball and Major League Baseball (MLB) pitcher who became a legend in his own lifetime by being known as perhaps the best pitcher in baseball history, by his longevity in the game, and by attracting record crowds wherever he pitched. Paige was a right-handed pitcher, and at age 42 in 1948, he was the oldest major league rookie while playing for the Cleveland Indians. He played with the St. Louis Browns until age 47, and represented them in the All-Star Game in 1952 and 1953.',

  'section_title': 'Chattanooga and Birmingham: 1926-29',

  'context': 'A former friend from the Mobile slums, Alex Herman, was the player/manager for the Chattanooga White Sox of the minor Negro Southern League. In 1926 he discovered Paige and offered to pay him $250 per month, of which Paige would collect $50 with the rest going to his mother. He also agreed to pay Lula Paige a $200 advance, and she agreed to the contract. The local newspapers--the Chattanooga News and Chattanooga Times--recognized from the beginning that Paige was special. In April 1926, shortly after his arrival, he recorded nine strikeouts over six innings against the Atlanta Black Crackers. Part way through the 1927 season, Paige\'s contract was sold to the Birmingham Black Barons of the major Negro National League (NNL). According to Paige\'s first memoir, his contract was for $450 per month, but in his second he said it was for $275. Pitching for the Black Barons, Paige threw hard but was wild and awkward. In his first big game in late June 1927, against the St. Louis Stars, Paige incited a brawl when his fastball hit the hand of St. Louis catcher Mitchell Murray. Murray then charged the mound and Paige raced for the dugout, but Murray flung his bat and struck Paige above the hip. The police were summoned, and the headline of the Birmingham Reporter proclaimed a "Near Riot." Paige improved and matured as a pitcher with help from his teammates, Sam Streeter and Harry Salmon, and his manager, Bill Gatewood. He finished the 1927 season 7-1 with 69 strikeouts and 26 walks in 89 1/3 innings. Over the next two seasons, Paige went 12-5 and 10-9 while recording 176 strikeouts in 1929. (Several sources credit his 1929 strikeout total as the all-time single-season record for the Negro leagues, though there is variation among the sources about the exact number of strikeouts.) On April 29 of that season he recorded 17 strikeouts in a game against the Cuban Stars, which exceeded what was then the major league record of 16 held by Noodles Hahn and Rube Waddell. Six days later he struck out 18 Nashville Elite Giants, a number that was tied in the white majors by Bob Feller in 1938. Due to his increased earning potential, Barons owner R. T. Jackson would "rent" Paige out to other ball clubs for a game or two to draw a decent crowd, with both Jackson and Paige taking a cut. CANNOTANSWER',

  'turn_ids': ['C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#0', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#1', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#2', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#3', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#4', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#5', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#6', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#7'],

  'questions': ['what did he do in Chattanooga', 'how did he discover him', 'what position did he play', 'how did they help him', 'when did he go to Birmingham', 'how did he feel about this', 'how did he do with this team', 'What made him leave the team'],

  'followups': [0, 2, 0, 1, 0, 1, 0, 1],

  'yesnos': [2, 2, 2, 2, 2, 2, 2, 2]

  'answers': {
    'answer_starts': [
      [480, 39, 0, 67, 39],
      [2300, 2300, 2300],
      [848, 1023, 848, 848, 1298],
      [2300, 2300, 2300, 2300, 2300],
      [600, 600, 600, 634, 600],
      [2300, 2300, 2300],
      [939, 1431, 848, 848, 1514],
      [2106, 2106, 2165]
    ],
    'texts': [
      ['April 1926, shortly after his arrival, he recorded nine strikeouts over six innings against the Atlanta Black Crackers.', 'Alex Herman, was the player/manager for the Chattanooga White Sox of the minor Negro Southern League. In 1926 he discovered Paige', 'A former friend from the Mobile slums, Alex Herman, was the player/manager for the Chattanooga White Sox of the minor Negro Southern League.', 'manager for the Chattanooga White Sox of the minor Negro Southern League. In 1926 he discovered Paige and offered to pay him $250 per month,', 'Alex Herman, was the player/manager for the Chattanooga White Sox of the minor Negro Southern League. In 1926 he discovered Paige and offered to pay him $250 per month,'],
      ['CANNOTANSWER', 'CANNOTANSWER', 'CANNOTANSWER'],
      ['Pitching for the Black Barons,', 'fastball', 'Pitching for', 'Pitching', 'Paige improved and matured as a pitcher with help from his teammates,'], ['CANNOTANSWER', 'CANNOTANSWER', 'CANNOTANSWER', 'CANNOTANSWER', 'CANNOTANSWER'],
      ["Part way through the 1927 season, Paige's contract was sold to the Birmingham Black Barons", "Part way through the 1927 season, Paige's contract was sold to the Birmingham Black Barons", "Part way through the 1927 season, Paige's contract was sold to the Birmingham Black Barons", "Paige's contract was sold to the Birmingham Black Barons of the major Negro National League (NNL", "Part way through the 1927 season, Paige's contract was sold to the Birmingham Black Barons"], ['CANNOTANSWER', 'CANNOTANSWER', 'CANNOTANSWER'],
      ['game in late June 1927, against the St. Louis Stars, Paige incited a brawl when his fastball hit the hand of St. Louis catcher Mitchell Murray.', 'He finished the 1927 season 7-1 with 69 strikeouts and 26 walks in 89 1/3 innings.', 'Pitching for the Black Barons, Paige threw hard but was wild and awkward.', 'Pitching for the Black Barons, Paige threw hard but was wild and awkward.', 'Over the next two seasons, Paige went 12-5 and 10-9 while recording 176 strikeouts in 1929. ('],
      ['Due to his increased earning potential, Barons owner R. T. Jackson would "rent" Paige out to other ball clubs', 'Due to his increased earning potential, Barons owner R. T. Jackson would "rent" Paige out to other ball clubs for a game or two to draw a decent crowd,', 'Jackson would "rent" Paige out to other ball clubs for a game or two to draw a decent crowd, with both Jackson and Paige taking a cut.']
    ]
  },

  'orig_answers': {
    'answer_starts': [39, 2300, 1298, 2300, 600, 2300, 1514, 2165],
    'texts': ['Alex Herman, was the player/manager for the Chattanooga White Sox of the minor Negro Southern League. In 1926 he discovered Paige and offered to pay him $250 per month,', 'CANNOTANSWER', 'Paige improved and matured as a pitcher with help from his teammates,', 'CANNOTANSWER', "Part way through the 1927 season, Paige's contract was sold to the Birmingham Black Barons", 'CANNOTANSWER', 'Over the next two seasons, Paige went 12-5 and 10-9 while recording 176 strikeouts in 1929. (', 'Jackson would "rent" Paige out to other ball clubs for a game or two to draw a decent crowd, with both Jackson and Paige taking a cut.']
  },
}

```

#### 格式说明

- `dialogue_id`: ID of the dialogue.
- `wikipedia_page_title`: title of the Wikipedia page.
- `background`: first paragraph of the main Wikipedia article.
- `section_tile`: Wikipedia section title.
- `context`: Wikipedia section text.
- `turn_ids`: list of identification of dialogue turns. One list of ids per dialogue.
- `questions`: list of questions in the dialogue. One list of questions per dialogue.
- `followups`: list of followup actions in the dialogue. One list of followups per dialogue. `y`: follow, `m`: maybe follow yp, `n`: don't follow up.
- `yesnos`: list of yes/no in the dialogue. One list of yes/nos per dialogue. `y`: yes, `n`: no, `x`: neither.
- `answers`: dictionary of answers to the questions (validation step of data collection)
  - `answer_starts`: list of list of starting offsets. For training, list of single element lists (one answer per question).
  - `texts`: list of list of span texts answering questions. For training, list of single element lists (one answer per question).
- `orig_answers`: dictionary of original answers (the ones provided by the teacher in the dialogue)
  - `answer_starts`: list of starting offsets
  - `texts`: list of span texts answering questions.

#### 数据集大小

| 数据集 | 大小  | 备注 |
| :----- | :---- | :--- |
| dev    | 1000  | -    |
| train  | 11567 | -    |

#### 使用方式

```python
from datasets import load_dataset

dataset = load_dataset("quac")
dataset_val = dataset["validation"]  # train/validation
```

