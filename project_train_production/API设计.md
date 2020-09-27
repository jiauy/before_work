- download_pdf
    - @reconnet 重连次数限定
    - totalpages 获取目标网站有数据的页数
    - company_names_and_ids 获取目标网站全部公司名称和对应id
    - DownloadCompanysWxfhPdfs 创建或根据下载历史文件,下载指定日期或日期范围的pdf文件,并创建新的下载历史文件
    
- deal_pdf
    - DealPdf2Table 对指定日期范围的pdf文件进行处理
    
```
下载历史文件的格式：

{
    '公司名称'：
    {
    'pdf文件名'：'文件出版日期',
    'pdf文件名'：'文件出版日期',
    'pdf文件名'：'文件出版日期',
    },
}
