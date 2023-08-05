# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

modules = \
['gartic_room']
install_requires = \
['ayaka[nb2ob11,playwright]>=0.0.4.2,<0.0.5.0']

extras_require = \
{'htmlrender': ['nonebot_plugin_htmlrender>=0.2.0.3']}

setup_kwargs = {
    'name': 'gartic-room',
    'version': '0.0.2',
    'description': '你画我猜组队',
    'long_description': '# 你画我猜组队\n\n安装：`pip install gartic_room[htmlrender]`\n\n命令：`你画我猜`\n\n功能：自动创建gartic房间，主题为综合，将房间链接发送到群聊\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/gartic_room',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
