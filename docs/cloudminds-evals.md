## evals目录结构

```
├─datasets
│  ├─BoolQ
│  │  └─test.jsonl
│  │  └─train.jsonl
│  │  └─validation.jsonl
│  └─WSC
│  │  └─test.jsonl
│  │  └─train.jsonl
│  │  └─validation.jsonl
├─downloads
│  ├─BoolQ
│  │  └─dev.jsonl
│  │  └─test.jsonl
│  │  └─train.jsonl
│  └─WSC
│  │  └─dev.csv
│  │  └─test.csv
│  │  └─train.csv
├─evals
│  ├─cli
│  │  └─oaieval.py
│  │  └─oaievalset.py
│  ├─prompt
│  │  └─generate_en.py
│  │  └─generate_zh.py
│  ├─registry
│  │  ├─data
│  │  │  ├─BoolQ
│  │  │  │  └─BoolQ.jsonl
│  │  │  └─WSC
│  │  │  │  └─WSC.jsonl
│  │  ├─evals
│  │  |  └─BoolQ.yaml
│  │  |  └─WSC.yaml
│  │  ├─eval_sets
│  │  |  └─cloudminds.yaml
│  │  └─modelgraded
│  ├─utils
│  │  └─cloudminds.py
└─datasets_sync.py
```

## evals使用指南

### 1.拉取evals代码

```shell
git clone https://github.com/liuzhaobing/evals.git
```

### 2.手动创建测试集

#### 2.1测试集存放目录

```
├─evals
│  ├─registry
│  │  ├─data
│  │  │  ├─BoolQ
│  │  │  │  └─BoolQ.jsonl
│  │  │  └─WSC
│  │  │  │  └─WSC.jsonl
```

#### 2.2测试集单条测试用例详情

例如`BoolQ.jsonl`是一个测试集（JSON line格式），每一行数据是一个JSON格式，其中一行数据内容如下：

```json
{
	"input": [
		{
			"role": "system",
			"content": "TASK: Read a short passage and judge whether the given question is correct, in the format \"<answer>\". The answer must be 'true' or 'false' only."
		},
		{
			"role": "system",
			"content": "passage: Calvin Edwin Ripken Jr. (born August 24, 1960), nicknamed ``The Iron Man'', is an American former baseball shortstop and third baseman who played 21 seasons in Major League Baseball (MLB) for the Baltimore Orioles (1981--2001). One of his position's most offensively productive players, Ripken compiled 3,184 hits, 431 home runs, and 1,695 runs batted in during his career, and he won two Gold Glove Awards for his defense. He was a 19-time All-Star and was twice named American League (AL) Most Valuable Player (MVP). Ripken holds the record for consecutive games played, 2,632, surpassing Lou Gehrig's streak of 2,130 that had stood for 56 years and that many deemed unbreakable. In 2007, he was elected into the National Baseball Hall of Fame in his first year of eligibility, and currently has the fourth highest voting percentage of all time (98.53%)."
		},
		{
			"role": "user",
			"content": "question: is cal ripken jr in the hall of fame"
		}
	],
	"ideal": "True"
}
```

**说明**：

- `input`代表给模型的输入，`evals`会自动将`input`列表转换为自然语言（prompt字符串）;

- `ideal`代表本条测试用例的预期结果;

### 3.手动创建测试套件

#### 3.1测试套件存放目录

```
├─evals
│  ├─registry
│  │  ├─evals
│  │  |  └─BoolQ.yaml
│  │  |  └─WSC.yaml
```

#### 3.2测试套件配置详情

例如`BoolQ.yaml`是一个测试套件（yaml格式），具体内容如下：

```yaml
BoolQ_match:
  id: BoolQ.match1.v0
  metrics: [accuracy]
BoolQ.match1.v0:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: BoolQ/BoolQ.jsonl

BoolQ_fact:
  id: BoolQ.fact1.v0
  metrics: [accuracy]
BoolQ.fact1.v0:
  class: evals.elsuite.modelgraded.classify:ModelBasedClassify
  args:
    samples_jsonl: BoolQ/BoolQ.jsonl
    eval_type: cot_classify
    modelgraded_spec: fact
```

**说明**：

`BoolQ_match`和`BoolQ_fact`是测试套件中的两个不同的测试配置，其中`BoolQ_match`使用的是`evals.elsuite.basic.match:Match`（完全匹配）评估模型的结果，而`BoolQ_fact`使用的是`evals.elsuite.modelgraded.classify:ModelBasedClassify`（第三方模型辅助）评估模型的结果。具体参数说明如下：

