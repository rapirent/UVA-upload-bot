# toc_project
- 計算理論的作業:一個telegram bot
- based on python django framework
    - Django 1.11
    - python 3.5
    - python telegram bot


# frame tree
kuoteng_bot
├── kuoteng_bot
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-35.pyc
│   │   └── settings.cpython-35.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── telegram_bot
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py

# Setup

## clone this repo
```
cd ~/toc_project
```

## virtualenv

```
virtualenv -p python3 venv
source venv/bin/activate
```

you can use `deactivate` command to leave virtualenv

## install python packages

```
sudo python3 get-pip.py
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

![rapirent](https://github.com/rapirent)
