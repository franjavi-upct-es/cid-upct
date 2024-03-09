clear all;
close all;

% Crear un array de valores de t desde -10 hasta 10 con un paso de 0.1
t = -12:0.0001:12;

% Crear un array de valores de x
x = 2*exp(j*(t+pi/4));

indices = find(t < 0);
x(indices) = 0;

% Crear el gráfico
figure('Position', [0 0 1000 200])
plot(t, x, "LineWidth", 2)
title('Gráfico de x(t)')
xlabel('t')
ylabel('x(t)')
grid on
