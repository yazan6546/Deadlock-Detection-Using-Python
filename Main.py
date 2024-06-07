import numpy as np
import pandas as pd


def main():
    allocation, available, request = read_file()
    print("Note : All indices start from 0.")
    print("So {P1, P5, P3, P2} = [0, 4, 2, 1]\n\n")

    if check_dimensions(allocation, available, request):
        deadlock_detect(allocation, available, request)
    else:
        print("Dimensions are inconsistent!")


def deadlock_detect(allocation, available, request):
    """
    Detects deadlock in a system using the Banker's algorithm.

    The function checks if there is a deadlock by simulating resource allocation and request processes.
    It identifies processes that are deadlocked and provides a safe sequence if no deadlock is detected.

    Args:
        allocation (numpy.ndarray): 2D array representing the allocation matrix.
        available (numpy.ndarray): 1D array representing the available resources.
        request (numpy.ndarray): 2D array representing the request matrix.

    Returns:
        None
    """
    # Number of processes and resources
    n, m = allocation.shape

    # List to store indices of deadlocked processes
    list_deadlocked = []

    # Work vector to keep track of available resources
    work = np.copy(available)

    # List to store the safe sequence of processes
    list_sequence = []

    # Finish array to indicate if a process can finish
    finish = np.full(n, False, dtype=bool)

    # Mark processes with zero allocation as finished
    for i in range(n):
        if np.all(allocation[i] == 0):
            finish[i] = True

    # Variable to indicate if a process was found in the current iteration
    found = True

    # Loop to find processes that can complete
    while found:
        found = False  # Assume no process can complete

        for i in range(n):
            # Check if the process can complete
            if (not finish[i]) and (np.all(request[i] <= work)):
                # If it can, simulate it finishing by adding its allocation to work
                work += allocation[i]
                finish[i] = True
                found = True
                list_sequence.append(i)

    # Identify deadlocked processes
    for i in range(n):
        if not finish[i]:
            list_deadlocked.append(i)

    # Output the result
    if list_deadlocked:
        print("Deadlock detected!")
        print("Deadlocked processes:")
        print(list_deadlocked)
    else:
        print("No deadlock detected!")
        print("Safe sequence:")
        print(list_sequence)


def check_dimensions(allocation, available, request):
    """
    Checks if the dimensions of the allocation, available, and request arrays are compatible.

    The function verifies that:
    - The number of rows in the allocation and request arrays are the same.
    - The number of columns in the allocation and request arrays are the same.
    - The number of columns in the available array matches the number of columns in the request array.
    - The number of columns in the allocation array matches the number of columns in the available array.

    Args:
        allocation (numpy.ndarray): 2D array representing allocation data.
        available (numpy.ndarray): 1D array representing available resources data.
        request (numpy.ndarray): 2D array representing request data.

    Returns:
        bool: True if all dimensions are compatible, False otherwise.
    """
    # Get the number of rows and columns for the allocation array
    n1, m1 = allocation.shape
    # Get the number of rows and columns for the request array
    n2, m2 = request.shape
    # Get the number of columns for the available array
    m3 = available.shape[1]

    # Check if the dimensions are compatible
    if (n1 != n2) or (m1 != m2) or (m2 != m3) or (m1 != m3):
        return False
    return True


def read_file():
    """
    Reads and processes allocation, available, and request data from CSV files.

    The function reads three CSV files:
    - "Inputs/Allocation.csv": Contains allocation data.
    - "Inputs/Available.csv": Contains available resources data.
    - "Inputs/Request.csv": Contains request data.

    It processes the data by removing the first column from the allocation and request data,
    and converting all values to integers.

    Returns:
        tuple: A tuple containing three numpy arrays:
            - allocation: 2D array of allocation data without the first column.
            - available: 1D array of available resources data.
            - request: 2D array of request data without the first column.
    """
    # Read the allocation data from the CSV file
    df = pd.read_csv("Inputs/Allocation.csv")
    # Remove the first column and convert the remaining values to integers
    allocation = np.delete(df.values, 0, axis=1).astype(int)

    # Read the available resources data from the CSV file
    available = pd.read_csv("Inputs/Available.csv")
    # Convert the data to integers
    available = available.values.astype(int)

    # Read the request data from the CSV file
    df = pd.read_csv("Inputs/Request.csv")
    # Remove the first column and convert the remaining values to integers
    request = np.delete(df.values, 0, axis=1).astype(int)

    return allocation, available, request


if __name__ == "__main__":
    main()
