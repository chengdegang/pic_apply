import cv2
import os
import glob

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
                        frame = cv2.rotate(frame, 0)
                    cv2.imwrite(file_name, frame)
            else:
                break

        cap.release()
        cv2.destroyAllWindows()
    print("done")


if __name__ == '__main__':
    video_path = '/Users/jackrechard/PycharmProjects/pic_apply/oridata'
    save_path = f'{video_path}/restemp'
    interval = 10
    need_rotate = True
    process_video(video_path, save_path, interval, need_rotate)
    need_change = True
    if need_change:
        changesize(save_path)
