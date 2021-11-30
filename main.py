import argparse
import base64
import configparser
import os

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
    parser.add_argument('-sw', '--switch-wallet', help='Switch to new wallet. Pass wallet name as parameter')
    parser.add_argument('-s', '--setup', action='store_true', help='First time setup')


def __parse_arguments():
    return parser.parse_args()


def __setup():
    print('Configuring directories.....')
    app_data_dir = os.getenv('APPDATA')
    blockchain_cli_dir = app_data_dir + '\\blockchain-cli'
    # Create script dir
    os.mkdir(blockchain_cli_dir)
    wallet_dir = blockchain_cli_dir + '\\wallets'
    # Create wallet dir
    os.mkdir(wallet_dir)
    print('Creating configuration file......')
    config = configparser.ConfigParser()
    config['Wallet'] = {
        'pub_key': '',
        'priv_key': ''
    }
    config['Blockchain'] = {
        'host': ''
    }
    with open(blockchain_cli_dir + '\\config.ini', 'w') as file:
        config.write(file)
    print('Finished setup!')


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
        # Make it shorter and therefore moros.getenv('APPDATA') + '\\blockchain-cli\\walletse readable
        public_key = base64.b64encode(bytes.fromhex(public_key))

        filename = input('Write the name of your new address: ') + '.txt'
        file_path = os.getenv('APPDATA') + '\\blockchain-cli\\wallets\\' + filename
        with open(file_path, 'w') as f:
            f.write('Private key:{0}\nWallet address / Public key:{1}'.format(private_key, public_key.decode()))
        print('Your new address and private key are now in the file {0}'.format(file_path))
    elif args.setup:
        print('Starting setup')
        __setup()
    elif args.switch_wallet:
        available_wallets = os.listdir(os.getenv('APPDATA') + '\\blockchain-cli\\wallets')
        for wallet in available_wallets:
            if args.switch_wallet == wallet.split('.')[0]:
                with open(os.getenv('APPDATA') + '\\blockchain-cli\\wallets\\' + wallet, 'r') as wallet_file:
                    wallet_content = wallet_file.readlines()
                    my_config = configparser.ConfigParser()
                    my_config.read(os.getenv('APPDATA') + '\\blockchain-cli\\config.ini')
                    for content in wallet_content:
                        split_content = content.strip().split(':')
                        if 'Private key' in split_content[0]:
                            my_config['Wallet']['priv_key'] = split_content[1]
                        elif 'Wallet address / Public key' in split_content[0]:
                            my_config['Wallet']['pub_key'] = split_content[1]
                    with open(os.getenv('APPDATA') + '\\blockchain-cli\\config.ini', 'w') as config_file:
                        my_config.write(config_file)

        print('Switched Wallet to: ' + args.switch_wallet)


