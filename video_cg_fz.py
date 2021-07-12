#   Author      : qinyu

import cv2
import threading
import glob
import os
import numpy as np
import shutil

def mkdir(path):
    """
    if the path exists, this function will remove it at first and create the new one then
    :param path:
    :return:
    """
    if os.path.exists(path):
        shutil.rmtree(path)

    if not os.path.exists(path):
        os.mkdir(path)

def video2frame(data_dir, interval, stage, is_data_aug=True, **kwargs):
    """
    split the video to images
    :param data_dir: list, list of cls data dir
    :param stage: train or test
    :param data_dir: str, path to data dir
    :param interval:　the frames
    :param is_data_aug: bool, whether or not data augment
    :return:
    """

    def threads_process_video(thread_name_inner, target_dir_inner):
        video_lst = glob.glob(target_dir_inner + "/*")
        # load video file with list
        video_lst = list(filter(lambda x: ".mp4" in x or ".MP4" in x, video_lst))

        if len(video_lst) == 0:
            return
        # create each video dirs based on the name
        # each video: ..../video_name.mp4
        print("Launch thread: {}".format(thread_name_inner))
        for each_video_path in video_lst:
            video_name = os.path.basename(os.path.splitext(each_video_path)[0])
            # video_dir = os.path.join(os.path.dirname(each_video_path), "samples_data", video_name)
            video_dir = os.path.join(os.path.dirname(each_video_path), video_name)
            mkdir(video_dir)

            # create src and data_aug dir for saving original img and the data augmentation
            # src_dir_name = "src_images"
            # src_dir = os.path.join(video_dir, src_dir_name)

            # data_aug_dir_name = "aug_images"
            # data_aug_dir = os.path.join(video_dir, data_aug_dir_name)

            # mkdir(src_dir)
            # if is_data_aug:
            #     mkdir(data_aug_dir)

            # read the video
            cap = cv2.VideoCapture(each_video_path)
            frame_index = 0
            frame_count = interval
            if cap.isOpened():
                success = True
            else:
                success = False
                print("read failed!")
            try:
                while success:
                    success, frame = cap.read()

                    # todo(qinyu) This line of code will be deleted
                    # if video_name.endswith("540960"):
                    #     pass
                    # else:
                    #     frame = np.rot90(frame, -1)
                    frame_width = frame.shape[1]
                    frame_height = frame.shape[0]
                    if frame_index % interval == 0:
                        resize_frame = cv2.resize(
                            frame, (frame_width, frame_height),
                            interpolation=cv2.INTER_AREA)

                        # cropped_frame = frame[120:840]
                        image_saved_path = video_dir + "/" + "{:0>5d}.jpg".format(frame_count)
                        cv2.imwrite(image_saved_path, resize_frame)
                        # data augmentation
                        if is_data_aug:
                            image_name = os.path.basename(os.path.splitext(image_saved_path)[0])
                            # data_augmentation(resize_frame, data_aug_dir,image_name=image_name, **kwargs)
                        frame_count += interval
                    frame_index += 1
            except Exception:
                continue

        print("thread: {} complete".format(thread_name_inner))

    thread_indice_lst = [i for i in range(len(data_dir))]
    target_dir_lst = [dir_path for dir_path in data_dir]
    threads = []
    print("process the {} image".format(stage))
    for index in thread_indice_lst:
        target_dir = target_dir_lst[index]
        thread_name = os.path.basename(target_dir)
        t = threading.Thread(target=threads_process_video, args=(thread_name, target_dir))
        # launch thread
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def data_augmentation(img, outputdir, image_name, **kwargs):
    """
    the data augmentation: constrast
    :param image_name: str, the image to be saved with such name
    :param outputdir: str, the destination path
    :param img: ndarray
    :return:
    """
    src = img.copy()
    # constrast = True
    # gaussian_nose = True
    # mirror = True
    # mean_filter = True
    # rotate = True

    outputpath = os.path.join(outputdir, image_name)

    def constrast_img(src_, alpha_, b_, output):
        """
        constrast images
        :param output: str, output path
        :param src_: the original images
        :param alpha_: weights
        :param b_:bias
        :return:
        """
        rows, cols, channels = img.shape
        blank = np.zeros([rows, cols, channels], img.dtype)
        dst = cv2.addWeighted(src_, alpha_, blank, 1 - alpha_, b_)
        cv2.imwrite(output + "_1.jpg", dst)

    def gaussian_nose_img(src_, mean_, var_, output_):
        """
        add noise to original img
        :param output_:
        :param src_:
        :param mean_: mean value
        :param var_: variance
        :return:
        """
        image = np.array(src_ / 255, dtype=float)
        noise = np.random.normal(mean_, var_ ** 0.5, image.shape)
        dst = image + noise
        if dst.min() < 0:
            low_clip = -1.
        else:
            low_clip = 0.
        dst = np.clip(dst, low_clip, 1.0)
        dst = np.uint8(dst * 255)
        cv2.imwrite(output_ + "_2.jpg", dst)

    def mirror_img(src_, output):
        dst = cv2.flip(src_, 1)
        cv2.imwrite(output + "_3.jpg", dst)

    def mean_filter_img(src_, output):
        dst = cv2.blur(src_, (3, 3))
        cv2.imwrite(output + "_4.jpg", dst)

    def rotate_img(src_, output):
        dst = np.rot90(src_, k=1)
        cv2.imwrite(output + "_5.jpg", dst)
        dst = np.rot90(src_, k=2)
        cv2.imwrite(output + "_6.jpg", dst)
        dst = np.rot90(src_, k=3)
        cv2.imwrite(output + "_7.jpg", dst)

    if kwargs["contrast"]:
        alpha = 1.3
        b = 3
        constrast_img(src, alpha, b, outputpath)

    if kwargs["gaussian_nose"]:
        mean = 0
        var = 0.001
        gaussian_nose_img(src, mean, var, outputpath)

    if kwargs["mirror"]:
        mirror_img(src, outputpath)

    if kwargs["mean_filter"]:
        mean_filter_img(src, outputpath)

    if kwargs["rotate"]:
        rotate_img(src, outputpath)


if __name__ == '__main__':
    data_aug_kwargs = {
        "contrast": False,
        "gaussian_nose": False,
        "mirror": False,
        "mean_filter": False,
        "rotate": False
    }

    data_dir = ['/Users/jackrechard/PycharmProjects/pic_apply/oridata']
    # data_cls_dir = [
    #     '{}/{}'.format(data_dir, ''),
    #     '{}/{}'.format(data_dir, 'others'),
    #
    # ]
    video2frame(data_dir, 10, "train", is_data_aug=False, **data_aug_kwargs)


    
