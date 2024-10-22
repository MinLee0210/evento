import os
import json
import requests
import glob
import time
import timeit
import statistics
from typing import Callable, Tuple, List
from tqdm import tqdm

# TODO: Adjust based on your setting host
URL = "http://103.20.97.115:8080/search"

def measure_single_inference_time(inference_function: Callable, input_data: any) -> float:
    """Measures the time for a single inference call."""
    start_time = time.perf_counter()
    inference_function(input_data)
    end_time = time.perf_counter()
    return end_time - start_time

def analyze_inference_times(inference_times: List[float]) -> Tuple[float, float, float]:
    """Analyzes inference times and returns statistics."""
    mean = statistics.mean(inference_times)
    stdev = statistics.stdev(inference_times)
    median = statistics.median(inference_times)
    return mean, stdev, median


def analyze_and_print_results(inference_times: List[float]):
    """
    Analyzes inference times and prints a formatted summary of the results.
    """
    mean, stdev, median = analyze_inference_times(inference_times)
    print("Inference Time Analysis:")
    print(f"  Mean: {mean:.4f} seconds")
    print(f"  Standard Deviation: {stdev:.4f} seconds")
    print(f"  Median: {median:.4f} seconds")


def get_data(dir, mode:str='all'): 
    data_packts = os.listdir(dir)
    dataset = []
    dataset_src = []
    if mode == 'all': 
        for packt in data_packts: 
            data_dir = os.path.join(dir, packt)
            dataset_src += glob.glob(f'{data_dir}/*.txt')

    else: 
        data_dir = os.path.join(dir, mode)
        dataset_src += glob.glob(f'./{data_dir}/*.txt')
    for src in dataset_src: 
        data = open(src, 'r').read()
        dataset.append(data)

    return dataset


def inference(query, top_k:int=20, high_performance:str="blip", smart_query:str='plain'): 
    data = {
        'query': query, 
        'top_k': top_k, 
        'high_performance': high_performance, 
        'smart_query': smart_query
    }
    response = requests.post(url=URL, 
                             json=json.dumps(data))
    
    return response.status_code


if __name__ == "__main__": 
    dataset = get_data(dir='./docs/test_query', mode='all')
    top_k = 20
    high_performance = 'blip_des'
    smart_query = 'explore'

    time_responses = []

    for data in tqdm(dataset): 
        time_respone = measure_single_inference_time(inference_function=inference, 
                                                     input_data=data)
        time_responses.append(time_respone)

    analyze_and_print_results(time_responses)