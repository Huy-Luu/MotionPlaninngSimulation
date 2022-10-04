from StanleyController import StanleyController

class Simulation:
    
    @staticmethod
    def simulate(vehicle, dt, max_sim_time, target_speed, scontroller):
        ai = pid_control(targetr_speed, vehicle.v)
        di, target_idx = scontroller.stanleyControl(vehicle, cx, cy, cyaw, target_idx)
