#!/usr/bin/env python3
import codefast as cf
from celery import Celery
from simauth import OnlineAuth

from bordercollie.auth import auth

try:
    broker = auth.celery_backend
except:
    broker = OnlineAuth('https://cf.ddot.cc/api').auth('broker')
app = Celery('collie_workflow', broker=broker, backend=broker)

app.conf.result_expires = 120


@app.task(time_limit=30, soft_time_limit=30)
def shell(cmd: str) -> str:
    try:
        return cf.shell(cmd)
    except Exception as e:
        return str(e)
