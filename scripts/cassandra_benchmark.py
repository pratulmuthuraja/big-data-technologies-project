import sys
import time
import json

from cassandra.cluster import Cluster
from cassandra.metrics import Metrics

KEYSPACE = "hw7"
TABLENAME = "benchmark"

THREADS = 4
NODES = [
    "10.237.138.103",
    "10.237.138.131",
    "10.237.138.48",
    "10.237.138.116",
    "10.237.138.143",
    "10.237.138.12",
    "10.237.138.125",
    "10.237.138.202"
]


setup = True if sys.argv[1] == "True" else False
operation = sys.argv[2]

cluster = Cluster(
    NODES,
    metrics_enabled=True,
    executor_threads=THREADS
)
session = cluster.connect()



def create_infra(KEYSPACE, TABLENAME):
    # create keyspace
    query = (
        f"CREATE KEYSPACE IF NOT EXISTS {KEYSPACE} WITH""",
        "replication = {'class':'SimpleStrategy','replication_factor':1};"
    )
    session.execute(query);
    session.execute(f"USE {KEYSPACE}");
    # create table
    query = f"CREATE TABLE IF NOT EXISTS {KEYSPACE}.{TABLENAME} (key text PRIMARY KEY, value text);"
    session.execute(query)


# Display initial rows
def print_rows():
    query = f"SELECT * FROM {KEYSPACE}.{TABLENAME}";
    rows = session.execute(query)
    for key, value in rows:
        print(key, " -> ", value)



# Insert query
def insert_row(key, value):
    session.execute(f"INSERT INTO {KEYSPACE}.{TABLENAME} (key, value) VALUES ({key}, {value})")

def lookup_row(key):
    data = session.execute(f"SELECT * FROM {KEYSPACE}.{TABLENAME} WHERE key = {key}")

def remove_row(key):
    session.execute(f"DELETE FROM {KEYSPACE}.{TABLENAME} WHERE key={key} IF EXISTS")

def performance_metrics(start, end):
    ops = cluster.metrics.request_timer['count']
    time_diff = end - start
    throughput = ops/time_diff
    latency = cluster.metrics.request_timer['mean']
    
    performance_dict = {
        "time": time_diff,
        "throughput": throughput,
        "latency": latency
    }
    print(f"Time to execute: {time_diff} secs")
    print(f"Throughput: {throughput} ops/sec")
    print(f"Latency: {latency}s")

    with open("cassandra_bench", "w") as outfile:
        json.dump(performance_dict, outfile)

# Insert 10 random records
def insert():
    start = time.perf_counter()
    file = open('data.txt', 'r')
    lines = file.readlines()
    for line in lines:
        key = line[0:10]
        value = line[11:]
        value = value + "\r"
        insert_row(key, value)
    end = time.perf_counter()
    performance_metrics( start, end)
    return None

def lookup():
    file = open('data.txt', 'r')
    lines = file.readlines()
    start = time.perf_counter()
    for line in lines:
        key = line[0: 10]
        lookup_row(key)
    end = time.perf_counter()
    performance_metrics( start, end)
    return None

def remove():
    file = open('data.txt', 'r')
    lines = file.readlines()
    start = time.perf_counter()
    for line in lines:
        key = line[0:10]
        remove_row(key)
    end = time.perf_counter()
    performance_metrics(start, end)
    return None

def switch_func(value):
    switcher={
        'insert': insert,
        'lookup': lookup,
        'remove': remove,
    }
    switcher.get(value,lambda :'Invalid')()

if(setup == False):
    print("Running: ", operation)
    switch_func(operation)

if(setup == True):
    print("Setting up...")
    create_infra(KEYSPACE, TABLENAME)
    print("Setup complete...")


