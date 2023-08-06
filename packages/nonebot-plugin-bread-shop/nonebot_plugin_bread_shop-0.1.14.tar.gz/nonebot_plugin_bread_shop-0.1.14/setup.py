# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_bread_shop']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0', 'nonebot2>=2.0.0-beta.2,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-bread-shop',
    'version': '0.1.14',
    'description': 'nobebot2面包店插件',
    'long_description': '# nonebot-plugin-bread-shop\n\n![OSCS Status](https://www.oscs1024.com/platform/badge/Mai-icy/nonebot-plugin-bread-shop.svg?size=small)\n[![VERSION](https://img.shields.io/pypi/v/nonebot-plugin-bread-shop)](https://pypi.org/project/nonebot-plugin-bread-shop/)\n![GitHub license](https://img.shields.io/badge/python-3.7+-blue.svg)\n[![GitHub license](https://img.shields.io/github/license/Mai-icy/nonebot-plugin-bread-shop)](https://github.com/Mai-icy/nonebot-plugin-bread-shop/blob/main/LICENSE)\n![Lines of code](https://img.shields.io/tokei/lines/github/Mai-icy/nonebot-plugin-bread-shop)\n\n\n---\n\n\n## ⚠️警告须知！\n\n本插件不适宜用于群人员较多的群，经过测试，本功能具有极大上瘾性，容易造成bot刷屏，影响正常聊天！\n\n## 📄介绍\n\n面包小游戏，用户可以通过“买”，“吃”，“抢”，“送”，”猜拳“操作来获取面包和使用面包。\n\n将会记录所有用户的面包数据进行排行\n\n所有的操作都可能产生特殊面包事件哦！\n\n一起来买面包吧！\n\n> 注：**面包数据库一个群一个，排行均属于群内排行，不同群所有数据不相干。**\n\n## 💿安装\n- 使用 nb-cli\n\n```shell\nnb plugin install nonebot-plugin-bread-shop\n```\n\n- 使用 pip\n\n```shell\npip install nonebot-plugin-bread-shop\n```\n\n## 🤔使用\n\n| 指令 | 说明 | 其它形式 |\n|:-----:|:----:|:----:|\n| 买面包 | 购买随机数量面包 |buy，🍞|\n| 啃面包 | 吃随机数量面包 |eat，🍞🍞，吃面包|\n| 抢面包 + @指定用户 | 抢指定用户随机数量面包 |rob，🍞🍞🍞|\n| 送面包 + @指定用户 | 送指定用户随机数量面包 |give，送|\n| 查看面包 + @指定用户 | 查看指定用户的面包数据 |check，偷看面包，查看面包|\n| 面包记录 + @指定用户 | 查看指定用户的操作次数 |logb，记录|\n| 面包记录 + “买吃抢赠送猜拳” | 查看操作次数最多的人 |logb，记录|\n| 赌面包 + “石头剪刀布” | 和bot进行猜拳赌随机数量面包 |bet，面包猜拳|\n| 面包帮助 | 送指定用户随机数量面包 |breadhelp，helpb|\n| 面包排行 | 发送面包店操作指南（可加查询范围） |breadtop，面包排名|\n\n## ⚙️自定义配置\n\n**配置方式**：请在 `NoneBot` 全局配置文件中添加以下配置项即可。\n\n**参数说明**：\n\n**bread_thing**：可修改默认的“面包”改为其他物品例如： “炸鸡”，“蛋糕”等等（全局）\n\n**special_thing_group** ：分群设置物品例如：{"群号": "炸鸡"}\n\n> 可设置主次词，主次物品词bot将以主物品词进行回复，次物品词只用于触发指令，主关键词为列表第一个元素，次关键词可多个 示例：{"群号": ["炸鸡", "面包", "蛋糕"]}\n\n**global_bread**：面包全局开关\n\n**black_bread_groups**：黑名单\n\n**white_bread_groups**：白名单\n\n**level_bread_num**：修改升级一级所需要吃的面包数量，默认为10\n\n(注意：等级不被数据库记录数据库只记录已经吃了的数量，修改该值会使用户等级变化，变化可逆)\n\n**cd_buy,cd_eat,cd_rob,cd_give,cd_bet**：操作冷却（单位：秒）\n\n**max_buy,max_eat,max_rob,max_give,max_bet**：操作随机值上限\n\n**min_buy,min_eat,min_rob,min_give,min_bet**：操作随机值下限\n\n**is_random_give,is_random_eat等**：设置是否操作值都由随机值决定(全局)\n\n**is_random_robbed**： 抢面包操作不指定群员可随机抢\n\n**is_random_given**： 送面包操作不指定群员可随机送\n\n(注意：改为False之后用户可以通过 "操作名 + @ + 数量" 或 "操作名 + 数量" 达到效果)\n\n**special\\_操作名_group**：设置特别处理的群 （示例： {"群号": bool}）\n\n\n**global_database**: 数据库是否全局，若设置了group_database，以其为优先，全局数据库文件夹名为"global"\n\n**group_database**: 合并一些群的数据库 分组id将作为文件夹名 例：{"分组id":["群号1", "群号2", "群号3"]}\n\n**is_at_valid**: 选择是否启用有效at （由于担心风控影响，可自行选择）\n\n>注意：此处的分组id将生效于 special_thing_group 的设置 示例{"分组id": "炸鸡"}，原来的设置将失效。特殊事件同理设置的群聊id同理请改为组id\n\n\n详情请见config.py文件\n\n## 🍞自定义事件\n\n在**bread_event.py**中可以编写特殊事件！\n\n**可以在[issue](https://github.com/Mai-icy/nonebot-plugin-bread-shop/issues/5)中提供你的点子！**\n\n特殊事件模板：\n\ngroup_id_list默认为全部群聊\n\npriority默认为5，数字越低越优先，优先级相同的事件先后顺序每次随机\n\n```python\n@probability(概率, Action.操作, priority=优先级, group_id_list=["群号1", "群号2"])\ndef 函数名(event: 操作):\n    # event.user_data 可以查看操作的用户的面包数据\n    # event.user_id   可以获取操作的用户的id（qq）\n    # event.user_id   可以获取操作的用户的id（qq）\n    # event.bread_db.reduce_bread(event.user_id, eat_num) 减少用户面包数量\n    # event.bread_db.reduce_bread(event.user_id, eat_num) 增加用户面包数量\n    # event.bread_db.add_bread(event.user_id, eat_num, "BREAD_EATEN")  增加用户面包食用量\n    # event.bread_db.update_no(event.user_id)  更新用户排名\n    # event.bread_db.ban_user_action(event.user_id, Action.EAT, 1800) 禁止用户操作\n    # event.bread_db.cd_refresh(event.user_id, Action.EAT)        刷新用户CD\n    # event.bread_db.update_cd_stamp(event.user_id, Action.GIVE)  重置用户CD\n    # 等等见源码\n    return append_text  # 返回回答，由bot发送\n```\n\n特殊事件示例：\n\n```python\n@probability(0.1, Action.EAT, priority=5)\ndef eat_event_much(event: EatEvent):\n    if event.user_data.bread_num <= MAX.EAT.value:\n        return\n    eat_num = random.randint(MAX.EAT.value, min(MAX.EAT.value * 2, event.user_data.bread_num))\n    event.bread_db.reduce_bread(event.user_id, eat_num)\n    event.bread_db.add_bread(event.user_id, eat_num, "BREAD_EATEN")\n    append_text = f"成功吃掉了{eat_num}个面包w！吃太多啦，撑死了，下次吃多等30分钟！"\n    event.bread_db.update_no(event.user_id)\n    event.bread_db.ban_user_action(event.user_id, Action.EAT, 1800)\n    return append_text\n```\n\n若想要设置买面包打烊时间如：\n\n```python\n@probability(1, Action.EAT, priority=1, group_id_list=["群号1", "群号2"])\ndef closing_time(event: EatEvent):\n    if 判断时间:\n        event.bread_db.reduce_user_log(event.user_id, Action.EAT)  # 防止记录\n    \treturn "打烊"\n```\n\n其他注意点：\n\nevent.normal_event()为事件正常进行全流程并返回原来的话。\n\n例如：\n\n```python\n@probability(0.1, Action.BET, priority=5)\ndef bet_event_addiction(event: BetEvent):\n    append_text = event.normal_event()\n    append_text += " 有点上瘾，你想再来一把！"\n    event.bread_db.cd_refresh(event.user_id, Action.BET)\n    return append_text\n```\n\n\n\nreturn None 相当于事件不触发，返回任何字符串都认定为事件触发\n\n',
    'author': 'Mai Icy',
    'author_email': 'maiicy@Foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Mai-icy/nonebot-plugin-bread-shop',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.7,<4.0.0',
}


setup(**setup_kwargs)
