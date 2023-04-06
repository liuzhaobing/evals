#!/usr/bin/env python
"""
# @Time    : 2022/5/7 15:29
# @Author  : woyaoludaima
# @File    : S3_fac.py
# @Version : v1.0
# @Description :
"""
import argparse
import os
import sys

import boto3
import urllib3
from loguru import logger

urllib3.disable_warnings()


class S3:
    def __init__(self, StorageClass):
        self.endpoint_url = "https://dev-s3.harix.iamidata.com"
        self.access_key = 'RQ6WBG2Z4IL6IUE6SOGN'
        self.secret_key = 'j8miGyDF1mrXSH9QjDUryvhR4suRCPuuyLKpe2sf'
        self.region_name = 'spider'
        self.num = 1
        self.StorageClass = StorageClass

        # 连接s3
        self.s3 = boto3.resource(
            service_name='s3',
            region_name=self.region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint_url,
            verify=False
        )

        self.client = boto3.client(
            service_name='s3',
            region_name=self.region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint_url,
            verify=False
        )

    def create_bucket(self, name):
        try:
            if self.check_bucket(name):
                self.s3.create_bucket(Bucket=name)
                self.bucket_name = name
                logger.info(f'创建桶{name}成功!')
                return True
            else:
                logger.warning('桶存在!')
                return False
        except Exception as r:
            print(r)
            logger.error('创建桶失败!')
            return False

    def delete_bucket(self, name):
        bucket = ''
        for i in self.s3.buckets.all():
            if i.name == name:
                bucket = i
                break
        if bucket:
            try:
                bucket.objects.all().delete()
                bucket.delete()
                logger.info(f'删除桶{bucket.name}成功!')
            except:
                logger.error(f'删除桶{bucket.name}失败!')

    def check_bucket(self, name):
        for i in self.s3.buckets.all():
            if i.name == name:
                return False
        return True

    def upload_file_s3(self, bucket, path, dir_name):
        """
        上传本地文件到s3指定文件夹下
        :param path: 本地文件路径
        :param bucket: 桶名称
        :param dir_name:要上传到的s3文件夹名称
        :return: 上传成功返回True，上传失败返回False，并打印错误
        """
        file_name = os.path.basename(path)
        try:
            path1 = ''
            if '/' in path:
                path1 = path.lstrip('/') if not dir_name else dir_name
                if dir_name:
                    path1 = f'{path1}/{file_name}'
                else:
                    path1 = f'{file_name}'
            elif '\\' in path:
                path1 = path.lstrip('\\') if not dir_name else dir_name
                if dir_name:
                    path1 = f'{path1}/{file_name}'
            self.s3.Object(bucket, path1).upload_file(Filename=path, ExtraArgs={"StorageClass": self.StorageClass})
            logger.info(f'{bucket}/{path}上传成功!')
        except Exception as e:
            raise ValueError(str(e))

    def download_file_s3(self, bucket, file_source_name, file_save_name):
        """
        下载s3文件到指定本地目录
        :param file_save_name: 本地文件名
        :param bucket: 桶名称
        :param file_source_name:s3文件夹名称
        """
        self.client.download_file(bucket, file_source_name, file_save_name)
        logger.info(f'{bucket}/{file_save_name}下载成功!')

    def get_list_s3(self, bucket_name):
        """
        :param bucket_name: 桶名称
        :return: 该目录下所有文件列表
        """
        # 用来存放文件列表
        response = self.client.list_objects_v2(
            Bucket=bucket_name,
            # Delimiter='/',
            # Prefix=file_name,
        )
        file_list = []
        while 'NextContinuationToken' in response:
            if response['Contents']:
                file_list += response['Contents']
            if response['NextContinuationToken']:
                response = self.client.list_objects_v2(Bucket=bucket_name,
                                                       ContinuationToken=response['NextContinuationToken'])
            else:
                response = self.client.list_objects_v2(Bucket=bucket_name)

        return file_list


s3 = S3('ARCHIVED')


def push_local_dir_to_s3(target_bucket, sync_pth, overwrite=False):
    if s3.check_bucket(target_bucket):
        s3.create_bucket(target_bucket)
    uploaded_list = [item["Key"] for item in s3.get_list_s3(target_bucket)]
    project_path = os.path.abspath(".")
    sync_dir = project_path
    if "\\" in sync_pth:
        for item in sync_pth.strip().split("\\"):
            sync_dir = os.path.join(sync_dir, item)
    elif "/" in sync_pth:
        for item in sync_pth.strip().split("/"):
            sync_dir = os.path.join(sync_dir, item)
    for dir_path, dir_names, filenames in os.walk(sync_dir):
        for filepath in filenames:
            file_full_path = os.path.join(dir_path, filepath)
            s3_save_path = os.path.dirname(file_full_path).split(project_path)[-1]
            if "\\" in s3_save_path:
                s3_save_path = s3_save_path.replace("\\", "/")
            if s3_save_path not in uploaded_list or overwrite:
                s3.upload_file_s3(target_bucket, file_full_path, s3_save_path)


def pull_s3_dir_to_local(target_bucket, sync_pth, overwrite=False):
    if s3.check_bucket(target_bucket):
        logger.info(f'{target_bucket}/桶不存在无法下载!')
    project_path = os.path.abspath(".")
    sync_dir = project_path
    if "\\" in sync_pth:
        sync_pth_list = sync_pth.strip().split("\\")
        for item in sync_pth_list:
            sync_dir = os.path.join(sync_dir, item)

    elif "/" in sync_pth:
        sync_pth_list = sync_pth.strip().split("/")
        for item in sync_pth_list:
            sync_dir = os.path.join(sync_dir, item)
    else:
        sync_dir = os.path.join(sync_dir, sync_pth)
        sync_pth_list = [sync_pth]
    downloaded_list = []
    for dir_path, dir_names, filenames in os.walk(sync_dir):
        for filepath in filenames:
            file_full_path = os.path.join(dir_path, filepath)
            downloaded_list.append(file_full_path)
    for item in s3.get_list_s3(target_bucket):
        item_list = item["Key"].split("/")
        jump = False
        for i in range(len(sync_pth_list)):
            if sync_pth_list[i] != item_list[i + 1]:
                jump = True
        if jump:
            continue
        local_file_name = item["Key"].replace("/", "\\") if "\\" in project_path else item["Key"]
        local_file_name = project_path + local_file_name
        if local_file_name in downloaded_list and not overwrite:
            continue
        os.makedirs(os.path.dirname(local_file_name), exist_ok=True)
        s3.download_file_s3(target_bucket, item["Key"], local_file_name)


def main(fn, target_bucket, sync_pth, overwrite=False):
    if fn == "pull":
        return pull_s3_dir_to_local(target_bucket, sync_pth, overwrite)
    elif fn == "push":
        return push_local_dir_to_s3(target_bucket, sync_pth, overwrite)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="数据集管理")
    parser.add_argument("fn", type=str, help="拉取数据:pull  推送数据:push")
    parser.add_argument("target_bucket", type=str, help="S3对象存储bucket：如：evals-bucket", default="evals-bucket")
    parser.add_argument("sync_pth", type=str, help="推送/拉取数据路径如：datasets或evals/registry/data", default="datasets")
    parser.add_argument("overwrite", type=str, help="数据已存在时是否重写 重写overwrite 不重写no_overwrite", default="no_overwrite")
    args = parser.parse_args(sys.argv[1:])
    main(args.fn, args.target_bucket, args.sync_pth, True if args.overwrite == "overwrite" else False)
