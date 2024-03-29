# nsq2arangodb

NSQ is a realtime distributed messaging platform and ArangoDB is a multi-model database. While NSQ is data agnostic, it
is for sure possible to transport JSON. This package implements insertion of NSQ message bodies into an ArangoDB.

## Installation

```bash
pip install nsq2arangodb
```

It is recommended to do all this within a virtual enviornment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
```

## Usage

Successfully tested with `pyArango==2.0.1` and `pynsq==0.9.1`.

```bash
$ python nsq2arangodb/nsq2arangodb.py --help
usage: nsq2arangodb.py [-h] [--debug] [--arangodb-url ARANGODB_URL]
                       [--arangodb-database ARANGODB_DATABASE]
                       [--arangodb-username ARANGODB_USERNAME]
                       [--arangodb-password ARANGODB_PASSWORD]
                       [--nsq-address NSQ_ADDRESS] [--nsq-port NSQ_PORT]
                       [--nsq-channel-name NSQ_CHANNEL_NAME]
                       NSQ_TOPIC ARANGODB_COLLECTION

positional arguments:
  NSQ_TOPIC
  ARANGODB_COLLECTION

optional arguments:
  -h, --help            show this help message and exit
  --debug
  --arangodb-url ARANGODB_URL
  --arangodb-database ARANGODB_DATABASE
  --arangodb-username ARANGODB_USERNAME
  --arangodb-password ARANGODB_PASSWORD
  --nsq-address NSQ_ADDRESS
  --nsq-port NSQ_PORT
  --nsq-channel-name NSQ_CHANNEL_NAME
```

Most command line switches can also be set via corresponding environment variables.

## Command Line Examples

```bash
alias n2a="./path/to/nsq2arangodb.py"
export ARANGODB_URL="https://avocado.example.com/"
export ARANGODB_USERNAME="your-username"
export ARANGODB_PASSWORD="your-password"
export ARANGODB_DATABASE="your-database"

n2a nsq-topic arangodb-collection
n2a --channel custom-channel-name other-topic other-collection
```

## Code Examples

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import nsq2arangodb as n2a

n2a.Nsq2ArangoDB(
    logging.getLogger(),
    n2a.ArangoDBConfig(
        url='https://avocado.example.com/',
        username='your-username',
        password='your-password',
        database='your-database',
        collection='your-collection',
    ),
    n2a.NsqConfig(
        address='127.0.0.1',
        port=4150,
        topic='your-topic',
        channel='nsq2arangodb'
    )
)
```

## Limitations

* No concurrency (but in-flight support)
* JSON decoding errors are just logged as exceptions and not re-queued, potential solution here is to push them to
  another configurable queue

## Development

After switching into an appropriate virtual env, change to the root directory of this package and install it in
editable mode:

```bash
pip install -e .
```

## Changelog

| Version | Release Date | Change                                                        |
|---------|--------------|---------------------------------------------------------------|
| 1.0.0   | 2021-07-08   | Initial Release                                               |
| 1.0.0   | 2022-05-07   | In-flight count configurable, constraint errors are permanent |
| 1.1.0   | 2023-10-14   | Adds dependencies, adds support for client-side certificates  |
