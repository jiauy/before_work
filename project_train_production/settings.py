import os

class BaseEnv:
    source_info_url = 'http://www.neeq.com.cn/projectNewsController/infoResult.do?callback=jQuery211_1599964857562'
    pdf_source_info_url = 'http://www.neeq.com.cn/projectNewsController/infoDetailResult.do?id={}&callback=jQuery211_1600008606945'
    this_file_path=os.path.realpath(__file__)
    this_file_dir_path=os.path.dirname(this_file_path)
    default_save_path=os.path.join(this_file_dir_path,'PdfDownload')
    default_download_history_file_absolute_dir_path=os.path.join(default_save_path,'PdfDownloadHistory.json')

class ProductionEnv(BaseEnv):
    pass