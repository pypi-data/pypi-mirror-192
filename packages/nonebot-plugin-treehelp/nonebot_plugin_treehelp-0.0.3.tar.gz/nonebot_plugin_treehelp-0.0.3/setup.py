# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_treehelp']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-beta.5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-treehelp',
    'version': '0.0.3',
    'description': '适用于 Nonebot2 的树形帮助插件',
    'long_description': '<!-- markdownlint-disable MD033 MD036 MD041 -->\n\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# NoneBot Plugin TreeHelp\n\n_✨ NoneBot 树形帮助插件 ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/he0119/nonebot-plugin-treehelp/main/LICENSE">\n    <img src="https://img.shields.io/github/license/he0119/nonebot-plugin-treehelp.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-treehelp">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-treehelp.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n  <a href="https://codecov.io/gh/he0119/nonebot-plugin-treehelp">\n    <img src="https://codecov.io/gh/he0119/nonebot-plugin-treehelp/branch/main/graph/badge.svg?token=jd5ufc1alv"/>\n  </a>\n  <a href="https://jq.qq.com/?_wv=1027&k=7zQUpiGp">\n    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-730374631-orange?style=flat-square" alt="QQ Chat Group">\n  </a>\n</p>\n\n## 简介\n\n使用插件元数据获取插件信息，并通过插件与子插件的组织形式，来区分插件的多种功能。\n\n树形帮助插件，最重要的功能当然是显示插件树！\n\n发送 `/help --tree`，你将获得如下帮助：\n\n```text\n插件：\n帮助 # 获取插件帮助信息\n测试 # 一个测试插件\n├── 复杂功能 # 测试插件复杂子插件\n│   └── 二级功能 # 测试插件二级插件\n└── 简单功能 # 测试插件简单子插件\n```\n\n## 使用方式\n\n加载插件后发送 `/help` 或 `/help --help` 获取具体用法。\n\n插件与子插件写法可参考 [示例插件](./tests/plugins/tree/)。\n\n## 配置项\n\n配置方式：直接在 `NoneBot` 全局配置文件中添加以下配置项即可。\n\n暂时还没有可配置的东西。\n\n## 计划\n\n- [ ] 支持输出插件版本\n- [x] 支持输出插件树\n- [ ] 支持输出插件内的命令名称\n',
    'author': 'hemengyang',
    'author_email': 'hmy0119@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/he0119/nonebot-plugin-treehelp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
