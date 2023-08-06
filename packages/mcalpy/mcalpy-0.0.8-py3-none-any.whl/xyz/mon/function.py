import random


def mon(times: int = 1, log: bool = False) -> float:
    """It solves Monty Hall's problem"""
    suc = 0
    fail = 0
    answer = 0
    choice = 0
    Times = 0
    for i in range(times):
        Times += 1
        choice = random.randint(1,3)
        answer = random.randint(1,3)
        if choice == 1:
            if answer == 2 or answer == 3:
                suc += 1
            else:
                fail += 1
        elif choice == 2:
            if answer == 1 or answer == 3: 
                suc += 1
            else:
                fail += 1
        elif choice == 3:
            if answer == 1 or answer == 2:
                suc += 1
            else:
                fail += 1
        if log is True:
            print(f"{i+1}: {suc / Times * 100}, success: {suc}, fails: {fail}")
    return suc / Times * 100