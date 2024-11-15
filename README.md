# Python | 基于IP代理的爬虫方法——以豆瓣电影Top250爬取为例

原文见：http://www.manueld.me/index.php/archives/252/
1. web_crawler.py：为课堂上使用的演示代码，来源不详
2. web_crawler_new.py：为修改后的完整代码。相比于上一版，修改处如下：
- 修改askURL函数，使用代理IP发送请求，在main函数前设置代理IP的相关参数
- 在askURL函数中添加try/except以捕获错误
- 在getData函数的每次请求中添加随机延时，以防止IP被封
- 在getData函数中捕捉错误，在出现错误时再次尝试提交请求，即添加重试机制
- 修改了main函数中的savepath变量，删除保存位置目录中的result文件夹
