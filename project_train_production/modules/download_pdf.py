import datetime
import logging
import os
from contextlib import closing
import platform
import time
import json
import gevent
from gevent import monkey

monkey.patch_all()
import requests
from project_train_production.settings import Env


def reconnet(func):
    def inner(*args, **kwargs):
        n = 0
        t1 = time.time()
        try_times = 0
        while True:
            try:
                return func(*args, **kwargs)
                # 很关键 成功就要中断循环
                break
            except:
                time.sleep(10)
                t2 = time.time()
                if ((t2 - t1) // 60) % 2 == 0:
                    logging.info('{}  {}--任务已经等待了--{}--秒'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),str(args) + str(kwargs), (t2 - t1)))
                try_times += 1
                if try_times > Env.try_times:
                    logging.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'  '+str(*args, **kwargs) + '任务重试次数已经超过规定次数')

    return inner


@reconnet
def totalpages():
    source_info_url = Env.source_info_url
    post_args = {'page': 100, 'needFields[]': ['id', 'stockName', 'companyName']}
    response = requests.post(source_info_url, data=post_args, timeout=Env.timeout)
    json_data = json.loads(response.text[25:-2])
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
        source_info_url = Env.source_info_url
        try:
            response = requests.post(source_info_url, data=post_args, timeout=Env.timeout)
        except:
            logging.info('{}  链接超时,获取第{}页信息失败'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),page_num))
        # 提取数据
        json_data = json.loads(response.text[25:-2])
        company_num = len(json_data['listInfo']['content'])
        for index in range(company_num):
            company_name = json_data['listInfo']['content'][index]['companyName']
            company_id = json_data['listInfo']['content'][index]['id']
            company_names_and_ids_dict[company_name] = company_id
    return company_names_and_ids_dict


class DownloadCompanysWxfhPdfs:
    def __init__(self,
                 company_names_and_ids_dict,
                 start_date=Env.start_date,
                 end_date=Env.end_date,
                 load_download_history=True,
                 download_history_file_absolute_path=Env.download_history_file_absolute_dir_path,
                 save_path=Env.save_path):

        self.company_names_and_ids_dict = company_names_and_ids_dict
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        self.load_download_history = load_download_history
        self.load_download_history_file_absolute_path = download_history_file_absolute_path
        self.save_path = save_path
        self.pdf_source_info_url = Env.pdf_source_info_url
        if self.load_download_history:
            try:
                with open(self.load_download_history_file_absolute_path, 'r', encoding='utf-8') as f:
                    self.download_history = json.loads(f.read())
            except:
                self.download_history = {}
        else:
            self.download_history = {}
        # print(self.download_history)

    @reconnet
    def __download_one_company_pdf(self, company_name, company_id):
        # index 是公司的列表中的位置
        company_id = company_id
        company_name = company_name
        if not company_name in self.download_history.keys():
            self.download_history[company_name] = {}
        pdf_source_post_args = {'id': company_id, 'callback': 'jQuery211_1600008606945'}
        # 容易出现超时错误 502 Bad GateWay
        company_pdfdata_response = requests.post(self.pdf_source_info_url.format(company_id), data=pdf_source_post_args,
                                                 timeout=Env.timeout)
        try:
            company_pdfdata_response_json_data = json.loads(company_pdfdata_response.text[25:-2])
        except:
            logging.info('{}  company_pdfdata_response_json_data 加载出错,加载内容为{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                               company_pdfdata_response.text[25:-2]))
        # wxhf:问询回复
        wxhf_list = company_pdfdata_response_json_data['wxhfhInfo']  # 是一个列表,里面套着字典
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        count = 0
        pdf_file_num = len(wxhf_list)

        for pdf_info in wxhf_list:
            file_publish_date = datetime.datetime.strptime(pdf_info['publishDate'], '%Y-%m-%d')
            if (file_publish_date - self.start_date).days >= 0 and (file_publish_date - self.end_date).days <= 0:
                file_title = pdf_info['disclosureTitle']
                file_relative_url = pdf_info['destFilePath']
                file_absolute_url = 'http://www.neeq.com.cn' + file_relative_url
                file_name = file_title + '.pdf'
                file_save_path = os.path.join(self.save_path, file_name)
                count += 1
                if not os.path.exists(file_save_path):
                    with closing(
                            requests.get(file_absolute_url, stream=True, timeout=Env.timeout)) as response:
                        with open(file_save_path, "wb") as f:

                            for chunk in response.iter_content(chunk_size=512):
                                if chunk:
                                    f.write(chunk)
                    logging.info('{}  {}--的第--{}/{}个--文件--《{}.pdf》--下载完毕'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),company_name, count, pdf_file_num, file_title))
                if not file_name in self.download_history[company_name].keys():
                    self.download_history[company_name][file_name] = pdf_info['publishDate']  # 2020-09-09
                else:
                    logging.info('{}  {}--的第--{}/{}个--文件--《{}.pdf》--已存在'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),company_name, count, pdf_file_num, file_title))
        # print(self.download_history)

    def download(self):
        missions = []
        for company_name, company_id in self.company_names_and_ids_dict.items():
            missions.append(
                gevent.spawn(self.__download_one_company_pdf, company_name, company_id))
        gevent.joinall(missions)
        download_history_json = json.dumps(self.download_history, ensure_ascii=False)
        with open(self.load_download_history_file_absolute_path, 'w', encoding='utf-8') as f:
            f.write(download_history_json)


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='pdf_download.log',level=logging.DEBUG)# 可选filemode='w')
    t1 = time.time()
    DownloadCompanysWxfhPdfs(company_names_and_ids()).download()
    t2 = time.time()
    logging.info('{}  本次玩从头下载共耗时--{}--秒'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),(t2 - t1)))
