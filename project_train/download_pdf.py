import os
from contextlib import closing
import time
import json
import gevent
from gevent import monkey
monkey.patch_all()
import requests


def reconnet(func):
    def inner(*args, **kwargs):
        n = 0
        t1 = time.time()
        while True:
            try:
                func(*args, **kwargs)
                #很关键 成功就要中断循环
                break
            except:
                pass
            time.sleep(10)
            t2 = time.time()
            if ((t2 - t1) // 60) % 2 == 0:
                print('{}--任务已经等待了--{}--秒'.format(kwargs, (t2 - t1)))

    return inner


class DownloadCompanysPdf:
    def __init__(self, page_num):
        self.source_info_url = 'http://www.neeq.com.cn/projectNewsController/infoResult.do?callback=jQuery211_1599964857562'
        self.post_args = {'page': page_num, 'isNewThree': 1, 'sortfield': 'updateDate', 'sorttype': 'desc',
                          'needFields[]': ['id', 'stockName', 'companyName']}
        self.page_num = page_num
        try_times = 0
        while True:
            try:
                # 考虑到可能会用到多线程,互相挤占网速,数据传输时间设置的长一点 10min
                self.response = requests.post(self.source_info_url, data=self.post_args, timeout=(60*10,60 * 10))
                break
            except:
                try_times += 1
                if try_times > 3:
                    print('第{}页数据尝试三次仍未获取成功'.format(page_num))
                    break

        self.json_data = json.loads(self.response.text[25:-2])
        self.pdf_source_info_url = 'http://www.neeq.com.cn/projectNewsController/infoDetailResult.do?id={}&callback=jQuery211_1600008606945'

    @reconnet
    def __download_one_company_pdf(self, index):
        #index 是公司的列表中的位置
        base_dir = os.getcwd()
        company_id = self.json_data['listInfo']['content'][index]['id']
        company_name = self.json_data['listInfo']['content'][index]['companyName']
        pdf_source_post_args = {'id': company_id, 'callback': 'jQuery211_1600008606945'}

        # 容易出现超时错误 502 Bad GateWay
        company_pdfdata_response = requests.post(self.pdf_source_info_url.format(company_id), data=pdf_source_post_args,
                                                 timeout=(60 * 10, 60 * 10))
        company_pdfdata_response_json_data = json.loads(company_pdfdata_response.text[25:-2])
        # wxhf:问询回复
        wxhf_num = len(company_pdfdata_response_json_data['wxhfhInfo'])
        wxhf_json_data = company_pdfdata_response_json_data['wxhfhInfo']
        save_dir = os.path.join(base_dir, 'company', company_name)
        for pdf_index in range(wxhf_num):
            file_title = wxhf_json_data[pdf_index]['disclosureTitle']
            file_path = wxhf_json_data[pdf_index]['destFilePath']
            file_url_path = 'http://www.neeq.com.cn' + file_path
            save_path = os.path.join(save_dir, file_title) + '.pdf'
            if not os.path.exists(save_path):

                with closing(requests.get(file_url_path, stream=True, timeout=(60 * 10, 60 * 10))) as response:

                    with open(save_path, "wb") as f:
                        # chunk_size 512 bytes
                        for chunk in response.iter_content(chunk_size=512):
                            if chunk:
                                f.write(chunk)
                print('第--{}--页,第--{}--个公司的第--{}/{}个--pdf文件<{}>下载完毕'.format(self.page_num, index, pdf_index+1, wxhf_num,
                                                                            file_title))
            else:
                print('第--{}--页,第--{}--个公司的第--{}/{}个--pdf文件<{}>已存在'.format(self.page_num, index, pdf_index+1, wxhf_num,
                                                                            file_title))

    def download_onepage_pdf_with_multithreding(self):
        company_num = len(self.json_data['listInfo']['content'])
        missions = []
        for index in range(company_num):
            missions.append(
                gevent.spawn(self.__download_one_company_pdf, index=index))
        gevent.joinall(missions)


def download_allpages_pdf_with_mutithreading(total_page_num):
    missions = []
    for index in range(total_page_num):
        missions.append(
            gevent.spawn(DownloadCompanysPdf(index).download_onepage_pdf_with_multithreding()))
    gevent.joinall(missions)


if __name__ == '__main__':
    t1=time.time()
    download_allpages_pdf_with_mutithreading(4)
    t2=time.time()
    print('本次玩从头下载共耗时--{}--秒'.format(t2-t1))

