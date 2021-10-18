from typing import Text

from pymongo import response
import todo_pb2_grpc, todo_pb2
from concurrent import futures
import grpc
import time
import threading
import pymongo
import os
import asyncio


async def run():
    counter = 0
    pid = os.getpid()
    with grpc.insecure_channel("localhost:9999") as channel:
        stub = todo_pb2_grpc.TodoStub(channel=channel)
        while True:
            try:
                start = time.time()
                void_param = todo_pb2.voidParam()
                response = stub.readTodos(void_param, None, None)
                body = response.items
                # print(body)
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                channel.unsubscribe(close)
                exit()

def close(channel):
    channel.close()

def main():
    asyncio.run(run())


if __name__=="__main__":
    asyncio.run(run())
    # await main()