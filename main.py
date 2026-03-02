import random
import timeit
import matplotlib.pyplot as plt

def merge(arr, l, m, r):
    L = arr[l:m+1]
    R = arr[m+1:r+1]

    i = j = 0
    k = l

    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1

    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1


def mergeSort(arr, l, r):
    if l < r:
        m = (l + r) // 2
        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)


def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def hybridMergeSort(arr, l, r, k):
    if r - l + 1 <= k:
        for i in range(l + 1, r + 1):
            key = arr[i]
            j = i - 1
            while j >= l and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
    else:
        if l < r:
            m = (l + r) // 2
            hybridMergeSort(arr, l, m, k)
            hybridMergeSort(arr, m + 1, r, k)
            merge(arr, l, m, r)


sizes = [25, 50, 75, 100, 200, 500, 1000, 10000, 25000]

merge_times = []
insertion_times = []

for n in sizes:
    print(f"Testing n = {n}")

    if n <= 1000:
        repetitions = 100
    elif n <= 10000:
        repetitions = 10
    else:
        repetitions = 1

    def test_merge():
        arr = [random.randint(0, 1000000) for _ in range(n)]
        mergeSort(arr, 0, len(arr) - 1)

    merge_time = timeit.timeit(test_merge, number=repetitions) / repetitions
    merge_times.append(merge_time)

    def test_insertion():
        arr = [random.randint(0, 1000000) for _ in range(n)]
        insertionSort(arr)

    insertion_time = timeit.timeit(test_insertion, number=repetitions) / repetitions
    insertion_times.append(insertion_time)

    print(f"Merge Sort: {merge_time:.6f} sec")
    print(f"Insertion Sort: {insertion_time:.6f} sec")
    print("/n" * 40)


plt.figure()

plt.plot(sizes, merge_times, label="Merge Sort")
plt.plot(sizes, insertion_times, label="Insertion Sort", color="green")

plt.xlabel("Input Size (n)")
plt.ylabel("Time (seconds)")
plt.title("Merge Sort vs Insertion Sort (Measured with timeit)")

plt.legend(loc="center right")

plt.xscale("log")
plt.yscale("log")

plt.savefig("merge_vs_insertion.png", dpi=300, bbox_inches="tight")

plt.show()