import dataclasses

import requests


class Block:

    def __init__(self, owner: str, resource: str) -> None:
        self.owner = owner
        self.resource = resource


class BlockChainClient:

    def __init__(self, host: str = 'http://localhost:8080') -> None:
        self.host = host
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.functions = {
            'go': '/api/get_openchain',
            'gb': '/api/get_chain',
            'cb': '/api/create_block'
        }

    def execute(self, function_key: str):
        result = requests.get(url=self.host + self.functions[function_key])
        return result.text

    def create_block(self, block: Block):
        # FIXME: This causes following -> TypeError: 'Block' object is not iterable
        result = requests.post(url=self.host + self.functions['cb'], data=block, headers=self.headers)
        return result.text
