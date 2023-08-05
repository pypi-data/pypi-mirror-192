
#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "stusystem",      #这里是pip项目发布的名称
    version = "0.0.2",  #版本号，数值大的会优先被pip
    keywords = ["pip", "stusystem"],			# 关键字
    description = "Vinceeeeee9 code",	# 描述
    long_description = "Vinceeeeee9 code",
    license = "MIT Licence",		# 许可证

    url = "https://github.com/BaobaoAndDabao/stusystem.git",     #项目相关文件地址，一般是github项目地址即可
    author = "Vinceeeeee9",			# 作者
    author_email = "wenzhihaosuot@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []          #这个项目依赖的第三方库
)
