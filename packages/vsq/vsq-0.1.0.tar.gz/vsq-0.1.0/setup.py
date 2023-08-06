# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vsq']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vsq',
    'version': '0.1.0',
    'description': 'VALVE-Server Queries(now for L4D2)',
    'long_description': '<div align="center">\n\n# VALVE-Server Queries\n_✨基于A2S协议，一款可以查询求生服务器状态的库✨_\n\n_✨Based on the agreement with the Left 4 Dead 2 server, a library that can query the status of the survival server.✨_\n\n<a href="https://github.com/Umamusume-Agnes-Digital/VSQ/stargazers">\n    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Umamusume-Agnes-Digital/VSQ">\n</a>\n<a href="https://github.com/Umamusume-Agnes-Digital/VSQ/issues">\n    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Umamusume-Agnes-Digital/VSQ">\n</a>\n\n</div>\n## Description说明\n        目标是实现服务器全链接(1/N)\n\n\n## 🎉 available已实现\n - ipv4连接到求生之路2服务器并返回基本信息(A2S_INFO)\n - ipv4连接到求生之路2服务器并返回在线玩家信息(A2S_PLAYER)\n\n## 📖 to do list可能会做\n\n - 暂无\n\n## 👌 pip安装\n        pip install VSQ\n\n\n## 📖 use使用\n\n函数包括\n\n        # 总信息\n        server  (ip : str , port : int , times = 60) -> dict\n        ip:ipv4 ,port:端口号 , times 默认为60,也就是说一分钟内同时调用任意函数，服务器将使用第一次的缓存，这可以使得防止被当做DDOS\n        # 格式 {\'header\':xx,\'protocol\':xxx,...}\n        header, protocol, name, map_, folder, game, appid, players, max_players, bots, server_type, environment, visibility, vac, version, edf\n        # 分别代表服务器返回的参数\n\n---\n        # 玩家信息\n        players (ip : str , port : int , times = 60) -> dict:\n        # 格式\n        {\n        \'header\':1,\n        \'Players\':\n            [{\n                \'Index\':0,\n                \'Name\':xxx,\n                \'Score\':114514,\n                \'Duration\':int but who care\n            },\n            {\n                ...\n            }\n            ]\n        }\n\n## 🍻 exemple示例代码\n\n    如果我想要获取服务器名字/地图/玩家数量\n        from VSQ import l4d2\n        ip:str = \'127.0.0.1\' \n        port:int = 20715 \n        name = l4d2.name(ip,port)\n        map_ = l4d2.map_(ip,port)\n        players = await l4d2.players(ip,port)\n        print(name)\n        print(map_)\n        print(players)\n    \n    如果我想要获取服务器所有信息的字典（所有的键在上面，其中edf是bytes类，后面还有额外的附带信息所以有21个键对，如果有需求可以看源代码\n        from VSQ import l4d2\n        ip:str = \'127.0.0.1\' \n        port:int = 20715 \n        server_dict = await l4d2.server(ip,port)\n        print(server_dict)\n\n        from VSQ import l4d2\n        ip:str = \'127.0.0.1\' \n        port:int = 20715 \n        players_data =  await l4d2.players(ip,port)\n        players_number = players_data[\'header\']\n        for i in players_data[\'Players\'][0]\n            print(\'player_name\',i[\'Name\'])\n\n\n## 🌐 Communicate with me联系我\n\n    email:Z735803792@163.com',
    'author': 'Agnes_Digital',
    'author_email': 'Z735803792@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Umamusume-Agnes-Digital/VSQ',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
