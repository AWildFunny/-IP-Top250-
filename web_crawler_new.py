# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import random  # 添加用于随机选择代理IP
import time  # 添加用于延时

# 保持原有的正则表达式定义不变
findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

proxyHost = "dyn.horocn.com"
proxyPort = "50000"
proxyUser = "B8FG1815792430398662"  # 替换为你的订单号
proxyPass = "LBBtHWxOyTewmd8M"           # 替换为你的密码

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}


def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = "./豆瓣电影Top250.xls"
    saveData(datalist, savepath)


def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        print(f"正在爬取第 {i + 1} 页...")
        # 添加随机延时
        time.sleep(random.uniform(1, 3))
        html = askURL(url)
        if not html:
            print(f"第 {i + 1} 页爬取失败，尝试下一页...")
            continue

        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            try:
                data = []
                item = str(item)
                link = re.findall(findLink, item)[0]
                data.append(link)
                imgSrc = re.findall(findImgSrc, item)[0]
                data.append(imgSrc)
                titles = re.findall(findTitle, item)
                if (len(titles) == 2):
                    ctitle = titles[0]
                    data.append(ctitle)
                    otitle = titles[1].replace("/", "")
                    data.append(otitle)
                else:
                    data.append(titles[0])
                    data.append(' ')
                rating = re.findall(findRating, item)[0]
                data.append(rating)
                judgeNum = re.findall(findJudge, item)[0]
                data.append(judgeNum)
                inq = re.findall(findInq, item)
                if len(inq) != 0:
                    inq = inq[0].replace("。", "")
                    data.append(inq)
                else:
                    data.append(" ")
                bd = re.findall(findBd, item)[0]
                bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)
                bd = re.sub('/', "", bd)
                data.append(bd.strip())
                datalist.append(data)
            except Exception as e:
                print(f"解析数据时出错: {str(e)}")
                continue

    return datalist


def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }

    try:
        # 设置代理
        proxy_handler = urllib.request.ProxyHandler({
            "http": proxyMeta,
            "https": proxyMeta,
        })

        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [(k, v) for k, v in head.items()]
        urllib.request.install_opener(opener)

        response = urllib.request.urlopen(url, timeout=10)
        html = response.read().decode("utf-8")
        return html

    except Exception as e:
        print(f"访问URL失败: {str(e)}")
        return None


def saveData(datalist, savepath):
    print("开始保存数据...")
    try:
        book = xlwt.Workbook(encoding="utf-8", style_compression=0)
        sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
        col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")

        # 写入列名
        for i in range(0, 8):
            sheet.write(0, i, col[i])

        # 写入数据
        for i in range(len(datalist)):
            print(f"正在保存第 {i + 1} 条数据")
            data = datalist[i]
            for j in range(0, 8):
                sheet.write(i + 1, j, data[j])

        book.save(savepath)
        print(f"数据保存成功！共保存 {len(datalist)} 条记录到 {savepath}")
    except Exception as e:
        print(f"保存数据时出错: {str(e)}")


if __name__ == "__main__":
    print("开始爬取...")
    main()
    print("爬取完毕！")