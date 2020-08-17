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


def sub(env):
    while env.now < 30:
        yield env.timeout(1)
        print("fueling tank", env.now)


def parent(env):
    sub_proc = yield start_delayed(env, sub(env), delay=20)
    ret = yield sub_proc
    return ret


env = simpy.rt.RealtimeEnvironment(factor=1)
# env.run(env.process(sub(env)))
env.process(bool_check(env, "Check TVC", 5))
env.process(bool_check(env, "Software Setup Check", 10))
env.process(parent(env))
env.process(bool_check(env, "M1D Check", 30))
env.run(until=40)

# env.process(fill_tank(env, 0.5))
#
# env.process(bool_check(env, "Final Setup Check", 10))
# env.run(until=60)