- `BoolQ_match`：测试配置名称，`可自定义`
  - `id`：测试配置UUID，`可自定义`
  - `metrics`：评估指标，目前内置的指标有`accuracy`和`f1_score`
- `BoolQ.match1.v0`：测试配置UUID，需要与上面的UUID保持一致
  - `class`：评估时调用的方法，当前支持`evals.elsuite.basic.match:Match`（完全匹配）、`evals.elsuite.basic.fuzzy_match:FuzzyMatch`（模糊匹配）、`evals.elsuite.basic.includes:Includes`（包含）、`evals.elsuite.modelgraded.classify:ModelBasedClassify`（第三方模型辅助评估）
  - `args`：下面填写方法的入参
    - `samples_jsonl`：测试集的相对路径（相对evals/evals/registry/data），例如测试集的全路径为`evals/evals/registry/data/BoolQ/BoolQ.jsonl`那么此处填写`BoolQ/BoolQ.jsonl`
    - `eval_type`：此参数只针对`evals.elsuite.modelgraded.classify:ModelBasedClassify`生效，详细说明见第2点。
    - `modelgraded_spec`：此参数只针对`evals.elsuite.modelgraded.classify:ModelBasedClassify`生效，详细说明见第2点。

接上，`cot_classify`和`fact`的作用是：在第三方模型辅助评估时，将被测模型的输入、输出、期望答案二次封装成自然语言（prompt字符串），然后扔给第三方模型去做回答。

其中`fact`的定义在`evals.registry.modelgraded.fact.yaml` ，主要功能是将被测模型的输入、输出、期望答案二次封装。而`cot_classify`的定义在`evals.elsuite.modelgraded.classify_utils:ANSWER_PROMPTS.cot_classify`，主要功能是为二次封装的prompt限制模型输出。

我们内部也提供了中文的辅助prompt，见`evals.registry.modelgraded.fact_zh.yaml`和`evals.elsuite.modelgraded.classify_utils:ANSWER_PROMPTS.cot_classify_zh`



**举个例子**：

`fact_zh.yaml`的内容如下：

```yaml
fact_zh:
  prompt: |-
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
  choice_strings: ABCDEF
  input_outputs:
    input: completion
```

`cot_classify`的内容如下：

```
首先，一步步写出你的推理，确保你的结论是正确的。 避免一开始就简单地陈述正确答案。 然后只打印 {choices} 中的一个选项（不带引号或标点符号）在它自己的对应于正确答案的行上。 最后，在新行中单独重复答案，请在新行中单独重复答案，一定要在新行中单独重复答案。

推理：
```

那么在扔给第三方模型辅助评估时的prompt是这样的：

```
现在需要你根据问题和标准答案评估另一个模型的回复。只需要答案包含即可，模型提供了额外的信息不算分歧, 下面是数据:
[BEGIN DATA]
************
[问题]: 任务：根据客人的评语推测他对本次酒店入住体验是积极还是消极态度。\nUser: 评语：装修的味道特重，熏的人特难受，临街的房间特吵，吵的无法入睡\n
************
[标准答案]: 积极
************
[模型提交的答案]: 根据客人的评语，可以推测他对本次酒店入住体验是消极态度的。客人提到酒店装修味道特重，熏的人特难受，临街的房间特吵，吵的无法入睡。综合来看，客人对本次酒店入住体验持消极态度，对环境和设施提出了一些负面评价。
************
[END DATA]

将标准答案与模型提交的答案进行比较。 忽略风格、语法或标点符号的任何差异。
模型提交的答案可能是标准答案的子集或超集，也可能与其冲突。 确定适用哪种情况。 通过选择以下选项之一回答问题：
(A) 模型提交的答案是标准答案的子集，并且与其完全一致。
(B) 模型提交的答案是标准答案的超集，并且与其完全一致。
(C) 模型提交的答案包含与标准答案相同的所有细节。
(D) 模型提交的答案与标准答案存在分歧。
(E) 模型提交的答案和标准答案不同，但从事实性的角度来看，这些差异无关紧要。
首先，一步步写出你的推理，确保你的结论是正确的。 避免一开始就简单地陈述正确答案。 然后只打印 \"A\" or \"B\" or \"C\" or \"D\" or \"E\" or \"F\" 中的一个选项（不带引号或标点符号）在它自己的对应于正确答案的行上。 最后，在新行中单独重复答案，请在新行中单独重复答案，一定要在新行中单独重复答案。

推理：
```

而辅助模型的答复是这样的：以下为`gpt-3.5`的输出结果。（辅助模型会按照如上prompt的要求在新的一行中单独打印答案。）

