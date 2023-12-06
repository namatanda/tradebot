#bubble sort
def sort(arr):
    
    """
    Sorts the given array in ascending order using the bubble sort algorithm.

    Parameters:
        arr (list): The list of elements to be sorted.

    Returns:
        list: The sorted list in ascending order.
    """

    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

#Genetate the main
if __name__ == 'main':
    print(sort([5, 2, 9, 1, 7]))