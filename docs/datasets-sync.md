## 数据集管理

`datasets_sync.py`实现S3对象存储管理数据集、测试集等

参数说明：

`fn`: 拉取数据:`pull`  推送数据:`push`
`target_bucket`: S3对象存储bucket 如：`evals-bucket`
`sync_pth`: 推送/拉取数据路径如：`datasets`或`evals/registry/data`
`overwrite`: 数据已存在时是否重写， 重写`overwrite` 不重写`no_overwrite`

案例：

1.从存储中拉取数据，例如从S3存储中拉取datasets目录到本地的datasets目录：

```shell
python3 datasets_sync.py pull evals-bucket datasets no_overwrite
```

2.已经生成了自己的用例，将本地用例存储至S3，例如将本地的指定目录`evals/registry/data`上传到新的bucket：`evals-bucket-new`（S3如果没有此bucket，会自动新建）

```shell
python3 datasets_sync.py push evals-bucket-new evals/registry/data no_overwrite
```

说明：

`evals-bucket`是默认桶，可以根据需要选择自己的桶进行管理

以上基于项目根目录，pull和push操作会自动同步目录层级