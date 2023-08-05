#!/usr/bin/env python3
import os

import codefast as cf
import fire

from bordercollie.apps.monitor import depthwatch, nsqtopic
from bordercollie.asrsummary import calculate_summary, save_record


def pip(cmd: str, douban: bool = False):
    """Python package installer"""
    pypi = "https://pypi.douban.com/simple" if douban else "https://pypi.org/simple"
    cmd = 'python3 -m pip install {} -i {}'.format(cmd, pypi)
    os.system(cmd)


def transfer(file):
    """transfer.sh script"""
    cmd = f"curl -s -o /tmp/transfer.pl https://host.ddot.cc/transfer.pl && perl /tmp/transfer.pl {file} && rm /tmp/transfer.pl"
    try:
        resp = cf.shell(cmd)
        cf.info(resp)
    except Exception as e:
        print(e)


def sync(file):
    """sync file to gofile"""
    try:
        # still file.ddot
        cmd = f"curl -s https://file.ddot.cc/gofil|bash -s '{file}'"
        resp = cf.shell(cmd)
        cf.info(resp)
    except FileNotFoundError as e:
        print(e)


def jq(file):
    """sync file to gofile"""
    import json
    import ast

    def eval(s: str):
        try:
            return json.loads(s)
        except json.decoder.JSONDecodeError as e:
            return ast.literal_eval(s)

    jsf = file
    from tqdm import tqdm
    cf.info("formatting {}".format(file))
    assert cf.io.exists(jsf), "file {} not found".format(jsf)
    content = cf.io.reads(jsf).split('\n')[0].lstrip().rstrip()
    size = len(content)
    for i in tqdm(range(300)):
        for j in range(10):
            try:
                js = eval(content[i:size-j])
                cf.js.write(js, jsf + '-formated.json')
                cf.info('exported to "{}"'.format(jsf+'-formated.json'))
                return
            except Exception as e:
                pass
    cf.warning('failed to format {}'.format(file))


def esync(file: str):
    """sync file with encryption"""
    try:
        cmd = f"curl -s https://host.ddot.cc/gofile|bash -s '{file}'"
        resp = cf.shell(cmd)
        cf.info(resp)
    except FileNotFoundError as e:
        print(e)


def grep(kw: str):
    """search from log"""
    print(cf.shell('grep {} /log/serving/serving.log'.format(kw)))


def bash(cmd: str):
    # The following import requires auth, do not put it at the top
    from bordercollie.apps.workflow import shell
    resp = shell.delay(cmd)
    print(resp.get(timeout=10))


def main():
    fire.Fire()
