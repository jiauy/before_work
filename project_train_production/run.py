from modules.download_pdf import DownloadCompanysWxfhPdfs,company_names_and_ids
from apscheduler.schedulers.blocking import BlockingScheduler


def job1():
    print('这是job1')


def job2():
    print('这是job2')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(DownloadCompanysWxfhPdfs(company_names_and_ids()).download, 'interval', max_instances=100,seconds=5, id='test_job1')
    scheduler.add_job(DownloadCompanysWxfhPdfs(company_names_and_ids()).download, 'interval', max_instances=100,seconds=10, id='test_job2')
    scheduler.start()

