# Created by Hannah at 13.06.2024 19:01
import  opensim

model = opensim.Model("simple_model.osim")
for force in model.getForceSet():
    print(force.getName())
for name, muscle in model.getMuscles():
    print(name, muscle.get_max_isometric_force())