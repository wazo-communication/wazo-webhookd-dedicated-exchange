#!/usr/bin/env python3
# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import kombu
import logging
import sys

from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(process)d] (%(levelname)s) (%(name)s): %(message)s')

_DEFAULT_CONFIG = {
    'username': 'guest',
    'password': 'guest',
    'host': 'localhost',
    'vhost': '',
    'port': 5672,
    'webhookd_exchange_name': 'wazo-webhookd',
    'webhookd_exchange_type': 'headers',
}


def main():
    config = _DEFAULT_CONFIG

    bus_url = 'amqp://{username}:{password}@{host}:{port}/{vhost}'.format(**config)
    with kombu.Connection(bus_url) as connection:
        webhookd_exchange = kombu.Exchange(config['webhookd_exchange_name'], type=config['webhookd_exchange_type'], durable=True)(connection.default_channel)
        webhookd_exchange.delete()


if __name__ == '__main__':
    main()
