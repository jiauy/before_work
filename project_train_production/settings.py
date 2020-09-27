import datetime
import os

class BaseEnv:
    source_info_url = 'http://www.neeq.com.cn/projectNewsController/infoResult.do?callback=jQuery211_1599964857562'
    pdf_source_info_url = 'http://www.neeq.com.cn/projectNewsController/infoDetailResult.do?id={}&callback=jQuery211_1600008606945'
    Pdf2Table_url = 'http://qianliyan2.memect.cn:6111/api/pdf2table'
    this_file_path=os.path.realpath(__file__)
    this_file_dir_path=os.path.dirname(this_file_path)
    save_path=os.path.join(this_file_dir_path,'PdfDownload')
    download_history_file_absolute_dir_path=os.path.join(save_path,'PdfDownloadHistory.json')
    timeout=(10,10)
    try_times=3
    start_date='1990-01-01'
    end_date=datetime.datetime.now().strftime('%Y-%m-%d')
    log_dir_path=os.path.join(this_file_dir_path,'log')
    if not os.path.exists(log_dir_path):
        os.mkdir(log_dir_path)
    log_path=os.path.join(this_file_dir_path,'log','download_and_deal.log')

class ProductionEnv(BaseEnv):
    pass