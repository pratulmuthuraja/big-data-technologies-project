import time
import json

from bson import ObjectId
from pymongo import MongoClient


try:
    client = MongoClient('mongodb://mongo-admin:password@node2:27017/admin?retryWrites=false')
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")
    exit()

db = client.exampleDB


def read_file(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()
    return lines


def insert_row(key, value, database):
    doc = {'key': key, "value": value}
    ins_id = database.exampleCollection.insert_one(doc).inserted_id
    return ins_id



def look_up(inserted_id, database):
    doc = database.exampleCollection.find_one(inserted_id)
    return doc



def delete_doc(inserted_id, database):
    database.exampleCollection.delete_one({'_id': ObjectId(inserted_id)})


def performance(number_of_operations, start, end):
    time_elapsed = end - start
    throughput = number_of_operations / (time_elapsed / (10 ** 9))
    latency = (time_elapsed / (10 ** 6)) / number_of_operations
    performance_dict = {
        "time": time_elapsed / (10 ** 9),
        "throughput": throughput,
        "latency": latency
    }
    print("Time to execute: ", time_elapsed / (10 ** 9), "secs")
    print("Throughput: ", throughput, "ops/sec")
    print("Latency: ", latency, "ms")

    with open("mongo_bench.json", "w") as outfile:
        json.dump(performance_dict, outfile)

def perform_operations():
    print("Inside Perform Operations")
    lines = read_file('data.txt')
    number_of_operations = len(lines)

    start = time.time_ns()
    ins_ids = []

    print("Insertion Operation Started")
    for line in lines:
        key = line[0: 10]
        value = line[10:]
        ins_id = insert_row(key, value, db)
        ins_ids.append(ins_id)
    print("Insertion Operation Completed")

    print("Lookup Operation Started")
    for ins_id in ins_ids:
        doc = look_up(ins_id, db)
    print("Lookup Operation Completed")

    print("Deletion Operation Started")
    for ins_id in ins_ids:
        delete_doc(ins_id, db)
    print("Deletion Operation Completed")

    end = time.time_ns()
    performance(3 * number_of_operations, start, end)


perform_operations()

