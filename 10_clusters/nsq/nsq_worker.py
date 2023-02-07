import json
from functools import partial
from math import sqrt

import nsq


def is_prime(number):
    if number % 2 == 0:
        return False
    for i in range(3, int(sqrt(number)) + 1, 2):
        if number % i == 0:
            return False
    return True


def write_message(topic, data, writer):
    response = writer.pub(topic, data)
    if isinstance(response, nsq.Error):
        print("Error with Message: {}: {}".format(data, response))
        return write_message(data, writer)
    else:
        print("Published Message: ", data)


def calculate_prime(message, writer):
    data = json.loads(message.body)

    prime = is_prime(data["number"])
    data["prime"] = prime
    if prime:
        topic = "prime"
    else:
        topic = "non_prime"

    output_message = json.dumps(data).encode("utf8")
    write_message(topic, output_message, writer)
    message.finish()  # <1>


if __name__ == "__main__":
    writer = nsq.Writer(["127.0.0.1:4150"])
    handler = partial(calculate_prime, writer=writer)
    reader = nsq.Reader(
        message_handler=handler,
        nsqd_tcp_addresses=["127.0.0.1:4150"],
        topic="numbers",
        channel="worker_group_a",
    )
    nsq.run()
