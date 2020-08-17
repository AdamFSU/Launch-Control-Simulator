import simpy
from simpy.util import start_delayed


def clock(env, name, tick):
    while True:
        print(name, env.now)
        yield env.timeout(tick)


def fill_tank(env, tick):
    while True:
        print("filling tank: ", env.now)
        yield env.timeout(tick)


def bool_check(env, process_name, duration):
    yield env.timeout(duration)
    print(process_name, env.now)


def sub(env, process_name, duration):
    start_time = env.now
    while env.now - start_time < duration:
        yield env.timeout(1)
        print(process_name, env.now)


def continuous_process(env, process_name, start_time, duration):
    sub_proc = yield start_delayed(env, sub(env, process_name, duration), delay=start_time)
    ret = yield sub_proc
    return ret


env = simpy.rt.RealtimeEnvironment(factor=1)
env.process(bool_check(env, "Check TVC", 5))
env.process(bool_check(env, "Software Setup Check", 10))
env.process(continuous_process(env, "M1D Hydraulic Pressurization", 20, 20))
env.process(bool_check(env, "M1D Check", 30))
env.process(continuous_process(env, "LOX Fueling", 30, 20))
env.process(bool_check(env, "RCS Check", 40))
env.run(until=60)
