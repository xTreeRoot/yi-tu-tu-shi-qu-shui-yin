import cv2
import numpy as np


def process_image(img_path):
    # 读入图片并将其转换为RGB格式
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    color = [2, 127, 255]
    range = 10
    # 定义需要查找的颜色和范围
    lower = np.array([color[0] - range, color[1] - range, color[2] - range])
    upper = np.array([color[0] + range, color[1] + range, color[2] + range])

    # 对图像进行阈值处理，并检查是否存在符合条件的像素
    mask = cv2.inRange(img, lower, upper)
    if np.sum(mask) > 0:
        print('图片中包含亿图图示LOGO颜色！')
    else:
        print('图片中包含亿图图示LOGO颜色！')
    # 对阈值化后的图像进行轮廓检测
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 筛选出符合条件的轮廓
    color_contours = []
    for contour in contours:
        # 提取轮廓内部像素
        mask_tmp = np.zeros(img.shape[:2], np.uint8)
        cv2.drawContours(mask_tmp, [contour], -1, 255, -1)
        pixel_values = img[mask_tmp == 255]
        # 计算像素的平均颜色
        mean_color = cv2.mean(pixel_values)

        if np.abs(mean_color[0] - color[0]) <= range and np.abs(mean_color[1] - color[1]) <= range and np.abs(
                mean_color[2] - color[2]) <= range:
            # 如果符合条件，则将其加入到目标列表中
            color_contours.append(contour)

    # 对符合条件的轮廓进行绘制
    for contour in contours:
        # 获取轮廓的外接矩形
        x, y, w, h = cv2.boundingRect(contour)
        if x >= 180 and x + w <= 350 and y >= 80 and y + h <= 300:  # 判断矩形是否在该区域内
            continue
            # 在原图上 绘制白色矩形，覆盖矩形内部
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), -1)

    # 拆分通道
    channels = cv2.split(img)
    # 遍历每个通道
    for i, channel in enumerate(channels):
        # 对 RGB 通道进行处理
        _, binary = cv2.threshold(channel, 200, 255, cv2.THRESH_BINARY)
        img[:, :, i] = cv2.bitwise_not(binary)
        print("处理图层" + str(i))

        # 将颜色层转换为单通道图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 对单通道图像进行二值化处理，将白色区域变成255，黑色区域变成0
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        # 取反，将白色变成0，黑色变成255
        binary = cv2.bitwise_not(binary)
        # 将二值化图像转换为带透明通道的三通道图片
        result = cv2.merge([binary, binary, binary])

    # 返回处理结果
    return result
