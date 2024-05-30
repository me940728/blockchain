import hashlib
import json
from time import time, localtime, strftime
import random
import requests
from flask import Flask, request, jsonify

class Blockchain(object):
    
    def __init__(self):
        self.chain = []
        self.current_transaction = [] # 거래 내역 저장
        self.nodes = set() # 블록체인을 운영하는 노드 정보들
        self.new_block(previous_hash=1, proof=100) # 첫 블록을 생성하는 코드
    
    # 24.5.27 최별규 -> 해시 암호화 함수 정의
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    # 24.5.27 최별규 -> 마지막 블록 호출 함수 why? 블록의 최근 nonce 값을 가져와서 새로운 nonce 값 찾기위함
    @property
    def last_block(self):
        return self.chain[-1] # -1은 가장 마지막
    
    # 24.5.27 최별규 -> 검증 작업 why? 마지막 넌스와 새로운 넌스를 조합하여 첫 4자리가 0000이면 유효(valid)하다고 판단한다.
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof + proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000" # Ture or False 
    
    # 24.5.27 최별규 -> 작업 증명
    def pow(self, last_proof):
        # 무작위 방식의 채굴
        #proof = random.randint(-1000000, 1000000) # -10만 10만 사이 무작위 정수를 추출
        #while self.valid_proof(last_proof, proof) is False: # 유요한 난스값인지 비교하여 유요한 난스값이면 올바른 난스값을 반환한다.
        #    proof = random.randint(-1000000, 1000000)
        #return proof
        # 증분을 통한 넌스값 채굴
        proof = 0
        while not self.valid_proof(last_proof, proof): # 유효한 넌스값인지 비교하여 유효한 넌스값이면 올바른 넌스값을 반환한다.
            proof += 1
        return proof
    
    # 24.5.27 최별규 -> 거래내역 추가 함수 -> 매번 블록이 생성되기 전까지 지속적으로 예비 블록 내 작업이 append 된다.
    def new_transaction(self, sender, recipient, amount):
        self.current_transaction.append(
            {
                'sender' : sender, # 송신자
                'recipient' : recipient, # 수신자
                'amount' : amount, #금액
                'timestamp' : strftime( '%Y-%m-%d %H:%M:%S', localtime( time() ) ), #작업 시간 기존 time() 1970년 이후 시간으로 가독성 떨어져 수정함
            }
        )
        return self.last_block['index'] + 1 # 마지막 블록의 인덱스에 하나 큰 값으로 추가함
    
    # 24.5.27 최별규 -> 블록추가 
    # -> current_transaction에 거래내역이 추가 됨, 추가는 PoW 작업을 통해 유요한 nonce 값이 찾아졌을 때 신규 불록이 생성된다.
    # -> 블록에 거래내역이 저장되면 current_transaction는 초기화 되어야 한다. 생성된 블록은 객체 체인 리스트에 추가된다.
    def new_block(self, proof, previous_hash=None): # 기본값 None
        block = {
            'index': len(self.chain) + 1, # 블록 번호
            'timestamp': strftime( '%Y-%m-%d %H:%M:%S', localtime( time() ) ), # 생성 시간
            'transaction': self.current_transaction, # 거래 내역
            'nonce': proof, # 검증된 넌스 값
            'previous_hash': previous_hash or self.hash(self.chain[-1]) # None이 아니면 매개변수 그대로 사용 None이면 마지막 체인 값 사용
        }
        self.current_transaction = [] # 작업 중인 거래 내역 초기화
        self.chain.append(block) # 체인에 연결
        return block
    
    # 24.5.27 최별규 -> 블록 검증
    # -> 블록이 이상없는 검증 해야함 마지막 생성된 블록의 해시값이랑 그전 블록을 해시한 값을 비교하여 변동된 것은 없는지 확인함 
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1
        
        while current_index < len(chain):
            block = chain[current_index]
            print('Last Block: %s' % last_block)
            print('Current Block: %s' % block)
            print("\n-----------\n")
            
            if block['previous_hash'] != self.hash(last_block):
                return False

            last_block = block
            current_index += 1
        return True
# 테스트 코드 작성
def test_blockchain():
    # 블록체인 객체 생성
    blockchain = Blockchain()

    # 제네시스 블록 확인
    print("Genesis Block:", blockchain.chain[0])

    # 새로운 거래 추가
    blockchain.new_transaction(sender="Alice", recipient="Bob", amount=50)
    blockchain.new_transaction(sender="Bob", recipient="Charlie", amount=25)
    blockchain.new_transaction(sender="Choi", recipient="Charlie", amount=30)

    # 작업 증명 및 블록 추가
    last_proof = blockchain.last_block['nonce']
    proof = blockchain.pow(last_proof)
    blockchain.new_block(proof)

    # 체인 상태 출력
    for block in blockchain.chain:
        print("Block : %s" %block, '\n')

    # 체인 유효성 검사
    is_valid = blockchain.valid_chain(blockchain.chain)
    print("Is blockchain valid?", is_valid)

    # 의도적으로 체인 변조 후 유효성 검사
    print('blockchain.chain leng : %s' % len( blockchain.chain), '\n')
    print('blockchain.chain val : \n %s' % blockchain.chain, '\n' )
    
    blockchain.chain[1]['transaction'][2]['amount'] = 9999 # Choi 의 거래가격 위조
    print('\n')
    current_chain = hashlib.sha256(json.dumps(blockchain.chain[-1], sort_keys=True).encode() ).hexdigest()
    last_chain =  blockchain.chain[-1][2]
    print('Err : %s')

if __name__ == "__main__":
    test_blockchain()