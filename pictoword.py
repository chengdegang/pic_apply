import base64
import requests
import os
import cv2

"""
传入图片路径，输出其中的文字（str）
"""
def run_pic(picpath):
    # 获取token
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
           'client_id=C3nVkGT1G0iwV6whSpvPHB1b&client_secret=XwWphXeULnsFWxvkaQnfg1H8vR5ITnGi'
    response = requests.get(host)
    if response:
        # print(response.json())
        access_token = str(response.json()['access_token'])
        # print(access_token)
    #发送请求
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    with open(picpath, 'rb') as f:
        #判断img是否大于xx像素

        img = base64.b64encode(f.read())
    params = {"image": img}
    access_token = access_token
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        words = response.json()['words_result']
        # print(words)
        wordsdeal = '' #处理后的文字
        for i in range(len(response.json()['words_result'])):
            wordsdeal = wordsdeal + words[i]['words'] + '\n'
            # print(words[i])
        print(wordsdeal)
    return wordsdeal

def size_change(picpath):
    img = cv2.imread(picpath)
    print(img.shape)#打印图片大小

"""
遍历指定路径下的所有文件，并找出png、jpg的文件写入列表中返回
"""
def dpath(file,jpg=False,gif=False):
    path = []
    for root, dirs, files in os.walk(file):
        for file in files:
            if '.png' in file:
                print(os.path.join(root,file))
                path.append(os.path.join(root,file))
            if jpg == True:
                if '.jpg' in file:
                    print(os.path.join(root, file))
                    path.append(os.path.join(root, file))
            if gif == True:
                if '.jpg' in file:
                    print(os.path.join(root, file))
                    path.append(os.path.join(root, file))

    print(path)
    return path

if __name__ == '__main__':
    # dpath('/Users/jackrechard/PycharmProjects/pic_apply/',jpg=False)
    run_pic('ces3.png')
    # size_change('ces.png')


