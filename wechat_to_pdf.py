import requests
import json
import time
import pdfkit


def parse(index, biz, uin, key):
    # url前缀
    url = "https://mp.weixin.qq.com/mp/profile_ext"

    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 "
                      "Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.901.400 "
                      "QQBrowser/9.0.2524.400",
    }

    proxies = {
        'https': None,
        'http': None,
    }

    # 重要参数
    param = {
        'action': 'getmsg',
        '__biz': biz,
        'f': 'json',
        'offset': index * 10,
        'count': '10',
        'is_ok': '1',
        'scene': '124',
        'uin': uin,
        'key': key,
        'wxtoken': '',
        'x5': '0',
    }

    # 发送请求，获取响应
    response = requests.get(url, headers=headers, params=param, proxies=proxies)
    response_dict = response.json()

    print(response_dict)

    next_offset = response_dict['next_offset']
    can_msg_continue = response_dict['can_msg_continue']

    general_msg_list = response_dict['general_msg_list']
    data_list = json.loads(general_msg_list)['list']

    # print(data_list)

    for data in data_list:
        try:
            # 文章发布时间
            datetime = data['comm_msg_info']['datetime']
            date = time.strftime('%Y-%m-%d', time.localtime(datetime))

            msg_info = data['app_msg_ext_info']

            # 文章标题
            title = msg_info['title']

            # 文章链接
            url = msg_info['content_url']

            # 自己定义存储路径（绝对路径）
            pdfkit.from_url(url, 'C:/Users/admin/Desktop/wechat_to_pdf/' + date + title + '.pdf')

            print(title + date + '成功')
            print('-' * 20)

        except:
            print("不是图文消息")

    if can_msg_continue == 1:
        return True
    else:
        print('爬取完毕')
        return False


if __name__ == '__main__':

    index = 0

    # 这三个参数要换成自己的
    biz = 'MzUyOTA2MjA2NQ=='
    uin = 'MTQzOTAxMDg4MA=='
    key = '7865e1e5a7ba115ef0d91d71114266468e9cdcaf5c8bcea269a4d17c1a08b6b803b401375e14e84265308f9817405ec6caee17e' \
          'cf3479252657c295a1073dcfde564bff81e7ee9d6a01fd428ff27176b'
    while 1:

        result = parse(index, biz, uin, key)

        time.sleep(2)
        index += 1

        if not result:
            break
