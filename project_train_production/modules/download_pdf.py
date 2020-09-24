import os
from contextlib import closing
import time
import json
import gevent
from gevent import monkey

monkey.patch_all()
import requests
from project_train_production.settings import ProductionEnv


def totalpages():
    source_info_url = ProductionEnv.source_info_url
    post_args = {'page': 100, 'needFields[]': ['id', 'stockName', 'companyName']}
    response = requests.post(source_info_url, data=post_args, timeout=(60 * 10, 60 * 10))
    print(response.text)
    json_data = json.loads(response.text[25:-2])
    print(json_data)
    total_pages_num = json_data['listInfo']['totalPages']
    return total_pages_num


# 获取网站上当前公司的名称与id，返回格式为字典
def company_names_and_ids():
    company_names_and_ids_dict = {}
    total_pages_num = totalpages()
    for page_num in range(total_pages_num):
        post_args = {'page': page_num, 'isNewThree': 1, 'sortfield': 'updateDate', 'sorttype': 'desc',
                     'needFields[]': ['id', 'stockName', 'companyName']}
        # 建立链接:
        source_info_url = ProductionEnv.source_info_url
        try:
            response = requests.post(source_info_url, data=post_args, timeout=(60 * 10, 60 * 10))
        except:
            print('链接超时,获取第{}页信息失败'.format(page_num))
        # 提取数据
        json_data = json.loads(response.text[25:-2])
        print(json_data)
        print(type(json_data))
        company_num = len(json_data['listInfo']['content'])
        for index in range(company_num):
            company_name = json_data['listInfo']['content'][index]['companyName']
            company_id = json_data['listInfo']['content'][index]['id']
            company_names_and_ids_dict[company_name] = company_id
    return company_names_and_ids_dict


def reconnet(func):
    def inner(*args, **kwargs):
        n = 0
        t1 = time.time()
        while True:
            try:
                func(*args, **kwargs)
                # 很关键 成功就要中断循环
                break
            except:
                pass
            time.sleep(10)
            t2 = time.time()
            if ((t2 - t1) // 60) % 2 == 0:
                print('{}--任务已经等待了--{}--秒'.format(kwargs, (t2 - t1)))

    return inner


class DownloadCompanysWxfhPdfs:
    def __init__(self, company_names_and_ids_dict, load_download_history=False,
                 download_history_file_absolute_path=ProductionEnv.default_download_history_file_absolute_path,
                 save_path=ProductionEnv.default_save_path):
        self.company_names_and_ids_dict = company_names_and_ids_dict
        self.load_download_history = load_download_history
        self.load_download_history_file_absolute_path = download_history_file_absolute_path
        self.save_path = save_path
        self.pdf_source_info_url = ProductionEnv.pdf_source_info_url

    @reconnet
    def __download_one_company_pdf(self, company_name, company_id):
        # index 是公司的列表中的位置
        company_id = company_id
        company_name = company_name
        pdf_source_post_args = {'id': company_id, 'callback': 'jQuery211_1600008606945'}
        # 容易出现超时错误 502 Bad GateWay
        company_pdfdata_response = requests.post(self.pdf_source_info_url.format(company_id), data=pdf_source_post_args,
                                                 timeout=(60 * 10, 60 * 10))
        company_pdfdata_response_json_data = json.loads(company_pdfdata_response.text[25:-2])
        # wxhf:问询回复
        wxhf_list = company_pdfdata_response_json_data['wxhfhInfo']  # 是一个列表,里面套着字典
        save_dir = os.path.join(self.save_path, 'PDFdownload')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        count=0
        pdf_file_num=len(wxhf_list)
        for pdf_info in wxhf_list:
            print(pdf_info)
            file_title = pdf_info['disclosureTitle']
            file_relative_path = pdf_info['destFilePath']
            file_absolute_path = 'http://www.neeq.com.cn' + file_relative_path
            save_path = os.path.join(save_dir, file_title) + '.pdf'
            count += 1
            if not os.path.exists(save_path):
                with closing(requests.get(file_absolute_path, stream=True, timeout=(60 * 10, 60 * 10))) as response:
                    with open(save_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=512):
                            if chunk:
                                f.write(chunk)

                print('{}--的第--{}/{}个--文件--《{}.pdf》--下载完毕'.format(company_name,count,pdf_file_num,file_title))
            else:
                print('{}--的第--{}/{}个--文件--《{}.pdf》--已存在'.format(company_name,count,pdf_file_num,file_title))

    def download(self):
        missions = []
        for company_name, company_id in self.company_names_and_ids_dict.items():
            missions.append(
                gevent.spawn(self.__download_one_company_pdf, company_name, company_id))
        gevent.joinall(missions)



if __name__ == '__main__':
    t1=time.time()
    DownloadCompanysWxfhPdfs(company_names_and_ids()).download()
    t2=time.time()
    print('本次玩从头下载共耗时--{}--秒'.format(t2-t1))

