# Created by Hannah at 28.05.2024 13:07
import opensim as osim


# class PendulumController:


# def controlFirstJoint(state, ref, Kp, Kv, getErr):
#     xt_0 = getAngleFromJoints('q1', state)
#     xt_1 = 0
#     err = getErr(ref, xt_0)
#     if getErr is None:
#         getErr = err
#     dx = (xt_0 - xt_1) / 0.33
#     xt_1 = xt_0
#     torque = Kp * err - Kv * dx
#     return torque
#

# Создаем пустую модель
model = osim.Model()
model.setName("CylinderPendulum")
model.setAuthors("HannahSavon")
model.setUseVisualizer(True) # отображение в realtime

# Устанавливаем гравитацию
model.setGravity(osim.Vec3(0, -9.8065, 0))

# Входные данные
cylinderMass = 0.1
cylinderLength = 0.5
cylinderDiameter = 0.06

cubeMass = 20.0
cubeLength = 0.2

# Задаем инерцию цилиндра (немного не так, как в дипломе. См скрин в ноушене)
cylinderRadius = cylinderDiameter/2
I_xx = (1/12) * cylinderMass * (3 * cylinderRadius**2 + cylinderLength**2)
I_yy = (1/2) * cylinderMass * cylinderRadius**2
I_zz = I_xx
cylinderInertia = osim.Inertia(I_xx, I_yy, I_zz, 0, 0, 0)

# Создаем первое тело маятника(cylynder)
body1 = osim.Body("body1", cylinderMass, osim.Vec3(0, cylinderLength/2, 0), cylinderInertia)
# Body(<aName>, <aMass>, <aMassCenter>, <aInertia>)
model.addBody(body1)

# Создаем шарнир (Joint) для первого тела
joint1 = osim.PinJoint("joint1",
                       model.getGround(),  # Parent body
                       osim.Vec3(0, 0, 0),  # Location in parent
                       osim.Vec3(0, 0, 0),  # Orientation in parent
                       body1,  # Child body
                       osim.Vec3(0, cylinderLength/2, 0),  # Location in child
                       osim.Vec3(0, 0, 0))  # Orientation in child
model.addJoint(joint1)

# Добавляем координату (Coordinate) для первого шарнира????
coord1 = joint1.updCoordinate()
coord1.setName("angle1")
coord1.setDefaultValue(0.3)  # начальный угол в радианах
coord1.setRangeMin(-3.14)
coord1.setRangeMax(3.14)

# Добавляем геометрический объект для визуализации первого тела
cylinder1 = osim.Cylinder(cylinderDiameter, cylinderLength/2) # размер фигуры
cylinder1.setColor(osim.Vec3(0, 0, 0))  # цвет фигуры
body1.attachGeometry(cylinder1) # добавили фигуру


body2 = osim.Body("body2", cylinderMass, osim.Vec3(0, cylinderLength/2, 0), cylinderInertia)
model.addBody(body2)

joint2 = osim.PinJoint("joint2",
                       body1,  # Parent body
                       osim.Vec3(0, -cylinderLength/2, 0),  # Location in parent
                       osim.Vec3(0, 0, 0),  # Orientation in parent
                       body2,  # Child body
                       osim.Vec3(0, cylinderLength/2, 0),  # Location in child
                       osim.Vec3(0, 0, 0))  # Orientation in child
model.addJoint(joint2)

# Добавляем координату (Coordinate) для первого шарнира????
coord2 = joint2.updCoordinate()
coord2.setName("angle2")
coord2.setDefaultValue(0.5)  # начальный угол в радианах
coord2.setRangeMin(-3.14)
coord2.setRangeMax(3.14)

# Добавляем геометрический объект для визуализации первого тела
cylinder2 = osim.Cylinder(cylinderDiameter, cylinderLength/2) # размер фигуры
cylinder2.setColor(osim.Vec3(0, 2, 0))  # цвет фигуры
body2.attachGeometry(cylinder2) # добавили фигуру

# Задаем инерцию цилиндра (немного не так, как в дипломе. См скрин в ноушене)
I_xx_cube = I_yy_cube = I_zz_cube = (1/6) * cubeMass * cubeLength**2
cubeInertia = osim.Inertia(I_xx_cube, I_yy_cube, I_zz_cube)

# Создаем второе тело маятника
body3 = osim.Body("body3", cubeMass, osim.Vec3(0), cubeInertia)
model.addBody(body3)

# Создаем шарнир (Joint) для второго тела
joint3 = osim.PinJoint("joint3",
                       body2,  # Parent body
                       osim.Vec3(0, -cylinderLength/2, 0),  # Location in parent
                       osim.Vec3(0, 0, 0),  # Orientation in parent
                       body3,  # Child body
                       osim.Vec3(0, 0, 0),  # Location in child
                       osim.Vec3(0, 0, 0))  # Orientation in child
model.addJoint(joint3)

# Добавляем координату (Coordinate) для второго шарнира
coord3 = joint3.updCoordinate()
coord3.setName("angle3")
coord3.setDefaultValue(-0.8)  # начальный угол в радианах
coord3.setRangeMin(-3.14)
coord3.setRangeMax(3.14)

# Добавляем геометрический объект для визуализации второго тела
cube3 = osim.Brick(osim.Vec3(0.2))
cube3.setColor(osim.Vec3(0, 0, 1))  # Задаем цвет для визуализации
body3.attachGeometry(cube3)
#_______________________________________________________________________

# actuatorJoint1 = osim.TorqueActuator()
# actuatorJoint1.setName("joint1 actuator")
# actuatorJoint1.setBodyA(model.getBodySet().get("body1"))
# actuatorJoint1.setBodyB(model.getBodySet().get("body2"))
# actuatorJoint1.setOptimalForce(20)

# 211-230 from 8.1




# Инициализируем модель и создаем систему
state = model.initSystem()

# Создаем менеджер интеграции
manager = osim.Manager(model)
manager.initialize(state)

# Запускаем симуляцию на 25 секунд
final_time = 10.0
state.setTime(0)
manager.integrate(final_time)

# Выводим результирующее состояние
print(f"Final state: {state}")

# Сохраняем модель и состояние
model.printToXML("double_pendulum_model.osim")
