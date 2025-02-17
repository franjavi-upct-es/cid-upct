import numpy as np
import matplotlib.pyplot as plt

# Definir el rango de tiempo para la señal continua
t_continuous = np.linspace(-10, 10, 500)  # De 0 a 10 para una buena visualización

# Definir la señal original e^(-t) con restricción x(t) = 0 para t < 3
x_continuous = np.exp(-t_continuous) * (t_continuous >= 3)  # Aplicamos la restricción

# Función para aplicar transformaciones en tiempo continuo
def transform_x_continuous(t, shift=0, reflect=False, exponent=None):
    """Aplica transformaciones a la señal continua x(t) = e^(-t) para t >= 3"""
    if exponent is not None:
        if reflect:
            t_transformed = -exponent * t + shift  # Reflexión y desplazamiento
        else:
            t_transformed = exponent * t - shift  # Solo desplazamiento
        condition = t>=3 / abs(exponent)
    else:
        if reflect:
            t_transformed = -t + shift  # Reflexión y desplazamiento
        else:
            t_transformed = t - shift  # Solo desplazamiento
        condition = t_transformed >= 3
    # Evaluar la nueva señal
    x_transformed = np.exp(-t_transformed) * condition
    return x_transformed

plt.figure(figsize=(8, 4))
plt.plot(t_continuous, x_continuous, color="#007aff", linewidth=2)
plt.gca().spines['left'].set_position('zero')
plt.gca().spines['bottom'].set_position('zero')
plt.gca().spines['right'].set_color('none')  # Ocultar el lado derecho
plt.gca().spines['top'].set_color('none')    # Ocultar la parte superior
plt.title(r"$x(t)$")
plt.yticks([])
plt.xticks([i for i in np.arange(-10, 11)])
plt.gca().set_facecolor("none")
plt.gcf().set_facecolor("none")
plt.savefig("Figure 1.png")

# Definir las transformaciones en tiempo continuo
transforms_continuous = [
    ("$x(1 - t)$", transform_x_continuous(t_continuous, shift=1, reflect=True)),
    ("$x(1 - t)+x(2 - t)$", transform_x_continuous(t_continuous, shift=1, reflect=True) + transform_x_continuous(t_continuous, shift=2, reflect=True)),
    ("$x(1 - t)x(2 - t)$", transform_x_continuous(t_continuous, shift=1, reflect=True) * transform_x_continuous(t_continuous, shift=2, reflect=True)),
    ("$x(3t)$", transform_x_continuous(t_continuous, shift=0, reflect=False, exponent=3)),
    (r"$x\left(\dfrac{t}{3}\right)$", transform_x_continuous(t_continuous, shift=4, reflect=False, exponent=1/3)),
]

# Graficar cada transformación en gráficos separados y guardarlas como png
for i, (title, x_trans) in enumerate(transforms_continuous, start=2):
    plt.figure(figsize=(8, 4))
    
    plt.gca().spines['left'].set_position('zero')
    plt.gca().spines['bottom'].set_position('zero')
    plt.gca().spines['right'].set_color('none')  # Ocultar el lado derecho
    plt.gca().spines['top'].set_color('none')    # Ocultar la parte superior
    plt.gca().set_facecolor("none")
    plt.gcf().set_facecolor("none")
    plt.plot(t_continuous, x_trans, label=title, color='#007AFF', linewidth=2)
    plt.xticks([n for n in np.arange(-10, 11)])
    plt.yticks([])
    plt.title(title)
    plt.savefig(f"Figure {i}.png")
    plt.close()
