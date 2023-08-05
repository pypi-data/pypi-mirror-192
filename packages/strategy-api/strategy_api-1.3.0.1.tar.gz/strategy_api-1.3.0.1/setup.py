#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Kevin
# @Time     : 2022/12/12

import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='strategy_api',
    version='1.3.0.1',
    author='Kevin',
    author_email='1782552261@qq.com',
    description='仓位查询 API 添加, 修改bug',
    long_description=long_description,
    url='https://gitee.com/Jason520deng/strategy_api',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

