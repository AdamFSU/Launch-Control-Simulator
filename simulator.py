import simpy.rt
import random
import statistics

class Falcon9(object):
    def __init__(self, env):
        self.env = env
        # start the launch process everytime an instance is created
        self.action = env.process(self.launch())

    def launch(self):
        yield self.env.process(self.bool_process(env, "Starting Launch", 5))
        yield self.env.process(self.bool_process(env, "TVC check", 5))
        yield self.env.process(self.bool_process(env, "Flight Software Setup Complete", 5))
        yield self.env.process(self.bool_process(env, "M1D Trim Valve Setup Complete", 45))

    def bool_process(self, env, process_name, duration):
        print(process_name, env.now)
        yield self.env.timeout(duration)

# def bool_check(env):
#     print("T-10:00")
#     yield env.timeout(10)
#     print("Flight Software Final Setups complete", "\tT-09:50")
#     yield env.timeout(5)
#     print("TEA-TEB Ignition System Setup", "\tT-09:45")
#     print("Stage 2 Transmitter Re-Activation", "\tT-09:45")
#     yield env.timeout(45)
#     print("M1D Trim Valve Setup Complete", "\tT-09:00")
#
# def bool_check_gen(env):
#     print("T-10:00")
#     while True:


env = simpy.rt.RealtimeEnvironment(factor=1)
# env.process(bool_check(env))
f9 = Falcon9(env)
env.run(until=61)
