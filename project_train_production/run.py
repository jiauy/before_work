from project_train_production.modules.deal_pdf import DealPdf2Table
from project_train_production.modules.download_pdf import DownloadCompanysWxfhPdfs,company_names_and_ids
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import logging
from project_train_production.settings import ProductionEnv

def main():
    logging.basicConfig(filename=ProductionEnv.log_path, filemode='w', level=logging.DEBUG)  # 可选filemode='w')
    DownloadCompanysWxfhPdfs(company_names_and_ids()).download()
    DealPdf2Table().deal()


if __name__ == '__main__':
    try:
        scheduler = BlockingScheduler()
        scheduler.add_job(main, 'interval', max_instances=100,seconds=60*60*24, id='download_and_deal_today_pdf_to_table')
        scheduler.start()
    except:
        scheduler.shutdown()

    #for test
    # main()
