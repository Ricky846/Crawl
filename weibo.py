import requests
import json
import os
from hashlib import md5
from urllib.parse import urlencode
from requests.exceptions import RequestException
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'cookie': 'SINAGLOBAL=3658141141929.736.1583335926908; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFXnnELYwLIxvxsLSphMmZN5JpX5KzhUgL.FoepS05E1Kqpeoz2dJLoI74kHg4bMJHyIc8bdsHkS5tt; wvr=6; login_sid_t=972d21c625cbdae85b32a94929c4b1ed; cross_origin_proto=SSL; _s_tentry=login.sina.com.cn; Apache=4388980327761.9243.1583631079745; ULV=1583631079751:3:3:1:4388980327761.9243.1583631079745:1583592135295; SUB=_2A25zYDsoDeRhGeVP7FIT-SjNyT6IHXVQFCvgrDV8PUNbmtAfLUbRkW9NTO1olw9qOY_qewhIYOxDUfSJAZ92WyxK; SUHB=0D-V2jqciGzQAT; ALF=1615167223; SSOLoginState=1583631224; UOR=www.moe.gov.cn,widget.weibo.com,login.sina.com.cn; webim_unReadCount=%7B%22time%22%3A1583631257408%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; WBStorage=42212210b087ca50|undefined'

}
base_url = 'https://photo.weibo.com/photos/get_all?'


def get_page(timestamp, page):
    Query_params = {
        'uid': '5644764907',  # 所爬取微博博主账户，需通过检查元素获得
        'count': '30',
        'page': page,
        'type': '3',
        '__rnd': timestamp,
    }
    url = base_url + urlencode(Query_params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.text
            return result
        return None
    except RequestException:
        print('请求索引页出错')
        return None


def get_image(result):
    results = json.loads(result)
    results = results['data']
    for i in results['photo_list']:
        pics_path = i['pic_host'] + '/mw690/' + i['pic_name']
        download_image(pics_path)


def download_image(url):
    print('正在下载', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片错误', url)
        return None


def save_image(content):
    # os.getcwd()为返回到当前的根目录，{1}为用户在该根目录下所创建获取图片的文件夹，md5用来排除重复的图片
    file_path = '{0}/{1}/{2}.{3}'.format(os.getcwd(), '刘亦菲', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main():
    timestamp = int(round(time.time() * 1000))
    page = eval(input('请输入页数：'))
    for i in range(1, page + 1):
        result = get_page(timestamp, i)
        image = get_image(result)
        if image:
            print(image)


if __name__ == '__main__':
    main()
