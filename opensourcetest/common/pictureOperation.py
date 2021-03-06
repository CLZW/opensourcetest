#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : opensourcetest
@Time    : 2020/12/30 17:28
@Auth    : chineseluo
@Email   : 848257135@qq.com
@File    : pictureOperation.py
@IDE     : PyCharm
------------------------------------
"""
import logging
import time
import allure
from typing import Text
from opensourcetest.common.fileOperation import FileOption


def screen_picture(driver) -> Text:
    logging.info("Screenshot operation in progress!")
    picture_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    file_path = "Report/picture"
    file_name = picture_time + ".png"
    FileOption.file_mkdir(file_path)
    res = driver.get_screenshot_as_file(file_path + '/' + file_name)
    picture_url = file_path + '/' + file_name
    try:
        allure.attach.file(picture_url, attachment_type=allure.attachment_type.PNG)
        logging.info(f"The screenshot is successful. The photo address is:{picture_url}")
    except Exception as e:
        logging.error(f"Screenshot failed,The error message is:{e}")
    finally:
        return picture_url
