# Теор рассчеты по маятнику

import numpy as np
import matplotlib.pyplot as plt


# метод разверток (пришлет ВЮ)
# поиграть с параметрами (скользящие окна)



# Параметры модели маятника
length = 1.0  # Длина маятника
g = 9.8  # Ускорение свободного падения


# Функция для расчета угла и скорости маятника
def pendulum_motion(theta0, omega0, dt, steps):
    theta = np.zeros(steps)
    omega = np.zeros(steps)
    time = np.zeros(steps)

    theta[0] = theta0
    omega[0] = omega0

    for i in range(1, steps):
        alpha = -g / length * np.sin(theta[i - 1])
        omega[i] = omega[i - 1] + alpha * dt
        theta[i] = theta[i - 1] + omega[i] * dt
        time[i] = time[i - 1] + dt

    return time, theta


# Начальные условия
theta0 = np.pi / 4  # Начальный угол
omega0 = 0.0  # Начальная скорость
dt = 0.01  # Временной шаг
steps = 1000  # Количество шагов

# Расчет движения маятника
time, theta = pendulum_motion(theta0, omega0, dt, steps)

# Визуализация движения маятника
# для отображения в gui нужна другая версия((
plt.plot(time, theta)
plt.title("Pendulum Motion")
plt.xlabel("Time (s)")
plt.ylabel("Theta (radians)")
plt.grid(True)
plt.show()
