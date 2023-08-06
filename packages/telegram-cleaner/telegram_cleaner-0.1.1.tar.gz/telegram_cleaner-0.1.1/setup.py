# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_cleaner']

package_data = \
{'': ['*']}

install_requires = \
['pyrogram>=2.0.99,<3.0.0', 'tgcrypto>=1.2.5,<2.0.0']

entry_points = \
{'console_scripts': ['tg-clean = telegram_cleaner.cli:cli']}

setup_kwargs = {
    'name': 'telegram-cleaner',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Telegram Cleaner ♻️\n\nDelete all your messages of any type.\n\n**🇷🇺 RUSSIAN DISCLAIMER**: Telegram не является анонимным и никогда им не был. Сотрудникам спецслужб известны телефонные номера около 30 миллионов пользователей Telegram из России, а равно и паспортные данных их владельцев. До 2020 года по телефону можно было найти любого пользователя. Чекистские подстилки массово скупали симки, вбивали в контакты тысячи случайных номеров, а потом сохраняли в базе связку id пользователя и номера телефона. Так собиралась пользовательская база, например, «Глаза Бога». С учетом того, что Роскомнадзор запустил бота для поиска экстремистских комментариев в сети, в т.ч. в Telegram, я настоятельно рекомендую вам потереть свои старые комментарии в каналах и группах. Также помните, что Telegram сотрудничает с ФСБ и другими спецслужбами и занимается выдачей террористов. Если сотрудники телеги получат на вас запрос от гэбни, то никто из них не удосужится выяснить, настоящий вы террорист ИГИЛ или это обычный спам запросами на неугодных режиму, они просто передадут ваши ip-адрес и номер телефона.\n\n**⚠️ WARNING**: before using this utility, you can save all your data using the desktop application: `Settings ` > ` Advanced` > `Export Telegram data`.\n\nInstallation:\n\n```bash\n# via pip\n$ pip install -U telegram-cleaner\n\n# via pipx\n$ pipx install telegram-cleaner\n```\n\nUsage:\n\n```bash\n# see help\n$ tg-clean -h\n\n# first save your chats\n$ tg-clean dump_chats > mychats.json\n\n# later you can extract data from this file using jq\n$ jq -r \'.[] | "\\( .id ) \\( .username  ) " + if has("title") then .title else "\\( .first_name ) \\( .last_name  )" end\' mychats.json\n777000 null Telegram null\n-1001436354653 nwsru NEWS.ru | Новости\n...\n\n# delete messages in group chats, comments, posts\n$ tg-clean -vv delete_group_messages\n\n# delete private chats without confirmation\n$ tg-clean -y delete_private_chats\n\n# delete all your messages of any type\n$ tg-clean\n\n# You can use you own API_ID and API_HASH\n# Also you can use .env files with zsh dotenv plugin\n# Add this lines to ~/.bashrc or ~/.zshrc\nexport TG_API_ID=6\nexport TG_API_HASH=eb06d4abfb49dc3eeb1aeb98ae0f581e\n```\n',
    'author': 'Senior YAML Developer',
    'author_email': 'yamldeveloper@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
