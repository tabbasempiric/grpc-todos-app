from typing import Text
import todo_pb2_grpc, todo_pb2
from concurrent import futures
import grpc
import time
import threading
import pymongo
import json

MONGO_CONFIG = "mongo_config.txt"


def read_mcloud_config(config_file):
    """
    Read Atlas Cloud configuration
    """

    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf


MONGO_CONFIG = read_mcloud_config(MONGO_CONFIG)


class Todo(todo_pb2_grpc.TodoServicer):
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(MONGO_CONFIG["CONNECT"])
        self.db = self.client.todos
        self.Todo = {}
        self.request_count = 0
        self.timer = time.time()
        super().__init__()

    def readTodos(self, request, context):
        todos_list: list = []
        todos = self.db.todos.find()
        for next in todos:
            one_todo = todo_pb2.TodoItem(id=str(next["_id"]), text=next["action"])
            todos_list.append(one_todo)
        self.request_count +=1
        if self.request_count % 1000 == 0:
            print(f'total requests served : {self.request_count}, time per 1000 : {time.time() - self.timer}')
            self.timer = time.time()
        return todo_pb2.TodoItems(items=todos_list)

    def createTodo(self, request, context):
        return super().createTodo(request, context)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=500))
    todo_pb2_grpc.add_TodoServicer_to_server(Todo(), server=server)
    server.add_insecure_port('[::]:9999')
    server.start()
    try:
        while True:
            print(f'Server on: threads running {threading.active_count()}')
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("Keyboard interrupt!\n")
        server.stop(grace=1)


if __name__ == "__main__":
    serve()
