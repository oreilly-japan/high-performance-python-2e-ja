import argparse
import random
import string
import time

import requests


def generate_urls(base_url, num_urls):
    """
    We add random characters to the end of the URL to break any caching
    mechanisms in the requests library or the server
    """
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))


def run_experiment(base_url, num_iter=1000):
    response_size = 0
    for url in generate_urls(base_url, num_iter):
        response = requests.get(url)
        response_size += len(response.text)
    return response_size


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    delay = 100
    num_iter = 1000
    base_url = f"http://127.0.0.1:{args.port}/add?name=serial&delay={delay}&"

    start = time.time()
    result = run_experiment(base_url, num_iter)
    end = time.time()
    print(f"Result: {result}, Time: {end - start}")
