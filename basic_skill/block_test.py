import hashlib
import json
from time import time, localtime, strftime

class Blockchain(object):
    
    def __init__(self):
        self.chain = []
        self.current_transaction = [] # 거래 내역 저장
        self.nodes = set() # 블록체인을 운영하는 노드 정보들
        self.new_block(previous_hash='1', proof=100) # 첫 블록을 생성하는 코드
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1] # -1은 가장 마지막
    
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000" # True or False
    
    def pow(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof): # 유효한 넌스값인지 비교하여 유효한 넌스값이면 올바른 넌스값을 반환한다.
            proof += 1
        return proof
    
    def new_transaction(self, sender, recipient, amount):
        self.current_transaction.append(
            {
                'sender': sender, # 송신자
                'recipient': recipient, # 수신자
                'amount': amount, # 금액
                'timestamp': time() # 작업 시간
            }
        )
        return self.last_block['index'] + 1 # 마지막 블록의 인덱스에 하나 큰 값으로 추가함
    
    def new_block(self, proof, previous_hash=None): # 기본값 None
        block = {
            'index': len(self.chain) + 1, # 블록 번호
            'timestamp': time(), # 생성 시간
            'transaction': self.current_transaction, # 거래 내역
            'nonce': proof, # 검증된 넌스 값
            'previous_hash': previous_hash or self.hash(self.chain[-1]) # None이 아니면 매개변수 그대로 사용 None이면 마지막 체인 값 사용
        }
        self.current_transaction = [] # 작업 중인 거래 내역 초기화
        self.chain.append(block) # 체인에 연결
        return block
    
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print('Last Block: %s' % last_block)
            print('Current Block: %s' % block)
            print("\n-----------\n")

            # Check that the previous hash is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the proof of work is correct
            if not self.valid_proof(last_block['nonce'], block['nonce']):
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

    # 작업 증명 및 블록 추가
    last_proof = blockchain.last_block['nonce']
    proof = blockchain.pow(last_proof)
    blockchain.new_block(proof)

    # 체인 상태 출력
    for block in blockchain.chain:
        print(block)

    # 체인 유효성 검사
    is_valid = blockchain.valid_chain(blockchain.chain)
    print("Is blockchain valid?", is_valid)

    # 의도적으로 체인 변조 후 유효성 검사
    blockchain.chain[1]['transaction'][0]['amount'] = 9999
    is_valid_after_tampering = blockchain.valid_chain(blockchain.chain)
    print("Is blockchain valid after tampering?", is_valid_after_tampering)

def time_test():
    # 현지 시간을 사람이 읽을 수 있는 형식으로 변환
    formatted_time = strftime( '%Y-%m-%d %H:%M:%S', localtime( time() ) )

    print("현재 시간:", formatted_time)
    
time_test()
