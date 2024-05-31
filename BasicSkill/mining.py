import random
import string
import hashlib

#===============[ Network 문제 * 원격을 가정]=====================
PROBLEM_WORD = "a"
PROBLEM_DIFFICULTY = 1 # 상수 숫자가 높으면 채굴 난이도 올라감
#=============================================================

start_nonce = random.choice(string.ascii_letters) # 초기 난스값 무작위 선택

i = 0
while True:
    nonce = start_nonce + str(i)
    nonce_result = hashlib.sha256((nonce).encode()).hexdigest() # nonce 값을 byte로 인코딩 > 16진수로 변환
    print(i, nonce, nonce_result)
    if nonce_result[0 : PROBLEM_DIFFICULTY] == PROBLEM_WORD * PROBLEM_DIFFICULTY: # 0~(PROBLEM_DIFFICULTY-1) 만큼 문자열 Partial Hash Collision 나야함
        nonce = nonce_result                                                   
        break
    i += 1
    



