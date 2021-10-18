from multiprocessing import Process
import client

if __name__ == "__main__":
    COUNT = 8
    PROCESSES = {}
    for x in range(COUNT):
        PROCESSES[x] = Process(target=client.main)

    for x in range(COUNT):
        PROCESSES[x].start()