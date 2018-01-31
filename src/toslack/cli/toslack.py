# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
# Copyright (c) 2018 Taro Sato
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import argparse
import logging

import requests
from ..pipe_reader import PipeReader


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def _main(webhook_url):
    pipe = PipeReader()
    content = pipe.read(wait=3)
    payload = {
        'channel': '@taro',
        'attachments': [{
            # 'pretext': 'boo',
            'text': '```{}```'.format(content),
            'mrkdwn_in': ['text']}
        ]
    }
    print(content)
    resp = requests.post(webhook_url, json=payload)
    print(resp)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('url')
    args = p.parse_args()
    _main(webhook_url=args.url)
