# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_cleaner']

package_data = \
{'': ['*']}

install_requires = \
['pyrogram>=2.0.99,<3.0.0', 'tgcrypto>=1.2.5,<2.0.0']

entry_points = \
{'console_scripts': ['tg-clean = telegram_cleaner.cli:main']}

setup_kwargs = {
    'name': 'telegram-cleaner',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Telegram Cleaner\n\nDelete telegram messages, chats, leave groups.\n\n**RUSSIAN DISCLAIMER**: Telegram не является анонимным и никогда им не был. Сотрудникам спецслужб известны телефонные номера около 30 миллмонов пользователей Telegram, а равно и паспортные данных их владельцев. До 2020 года по телефону можно было найти любого пользователя. Чекистские подстилки массово скупали симки, вбивали в контакты тысячи случайных номеров, а потом сохраняли в базе связку id и номер телефона. Так собиралась пользовательская база, например, «Глаза Бога». С учетом того, что Роскомнадзор запустил бота для поиска экстремистских комментариев в сети, в т.ч. в Telegram настоятельно советую удалить свои старые аккаунты, предварительно потерев комментарии в группах. Также помните, что Telegram сотрудничает с ФСБ и другими спецслужбами и занимается выдачей террористов. Если сотрудники телеги получат на вас запрос от гэбни, то никто из них не удосужится выяснить, настоящий вы террорист ИГИЛ или это обычный спам запросами на неугодных режиму, они просто передадут ваши ip-адрес и номер телефона.\n\n**WARNING**: before using this utility, you can save all your data using the desktop application: `Settings ` > ` Advanced` > `Export Telegram data`.\n\nInstall:\n\n```bash\n# via pip\n$ pip install -U telegram-cleaner\n\n# via pipx\n$ pipx install telegram-cleaner\n```\n\nUsage:\n\n```bash\n# Show help and exit\n$ tg-clean -h\n\n# Run all\n$ tg-clean\n\n# Delete only private chats\n$ tg-clean -vvy delete_private_chats\n\n# Output chats with identifiers\n$ tg-clean print_chats\n\n# You cand use you own telegram application\nexport TG_API_ID=<API_ID>\nexport TG_API_HASH=<API_HASH>\n```\n',
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
