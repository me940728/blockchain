import importlib.util
import sys, os
from flask import Flask, jsonify, request, Response
from importlib.metadata import version # 버전 확인용 라이브러리 임포트
#flask_version = version("flask")
#print(f"Flask version: {flask_version}")

'''
'24.6.3 [INIT] 최별규
 - 싱글노드 상태에서 블록체인 테스트를 위한 파이썬 파일
[log] python 3.8 based
1) conda env blockchain
2) conda install flask
'''
#=================================[ 모듈 경로 설정 ] ================================
module_name = "Blockchain"
module_path = os.path.join(os.path.dirname(__file__), 'modules', 'Blockchain.py')
#=================================================================================
#=================================[ 모듈 불러 오기 ] =================================
spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)
#==================================================================================

# Single Node Operation Test Code
# [INIT] 24.5.31 최별규 => 단일 노드 운영 테스트 코드
Blockchain = module.Blockchain
blockchain = Blockchain

# 테스트 운영할 노드의 key 값 설정(node_identifier, 노드 IP + 포트 번호)
my_ip = '0.0.0.0'
my_port = '50001'
node_identifier = 'node_' + my_port
mine_owner = 'master'
mine_profit = 0.1

# app 정의
app = Flask(__name__)

# 24.6.3 최별규 -> 블록체인 정보 조회
# request : -
# response : 블록체인 내 블록 길이, 정보
@app.route('/chain', methods=['GET'])
def full_chain():
    print("chain info requested")
    response = {
        'chian' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response), 200

# 24.6.3 최별규 -> 신규 거래 추가
# request : json {'sender' : , 'recipient' : , 'amount' : } 3개 인자는 필수임
# response : 요청 이상 => 400, 요청 이상없고 블록에 거래 내역 추가시 => 201
@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    print("new transaction => " , values)
    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'missing values', 400
    
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message' : 'Transaction will be added to Block {%s}' %index}
    return jsonify(response), 201

# 24.6.3 최별규 -> 채굴
# request : 
# response : 채굴 성공시 200
@app.route('/mine', methods=['GET'])
def mine():
    print("MINING STARTED")
    last_block = blockchain.last_block # 마지막 블록 부름
    last_proof = last_block['nonce'] # 마지막 블록의 nonce 값 가져옴
    proof = blockchain.pow(last_proof) # 마지막 블록읜 nonce 값으로 작업 증명 시도
    
    blockchain.new_transaction(
        sender = mine_owner,
        recipient=node_identifier,
        amount = mine_profit # coinbase transaction
    )
    
    previos_hash = blockchain.hash(last_block) # 마지막 블록을 해시함
    block = blockchain.new_block(proof, previos_hash) # 마지막 블록의 해시 정보를 검증 및 블록에 생성함
    print("MINING FINISHED")
    
    response = {
        'message' : 'new block found',
        'index' : block['index'],
        'transaction' : block['transaction'],
        'nonce' : block['nonce'],
        'previos_hash' : block['previos_hash']
    }
     
    return jsonify(response), 200 # 성공 시 200 리턴

# 노드 운영 => 노드의 ip 정보, port 정보 활용
if __name__ == '__main__':
    app.run(host = my_ip, port = my_port)
'''
# 실행 테스트
if __name__ == "__main__":
    obj = blockchain()
    obj.module_test()
'''
