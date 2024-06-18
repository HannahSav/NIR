import opensim as osim
import math


# Определение переменных
gravity = osim.Vec3(0, -9.8065, 0)
init_time = 0
end_time = 10
cylinder_mass = 0.1
cylinder_length = 0.5
cylinder_diameter = 0.06
cylinder_mass_center = osim.Vec3(0, cylinder_length / 2, 0)
cylinder_inertia = osim.Inertia(0.1, 0.1, 0.1)  # Создаем инерцию вручную с малыми значениями

# Создание модели
osim_pendulum = osim.Model()
osim_pendulum.setName("SimpleDoublePendulum")
osim_pendulum.setAuthors("Example Author")
osim_pendulum.setUseVisualizer(True)
osim_pendulum.setGravity(gravity)

# Создание первого цилиндра
first_cylinder = osim.Body("firstCylinder", cylinder_mass, cylinder_mass_center, cylinder_inertia)
first_cylinder.attachGeometry(osim.Cylinder(cylinder_diameter / 2, cylinder_length / 2))

# Создание второго цилиндра
second_cylinder = osim.Body("secondCylinder", cylinder_mass, cylinder_mass_center, cylinder_inertia)
second_cylinder.attachGeometry(osim.Cylinder(cylinder_diameter / 2, cylinder_length / 2))

# Создание суставов
ground = osim_pendulum.getGround()
pin1 = osim.PinJoint("pin1", ground, osim.Vec3(0, 0, 0), osim.Vec3(0, 0, 0), first_cylinder, osim.Vec3(0, cylinder_length / 2, 0), osim.Vec3(0, 0, 0))
pin2 = osim.PinJoint("pin2", first_cylinder, osim.Vec3(0, -cylinder_length / 2, 0), osim.Vec3(0, 0, 0), second_cylinder, osim.Vec3(0, cylinder_length / 2, 0), osim.Vec3(0, 0, 0))

print("done1")
# Добавление тел и суставов в модель
osim_pendulum.addBody(first_cylinder)
osim_pendulum.addBody(second_cylinder)
osim_pendulum.addJoint(pin1)
osim_pendulum.addJoint(pin2)

# Инициализация модели
state = osim_pendulum.initSystem()

# Настройка начального состояния
state.setTime(init_time)
pin1.getCoordinate().setValue(state, math.pi / 2)
pin2.getCoordinate().setValue(state, math.pi / 2)

# Создание менеджера интеграции и выполнение симуляции
manager = osim.Manager(osim_pendulum)
#  (init_time))
# manager.setFinalTime(end_time)

# Выполнение симуляции
osim_pendulum.printToXML("simple_double_pendulum.osim")
print("done")
manager.integrate(state)

print("Симуляция завершена")
