import asyncio
import simpy
import socket
from _thread import *
import threading
from simpy.util import start_delayed


def bool_check(env, process_name, duration):
    yield env.timeout(duration)
    print(process_name, env.now)


def sub(env, process_name, duration, conn):
    start_time = env.now
    while env.now - start_time < duration:
        yield env.timeout(0.1)
        json_string = '{"name": "' + process_name + '", "value1": ' + str("%.3f" % (env.now / 2)) \
                      + ', "value2": ' + ("%.3f" % env.now) + '}'
        conn.send(bytes(json_string, "utf-8"))
        print(process_name, env.now)


def continuous_process(env, process_name, start_time, duration, conn):
    sub_proc = yield start_delayed(env, sub(env, process_name, duration, conn), delay=start_time)
    ret = yield sub_proc
    return ret


async def tcp_echo_client(message):
    print("this is a test 1")
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 1234)
    print("This is a test 2")

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')


async def run_simulator():
    HOST = '127.0.0.1'  # hostname
    PORT = 1234

    socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_connection.connect((HOST, PORT))
    env = simpy.rt.RealtimeEnvironment(factor=0.5)
    env.process(bool_check(env, "Check TVC", 5))
    env.process(bool_check(env, "Software Setup Check", 10))
    env.process(continuous_process(env, "M1D Hydraulic Pressurization", 20, 20, socket_connection))
    env.process(bool_check(env, "M1D Check", 30))
    env.process(continuous_process(env, "LOX Fueling", 30, 20, socket_connection))
    env.process(bool_check(env, "RCS Check", 40))
    env.run(until=60)


async def main():
    loop.create_task(tcp_echo_client("Hello World"))
    loop.create_task(run_simulator())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())