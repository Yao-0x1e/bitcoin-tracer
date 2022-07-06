from collections import namedtuple
from typing import List, Tuple
import binascii
import hashlib

import base58

from src.bitcoin.rpc import BitcoinRPC

TxIn = namedtuple('TxIn', ['payer', 'balance'])
TxOut = namedtuple('TxOut', ['payee', 'balance'])


class BitcoinUtils:
    @staticmethod
    def convert_pubkey_to_address(pubkey: str) -> str:
        sha256_value = hashlib.sha256(binascii.unhexlify(pubkey)).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_value)
        ripemd160_value = ripemd160.digest()
        address = b"\x00" + ripemd160_value
        checksum = hashlib.sha256(hashlib.sha256(address).digest()).digest()[:4]
        address = base58.b58encode(address + checksum)
        return address.decode()

    @staticmethod
    def is_coinbase_tx(tx: dict):
        return 'coinbase' in tx['vin'][0]

    @staticmethod
    def parse_vout(vout: dict) -> Tuple[str, float]:
        script: dict = vout['scriptPubKey']
        script_type: str = script['type']
        if script_type == 'pubkey':
            asm: str = script['asm']
            parts = asm.split(' ')
            assert len(parts) == 2
            pubkey = parts[0]
            address = BitcoinUtils.convert_pubkey_to_address(pubkey)
            balance = float(vout['value'])
            return address, balance
        else:
            address = script['address'] if 'address' in script else 'Unknown Address'
            balance = float(vout['value']) if 'value' in vout else 0.0
            return address, balance

    @staticmethod
    def get_tx_outputs(tx: dict) -> List[TxOut]:
        vouts: list = tx['vout']
        outputs = list()
        for vout in vouts:
            payee, balance = BitcoinUtils.parse_vout(vout)
            outputs.append(TxOut(payee, balance))
        return outputs

    @staticmethod
    def get_tx_inputs(tx: dict) -> List[TxIn]:
        inputs = list()
        if BitcoinUtils.is_coinbase_tx(tx):
            return inputs
        for item in tx['vin']:
            spent_txid: str = item['txid']
            vout_no: int = item['vout']
            spent_tx = BitcoinRPC.get_raw_transaction(spent_txid)
            vouts: list = spent_tx['vout']
            payer, balance = BitcoinUtils.parse_vout(vouts[vout_no])
            inputs.append(TxIn(payer, balance))
        return inputs

    @staticmethod
    def get_spent_txids(tx: dict) -> List[str]:
        txids = list()
        for item in tx['vin']:
            spent_txid: str = item['txid']
            txids.append(spent_txid)
        return txids

    @staticmethod
    def get_latest_txids(block_count: int) -> List[str]:
        txids = list()
        block_hash = BitcoinRPC.get_latest_block_hash()
        for _ in range(block_count):
            block = BitcoinRPC.get_block(block_hash, True)
            txids += block['tx']
        return txids

    @staticmethod
    def get_total_balance(tx: dict) -> float:
        balance = 0.0
        outputs = BitcoinUtils.get_tx_outputs(tx)
        for out in outputs:
            balance += out.balance
        return balance
