# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

modules = \
['gartic_room']
install_requires = \
['ayaka[nb2ob11]>=0.0.4.2b5', 'nonebot_plugin_htmlrender>=0.2.0.3']

setup_kwargs = {
    'name': 'gartic-room',
    'version': '0.0.1',
    'description': '你画我猜组队',
    'long_description': '# 你画我猜组队\n\n安装 `pip install gartic_room`\n\n很简单的功能\n\n自动创建gartic房间，主题为综合，将链接发送到群聊\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
