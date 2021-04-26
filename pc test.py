from bs4 import BeautifulSoup
import urllib.request, urllib.error
import re
import requests


def reptile_silisili(url):
    # url:需要爬取的网页
    # 爬取网页
    datelist = getDate(url)
    print(datelist)


# 爬取网页
def getDate(url):
    list_tatil = []  # 片名
    list_img = []  # 图片
    list_moive = []  # 播放
    list_end = []  # 汇总
    # 换页
    for i in range(10):  # 循环获取每一页的html
        a = str(i * 25)
        url1 = url + a
        html = askUrl(url1, a)  # 获取当前页源代码
        # 正则解析数据
        soup = BeautifulSoup(html, 'html.parser')  # 对网页进行解析
        # 获取img标签 分别提取姓名和图片
        for item in soup.find_all('img'):
            item = str(item)
            # 去除片名前后
            a = re.sub('<img alt="', "", item)
            b = re.sub('" c.*', '', a)
            # 去除图片前后
            c = re.sub('.*src="', '', a)
            d = re.sub('" width="100"/>', '', c)
            # 添加列表
            if b != None and b != '扫码下载豆瓣 App" height="80" src="https://img3.doubanio.com/f/movie/a02f6ed325fc52e220f299d51e730c422e2bcd16/pics/movie/douban_app_ad/qrcode.png" width="80">\n</img>':
                list_tatil.append(b)
                list_img.append(d)
        num1 = 0
        # 爬取播放网址
        for item in soup.find_all('a', herf=''):
            item = str(item)
            # 通过try洗数据
            try:
                a = item.index(r'https://movie.douban.com/subject/')
                b = item[a:a + 42]
                num1 += 1
                # 去掉末尾引号
                if num1 % 2 == 0:
                    if b[-1] == '"':
                        b = b.replace(r'"', '')
                        list_moive.append(b)
                    else:
                        list_moive.append(b)
            except:
                pass
        # 合并表单
        for i in range(len(list_moive)):
            list_end.append(list_tatil[i])
            list_end.append(list_img[i])
            list_end.append(list_moive[i])

    return list_end


# 单次获取html
def askUrl(url1, a):
    # 定义头部信息
    cookies = {
        'douban-fav-remind': '1',
        '__gads': 'ID=f90f9d630b374c2b-22aacc5d79c70059:T=1618919629:RT=1618919629:S=ALNI_MbSYhj29OjZKEP46BUdA2FSpiIdrw',
        'viewed': '24708143',
        'gr_user_id': 'ac336a7c-b47a-47e4-89dc-280773eecf1d',
        '__utmc': '30149280',
        'll': '118249',
        '__yadk_uid': 'OJp3CUPu2A6j4rm481uKz27j2BoEvTBk',
        '_vwo_uuid_v2': 'DF6FC581B51FE32C0895065416B3A81F3|a9220bc80393fc18613e8207f46a58de',
        'UM_distinctid': '17902e0bfcc821-0ac0281db7db1a-21722040-58abc-17902e0bfcda7',
        'Hm_lvt_19fc7b106453f97b6a84d64302f21a04': '1619250954',
        '_ga': 'GA1.2.1002912388.1618919626',
        '_gid': 'GA1.2.2065911595.1619250955',
        'bid': 'f03tMCwrQ_U',
        'ct': 'y',
        'Hm_lpvt_19fc7b106453f97b6a84d64302f21a04': '1619252147',
        '_ck_desktop_mode': '1',
        'vmode': 'pc',
        '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1619271666%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D3punFryoNTgp2CfSZWoY1eB7Z-sYFYBWmi5I8Vtm_YmFeVmAfC4J9rpFtecOtKS9%26wd%3D%26eqid%3Dc10b09e2000d74450000000360841ff1%22%5D',
        '_pk_ses.100001.4cf6': '*',
        '__utma': '30149280.1002912388.1618919626.1619257349.1619271666.5',
        '__utmb': '30149280.0.10.1619271666',
        '__utmz': '30149280.1619271666.5.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        'ap_v': '0,6.0',
        '_pk_id.100001.4cf6': 'da4c9dd10b814fea.1619250659.3.1619272028.1619257352.',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    params = (
        ('start', a),
    )
    try:
        # 爬取网站源码并进行异常处理
        response = requests.get(url1, headers=headers, params=params, cookies=cookies)

        # NB. Original query string below. It seems impossible to parse and
        # reproduce query strings 100% accurately so the one below is given
        # in case the reproduced version is not "correct".
        # response = requests.get('https://movie.douban.com/top250?start=0', headers=headers, cookies=cookies)

        # 获取并解码html

        html = response.content.decode()


    except urllib.error.URLError as x:
        if hasattr(x, 'code'):
            print(x.code, )
        if hasattr(x, 'reason'):
            print(x.reason, )
    return html


if __name__ == '__main__':
    url = 'https://movie.douban.com/top250?start='
    reptile_silisili(url)
