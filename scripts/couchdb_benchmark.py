import time
import couchdb


try:
    couch = couchdb.Server('https://admin:password@node1:5984/')
    print("Connected successfully!!!")
except:
    print("Could not connect to couchDB")
    exit()

db = couch['mydb']


def read_file(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()
    return lines


def insert_row(key, value, database):
    doc = {'key': key, "value": value}
    ins_id = database.save.(doc)[0]
    return ins_id



def look_up(inserted_id, database):
    doc = database[inserted_id]
    return doc



def delete_doc(inserted_id, database):
    doc = database[inserted_id]
    database.delete(doc)


def performance(number_of_operations, start, end):
    time_elapsed = end - start
    throughput = number_of_operations / (time_elapsed / (10 ** 9))
    latency = (time_elapsed / (10 ** 6)) / number_of_operations
    print("Time to execute: ", time_elapsed / (10 ** 9), "secs")
    print("Throughput: ", throughput, "ops/sec")
    print("Latency: ", latency, "ms")


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

