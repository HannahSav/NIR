# Created by Hannah at 11.06.2024 13:40

import opensim as osim
import math

# class PendulumController:

if __name__ == '__main__':
    gravity = osim.Vec3(0, -9.8065, 0)
    init_time = 0
    end_time = 40

    pendulum_model = osim.Model()
    pendulum_model.setName("Pendulum")
    pendulum_model.setAuthors("Hannah Savon")
    pendulum_model.setUseVisualizer(True)
    pendulum_model.setGravity(gravity)

    # ground = pendulum_model.getBodySet()
    # ground = pendulum_model.get_ground()
    # ground = pendulum_model.getGround()
    # pendulum_model.add

    cylinder_mass = 0.5
    cylinder_length = 2.5
    cylinder_diameter = 0.3
    cylinder_dimensions = osim.Vec3(cylinder_diameter, cylinder_length, cylinder_diameter)
    cylinder_mass_center = osim.Vec3(0, cylinder_length/2, 0)
    # кажется, это что-то странное (должно юыть из simTK)
    cylinder_inertia = osim.Inertia(0.1, 0.1, 0.1)

    # Создание первого цилиндра
    # инерцию надо домножить
    first_cylinder = osim.Body("firstCylinder", cylinder_mass, cylinder_mass_center, cylinder_inertia)
    first_cylinder.attachGeometry(osim.Cylinder(cylinder_diameter / 2, cylinder_length / 2))

    # Создание второго цилиндра
    second_cylinder = osim.Body("secondCylinder", cylinder_mass, cylinder_mass_center, cylinder_inertia)
    second_cylinder.attachGeometry(osim.Cylinder(cylinder_diameter / 2, cylinder_length / 2))

    ground = pendulum_model.getGround()
    pin1 = osim.PinJoint("pin1", ground, osim.Vec3(0, 0, 0), osim.Vec3(0, 0, 0), first_cylinder,
                         osim.Vec3(0, cylinder_length / 2, 0), osim.Vec3(0, 0, 0))
    pin2 = osim.PinJoint("pin2", first_cylinder, osim.Vec3(0, -cylinder_length / 2, 0), osim.Vec3(0, 0, 0),
                         second_cylinder, osim.Vec3(0, cylinder_length / 2, 0), osim.Vec3(0, 0, 0))


    # print("fgh")
    # state = pendulum_model.initSystem()
    # state.setTime(init_time)
    # pin1.getCoordinate().setValue(state, math.pi/2)
    # pin2.getCoordinate().setValue(state, math.pi / 2)
    # print("jfj")
    # manager = osim.Manager(pendulum_model)
    # manager.setInitialTime(init_time)
    # manager.setFinalTime(end_time)

    pendulum_model.printToXML("cringe.osim")
    # manager.integrate(state)

    print("finish")