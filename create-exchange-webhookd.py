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
    'main_exchange_name': 'wazo-headers',
    'main_exchange_type': 'headers',
    'webhookd_exchange_name': 'wazo-webhookd',
    'webhookd_exchange_type': 'headers',
}


def main():
    config = _DEFAULT_CONFIG

    bus_url = 'amqp://{username}:{password}@{host}:{port}/{vhost}'.format(**config)
    with kombu.Connection(bus_url) as connection:
        main_exchange = kombu.Exchange(config['main_exchange_name'], type=config['main_exchange_type'])
        webhookd_exchange = kombu.Exchange(config['webhookd_exchange_name'], type=config['webhookd_exchange_type'], durable=True)(connection.default_channel)
        webhookd_exchange.declare()
        for name in (
            'auth_user_external_auth_added',
            'auth_user_external_auth_deleted',
            'call_created',
            'call_updated',
            'call_answered',
            'call_ended',
            'call_held',
            'call_resumed',
            'call_dtmf_created',
            'call_push_notification',
            'call_cancel_push_notification',
            'chatd_user_room_message_created',
            'user_missed_call',
            'user_voicemail_message_created',
        ):
            headers = {
                'name': name,
            }
            binding = kombu.binding(main_exchange, None, headers, headers)
            binding.bind(webhookd_exchange)


if __name__ == '__main__':
    main()
