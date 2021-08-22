from random import randrange
from user import NodeUser

for _ in range(1000):
    node = NodeUser()
    key = randrange(0, 2**32)
    value = str(key)
    node.put(key, value)
    retorno = node.get(key)
    if retorno != value: 
        print("ERRO!!!")
        break