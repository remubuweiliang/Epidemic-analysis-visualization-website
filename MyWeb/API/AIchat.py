import requests


def get_data(text):
    # 请求思知机器人API所需要的一些信息
    data = {
        "appid": "c70bd1d89ff502540d7ae2b951e80719",
        "userid": "4Ee1yHiK",
        "spoken": text,
    }
    return data


def get_answer(text):
    # 获取思知机器人的回复信息
    data = get_data(text)
    url = 'https://api.ownthink.com/bot'  # API接口
    response = requests.post(url=url, data=data)  # , headers=headers)
    response.encoding = 'utf-8'
    result = response.json()
    res = result['data']['info']['text']
    # print(res)
    return res


# if __name__ == "__main__":
#     answer = get_answer("哈哈哈哈哈哈哈")  # 收到信息时，调用思知机器人并获取机器人的回复信息
