# -*- coding:utf-8 -*-
import glob
import os
import cv2

def process_video(video_path, save_path, interval=10, need_rotate=False):
    """
    :param video_path: 视频所在文件夹路径。脚本会读取该路线下所有的文件，包括子文件夹中的文件
    :param save_path:生成的图片的保存路径。如果路径不存在，脚本会自动创建
    :param interval:表示每隔多少帧选取一张图片
    :param need_rotate:图片是否需要旋转，值为True / False。手机竖屏拍摄的视频为True（需要旋转），手机横屏拍摄的视频为False（不需要旋转）
    :return:
    """
    #返回当前路径下的所有匹配
    video_data = glob.glob(f"{video_path}/*.*", recursive=True)
    print(video_data)
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

def word():
    words0 = [{'words': 'ARKit识别平面缺陷'}, {'words': 'ARKit识别扫描尽管在这个过程当中,经常会产生可观的准确度,从而让AR的体验更加真实。然而,它严重依赖于设备物理环境的相关细节,而这些细节'}, {'words': '并不总是一致,有些时候也难以实时测量,这也就导致这些物理细节往往都会存在某种程度的错误。要建立高品质的AR体验,那么请注意下述这些注意'}, {'words': '事项和提示'}, {'words': '1基于可见的照明条件来设计AR场景。全局追踪涉及到了图像分析的相关內容,因此就需要我们提供清晰的图像。如果摄像头没有办法看到相关的物理细'}, {'words': '节,比如说摄像头拍到的是一面空空如也的墙壁,或者场景的光线实在太暗的话,那么全局追踪的质量就会大大降低。'}, {'words': '2根据追踪质量的相关信息来给用户进行反馈提示。全局追踪会将图像分析与设备的动作模式关联起来。如果设备正在移动的话,那么 ARKit就可以更好'}, {'words': '地对场景进行建模,这样即便设备只是略微晃动,也不会影响追踪质量。但是一旦用户的动作过多、过快或者晃动过于激烈,就会导致图像变得模糊,或'}, {'words': '者导致视频帧中要追踪的特征之间的距离过大,从而致使追踪质量的降低。 ARCamera类能够提供追踪状态,此外还能提供导致该状态岀现的相关原因'}, {'words': '您可以在ω上展示这些信息,告诉用户如何解决追踪质量低这个问题。'}]
    words = [{'words': '微信'}, {'words': 'c'}, {'words': '企业微信'}, {'words': '网易邮箱大师'}]
    words1 = {'words': '微信'}
    print(words1['words'])
    print(str(words))
    words = list(str(words))
    allwords = ''
    print(words)
    # for i in range(int(len(words))):
    #     allwords = allwords + words[i]['words'] + '\n'
    #     # print(words[i]['words'])
    # print(allwords)


video_path = '/Users/jackrechard/PycharmProjects/pic_apply/oridata'
interval = 10
need_rotate = True

if __name__ == '__main__':
    #处理视频的部分
    # save_path = f'{video_path}/restemp'
    # process_video(video_path, save_path, int(interval), need_rotate)
    word()