# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：example.py

import yaml


def test_yaml_to():
    with open("./test.yaml", "rb") as f:
        fb = f.read()
        yaml_fb = yaml.safe_load(fb)
        print(yaml_fb)


"""第一天结束之后，我们总结"""
"""第二天结束之后，我们总结"""
"""第三天结束之后，我们总结"""
