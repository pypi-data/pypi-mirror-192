# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_phlogo']

package_data = \
{'': ['*'], 'nonebot_plugin_phlogo': ['resource/*']}

install_requires = \
['Pillow>=8.3.1', 'nonebot2>=2.0.0-beta.1']

setup_kwargs = {
    'name': 'nonebot-plugin-phlogo',
    'version': '0.0.3',
    'description': '生成ph风格logo',
    'long_description': '# nonebot-plugin-phlogo\n\n生成ph风格logo\n\n![nb](docs/png.png)\n# 安装\n\n直接使用 `pip install nonebot-plugin-phlogo` 进行安装\n\n然后在 `bot.py` 中 写入 `nonebot.load_plugin("nonebot_plugin_phlogo")`\n\n# 指令\n\n`phlogo/pornhub/ph图标 [text1] [text2]`\n\n# 配置\n\n## 字体文件 可选 环境配置\n\n```\nPHLOGO_FONT = "./data/font.ttf"\n```\n\n- 使用 truetype 字体\n- 建议使用微软雅黑\n',
    'author': 'kexue',
    'author_email': 'x@kexue.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kexue-z/nonebot-plugin-phlogo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3',
}


setup(**setup_kwargs)
