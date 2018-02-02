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
import socket

import requests

from ..pipe_reader import PipeReader


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def _main(webhook_url, channel=None, title=None):
    pipe = PipeReader()
    content = pipe.read()

    username = socket.gethostname()

    attachment = {'text': '```{}```'.format(content),
                  'mrkdwn_in': ['text', 'title']}
    if title:
        attachment['title'] = title

    payload = {'channel': '@taro',
               'attachments': [attachment],
               'username': 'from ' + username,
               'icon_emoji': ':star:'}
    if channel:
        payload['channel'] = channel

    print(content)
    resp = requests.post(webhook_url, json=payload)
    print(resp)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('url')
    p.add_argument('--channel', '-c')
    p.add_argument('--title', '-t')
    args = p.parse_args()
    _main(webhook_url=args.url, channel=args.channel, title=args.title)
