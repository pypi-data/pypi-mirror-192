import os
import re
from setuptools import setup,find_packages


requires = ["pycryptodome==3.16.0","aiohttp==3.8.3","asyncio==3.4.3","tinytag==1.8.1","Pillow==9.4.0"]
_long_description = """

## NanyRubika

> Elegant, modern and asynchronous Rubika MTProto API framework in Python for users and bots

<p align="center">
    <img src="https://s2.uupload.ir/files/img_20230208_141501_035_f545.jpg" alt="NanyRubika" width="128">
    <br>
    <b>library NanyRubika</b>
    <br>
</p>

###  Nanymous


### How to import the Rubik's library

``` bash
from NanyRubika import Nanybot

Or

from NanyRubika import Nany_Robot
```

### How to import the anti-advertising class

``` bash
from NanyRubika.Zedcontent import Antiadvertisement
```

### How to install the library

``` bash
pip install NanyRubika==3.1.5
```

### My ID in Telegram

``` bash
@Nanymous
```
## An example:
``` python
from NanyRubika import Nanybot

bot = Nanybot("Your Auth Account")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"NanyRubika Library")
```

## And Or:
``` python
from NanyRubika import Robot_Rubika

bot = Robot_Rubika("Your Auth Account")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"NanyRubika library")
```
Made by Team Nanymous

Address of our team's GitHub :

https://github.com/Nanymous/NanyRubika.git


### Key Features

- **Ready**: Install NanyRubika with pip and start building your applications right away.
- **Easy**: Makes the Rubika API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by pycryptodome, a high-performance cryptography library written in C.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Rubika's API to execute any official client action and more.


### Our channel in messengers

``` bash
Our channel in Ita

https://eitaa.com/Nanymous_Team

Our channel in Soroush Plus

https://splus.ir/Nanymous_Team

Our channel in Rubika

https://rubika.ir/GLSource

Our channel in the Gap

None

Our channel on Telegram

https://t.me/Nanymous
```
"""

setup(
    name = "NanyRubika",
    version = "3.1.5",
    author = "Mohammad _GeNeRal_",
    author_email = "Nanylibrary@gmail.com",
    description = (" Library Robot Rubika"),
    license = "MIT",
    keywords = ["Nany","nanyrubika","NanyRubika","nany","bot","Bot","BOT","Robot","ROBOT","robot","self","api","API","Api","rubika","Rubika","RUBIKA","Python","python","aiohttp","asyncio"],
    url = "https://github.com/Nanymous/NanyRubika.git",
    packages = ['NanyRubika'],
    long_description=_long_description,
    long_description_content_type = 'text/markdown',
    install_requires=requires,
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11'
    ],
)
