import opensim as osim

# Создаем пустую модель
model = osim.Model()
model.setName("DoublePendulum")

# Устанавливаем гравитацию
model.setGravity(osim.Vec3(0, -9.81, 0))

# Создаем первое тело маятника
body1 = osim.Body("body1", 1.0, osim.Vec3(0), osim.Inertia(1))
model.addBody(body1)

# Создаем шарнир (Joint) для первого тела
joint1 = osim.PinJoint("joint1",
                       model.getGround(),  # Parent body
                       osim.Vec3(0, 0, 0),  # Location in parent
                       osim.Vec3(0, 0, 0),  # Orientation in parent
                       body1,  # Child body
                       osim.Vec3(0, 1, 0),  # Location in child
                       osim.Vec3(0, 0, 0))  # Orientation in child
model.addJoint(joint1)

# Добавляем координату (Coordinate) для первого шарнира
coord1 = joint1.updCoordinate()
coord1.setName("angle1")
coord1.setDefaultValue(0.1)  # начальный угол в радианах
coord1.setRangeMin(-3.14)
coord1.setRangeMax(3.14)

# Добавляем геометрический объект для визуализации первого тела
sphere1 = osim.Sphere(0.05)
sphere1.setColor(osim.Vec3(1, 0, 0))  # Задаем цвет для визуализации
body1.attachGeometry(sphere1)

# Создаем второе тело маятника
body2 = osim.Body("body2", 1.0, osim.Vec3(0), osim.Inertia(1))
model.addBody(body2)

# Создаем шарнир (Joint) для второго тела
joint2 = osim.PinJoint("joint2",
                       body1,  # Parent body
                       osim.Vec3(0, 0, 0),  # Location in parent
                       osim.Vec3(0, 0, 0),  # Orientation in parent
                       body2,  # Child body
                       osim.Vec3(0, 1, 0),  # Location in child
                       osim.Vec3(0, 0, 0))  # Orientation in child
model.addJoint(joint2)

# Добавляем координату (Coordinate) для второго шарнира
coord2 = joint2.updCoordinate()
coord2.setName("angle2")
coord2.setDefaultValue(0.1)  # начальный угол в радианах
coord2.setRangeMin(-3.14)
coord2.setRangeMax(3.14)

# Добавляем геометрический объект для визуализации второго тела
sphere2 = osim.Sphere(0.05)
sphere2.setColor(osim.Vec3(0, 0, 1))  # Задаем цвет для визуализации
body2.attachGeometry(sphere2)

# Инициализируем модель и создаем систему
state = model.initSystem()

# Создаем менеджер интеграции
manager = osim.Manager(model)
manager.initialize(state)

# Запускаем симуляцию на 5 секунд
final_time = 25.0
state.setTime(0)
manager.integrate(final_time)

# Выводим результирующее состояние
print(f"Final state: {state}")

# Сохраняем модель и состояние
model.printToXML("double_pendulum_model.osim")
