- DownloadCompanysWxfhPdfs:在默认目录下，下载所有pdf文件
- DownloadCompanysWxfhPdfsByTime:在默认目录下，下载指定时间的pdf文件
- 每天查询文件，如果有更新，就下载，判断更新的标准是，文件名不在历史文件中。如果没有历史文件，就全部下载。
历史文件的格式：
{
    '公司名称'：
    {
    'pdf文件名'：文件出版日期,
    'pdf文件名'：文件出版日期,
    'pdf文件名'：文件出版日期,
    },
}