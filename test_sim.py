import simpy
import socket
from simpy.util import start_delayed


def bool_check(env, process_name, duration):
    yield env.timeout(duration)
    print(process_name, env.now)


def sub(env, process_name, duration):
    start_time = env.now
    while env.now - start_time < duration:
        yield env.timeout(0.1)
        socket_connection.send(bytes(str("%.3f" % env.now), "utf-8"))
        print(process_name, env.now)


def continuous_process(env, process_name, start_time, duration):
    sub_proc = yield start_delayed(env, sub(env, process_name, duration), delay=start_time)
    ret = yield sub_proc
    return ret


HOST = '127.0.0.1' # hostname
PORT = 1234

socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_connection.connect((HOST, PORT))


env = simpy.rt.RealtimeEnvironment(factor=0.2)
env.process(bool_check(env, "Check TVC", 5))
env.process(bool_check(env, "Software Setup Check", 10))
env.process(continuous_process(env, "M1D Hydraulic Pressurization", 20, 20))
env.process(bool_check(env, "M1D Check", 30))
env.process(continuous_process(env, "LOX Fueling", 30, 20))
env.process(bool_check(env, "RCS Check", 40))
env.run(until=60)
