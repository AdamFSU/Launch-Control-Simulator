import ast
import simpy
import random
import statistics


def launch_process_reader(file_name):
    for dic in open(file_name, "r"):
        data = ast.literal_eval(dic)

        print(data["name"])


class Falcon9(object):
    def __init__(self, env):
        self.env = env
        # start the launch process everytime an instance is created
        self.action = env.process(self.launch_process_reader("list_dict.txt"))

    def launch_process_reader(self, file_name):
        for dic in open(file_name, "r"):
            data = ast.literal_eval(dic)
            yield self.env.process(self.launch(env, data["name"], data["duration"], data["type"]))
            # print(data["name"])

    def launch(self, env, process_string, process_duration, process_type):
        yield self.env.process(self.process_manager(env, process_string, process_duration, process_type))

    def process_manager(self, env, process_name, duration, process_type):
        if process_type == 1:
            # process_boolean_check()
            print(process_name, env.now)
            yield self.env.timeout(duration)
        elif process_type == 2:
            # process_asynchronous_integer_check()
            print("test")


env = simpy.rt.RealtimeEnvironment(factor=1)
# env.process(bool_check(env))
f9 = Falcon9(env)
env.run(until=61)
