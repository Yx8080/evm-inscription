import time
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3

class EVM_Minter:
    def __init__(self,rpc,private_key,dataHex):
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.account = Account.from_key(private_key)
        self.start_nonce = self.w3.eth.get_transaction_count(self.account.address)
        self.nonce = self.start_nonce
        self.dataHex = dataHex

    # 获取gas
    def estimate_gas(self, txn):
        gas = self.w3.eth.estimate_gas({
            "from": txn['from'],
            "to": txn['to'],
            "value": txn['value'],
            "data": txn['data']
        })
        gas = int(gas + (gas / 10))  # increase 10% of the gas
        return gas
    # 开始铸造
    def mint(self):
        transaction = {
            "from": self.account.address,
            "nonce": self.nonce,
            "value": 0,
            "gas": 33036,
            "gasPrice": int(self.w3.eth.gas_price * 1.1),
            "to": self.account.address,
            "chainId": 137,
            "data": self.dataHex
        }

        transaction.update({'gas': int(self.estimate_gas(transaction))})

        signer = self.account.sign_transaction(transaction_dict=transaction)

        tx = self.w3.eth.send_raw_transaction(signer.rawTransaction)
        tx_hash = Web3.to_hex(tx)

        # 检查交易状态
        while True:
            try:
                result = self.w3.eth.get_transaction_receipt(transaction_hash=tx_hash)
                if result is None or result['blockNumber'] is None:
                    time.sleep(3)
                elif result['status']:
                    self.nonce += 1
                    return "[成功] - https://polygonscan.com/tx/{tx_hash}"
                else:
                    return "[失败] -  https://polygonscan.com/tx/{tx_hash}"
            except:
                time.sleep(2)
