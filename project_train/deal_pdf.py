import io
import os
import re
import time
import gevent
from gevent import monkey
monkey.patch_all()
import requests

#网站自带的函数封装了一个类,改变了一下保存路径,发现一个bug:zipfile没有open属性
class Pdf2TableAPI:
    def invoke_api(self, api, filename, company_name, file_name_without_pdf):
        # 异步执行
        output_format = 'zip'  # or json or bz2
        url = 'http://qianliyan2.memect.cn:6111/api/{}'.format(api)
        query = {
            # 表示异步执行，所以需要通过轮训获得结果
            # 'async': 'false', #true
            'async': 'true', #true
            'output-format': output_format
        }
        headers = {}
        with open(filename, 'rb') as fp:
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
            self.get_result(api, result.get('task').get('id'), company_name, file_name_without_pdf,
                            output_format=output_format)
            print('任务--{}--完成'.format(result.get('task')))
        else:
            # 执行失败等
            pass

    def get_result(self, api, task_id, company_name, file_name_without_pdf, output_format='json'):
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
                                tar.extractall('company/{}/{}'.format(company_name, file_name_without_pdf))
                        else:
                            import zipfile
                            with zipfile.ZipFile(fp) as zf:  # with zipfile.open(fp) as zf 报错 没有这个属性
                                zf.extractall('company/{}/{}'.format(company_name, file_name_without_pdf))
                                print('zip文件下载并解压成功')
                else:
                    with open('company/{}/{}.json'.format(company_name, file_name_without_pdf), 'wb') as fp:
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
    def __init__(self):
        self.base_dir = os.path.join(os.getcwd(), 'company')
        self.company_names = os.listdir(self.base_dir)

        # table,wbk,html,html-scale,layout,extract-classes
        self.query = {
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
            'output-format': 'zip',  # zip json json表示仅仅返回table.json文件，zip表示使用zip打包多个文件，bz2使用tar.bz2打包多个文件返回
        }

        self.headers = {}
        self.url = 'http://qianliyan2.memect.cn:6111/api/pdf2table'

    def deal_pdf_2table_with_1threading(self, company_index):
        # company_files
        company_path = os.path.join(self.base_dir, self.company_names[company_index])
        #第二次更新会含有以前解压好的文件夹,需要处理掉
        files_list = os.listdir(company_path)
        count=0
        for file_name in files_list:
            count+=1
            try:
                if re.findall('回复', file_name)[0] == '回复' and file_name[-3:]=='pdf':
                    file_path = os.path.join(self.base_dir, self.company_names[company_index], file_name)
                    #没有文件对应的目录才可以处理,否则就是之前处理过了
                    if not os.path.exists(file_path[:-4]):
                        self.invoke_api(api='pdf2table', filename=file_path, company_name=self.company_names[company_index],
                                        file_name_without_pdf=file_name[:-4])
                        print('{}-有-{}-个文件,当前处理进度为--{}/{}--异步提交成功'.format(self.company_names[company_index], len(files_list),
                                                                  count, len(files_list)))
            except:
                print('{}-有-{}-个文件,当前处理进度为--{}/{}--无回复字样或该文件是已处理好的目录'.format(self.company_names[company_index],len(files_list),count,len(files_list)))


    def deal_pdf_2table_with_multithreading(self):
        missions=[]
        for company_index in range(len(self.company_names)):
            missions.append(gevent.spawn(self.deal_pdf_2table_with_1threading(company_index)))
        gevent.joinall(missions)


if __name__ == '__main__':
    t1=time.time()
    DealPdf2Table().deal_pdf_2table_with_multithreading()
    t2=time.time()
    print('本次任务一共耗时--{}--秒'.format(t2-t1))
