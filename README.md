# toc_project

- 計算理論的作業:一個telegram bot
- based on python django framework
    - Django 1.11
    - python 3.5
    - python telegram bot


# frame tree

```
kuoteng_bot
├── db.sqlite3
├── demo.py
├── jieba_data
│   └── dict.txt.big
├── kuoteng_bot
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── med250.model.bin
├── my_stat_diagram.png
└── telegram_bot
    ├── admin.py
    ├── apps.py
    ├── fsm.py
    ├── __init__.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── __init__.py
    ├── models.py
    ├── my_stat_diagram.png
    ├── telegrambot.py
    ├── tests.py
    ├── urls.py
    ├── uva.py
    └── views.py
```

- you can also use `tree` instuction to show on your own shell

# Setup

## clone this repo



```
git clone https://github.com/rapirent/toc_project.git
cd ~/toc_project
```

## virtualenv


- you may probably need to `apt-get install python-software-properties` (or apt) with `apt upgrade` and `apg-get update`

```
apt install virtualenv
sudo apt install python3-dev
sudo python3 get-pip.py
virtualenv -p python3 venv
source venv/bin/activate
```

you can use `deactivate` command to leave virtualenv

## install python packages

```
pip install -r requirements.txt
```

## set WEBHOOK TOKEN

in kuoteng_bot create your `.secrets.json`
```
cd cd ~/toc_project/kuoteng_bot
vim .secrets.json
```


```
{
    "TOKEN": "YOUR-TOKEN",
    "WEBHOOK_URL": "YOUR-WEBHOOK_URL",
    "DJANGO_TOEKN": ""
}

```
## Deploy

```
python manage.py runserver
```

```
sudo uwsgi --ini bot.ini --touch-reload=/home/ubuntu/Life-all-in-one-bot/bot/bot.ini
```


# fsm
![](./kuoteng_bot/my_stat_diagram.png)

# author

[rapirent](https://github.com/rapirent)
