import sys, os
from random import randrange, randint
from user import NodeUser
from threading import Thread 
from time import time

n_users = 1
n_operations = 1000 #each

verbose = False

MAX_INT_ID = 2**32

user_threads = []

def run_user(user_id, users_success_tracker):
    user = NodeUser(verbose=verbose)
    sentKeys = []
    success = True
    print(f"User {user_id} started.")
    
    for i in range(n_operations):
        key = randrange(0, MAX_INT_ID)
        value = str(key)
        user.put(key, value)
        print(f"User {user_id} sent key {key} with value {value}.")
        sentKeys.append((key,value))
    
    input("Tecle enter para recuperar as chaves.")

    for key,value in sentKeys:
        retorno = user.get(key)
        if retorno != value: 
            print(f"User {user_id} - Op. nº{i}: ERROR!!!")
            print(f"User {user_id} - Op. nº{i}: Expected: '{value}', Actual: '{retorno}'")
            success = False
            break
    
    if success: print(f"User {user_id}: Succesfully realized {n_operations} put and get operations")
    users_success_tracker[user_id] = success



def main():
    print(f"Testing for {n_users} users.... ")
    users_success_track = [None]*n_users

    for i in range(n_users):
        t = Thread(target=run_user, args=(i,users_success_track))
        t.start()
        user_threads.append(t)
    for p in user_threads:
        p.join()

    print("Test finished.")
    if all(users_success_track): print(f"All tests passed for {n_users} users.")
    else: print(f"{users_success_track.count(True)}/{n_users} user tests passed.")

if __name__ == '__main__':
    start_time = time()
    try:
        main()
        print("--- %.5s seconds ---" % (time() - start_time))
    except KeyboardInterrupt:
        print('Interrupted')
        print("--- %.5s seconds ---" % (time() - start_time))
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)