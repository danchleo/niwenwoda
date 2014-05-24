# 值得问


## 环境

* Python 2.7
* pip
* virtualenv


## 安装

    git clone https://github.com/danchleo/niwenwoda.git
    cd niwenwoda

    virtualenv .env
    source .env/bin/activate
    pip install -r requirements.txt

    python manage.py syncdb
    python manage.py runserver

访问 `127.0.0.1:8000`，默认用户名 `test`， 密码 `test`
