import datetime
import io
import json
import logging
import os
import re
import time
import gevent
from gevent import monkey

monkey.patch_all()
import requests
from project_train_production.settings import ProductionEnv


# 网站自带的函数封装了一个类,改变了一下保存路径,发现一个bug:zipfile没有open属性
class Pdf2TableAPI:
    def invoke_api(self, api, file_path, file_save_path):
        # 异步执行
        output_format = 'zip'  # or json or bz2
        url = 'http://qianliyan2.memect.cn:6111/api/{}'.format(api)
        # query = {
        #     # 表示异步执行，所以需要通过轮训获得结果
        #     # 'async': 'false', #true
        #     'async': 'true', #true
        #     'output-format': output_format
        # }

        query = {
            'extract-image': 'true',
            'format': 4,  # 1 or 4 规定是4
            'textlines': 'false',  # testlinse or span
            'table': 'ybk',  # wbk ybk all
            # 'wbk': 2,                   #wbk的识别方式2快1慢
            # 'layout': 'default',
            # 'html': 'false',
            # 'html-scale': 1.5,
            # 'extract-classes': 'chart', #chart表示需要识别图表，diagram表示需要识别流程图等，多个使用逗号分割
            'output-files': 'raw.json',  # 表示同时返回raw.json，多个使用逗号分割
            # 'output-format': 'zip',  # zip json json表示仅仅返回table.json文件，zip表示使用zip打包多个文件，bz2使用tar.bz2打包多个文件返回
            'async': 'true',  # true
            'output-format': output_format
        }

        headers = {}
        with open(file_path, 'rb') as fp:
            data = fp.read()
        # 如果上传的是json，建议先压缩，如：
        # import gzip
        # data = gzip.compress(data)
        # headers={'Content-Encoding':'gzip'}
        r = requests.post(url, data=data, params=query, headers=headers)
        result = None
        if r.status_code == 200:
            result = r.json()
        elif r.status_code == 400:
            # 返回的是json
            result = r.json()
        else:
            # 其它的错误，如：500，系统错误
            print(r.text)

        # 等待结果
        if result and result.get('task'):
            # result={task:{id:''}}
            print('开始获取任务--{}--的结果'.format(result.get('task')))
            self.get_result(api, result.get('task').get('id'), file_save_path,
                            output_format=output_format)
            print('任务--{}--完成'.format(result.get('task')))
        else:
            # 执行失败等
            pass

    def get_result(self, api, task_id, file_save_path, output_format='json'):
        # api=pdf2json ,pdf2table,pdf2doc
        url = 'http://qianliyan2.memect.cn:6111/api/{}'.format(api)
        query = {
            'task_id': task_id
        }
        while True:
            r = requests.post(url, params=query)
            print(r.status_code)
            print(r.text)
            if r.status_code == 200:
                if output_format in ('zip', 'bz2'):
                    # 这里演示如何直接解压，也可以把zip文件保存到本地
                    with io.BytesIO(r.content) as fp:
                        if output_format == 'bz2':
                            import tarfile
                            with tarfile.open(fileobj=fp) as tar:
                                tar.extractall(file_save_path)
                        else:
                            import zipfile
                            with zipfile.ZipFile(fp) as zf:  # with zipfile.open(fp) as zf 报错 没有这个属性
                                zf.extractall(file_save_path)
                                print('zip文件下载并解压成功')
                else:
                    with open(file_save_path + 'json', 'wb') as fp:
                        fp.write(r.content)
                break
            elif r.status_code == 400:
                # 获得错误信息:{error:{code:'',message:''}}
                result = r.json()
                code = result.get('error').get('code')
                if code == 'error':
                    # 表示已经执行完毕，但是执行失败，不需要再轮训
                    break
                elif code in ('running', 'waiting'):
                    # running or waiting
                    # 等待1秒再次轮训
                    time.sleep(1)
                else:
                    # 其他的错误码？暂时没有，一样不需要继续了
                    break
            else:
                # 其他的错误，如：500，系统错误，不需要再轮训
                break


class DealPdf2Table(Pdf2TableAPI):
    def __init__(self,
                 start_date=ProductionEnv.start_date,
                 end_date=ProductionEnv.end_date,
                 source_dir=ProductionEnv.save_path,
                 output_dir=ProductionEnv.save_path):

        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.enf_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        self.source_dir = source_dir
        self.output_dir = output_dir

        # table,wbk,html,html-scale,layout,extract-classes

        self.headers = {}
        self.url = ProductionEnv.Pdf2Table_url

    def __deal1(self, file_name):
        # company_files
        # 第二次更新会含有以前解压好的文件夹,需要处理掉
        try:
            if re.findall('回复', file_name)[0] == '回复' and file_name[-3:] == 'pdf':
                file_path = os.path.join(self.source_dir, file_name)
                file_save_path = os.path.join(self.output_dir, file_name[:-4])
                # 没有文件对应的目录才可以处理,否则就是之前处理过了
                if not os.path.exists(file_path[:-4]):
                    self.invoke_api(api='pdf2table', file_path=file_path, file_save_path=file_save_path)
                    logging.info('{}  {}--异步提交成功'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),file_name))
                else:
                    logging.info('{}  {}--已经处理过'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),file_name))
        except:
            logging.info('{}  {}--文件--无回复字样'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),file_name))

    def deal(self):
        his_path = ProductionEnv.download_history_file_absolute_dir_path
        with open(his_path, 'r') as f:
            history = f.read()
        his_dict = json.loads(history)
        filelist = []

        for k, v in his_dict.items():
            for file_name, date in v.items():
                datetime_date = datetime.datetime.strptime(date, '%Y-%m-%d')
                if (datetime_date - self.start_date).days >= 0 and (datetime_date - self.enf_date).days <= 0:
                    filelist.append(file_name)

        missions = []
        for filename in filelist:
            missions.append(gevent.spawn(self.__deal1(filename)))
        gevent.joinall(missions)


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='pdf_deal.log',level=logging.DEBUG)# 可选filemode='w')
    t1 = time.time()
    DealPdf2Table().deal()
    t2 = time.time()
    logging.info('{}  本次任务一共耗时--{}--秒'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),(t2 - t1)))
