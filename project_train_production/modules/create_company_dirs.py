import os
import requests
import json


class CreateCompanyDirectory:

    def __init__(self, page_num):
        """
        :param page_num: 要下载第几页,从0开始
        """
        self.post_args = {'page': page_num, 'isNewThree': 1, 'sortfield': 'updateDate', 'sorttype': 'desc',
                          'needFields[]': ['id', 'stockName', 'companyName']}
        # 建立链接:
        self.source_info_url = 'http://www.neeq.com.cn/projectNewsController/infoResult.do?callback=jQuery211_1599964857562'
        try:
            self.response = requests.post(self.source_info_url, data=self.post_args)
        except Exception:
            print('链接超时,获取第{}页信息失败'.format(page_num))
        # 保存数据
        self.json_data = json.loads(self.response.text[25:-2])

    def create_company_directory(self):
        company_num = len(self.json_data['listInfo']['content'])
        base_dir = os.getcwd()
        for index in range(company_num):
            company_name = self.json_data['listInfo']['content'][index]['companyName']
            dir_path = os.path.join(base_dir, 'company', company_name)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)


if __name__ == '__main__':
    for i in range(4):
        page = CreateCompanyDirectory(i)
        page.create_company_directory()