```
模型提交的答案与标准答案存在分歧，因为标准答案是积极态度，而模型提交的答案是消极态度。虽然模型提交的答案包含了客人提到的负面评价，但是它的结论与标准答案相反。模型提交的答案与标准答案存在分歧。	

D
```

#### 3.3测试套件集存放目录

```
├─evals
│  ├─registry
│  │  ├─evals_sets
│  │  |  └─cloudminds_plan.yaml
```

#### 3.4测试套件集配置详情

例如`cloudminds_plan.yaml`是一个测试套件（yaml格式），具体内容如下：

```yaml
eval-cloudminds:
  evals:
    - lcqmc_fact
    - StoryCloze_fact
    - WinoGrande_fact
    - COPA_fact
    - WiC_fact
    - WSC_fact
    - ReCoRD_fact
    - CNNDailyMail_fact
    - tnews_fact
    - iflytek_fact
    - waimai_10k_fact
    - CoQA_fact
    - DROP_fact
    - SQuAD_fact
    - RACE_fact
    - cmrc_fact
    - csl_fact
```

**说明**：

- `eval-cloudminds`：测试套件集名称
  - `lcqmc_fact`：测试套件配置名称（需要哪些测试套件就放哪些）

### 4.对接被测模型

#### 4.1被测模型代码目录

```
├─evals
│  ├─utils
│  |  └─cloudminds.py
```

#### 4.2被测模型代码使用细则

**使用方法**：在cloudminds.py文件中新增类，新增的类需要继承`CloudMindsModel`这个类，并重写`create`函数和`MODEL_NAME`类属性，其中`create`函数的返回值需要字符串格式，函数的入参`prompt`信息需要从`kwargs`中抽取。



**案例**1：调用封装好的http接口

```python
class ChatGLMAPI(CloudMindsModel):
    MODEL_NAME = "chatglm_api"

    @classmethod
    def create(cls, *args, **kwargs):
        url = f'http://172.16.23.85:30592/chatglm/ask'
        resp = requests.post(url, json={
            "input": str(kwargs["prompt"]),
            "history": [],
            "conv_user_id": str(uuid.uuid4()),
        })
        return resp.json()["body"]["message"]
```

**案例**2：本地直接运行模型文件

```python
class HuggingFaceSBertPq(CloudMindsModel):
    MODEL_NAME = "sbert_pq"
    model = sentence_transformers.SentenceTransformer('inkoziev/sbert_pq').to(device)

    @classmethod
    def create(cls, *args, **kwargs):
        query = str(kwargs["prompt"])
        sentence1 = query.split("\n")[1].replace("User: 句子1：", "")
        sentence2 = query.split("\n")[2].replace("User: 句子2：", "")
        sentences = [sentence1, sentence2]

        embeddings = cls.model.encode(sentences)

        s = sentence_transformers.util.cos_sim(a=embeddings[0], b=embeddings[1])
        line = 0.7

        return "是" if s.item() > line else "否"

```

**说明**：

- create函数在测试每条用例时都会调用，因此模型文件加载的代码，建议写在类下面，只会调用一次。

- `cloudminds.py`提供了GPU检测，加载模型时可以使用`.to(device)`来调度GPU。前提是已经安装了GPU版本的`pytorch`

- 以上案例暂未写retry机制，即访问接口/执行失败后的retry，可以参考如下代码：

- ```python
  class SmartVoice(CloudMindsModel):
      MODEL_NAME = "flag_open"
      address = "172.16.23.85:30811"  # fit 86
      agent_id = 65
      is_conversation = False
      session_id = mock_trace_id()
  
      channel = grpc.insecure_channel(address)
      stub = talk_pb2_grpc.TalkStub(channel)
  
      @classmethod
      def create(cls, *args, **kwargs):
          for i in range(3):  # retry 3 times for 60 seconds
              msg = cls.call(*args, **kwargs)
              if msg != "":
                  return msg
              time.sleep(60)
  
      @classmethod
      def call(cls, *args, **kwargs):
          def talk_req(payload):
              yield payload
  
          try:
              message = talk_pb2.TalkRequest(is_full=True,
                                             agent_id=cls.agent_id,
                                             session_id=cls.session_id if cls.is_conversation else mock_trace_id(),
                                             question_id=mock_trace_id(),
                                             event_type=0,
                                             robot_id="5C1AEC03573747D",
                                             tenant_code="cloudminds",
                                             version="v3",
                                             test_mode=False,
                                             asr=talk_pb2.Asr(lang="CH", text=str(kwargs["prompt"])))
              stream_response = cls.stub.StreamingTalk(talk_req(message).__iter__())
              response_json = [json.loads(json_format.MessageToJson(response)) for response in stream_response]
              tts = response_json[-1]["tts"][0]
              try:
                  return tts["action"]["param"]["raw_data"]["wholeAnswer"]
              except:
                  if tts.__contains__("text"):
                      return tts["text"]
                  return ""
          except:
              return ""
  
  ```

