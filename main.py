import argparse
import base64

from core.blockchain_sdk import BlockChainClient
from core.blockchain_sdk import Block
from ecdsa import SigningKey, SECP256k1
import binascii
import random

client = BlockChainClient()

parser = argparse.ArgumentParser(description='Client to connect to CodeAmaterasu/blockchain')


def __register_arguments():
    parser.add_argument('-go', '--get-openchain', action='store_true', help='Get openchain from blockchain')
    parser.add_argument('-gb', '--get-blockchain', action='store_true', help='Get blockchain')
    parser.add_argument('-cb', '--create-block', action='store_true', help='Create new block on the blockchain')
    parser.add_argument('-cw', '--create-wallet', action='store_true', help='Create a new wallet for the blockchain')


def __parse_arguments():
    return parser.parse_args()


if __name__ == '__main__':
    __register_arguments()
    args = __parse_arguments()

    if args.get_openchain:
        print(client.execute('go'))
    elif args.get_blockchain:
        print(client.execute('gb'))
    elif args.create_block:
        # FIXME: Get it from somewhere locally, not hardcoded
        owner = 'abcv4531adfbjiup901'
        resource = input('Enter Resource\n')
        block = Block(owner=owner, resource=resource)
        # client.create_block(block={'owner': owner, 'resource': resource})
        client.create_block(block=block)
    elif args.create_wallet:
        sk = SigningKey.generate(curve=SECP256k1)
        private_key = sk.to_string().hex()
        vk = sk.get_verifying_key()
        public_key = vk.to_string().hex()
        public_key = base64.b64encode(bytes.fromhex(public_key))

        filename = input("Write the name of your new address: ") + ".txt"
        with open(filename, "w") as f:
            f.write("Private key: {0}\nWallet address / Public key: {1}".format(private_key, public_key.decode()))
        print("Your new address and private key are now in the file {0}".format(filename))


