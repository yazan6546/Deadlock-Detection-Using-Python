import numpy as np
import pandas


def main():
    allocation, available, request = read_file()
    print("Note : All indices start from 0.")
    print("So {P1, P5, P3, P2} = [0, 4, 2, 1]\n\n")

    if check_dimensions(allocation, available, request):
        deadlock_detect(allocation, available, request)
    else:
        print("Dimensions are inconsistent!")


def deadlock_detect(allocation, available, request):
    n, m = allocation.shape
    list_deadlocked = []
    work = np.copy(available)
    list_sequence = []
    finish = np.full(n, False, dtype=bool)

    for i in range(n):
        if np.all(allocation[i] == 0):
            finish[i] = True

    found = True

    while found:
        for i in range(n):
            if i == 0:
                found = False

            if (not finish[i]) and (np.all(request[i] <= work)):
                work += allocation[i]
                finish[i] = True
                found = True
                list_sequence.append(i)

    for i in range(n):
        if not finish[i]:
            list_deadlocked.append(i)

    length = len(list_deadlocked)

    if length != 0:
        print("Deadlock detected!")
        print("Deadlocked processes : ")
        print(list_deadlocked)
    else:
        print("No deadlock detected!")
        print("Safe sequence : ")
        print(list_sequence)


def check_dimensions(allocation, available, request):
    n1, m1 = allocation.shape
    n2, m2 = request.shape
    m3 = available.shape[1]

    if (n1 != n2) or (m1 != m2) or (m2 != m3) or (m1 != m3):
        return False
    return True


def read_file():
    df = pandas.read_csv("Allocation.csv")
    allocation = np.delete(df.values, 0, axis=1).astype(int)

    available = pandas.read_csv("Available.csv")
    available = available.values.astype(int)

    df = pandas.read_csv("Request.csv")
    request = np.delete(df.values, 0, axis=1)
    request = request.astype(int)

    return allocation, available, request


if __name__ == "__main__":
    main()