### 5.运行测试套件

集成工具路径：

```
├─evals
│  ├─cli
│  |  └─oaieval.py
│  |  └─oaievalset.py
```

#### 5.1运行单个测试套件

例如：

```shell
C:\Users\admin\.conda\envs\evals\python.exe D:\GitHub\evals\evals\cli\oaieval.py chatglm_api BoolQ_fact
```

其中第一个参数`chatglm_api`代表我们的被测模型，即写在`cloudminds.py`文件中的类属性`MODEL_NAME`的值。

第二个参数`BoolQ_fact`代表指定的测试套件名称，即写在`BoolQ.yaml`文件中的测试配置名称。

#### 5.2运行单个测试套件集

例如：

```
C:\Users\admin\.conda\envs\evals\python.exe D:\GitHub\evals\evals\cli\oaievalset.py chatglm_api eval-cloudminds
```

其中第一个参数`chatglm_api`代表我们的被测模型，即写在`cloudminds.py`文件中的类属性`MODEL_NAME`的值。

第二个参数`eval-cloudminds`代表指定的测试套件集名称，即写在`cloudminds_plan.yaml`文件中的测试配置名称。

### 6.查看测试结果

测试完成后会将日志存储到目录：`/tmp/evallogs/xxxx.jsonl`，如果是Windows系统，则会在某个盘符的根目录中生成目录tmp

当metrics为accuracy时，测试日志中有一条记录为：`{"final_report": {"accuracy": 0.8310312295894917}}`

当评估方法为辅助模型评估时，测试日志中有一条记录为：

```json
{
	"final_report": {
		"invalid_request_during_completion": 0,
		"invalid_request_during_evaluation": 0,
		"counts/choice/C": 8,
		"counts/choice/A": 89,
		"counts/choice/D": 3
	}
}
```

以上示例为测试报告日志，其余的日志为测试过程日志。

### 7.数据集管理

#### 7.1数据集管理脚本使用指南

`datasets_sync.py`实现S3对象存储管理数据集、测试集等

**参数说明**：

`fn`: 拉取数据:`pull`  推送数据:`push`
`target_bucket`: S3对象存储bucket 如：`evals-bucket`
`sync_pth`: 推送/拉取数据路径如：`datasets`或`evals/registry/data`
`overwrite`: 数据已存在时是否重写， 重写`overwrite` 不重写`no_overwrite`

**案例**：

1.从存储中拉取数据，例如从S3存储中拉取datasets目录到本地的datasets目录：

```shell
python3 datasets_sync.py pull evals-bucket datasets no_overwrite
```

2.已经生成了自己的用例，将本地用例存储至S3，例如将本地的指定目录`evals/registry/data`上传到新的bucket：`evals-bucket-new`（S3如果没有此bucket，会自动新建）

```shell
python3 datasets_sync.py push evals-bucket-new evals/registry/data no_overwrite
```

**说明**：

`evals-bucket`是默认桶，可以根据需要选择自己的桶进行管理（可用作版本管理）

以上基于项目根目录，pull和push操作会自动同步目录层级

#### 7.2数据集管理客户端使用指南

客户端下载地址：http://wiki.cloudminds.com/pages/viewpage.action?pageId=45012947

客户端连接参数：详细截图可参考如上链接

```
"Account Name": "nlp-gpt-evals",
"Account Type": "S3 Compatible Storage",
"REST Endpoint": "https://dev-s3.harix.iamidata.com",
"Access Key ID": "RQ6WBG2Z4IL6IUE6SOGN",
"Secret Access Key": "j8miGyDF1mrXSH9QjDUryvhR4suRCPuuyLKpe2sf"
```

### 8.自动生成测试集、测试套件

#### 8.1自动生成代码

```
├─evals
│  ├─prompt
│  │  └─generate_en.py
│  │  └─generate_zh.py
```

#### 8.2自动生成代码使用细则

**使用方法**：在`generate_*.py`文件中新增类，新增的类需要继承`Generate`或`GenerateZh`这个类，并重写以下函数：`extract_and_save_datasets`、`format_one_json`、`format_chat_prompt`，其中`format_chat_prompt`函数主要处理模型的输入prompt格式，`format_one_json`主要处理单条测试用例的格式，包括输入和期望，`extract_and_save_datasets`主要用于原始数据解析。

