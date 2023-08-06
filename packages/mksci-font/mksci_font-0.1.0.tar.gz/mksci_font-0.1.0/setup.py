# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mksci_font']

package_data = \
{'': ['*'], 'mksci_font': ['data/*']}

install_requires = \
['matplotlib>=3.7.0,<4.0.0']

setup_kwargs = {
    'name': 'mksci-font',
    'version': '0.1.0',
    'description': '',
    'long_description': '\nmksci-font\n==========\n\n`mksci-font` 用于方便地将 Matplotlib 支持中文字体允许您配置图形为“中文宋体、英文 Times New Roman”。\n\n## 安装\n\n使用喜欢的包管理工具安装：\n\n```bash\npip install mksci-font\n```\n\n使用方法\n----\n\n### 配置默认字体设置\n\n要为 Matplotlib 配置默认字体设置，可以使用 `config_font()` 函数。\n\npython\n\n```python\n# 同时还可以修改字号，以及其它任何 rcParams 支持的属性\nconfig_font({"font.size": 12})\n\n_, ax = plt.subplots(figsize=(4, 1))\nax.text(0.5, 0.5, msg, ha=\'center\', va=\'center\')\nplt.show();\n\n```\n\n![U73Adi](https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/U73Adi.jpg)\n\n### 针对做图函数修改\n\n对于返回`matplotlib.axes`的作图函数，可以简单使用 `@mksci_font` 装饰器，在修改字体的同时，可以将图中元素换成中文。\n\npython\n\n```python\nmsg = "让 Matplotlib 图件使用 \\n “中文宋体、英文 Times New Roman”"\nmapping_string = {\'Origin title\': \'替换后的标题\'}\n\n@mksci_font(mapping_string, ylabel="覆盖原Y轴标签")\ndef plot():\n    _, ax = plt.subplots(figsize=(4, 3))\n    ax.text(0.5, 0.6, "mksci-font 中文", ha=\'center\')\n    ax.text(0.5, 0.3, msg, ha=\'center\')\n    ax.set_ylabel("will be replaced...")  # will be replaced by \'中文\'\n    ax.set_xlabel("中文 & English & $TeX_{mode}$")\n    ax.set_title("Origin title")\n    return ax\n\n\nax = plot()\nshow()\n```\n\n![WbZq1I](https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/WbZq1I.jpg)\n\n### 更新现有图形的文本元素\n\n可以使用 `update_font()` 函数更新已有图像，使用方法与`@mksci_font`类似：\n\n```python\n_, ax = plt.subplots(figsize=(4, 3))\nax.text(0.5, 0.6, "mksci-font 中文", ha=\'center\')\nax.text(0.5, 0.3, msg, ha=\'center\')\nax.set_ylabel("will be replaced...")  # will be replaced by \'中文\'\nax.set_xlabel("中文 & English & $TeX_{mode}$")\nax.set_title("Origin title")\n\nmsg = "让 Matplotlib 图件使用 \\n “中文宋体、英文 Times New Roman”"\nmapping_string = {\'Origin title\': \'替换后的标题\'}\nupdate_font(ax, mapping_string, ylabel="覆盖原Y轴标签")\n```\n\n更多用法例子可以见[这个笔记本](tests/test_plot_jupyter.ipynb)\n\n许可证\n---\n\n本项目基于 MIT 许可证开源。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。\n\n关于作者\n---\n\n[Shuang Song](https://cv.songshgeo.com/), a scientist who also travels.\n\n<a href="https://www.buymeacoffee.com/USgxYspYW4" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>\n',
    'author': 'Shuang Song',
    'author_email': 'songshgeo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
