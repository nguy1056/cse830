import random
import timeit
import matplotlib.pyplot as plt
import numpy as np
import csv

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
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def hybridMergeSort(arr, l, r, k):
    if r - l + 1 <= k:
        subarray = arr[l:r+1]
        insertionSort(subarray)
        arr[l:r+1] = subarray
    else:
        if l < r:
            m = (l + r) // 2
            hybridMergeSort(arr, l, m, k)
            hybridMergeSort(arr, m + 1, r, k)
            merge(arr, l, m, r)


sizes = [25, 50, 75, 100, 200, 500, 1000, 10000, 25000]
k_values = list(range(5, 105, 5))
repetitions = 100  

merge_times = []
insertion_times = []
hybrid_best_times = []
best_k_per_n = {}

for n in sizes:
    print(f"\nTesting n = {n}")
    base_data = [random.randint(0, 1000000) for _ in range(n)]
    
    def test_merge():
        arr = base_data.copy()
        mergeSort(arr, 0, len(arr) - 1)
    merge_time = timeit.timeit(test_merge, number=repetitions) / repetitions
    merge_times.append(merge_time)
    
    def test_insertion():
        arr = base_data.copy()
        insertionSort(arr)
    insertion_time = timeit.timeit(test_insertion, number=repetitions) / repetitions
    insertion_times.append(insertion_time)

    k_times = []
    for k in k_values:
        def test_hybrid():
            arr = base_data.copy()
            hybridMergeSort(arr, 0, len(arr) - 1, k)
        hybrid_time = timeit.timeit(test_hybrid, number=repetitions) / repetitions
        k_times.append(hybrid_time)
    
    best_index = np.argmin(k_times)
    best_k = k_values[best_index]
    best_time = k_times[best_index]
    
    best_k_per_n[n] = best_k
    hybrid_best_times.append(best_time)
    
    print(f"Best k for n={n}: {best_k} (time={best_time:.6f}s)")


plt.figure()
plt.plot(sizes, merge_times, label="Merge Sort")
plt.plot(sizes, insertion_times, label="Insertion Sort")
plt.plot(sizes, hybrid_best_times, label="Hybrid (Best k)")
plt.xlabel("Input Size (n)")
plt.ylabel("Time (seconds)")
plt.title("Merge vs Insertion vs Hybrid Sort")
plt.legend()
plt.xscale("log")
plt.yscale("log")
plt.savefig("hybrid_comparison.png", dpi=300, bbox_inches="tight")
plt.show()


with open("best_k_table.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Input Size (n)", "Best k"])
    for n in sizes:
        writer.writerow([n, best_k_per_n[n]])
print("Table saved to 'best_k_table.csv'")


plt.figure()
best_k_values = [best_k_per_n[n] for n in sizes]
plt.plot(sizes, best_k_values, marker='o')
plt.xlabel("Input Size (n)")
plt.ylabel("Optimal k")
plt.title("Optimal k vs Input Size")
plt.xscale("log")
plt.savefig("best_k_vs_n.png", dpi=300, bbox_inches="tight")
plt.show()