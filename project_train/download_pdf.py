import os

import requests
import json

class DownloadCompanysPdf:
    def __init__(self,page_num):
        self.source_info_url = 'http://www.neeq.com.cn/projectNewsController/infoResult.do?callback=jQuery211_1599964857562'
        self.post_args = {'page': page_num, 'isNewThree': 1, 'sortfield': 'updateDate', 'sorttype': 'desc',
                          'needFields[]': ['id', 'stockName', 'companyName']}
        self.response = requests.post(self.source_info_url, data=self.post_args)
        self.json_data = json.loads(self.response.text[25:-2])
        self.pdf_source_info_url='http://www.neeq.com.cn/projectNewsController/infoDetailResult.do?id={}&callback=jQuery211_1600008606945'
    def download_onepage_pdf(self):
        company_num = len(self.json_data['listInfo']['content'])
        base_dir=os.getcwd()
        for index in range(company_num):
            company_id=self.json_data['listInfo']['content'][index]['id']
            company_name=self.json_data['listInfo']['content'][index]['companyName']
            pdf_source_post_args={'id':company_id,'callback': 'jQuery211_1600008606945'}
            company_pdfdata_response=requests.post(self.pdf_source_info_url.format(company_id), data=pdf_source_post_args)
            company_pdfdata_response_json_data=json.loads(company_pdfdata_response.text[25:-2])
            print(company_pdfdata_response_json_data)
            wxhf_num=len(company_pdfdata_response_json_data['wxhfhInfo'])
            wxhf_json_data=company_pdfdata_response_json_data['wxhfhInfo']
            print(wxhf_json_data)
            save_dir = os.path.join(base_dir, 'company', company_name)
            for pdf_index in range(wxhf_num):
                filr_title=wxhf_json_data[pdf_index]['disclosureTitle']
                file_path=wxhf_json_data[pdf_index]['destFilePath']
                file_url_path='http://www.neeq.com.cn'+file_path
                print(file_url_path)
                response = requests.get(file_url_path, stream=True)
                save_path=os.path.join(save_dir,filr_title)+'.pdf'
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=512):
                        f.write(chunk)
if __name__ == '__main__':
    # DownloadCompanysPdf(0).download_onepage_pdf()
    DownloadCompanysPdf(1).download_onepage_pdf()
    DownloadCompanysPdf(2).download_onepage_pdf()
    DownloadCompanysPdf(3).download_onepage_pdf()