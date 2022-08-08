# coding=utf-8

import time
from datetime import datetime
import configparser

import pyautogui


# 是否打印控制台日志
print_log = True

name = 'img/name.png'
password = 'img/password.png'
login = 'img/login.png'

name1 = 'img/name1.png'
password1 = 'img/password1.png'
login1 = 'img/login1.png'

zhong = 'img/zhong.png'

input_offset = 120
name_position = None
password_position = None
login_position = None

check_seconds = 3.0

name_text = None
password_text = None


def load_config():
    global name_text, password_text
    cf = configparser.ConfigParser()
    cf.read('config.ini', encoding='utf-8')
    if cf.has_section('base'):
        if cf.has_option('base', 'name'):
            name_text = cf.get('base', 'name')
        if cf.has_option('base', 'password'):
            password_text = cf.get('base', 'password')


def check_has_window():
    global name_position, password_position, login_position
    name_position = get_img_center_location(name)
    if name_position is None:
        name_position = get_img_center_location(name1)
    password_position = get_img_center_location(password)
    if password_position is None:
        password_position = get_img_center_location(password1)
    login_position = get_img_center_location(login)
    if login_position is None:
        login_position = get_img_center_location(login1)
    return name_position is not None and password_position is not None and login_position is not None


def check_input():
    zhong_position = get_img_center_location(zhong)
    if zhong_position is not None:
        pyautogui.hotkey("ctrl", "space")


def type_name():
    pyautogui.moveTo(name_position.x + input_offset, name_position.y, duration=0.1)
    pyautogui.leftClick()
    check_input()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.typewrite(name_text)


def type_password():
    pyautogui.moveTo(password_position.x + input_offset, password_position.y, duration=0.1)
    pyautogui.leftClick()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.typewrite(password_text)


def click_login():
    click_left(login_position)


# 点击左键
def click_left(position):
    pyautogui.click(position.x, position.y, clicks=1, interval=0.1, duration=0.1, button="left")


# 根据图片路径获取图片在屏幕中的中心位置坐标
# 其中的confidence根据官方文档：
# The optional confidence keyword argument specifies the accuracy with
# which the function should locate the image on screen.
# This is helpful in case the function is not able to locate an image due to negligible pixel differences:
# Note: You need to have OpenCV installed for the confidence keyword to work.
# 也就是配置像素差异导致的识别精度变化 需要本机安装OpenCV，本机截图的话估计可以去掉这个参数
def get_img_center_location(img_path):
    return pyautogui.locateCenterOnScreen(img_path, confidence=0.9)


# 打印开关
def trace(message):
    if print_log:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + str(message))


if __name__ == '__main__':
    load_config()
    while True:
        if check_has_window():
            trace('dooray已打开')
            type_name()
            type_password()
            click_login()
            break
        time.sleep(check_seconds)
        trace("等待" + str(check_seconds) + "秒\n")
