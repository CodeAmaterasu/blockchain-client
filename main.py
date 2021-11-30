import argparse
import base64
import configparser
import os

import ecdsa

from core.blockchain_sdk import BlockChainClient
from core.blockchain_sdk import Block
from ecdsa import SigningKey, SECP256k1
import websocket
config_parser = configparser.ConfigParser()
config_parser.read(os.getenv('APPDATA') + '\\blockchain-cli\\config.ini')

client = BlockChainClient(host=config_parser['Blockchain']['host'])

parser = argparse.ArgumentParser(description='Client to connect to CodeAmaterasu/blockchain')


def __register_arguments():
    parser.add_argument('-go', '--get-openchain', action='store_true', help='Get openchain from blockchain')
    parser.add_argument('-gb', '--get-blockchain', action='store_true', help='Get blockchain')
    parser.add_argument('-cb', '--create-block', action='store_true', help='Create new block on the blockchain')
    parser.add_argument('-cw', '--create-wallet', action='store_true', help='Create a new wallet for the blockchain')
    parser.add_argument('-sw', '--switch-wallet', help='Switch to new wallet. Pass wallet name as parameter')
    parser.add_argument('-iw', '--import-wallet', action='store_true', help='Import wallet')
    parser.add_argument('-m', '--mine', action='store_true', help='Mine on the blockchain')
    parser.add_argument('-sh', '--set-host', help='Set the blockchain host. Parameter host')
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


def __on_message(ws, message):
    print(message)
    # Mine
    client.execute('m')


if __name__ == '__main__':
    __register_arguments()
    args = __parse_arguments()

    if args.get_openchain:
        print(client.execute('go'))
    elif args.get_blockchain:
        print(client.execute('gb'))
    elif args.create_block:
        config = configparser.ConfigParser()
        config.read(os.getenv('APPDATA') + '\\blockchain-cli\\config.ini')
        owner = config['Wallet']['pub_key']
        resource = input('Enter Resource\n')
        block = Block(owner=owner, resource=resource)
        new_block = {
            "owner": str(owner),
            "resource": str(resource)
        }
        # client.create_block(block={'owner': owner, 'resource': resource})
        client.create_block(block=new_block)
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
    elif args.import_wallet:
        # Get the key pair
        priv_key = str(input('Enter the private key: \n'))
        pub_key = str(input('Enter the public key: \n'))
        # Recreate the ecdsa key objects
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(priv_key), curve=ecdsa.SECP256k1)
        vk = ecdsa.VerifyingKey.from_string(base64.b64decode(pub_key), curve=ecdsa.SECP256k1)
        # Sign a dummy message for the verificatio process
        sig = sk.sign(b'message')
        try:
            # Verify the key pair, throws exception when keys don't match
            vk.verify(sig, b'message')
            # Save the bad boy
            filename = input('Write the name of your new address: ') + '.txt'
            file_path = os.getenv('APPDATA') + '\\blockchain-cli\\wallets\\' + filename
            with open(file_path, 'w') as f:
                f.write('Private key:{0}\nWallet address / Public key:{1}'.format(priv_key, pub_key))
            print('Your new address and private key are now in the file {0}'.format(file_path))
        except ecdsa.keys.BadSignatureError as e:
            print("Error: It appears that you're not the owner of the wallet or the private key and public key are "
                  "incorrect")
    elif args.set_host:
        config_path = os.getenv('APPDATA') + '\\blockchain-cli\\config.ini'
        my_config = configparser.ConfigParser()
        my_config.read(config_path)
        my_config['Blockchain']['host'] = args.set_host
        with open(config_path, 'w') as config_file:
            my_config.write(config_file)
        print('Blockchain host updated')
    elif args.mine:
        ws = websocket.WebSocketApp(url='ws://localhost:8080/ws/openchain', on_message=__on_message)
        ws.run_forever()





