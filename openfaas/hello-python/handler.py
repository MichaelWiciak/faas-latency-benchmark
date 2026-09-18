import json


def handle(event, context):
    try:
        req_body = json.loads(event.body)
    except ValueError:
        return "Invalid JSON received.", 400

    data = req_body.get("data")
    length = req_body.get("len")

    if not data or not length:
        return "Please provide both 'data' and 'len' in the request body.", 400

    data_list = data.split(",")
    if len(data_list) != int(length):
        return "The length of 'data' does not match 'len'.", 400

    try:
        sorted_data = heap_sort(list(map(int, data_list)))
    except ValueError:
        return "Data contains non-integer values.", 400

    return f"Sorted data: {sorted_data}", 200


# Heap sort
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[i] < arr[left]:
        largest = left

    if right < n and arr[largest] < arr[right]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

    return arr
