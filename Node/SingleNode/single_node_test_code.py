import importlib.util
import sys, os
'''
싱글노드 상태에서 블록체인 테스트를 위한 파이썬 파일 입니다. 
conda env blockchain
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
#=================================================================================
# Single Node Operation Test Code
# [INIT] 24.5.31 최별규 => 단일 노드 운영 테스트 코드
Blockchain = module.Blockchain
blockchain = Blockchain

if __name__ == "__main__":
    obj = blockchain()
    obj.module_test()
