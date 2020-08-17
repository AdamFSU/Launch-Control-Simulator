import ast
import simpy
import random
import statistics
import socket


class Falcon9(object):
    def __init__(self, env):
        HOST = '127.0.0.1' # hostname
        PORT = 1234

        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_connection.connect((HOST, PORT))
            # self.socket_connection.sendall(b'Hello, world')
        #     data = self.socket_connection.recv(1024)
        #
        # print('Received', repr(data))

        self.env = env
        # start the launch process everytime an instance is created
        self.action = env.process(self.launch_process_reader("list_dict.txt"))

    def launch_process_reader(self, file_name):
        for dic in open(file_name, "r"):
            data = ast.literal_eval(dic)
            yield self.env.process(self.process_manager(env, data["name"], data["duration"], data["type"]))
            # print(data["name"])

    def process_manager(self, env, process_name, duration, process_type):
        if process_type == 1:
            # process_boolean_check()
            yield env.process(self.process_boolean_check(env, process_name, duration))
        elif process_type == 2:
            # process_asynchronous_integer_check()
            yield env.process(self.process_asynchronous_integer_check(env, process_name, duration))

    def process_boolean_check(self, env, process_name, duration):
        print(process_name, env.now)
        yield self.env.timeout(duration)

    def process_asynchronous_integer_check(self, env, process_name, duration):
        # send across socket to Qt
        self.socket_connection.send(bytes("Data to send", "utf-8"))
        print(process_name, " continuous data: ", env.now + 100)
        yield self.env.timeout(1)


# Create a main() function at some point, shouldn't script and do OOP classes together
# Look at realpython tutorial for simpy


env = simpy.rt.RealtimeEnvironment(factor=0.2)
# env.process(bool_check(env))
f9 = Falcon9(env)
env.run(until=180)
