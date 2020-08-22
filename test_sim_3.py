import asyncio
import simpy
import socket
from _thread import *
import threading
from simpy.util import start_delayed


def bool_check(env, process_name, duration):
    yield env.timeout(duration)
    print(process_name, env.now)


def sub(env, process_name, duration):
    start_time = env.now
    while env.now - start_time < duration:
        yield env.timeout(0.1)


def continuous_process(env, process_name, start_time, duration):
    sub_proc = yield start_delayed(env, sub(env, process_name, duration), delay=start_time)
    ret = yield sub_proc
    return ret


async def tcp_echo_client():
    print("this is a test 1")
    reader, writer = await asyncio.open_connection('127.0.0.1', 1234)
    print("This is a test 2")

    data = await reader.read()
    print(f'Received: {data.decode()!r}')
    print("This is a test 3")

    print("close the connection")
    writer.close()
    await writer.wait_closed()


async def run_simulator():
    env = simpy.rt.RealtimeEnvironment(factor=0.2)
    env.process(bool_check(env, "Check TVC", 5))
    env.process(bool_check(env, "Software Setup Check", 10))
    env.process(continuous_process(env, "M1D Hydraulic Pressurization", 20, 20))
    env.process(bool_check(env, "M1D Check", 30))
    env.process(continuous_process(env, "LOX Fueling", 30, 20))
    env.process(bool_check(env, "RCS Check", 40))
    env.run(until=60)
    print("simulation finished")


async def main():
    loop.create_task(tcp_echo_client())
    loop.create_task(run_simulator())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
