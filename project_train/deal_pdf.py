import os
import re
import requests

class DealPdf2Table:
    def __init__(self):
        self.base_dir=os.path.join(os.getcwd(),'company')
        self.company_names=os.listdir(self.base_dir)

        #table,wbk,html,html-scale,layout,extract-classes
        self.query = {
                    'extract-image': 'true',
                    'format': 4,                #1 or 4 规定是4
                    'textlines': 'false',       #testlinse or span
                    'table': 'ybk',             #wbk ybk all
                    #'wbk': 2,                   #wbk的识别方式2快1慢
                    #'layout': 'default',
                    #'html': 'false',
                    #'html-scale': 1.5,
                    #'extract-classes': 'chart', #chart表示需要识别图表，diagram表示需要识别流程图等，多个使用逗号分割
                    'output-files': 'raw.json', #表示同时返回raw.json，多个使用逗号分割
                    'output-format': 'zip',     #zip json json表示仅仅返回table.json文件，zip表示使用zip打包多个文件，bz2使用tar.bz2打包多个文件返回
        }

        self.headers = {}
        self.url = 'http://qianliyan2.memect.cn:6111/api/pdf2table'
    def deal_pdf_2table_with_1thread(self,company_index):

        #company_files
        company_path=os.path.join(self.base_dir,self.company_names[company_index])
        files_list=os.listdir(company_path)
        print(files_list)
        for file_name in files_list:
            print(file_name)
            try:
                if re.findall('回复',file_name)[0]=='回复':
                    file_path=os.path.join(self.base_dir,self.company_names[company_index],file_name)
                    print(file_path)

                    with open(file_path, 'rb') as fp:
                        data = fp.read()
                    r = requests.post(self.url, data=data, params=self.query, headers=self.headers)
                    if r.status_code == 200:
                        # 返回的是json，或者使用r.content，直接保存到文件中
                        r.json()
                    elif r.status_code == 400:
                        # 返回错误
                        r.json()
                    else:
                        # 其它的错误
                        pass
            except:
                pass

    def get_result(api, task_id, output_format='json'):
        # api=pdf2json ,pdf2table,pdf2doc
        url = 'http://127.0.0.1:6111/api/{}'.format(api)
        query = {
            'task_id': task_id
        }
        while True:
            r = requests.post(url, params=query)
            if r.status_code == 200:
                if output_format in ('zip', 'bz2'):
                    # 这里演示如何直接解压，也可以把zip文件保存到本地
                    with io.BytesIO(r.content) as fp:
                        if output_format == 'bz2':
                            import tarfile
                            with tarfile.open(fileobj=fp) as tar:
                                tar.extractall('local/a')
                        else:
                            import zipfile
                            with zipfile.open(fp) as zf:
                                zf.extractall('local/a')
                else:
                    with open('local/a.json', 'wb') as fp:
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

if __name__ == '__main__':
    DealPdf2Table().deal_pdf_2table_with_1thread(1)