**举个例子**：

```python
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
                {"role": "user", "content": f"关键词：{'、'.join(item['keyword'])}。"}]
```

**说明**：

- Generate和GenerateZh提供了默认的测试套件生成模板。如过需要改动测试套件模板，可以在新的类中重写`format_one_yaml`方法。

#### 8.2自动生成代码执行过程

**举例**：

```python
if __name__ == '__main__':
    sample = 100

    COQA(config=["validation", sample])  # train/validation

    MultiRC(config=["test"])  # test

    WSC(config=["test", sample])  # test

    BoolQ(config=["validation", sample])  # train/validation
```

选择需要的数据集进行测试用例生成，例如BoolQ这个类是用于生成【判断正误】测试集。其原始数据提供了validation和train两种，我们需要从validation这个数据集中抽取100条来生成测试用例，则配置情况为`BoolQ(config=["validation", 100])`，如果需要validation下所有的数据作为样本，则配置情况为`BoolQ(config=["validation"])`。



**执行过程**：

- **step1**: 系统会判断datasets目录下有没有`BoolQ/validation.jsonl`这个文件

  - 如果没有，则执行`extract_and_save_datasets`函数去拉取原始数据
    - 将原始数据下载并解压到本地downloads目录
    - 然后在datasets目录下生成`BoolQ/xxx.jsonl`文件
  - 如果有，则继续

- **step2**：系统读取`BoolQ/validation.jsonl`文件内容，

- **step3**：通过`generate_prompt_jsonl_batch`方法生成测试集，并存储到指定目录

- ```
  ├─evals
  │  ├─registry
  │  │  ├─data
  │  │  │  ├─BoolQ
  │  │  │  │  └─BoolQ.jsonl
  ```

- **step4**：通过`generate_evals_yaml_batch`方法生成测试套件，并存储到指定目录

- ```
  ├─evals
  │  ├─registry
  │  │  ├─evals
  │  │  |  └─BoolQ.yaml
  ```

  

## FAQ

### 1.辅助模型更改

使用其他模型辅助我们评估测试模型的回答是否ok，这里默认用的`gpt-3.5-turbo`，如需用chatglm或其他模型替代，则改动`evals.elsuite.modelgraded.classify:ModelBasedClassify`这个类下的eval_model的默认值。例如`chatglm_api`（封装在cloudminds.py中的MODEL_NAME）

```python
class ModelBasedClassify(evals.Eval):
    invalid_request_during_completion = 0
    invalid_request_during_evaluation = 0
    THIRD_MODELS = cloudminds.ChatCompletion.models

    def __init__(
        self,
        model_specs: evals.ModelSpecs,
        samples_jsonl: str,
        modelgraded_spec: str,
        *args,
        match_fn: str = "starts_or_endswith",
        max_tokens: int = 1024,
        multicomp_n: Union[int, str] = 1,
        multicomp_temperature: float = 0.4,
        samples_renamings: Optional[dict[str, str]] = None,
        eval_type: Optional[str] = None,
        eval_model: str = "gpt-3.5-turbo",  # <<< -------------------- 改这里 --------------------
        metaeval: bool = False,
        modelgraded_spec_args: Optional[dict[str, dict[str, str]]] = None,
        **kwargs,
    ):
        super().__init__(model_specs, *args, **kwargs)
```

### 2.测试套件集运行抛错解决

由于使用源码执行测试，没有生成可执行文件，因此需要修改`oaievalset.py`配置中的`command`

改动前：

```python
def run(args, unknown_args, registry: Optional[Registry] = None) -> None:
    registry = registry or Registry()
    commands: list[Task] = []
    eval_set = registry.get_eval_set(args.eval_set)
    for eval in registry.get_evals(eval_set.evals):
        command = ["oaieval", args.model, eval.key] + unknown_args
        if command in commands:
            continue
        commands.append(command)
    num_evals = len(commands)

```

改动后：

```python
def run(args, unknown_args, registry: Optional[Registry] = None) -> None:
    registry = registry or Registry()
    commands: list[Task] = []
    eval_set = registry.get_eval_set(args.eval_set)
    for eval in registry.get_evals(eval_set.evals):
        command = [r"C:\Users\admin\anaconda3\envs\evals\python.exe",
                   r"D:\GitHub\evals\evals\cli\oaieval.py", args.model, eval.key] + unknown_args
        if command in commands:
            continue
        commands.append(command)
    num_evals = len(commands)
```

