import cv2
import os
import glob

def process_video(video_path, save_path, interval=10, need_rotate=True):
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
    save_path = '/Users/jackrechard/PycharmProjects/pic_apply/result1'
    interval = 10
    need_rotate = True
    process_video(video_path, save_path, interval, need_rotate)
