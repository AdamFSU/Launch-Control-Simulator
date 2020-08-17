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
    print(process_name, env.now)
    yield env.timeout(duration)


env = simpy.rt.RealtimeEnvironment(factor=1)
start_delayed(bool_check(env, "Check TVC", 5), delay=5)
env.process(bool_check(env, "Check TVC", 5))
env.process(bool_check(env, "Software Setup Check", 10))
env.process(bool_check(env, "M1D Check", 10))
env.process(fill_tank(env, 0.5))
env.process(bool_check(env, "Final Setup Check", 10))
env.run(until=60)
