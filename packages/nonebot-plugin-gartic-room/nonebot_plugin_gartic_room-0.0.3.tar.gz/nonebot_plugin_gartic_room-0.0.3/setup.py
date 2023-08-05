# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

modules = \
['gartic_room']
install_requires = \
['ayaka[nb2ob11,playwright]>=0.0.4.2,<0.0.5.0',
 'nonebot_plugin_htmlrender>=0.2.0.3']

setup_kwargs = {
    'name': 'nonebot-plugin-gartic-room',
    'version': '0.0.3',
    'description': '你画我猜组队',
    'long_description': '# 你画我猜组队\n\n安装：`pip install nonebot_plugin_gartic_room`\n\n命令：`你画我猜`\n\n功能：自动创建gartic房间，主题为综合，将房间链接发送到群聊\n\n配置：可在`data/你画我猜/config.json`中自定义启动命令\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/gartic_room',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
