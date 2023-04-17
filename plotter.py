import sys
import matplotlib.pyplot as plt

USAGE="Usage: python3 plot.py"

def main(args):
    print(USAGE)
    
    nodes = [2, 4, 8]
    cassandra_latency = [1.26, 1.62, 2.43]
    mongodb_latency = [1.77, 1.80, 1.91]
    couchdb_latency = [1.61, 6.78, 12.18]

    cassandra_throughput = [1581, 2491, 2984]
    mongodb_throughput = [562, 721, 3521]
    couchdb_throughput = [1181, 1291, 1090]
    
    x = nodes

    plt.title("Throughput")
    plt.xlabel("# of Nodes")
    plt.ylabel("ops/sec")
      
    plt.plot(x, cassandra_throughput)
    plt.plot(x, mongodb_throughput)
    plt.plot(x, couchdb_throughput)

    plt.legend(["Cassandra", "MongoDB", "CouchDB"])
    plt.savefig('throughput.png')
    plt.figure()


    plt.title("Latency")
    plt.xlabel("# of Nodes")
    plt.ylabel("time (ms)")
      
    plt.plot(x, cassandra_latency)
    plt.plot(x, mongodb_latency)
    plt.plot(x, couchdb_latency)

    # plt.xscale("log")

    plt.legend(["Cassandra", "MongoDB", "CouchDB"])
    plt.savefig('latency.png')
    print("exiting")



if __name__ == "__main__":
    main(sys.argv)

