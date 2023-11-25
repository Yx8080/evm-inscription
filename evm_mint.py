import time
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/arbitrum"))

prk = input("请输入你的私钥：")
num = int(input("请输入你要铸造的数量："))

account: LocalAccount = Account.from_key(prk)
start_nonce = w3.eth.get_transaction_count(account.address)
nonce = start_nonce

def estimate_gas(txn):
    gas = w3.eth.estimate_gas({
        "from": txn['from'],
        "to": txn['to'],
        "value": txn['value'],
        "data": txn['data']
    })
    gas = int(gas + (gas / 10))  # increase 10% of the gas
    return gas

def Mint(private_key):
    global account
    global start_nonce
    global nonce

    transaction = {
        "from": account.address,
        "nonce": nonce,
        "value": 0,
        "gas": 33036,
        "gasPrice": int(w3.eth.gas_price * 1.1),
        "to": account.address,
        "chainId": 42161,  # only replay-protected (EIP-155) transactions allowed over RPC 如果出现下面错误说明需要携带链id
        "data": "0x646174613a2c7b2270223a22666169722d3230222c226f70223a226d696e74222c227469636b223a2266616972222c22616d74223a2231303030227d"
    }

    transaction.update({'gas': int(estimate_gas(transaction))})

    signer = account.sign_transaction(transaction_dict=transaction)

    tx = w3.eth.send_raw_transaction(signer.rawTransaction)
    tx_hash = Web3.to_hex(tx)

    # 检查交易状态
    while True:
        try:
            result = w3.eth.get_transaction_receipt(transaction_hash=tx_hash)
            if result is None or result['blockNumber'] is None:
                time.sleep(3)
            elif result['status']:
                print(f"[成功] - https://arbiscan.io/tx/{tx_hash}")
                nonce += 1
                return result['contractAddress']
            else:
                print(f"[失败] -  https://arbiscan.io/tx/{tx_hash}")
                return False
        except:
            time.sleep(2)

if __name__ == '__main__':
    try:
        for i in range(num):
            print("当前铸造的数量：", i + 1)
            Mint(prk)
        print("铸造完成...")
        time.sleep(2)
    except Exception as e:
        print("报错信息如下：")
        print(e)
    print("程序执行完毕自动退出")