import requests
import time
import random
import csv

# Azure
# URL = "https://heapsort.azurewebsites.net/api/http_trigger?"

# OpenFaas
URL = "http://20.254.66.18:8080/function/hello-python"


test_cases = [
    {"data": "5,2,3,4,1", "len": 5},  # Valid case
    {"data": "10,20,30", "len": 3},  # Another valid case
    {"data": "1,2,a,4", "len": 4},  # Invalid case (non-integer value)
    {"data": "1,2,3", "len": 5},  # Mismatch between len and data
    {"data": "", "len": 0},  # Edge case (empty input)
    {"data": "100", "len": 1},  # Single number
    {"data": "2,5,1,2,3", "len": 5},  # Repetitive numbers
]


def call_function(data):
    headers = {"Content-Type": "application/json"}
    start_time = time.perf_counter()
    response = requests.post(URL, json=data, headers=headers)
    end_time = time.perf_counter()
    latency = end_time - start_time  # Measure response time
    return response.status_code, response.text, latency


def testing():
    results = []
    for i, test in enumerate(test_cases):
        status, response_text, latency = call_function(test)
        results.append(
            {
                "test": i + 1,
                "status": status,
                "response": response_text,
                "latency": latency,
            }
        )
    for result in results:
        print(
            f"Test {result['test']}: Status={result['status']}, Latency={result['latency']:.4f}s, Response={result['response']}"
        )


def generate_test_case(length, minSize, maxSize):
    data = ",".join(str(random.randint(minSize, maxSize)) for _ in range(length))
    return {"data": data, "len": length}


# increasing length of numbers
def IncreasingLength():
    with open("results/IncreasingLength.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Latency", "Length of Numbers"])

        for i in range(1, 1000):
            test_case = generate_test_case(i, 1, 100)
            status, response_text, latency = call_function(test_case)
            writer.writerow([latency, i])


# start with decreasing length numbers
def DecreasingLength():
    with open("results/DecreasingLength.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Latency", "Length of Numbers"])

        for i in range(1000, 0, -1):
            test_case = generate_test_case(i, 1, 100)
            status, response_text, latency = call_function(test_case)
            writer.writerow([latency, i])


# give it same length over and over.
def SameLength():
    with open("results/SameLength.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Latency", "Length of Numbers"])

        for i in range(1000):
            test_case = generate_test_case(10, 1, 100)
            status, response_text, latency = call_function(test_case)
            writer.writerow([latency, 10])


def SameLengthHeavyComputation():
    with open("results/SameLengthHeavyComputation.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Latency", "Length of Numbers"])

        for i in range(100):
            test_case = generate_test_case(1000, 100000000, 1000000000)
            status, response_text, latency = call_function(test_case)
            writer.writerow([latency, 100000])


# random numbers of length: pretty useless
def RandomLength():
    with open("results/RandomLength.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Latency", "Length of Numbers"])

        for i in range(1000):
            randomLength = random.randint(1, 100)
            test_case = generate_test_case(randomLength, 1, 100)
            status, response_text, latency = call_function(test_case)
            writer.writerow([latency, randomLength])


# cold start heavy computation
def ColdStartHeavyComputation():
    with open("results/ColdStartHeavyComputation.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Latency", "Length of Numbers"])

        test_case = generate_test_case(100000, 10000000, 100000000)
        status, response_text, latency = call_function(test_case)
        writer.writerow([latency, 100000])


# warm start heavy computation
def WarmStartHeavyComputation():
    with open("results/WarmStartHeavyComputation.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Latency", "Length of Numbers"])

        # give it a easy computation first
        test_case = generate_test_case(10, 1, 100)
        status, response_text, latency = call_function(test_case)
        test_case = generate_test_case(100000, 10000000, 100000000)
        status, response_text, latency = call_function(test_case)
        writer.writerow([latency, 100000])


# cold start easy computation
def ColdStartEasyComputation():
    with open("results/ColdStartEasyComputation.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Latency", "Length of Numbers"])

        test_case = generate_test_case(10, 1, 100)
        status, response_text, latency = call_function(test_case)
        writer.writerow([latency, 10])


# warm start easy computation
def WarmStartEasyComputation():
    with open("results/WarmStartEasyComputation.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Latency", "Length of Numbers"])

        # give it a easy computation first
        test_case = generate_test_case(10, 1, 100)
        status, response_text, latency = call_function(test_case)
        test_case = generate_test_case(10, 1, 100)
        status, response_text, latency = call_function(test_case)
        writer.writerow([latency, 10])


# heavy computation, then stop for x amount of time, and heavy computation again. is there a difference?
def HeavyComputationStopHeavyComputation():
    # warm start
    with open(
        "results/HeavyComputationStopHeavyComputation.csv", "w", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["Latency", "Length of Numbers"])

        test_case = generate_test_case(100000, 10000000, 100000000)
        status, response_text, latency = call_function(test_case)
        writer.writerow([latency, 100000])
        time.sleep(10)
        test_case = generate_test_case(100000, 10000000, 100000000)
        status, response_text, latency = call_function(test_case)
        writer.writerow([latency, 100000])


# Uncomment the following line to run the tests
testing()

# Performance Testing
# IncreasingLength()
# time.sleep(10)
# DecreasingLength()
# time.sleep(10)
# SameLength()
# time.sleep(10)
# ColdStartHeavyComputation()
# time.sleep(10)
# WarmStartHeavyComputation()
# time.sleep(10)
# SameLengthHeavyComputation()
# time.sleep(10)
# ColdStartEasyComputation()
# time.sleep(10)
# WarmStartEasyComputation()
# time.sleep(10)
# HeavyComputationStopHeavyComputation()
