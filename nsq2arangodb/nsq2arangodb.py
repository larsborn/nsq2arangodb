#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data transportation from NSQ to ArangoDB.
"""
import argparse
import json
import logging
import os
from dataclasses import dataclass

import nsq
from pyArango.connection import Connection

__service__ = 'nsq2arangodb'
__version__ = '1.0.0'


@dataclass
class ArangoDBConfig:
    url: str
    username: str
    password: str
    database: str
    collection: str


@dataclass
class NsqConfig:
    address: str
    port: int
    topic: str
    channel: str


class Nsq2ArangoDB:
    def __init__(self, logger: logging.Logger, arangodb_config: ArangoDBConfig, nsq_config: NsqConfig):
        self._logger = logger
        connection = Connection(
            arangoURL=arangodb_config.url,
            username=arangodb_config.username,
            password=arangodb_config.password
        )
        self._collection = connection[arangodb_config.database][arangodb_config.collection]
        nsq.Reader(
            message_handler=self._handler,
            nsqd_tcp_addresses=[F'{nsq_config.address}:{nsq_config.port}'],
            topic=nsq_config.topic,
            channel=nsq_config.channel,
        )
        nsq.run()

    def _handler(self, message: nsq.Message):
        decoded_body = message.body.decode('utf-8')
        self._logger.debug(F'Transporting message with body of length={len(decoded_body)}')
        try:
            decoded_json = json.loads(decoded_body)
        except json.decoder.JSONDecodeError as e:
            self._logger.exception(e)
            return True  # do not requeue decoding errors
        self._insert_into_arangodb(decoded_json)
        return True

    def _insert_into_arangodb(self, json_doc):
        self._collection.createDocument(initDict=json_doc).save()


def main(args: argparse.Namespace):
    logger = logging.getLogger(__service__)
    logging.basicConfig()
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
    logger.info(F'Starting {__service__}/{__version__}')
    logger.debug(F'Arguments: {args}')
    Nsq2ArangoDB(
        logger,
        ArangoDBConfig(
            url=args.arangodb_url,
            username=args.arangodb_username,
            password=args.arangodb_password,
            database=args.arangodb_database,
            collection=args.arangodb_collection,
        ),
        NsqConfig(
            address=args.nsq_address,
            port=args.nsq_port,
            topic=args.nsq_topic,
            channel=args.nsq_channel_name,
        )
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--arangodb-url', default=os.environ.get('ARANGODB_URL'))
    parser.add_argument('--arangodb-database', default=os.environ.get('ARANGODB_DATABASE'))
    parser.add_argument('--arangodb-username', default=os.environ.get('ARANGODB_USERNAME'))
    parser.add_argument('--arangodb-password', default=os.environ.get('ARANGODB_PASSWORD'))
    parser.add_argument('--nsq-address', default=os.environ.get('NSQ_ADDRESS', '127.0.0.1'))
    parser.add_argument('--nsq-port', default=os.environ.get('NSQ_PORT', 4150), type=int)
    parser.add_argument('--nsq-channel-name', default=os.environ.get('NSQ_CHANNEL_NAME', __service__))
    parser.add_argument('nsq_topic')
    parser.add_argument('arangodb_collection')
    main(parser.parse_args())
