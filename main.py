import argparse
from core.blockchain_sdk import BlockChainClient
from core.blockchain_sdk import Block

client = BlockChainClient()

parser = argparse.ArgumentParser(description='Client to connect to CodeAmaterasu/blockchain')


def __register_arguments():
    parser.add_argument('-go', '--get-openchain', action='store_true', help='Get openchain from blockchain')
    parser.add_argument('-gb', '--get-blockchain', action='store_true', help='Get blockchain')
    parser.add_argument('-cb', '--create-block', action='store_true', help='Create new block on the blockchain')


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
