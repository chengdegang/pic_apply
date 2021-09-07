import glob
import os
import time
import cv2
import requests
import base64

def changesize(file):
    """
    输入路径在输入路径下创建result文件夹存放结果，将图片统一转换成指定像素大小
    """
    imagedirs = []
    resultdir = f"{'/'.join(file.split('/')[:-1])}/result/"
    # print(resultdir)
    if os.path.exists(resultdir) == True:
        print(f'写入路径 {resultdir} 已存在')
    else:
        os.makedirs(resultdir)
        # 找到指定路径下的所有图片文件
        for root, dirs, files in os.walk(file):
            for f in files:
                if '.jpg' in f:
                    # print(f)
                    # 打印文件路径
                    # print(os.path.join(root, f))
                    imagedirs.append(os.path.join(root, f))
        # 遍历所有图片并转换至当前路径
        for i in range(len(imagedirs)):
            image = cv2.imread(imagedirs[i])
            # 获取图片的名称
            name = imagedirs[i].split('/')[-1].split('.')[0]
            # print(name)
            change_image = cv2.resize(image, (640, 360))
            cv2.imwrite(f'{resultdir}{name}_cg.jpg', change_image)
            # print(imagedirs[i])
        print(f'已处理 {len(imagedirs)} 张图片')
        print(f'生成的路径为: {resultdir}')

def process_video(video_path, save_path, interval=10, need_rotate=False):
    """
    :param video_path: 视频所在文件夹路径。脚本会读取该路线下所有的文件，包括子文件夹中的文件
    :param save_path:生成的图片的保存路径。如果路径不存在，脚本会自动创建
    :param interval:表示每隔多少帧选取一张图片
    :param need_rotate:图片是否需要旋转，值为True / False。手机竖屏拍摄的视频为True（需要旋转），手机横屏拍摄的视频为False（不需要旋转）
    :return:
    """
    #返回所有匹配的路径列表
    video_data = glob.glob(f"{video_path}/**/*.*", recursive=True)
    # print(video_data)
    #如果不存在savepath，直接创建路径
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    count = 0

    for video in video_data:
        video_name = os.path.splitext(os.path.basename(video))[0]
        cap = cv2.VideoCapture(video)

        while (cap.isOpened()):
            ret, frame = cap.read()
            # cv2.imshow('frame', frame)
            # cv2.waitKey(0)
            count += 1

            if frame is not None:
                if count % interval == 0:
                    file_name = os.path.join(save_path, video_name + '_' + str(count) + '.jpg')
                    if need_rotate:
                        frame = cv2.rotate(frame, 0) #顺时针旋转90度
                        frame = cv2.rotate(frame, 0)
                        frame = cv2.rotate(frame, 0)
                    cv2.imwrite(file_name, frame)
            else:
                break

        cap.release()
        cv2.destroyAllWindows()
    print("done")

def post_cloud(ip,url,protobufEncodingData,imageEncodingData):
    url = f'https://{ip}{url}'
    # 入参
    data = {
    "alg": {
        "protobufEncodingData": f"{protobufEncodingData}",
        "imageEncodingData": f"{imageEncodingData}"
    }
}
    req = requests.post(url, json=data)
    # print(req.json()['msg']) #调试用
    # print(req.json()) #调试用
    return req.json()

def protobufEncodingData_deal():
    1
    # 暂不需要处理该入参，写死即可


def del_data():
    """
    测试数据删除，仅保留输入路径的文件数据
    """
    os.remove(os.path.join(video_path,'restemp'))
    os.remove(os.path.join(video_path,'result'))
    print('删除完成')

def imageEncodingData_deal(file):
    """
    遍历指定路径下的所有图片，并转换成base64
    """
    imagedirs = []
    base64_datas = []
    if os.path.exists(file) == False:
        print("该路径不存在")
    #查找路径下所有的jpg文件
    for root, dirs, files in os.walk(file):
        for f in files:
            if '.jpg' in f:
                # print(f)
                #打印文件路径
                # print(os.path.join(root, f))
                imagedirs.append(os.path.join(root, f))
    if len(imagedirs) == 0:
        print("当前路径下.jpg文件为0")

    # print(imagedirs)
    for i in range(len(imagedirs)):
        # print(i)
        with open(f'{imagedirs[i]}', "rb") as f:  # 转为二进制格式
            base64_data = str(base64.b64encode(f.read())) # 使用base64进行加密
            base64_data = f'data:image/jpg;base64,{base64_data[2:]}'
            base64_datas.append(base64_data)
            # print(f'data:image/jpg;base64,{base64_data[2:]}')
    # print(base64_datas[0])
    return base64_datas

video_path = '/Users/jackrechard/PycharmProjects/pic_apply/oridata/video'
# video_path = '/Users/jackrechard/PycharmProjects/pic_apply/oridata/w'
ip = 'reloc-gw.easexr.com'
url = '/api/alg/cloud/aw/reloc/proxy?routeApp=parkc&map=c6'
# url = '/api/alg/cloud/aw/reloc/proxy?routeApp=wh.jgs&map=entry'
interval = 10
need_rotate = True
need_change = True

# video_path = os.environ['video_path']
# ip = os.environ['ip']
# url = os.environ['furl']
# interval = os.environ['interval']
# need_rotate = os.environ['need_rotate']
# need_change = os.environ['need_change']

if __name__ == '__main__':
    #处理视频的部分
    save_path = f'{video_path}/restemp'
    process_video(video_path, save_path, int(interval), need_rotate)
    if need_change:
        changesize(save_path)

    #请求响应处理部分
    result_suc = 0
    result_fail = 0
    result_wrong = 0
    protobufEncodingData =['CNH30AkQwczLl/rvJxj///////////8BIlQKABABGQAAACDNv39AIQAAACDNv39AKQAAAODg6nNAMQAAAACXXWZAOQAAAAAAAAAAQQAAAAAAAAAASQAAAAAAAAAAUQAAAAAAAAAAWIAFYOgCaBAqVAoJdGVzdHNjZW5lEAEYACIbGQAAAAAAAPA/GQAAAAAAAABAGQAAAAAAAAhAKiQZAAAAAAAAAAAZAAAAAAAAAAAZAAAAAAAAAAAZAAAAAAAA8D8wGDCQAg==']
    imageEncodingData = imageEncodingData_deal(f'{video_path}/result')

    for i in range(len(imageEncodingData)):
    # for i in range(5):
        data1 = post_cloud(ip=ip, url=url,
                           protobufEncodingData=protobufEncodingData[0], imageEncodingData=imageEncodingData[i])
        try:
            algcode = str(data1['result']['algCode'])
            if algcode == '1':
                result_suc = result_suc + 1
            elif '16' in algcode:
                result_fail = result_fail + 1
        except Exception:
            result_wrong = result_wrong + 1

    timenow = time.strftime("%Y_%m_%d %H:%M:%S", time.localtime())
    print(f'-----test data({timenow})-----')
    print(f'总共 {len(imageEncodingData)} 张图片')
    print(f'定位成功的次数是:{result_suc}  定位失败的次数是:{result_fail}  请求错误的次数是:{result_wrong}')
    sucbai = (result_suc/len(imageEncodingData))*100
    print(f"定位成功率为 { float('%.2f' % sucbai) }%")
    print(f'本次测试请求链接是：{ip}{url}')
    print(f'本次测试数据源路径是：{video_path}')

    """
    调试部分
    """




