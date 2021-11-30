# blockchain-client
Client Program for creating wallets and interacting with the blockchain

## Installation & Setup

Install all requirements using this command:
```shell
pip install -r requirements.txt
```
Check if packages were installed correctly:
```shell
python main.py -h
```
The output should look something like this:
```shell
usage: main.py [-h] [-go] [-gb] [-cb] [-cw] [-sw SWITCH_WALLET] [-iw] [-m]
               [-sh SET_HOST] [-s]

Client to connect to CodeAmaterasu/blockchain

optional arguments:
  -h, --help            show this help message and exit
  -go, --get-openchain  Get openchain from blockchain
  -gb, --get-blockchain
                        Get blockchain
  -cb, --create-block   Create new block on the blockchain
  -cw, --create-wallet  Create a new wallet for the blockchain
  -sw SWITCH_WALLET, --switch-wallet SWITCH_WALLET
                        Switch to new wallet. Pass wallet name as parameter
  -iw, --import-wallet  Import wallet
  -m, --mine            Mine on the blockchain
  -sh SET_HOST, --set-host SET_HOST
                        Set the blockchain host. Parameter host
  -s, --setup           First time setup
```

Now you need to perform the first time setup:
```shell
python main.py -s
```
If everything worked, the output should look something like this:
```shell
Starting setup
Configuring directories.....
Creating configuration file......
Finished setup!
```

## How to use

The first step is to create a new wallet or importing one, in this example we're gonna create a new one.
<br>
Following command creates a new wallet:
```shell
python main.py -cw
```
The script will ask which name you want to give the wallet, here just enter whatever suits you, then the wallet should be generated.
<br>
Now you have to tell the script to use the newly created wallet for blockchain operations, this can be done using following command:
```shell
python main.py -sw <WALLET_NAME>
```
The second step is to tell the client to which blockchain node we want to connect to, this can be done like this:
```shell
python main.py -sh http://localhost:8080
```
After that the script updated the blockchain host.
<br>
<br>
Now we're set to use the blockchain. For example, we can create a new block/transaction using this command:
```shell
python main.py -cb
```
The script will ask what resource you want to "own", here you can enter a resource witch is defined in the blockchain host.
<br>
<br>
The newly created block is now in a list of unprocessed blocks, those can be seen using following command:
```shell
python main.py -go
```
Until those blocks are not mined, they will remain in this list and not entering the blockchain. Now you can mine the block you created using this command:
```shell
python main.py -m
```

The command connects to the blockchain via websocket and receives every 5 seconds an updated version of the "openchain".

If there is a block to mine, the client will mine it, if not the client will continue to listen to the socket.
