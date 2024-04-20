clear all;
close all;

% Ejercicio 1

% Definir el periodo y el paso de tiempo
T = 2; dt = 0.001;

% Crear el rango de tiempo para un periodo
t = -T/2:dt:T/2-dt;

% Inicializar la señal x con ceros
x = zeros(1, length(t));

% Encontrar los índices de tiempo donde 0<|t|<0.5 y asignar el valor 2 a x en esos índices
ti = find(abs(t)<=0.5); x(ti) = 2;

% Encontrar los índices de tiempo donde 0.5<|t|<1 y asignar el valor 0 a x en esos índices
ti = find(abs(t)> 0.5); x(ti) = 0;

% Graficar la señal para 3 periodos
% (a)
figure(1), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=\begin{cases}2 & 0<|t|<0.5\\0&0.5<|t|<1\end{cases}$','Interpreter','latex');

% (b)
x = 0.8*sin(2*pi*t) + 0.6*cos(pi*t) - 0.2*sin(3*pi*t + pi/4);
figure(2), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=0.8\sin(2\pi t)+0.6\cos(\pi t)-0.2\sin\left(3\pi t+\dfrac{\pi}{4}\right)$','Interpreter','latex');

% (c)
x = zeros(1, length(t));
ti = find(t>=-1 & t<0); x(ti) = -2*t(ti);
ti = find(t>0 & t<1); x(ti) = 2*t(ti);
figure(3), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=\begin{cases}2t & 0<t<1\\-2t&-1\le t\le0\end{cases}$','Interpreter','latex');

% (d)
ti = find(t==0); x(ti) = 0.5 * (1/dt);
figure(4), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=0.5\delta(t),\,-1\le t<1$', 'Interpreter', 'latex')

% (e)
x = abs(sin(pi/2.*t));
figure(5), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=\left|\sin\left(\dfrac{\pi}{2}t\right)\right|$', "Interpreter", "latex")

% (f)
x = exp(j*2*pi*t) + exp(-3*j*pi*t);
figure(6), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=e^{j2\pi t}+e^{-j3\pi t}$', 'Interpreter', 'latex')

% Ejercicio 2
T = 4;dt = 0.001;

% Inicializar la señal x con ceros
x = zeros(1, length(t));

% Encontrar los índices de tiempo donde 0<|t|<0.5 y asignar el valor 2 a x en esos índices
ti = find(abs(t)<=0.5); x(ti) = 2;

% Encontrar los índices de tiempo donde 0.5<|t|<1 y asignar el valor 0 a x en esos índices
ti = find(abs(t)> 0.5); x(ti) = 0;

% Graficar la señal para 3 periodos
% (a)
figure(7), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=\begin{cases}2 & 0<|t|<0.5\\0&0.5<|t|<1\end{cases}$','Interpreter','latex');

% (c)
x = zeros(1, length(t));
ti = find(t>=-1 & t<0); x(ti) = -2*t(ti);
ti = find(t>0 & t<1); x(ti) = 2*t(ti);
figure(8), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=\begin{cases}2t & 0<t<1\\-2t&-1\le t\le0\end{cases}$','Interpreter','latex');

% (d)
x = zeros(1, length(t));
ti = find(t==0); x(ti) = 0.5 * (1/dt);
figure(9), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=0.5\delta(t),\,-1\le t<1$', 'Interpreter', 'latex')

T = 6; dt = 0.001;

% Crear el rango de tiempo para un periodo
t = -T/2:dt:T/2-dt;

% Inicializar la señal x con ceros
x = zeros(1, length(t));

% Encontrar los índices de tiempo donde 0<|t|<0.5 y asignar el valor 2 a x en esos índices
ti = find(abs(t)<=0.5); x(ti) = 2;

% Encontrar los índices de tiempo donde 0.5<|t|<1 y asignar el valor 0 a x en esos índices
ti = find(abs(t)> 0.5); x(ti) = 0;

% (a)
figure(10), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=\begin{cases}2 & 0<|t|<0.5\\0&0.5<|t|<1\end{cases}$','Interpreter','latex');

% (c)
x = zeros(1, length(t));
ti = find(t>=-1 & t<0); x(ti) = -2*t(ti);
ti = find(t>0 & t<1); x(ti) = 2*t(ti);
figure(11), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=\begin{cases}2t & 0<t<1\\-2t&-1\le t\le0\end{cases}$','Interpreter','latex');

% (d)
x = zeros(1, length(t));
ti = find(t==0); x(ti) = 0.5 * (1/dt);
figure(12), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=0.5\delta(t),\,-1\le t<1$', 'Interpreter', 'latex')

% Ejercicio 4

% Definir el periodo y el paso de tiempo
T = 2; dt = 0.001; N=1;
t = -T/2:dt:T/2-dt;

% (a)
x = zeros(1, length(t));
ti = find(abs(t)<=0.5); x(ti) = 2;
ti = find(abs(t)> 0.5); x(ti) = 0;
ak_a = cfourier(x, T, N, dt);

% (b)
x = 0.8*sin(2*pi*t) + 0.6*cos(pi*t) - 0.2*sin(3*pi*t + pi/4);
ak_b = cfourier(x, T, N, dt);

% (c)
x = zeros(1, length(t));
ti = find(t>=-1 & t<0); x(ti) = -2*t(ti);
ti = find(t>0 & t<1); x(ti) = 2*t(ti);
ak_c = cfourier(x, T, N, dt);

% (d)
x = zeros(1, length(t));
ti = find(t==0); x(ti) = 0.5 * (1/dt);
ak_d = cfourier(x, T, N, dt);

% (e)
x = abs(sin(pi/2.*t));
ak_e = cfourier(x, T, N, dt);

% (f)
x = exp(j*2*pi*t) + exp(-3*j*pi*t);
ak_f = cfourier(x, T, N, dt);

% (a)
ic_a = icfourier(ak_a, T, N, dt);

% (c)
ic_c = icfourier(ak_c, T, N, dt);

% (d)
ic_d = icfourier(ak_d, T, N, dt);

% (e)
ic_e = icfourier(ak_e, T, N, dt);

% Ejercicio 7

% Calcular la suma de los cuadrados de los coeficientes de Fourier
sum_ak2_a = sum(abs(ak_a).^2);
sum_ak2_c = sum(abs(ak_c).^2);
sum_ak2_d = sum(abs(ak_d).^2);
sum_ak2_e = sum(abs(ak_e).^2);

% Calcular la integral de la señal al cuadrado
int_x2_a = dt * sum(abs(ic_a).^2);
int_x2_c = dt * sum(abs(ic_c).^2);
int_x2_d = dt * sum(abs(ic_d).^2);
int_x2_e = dt * sum(abs(ic_e).^2);


% Apartado 2
% Ejercicio 1
% a)
t = -5:0.002:5;
x = zeros(size(t));
x(t <= 0.6) = 1;
figure(13); plot(t, x, "LineWidth", 1.5, "color", "#007AFF");
title(' $x(t)=\begin{cases}1, & t\le0.6\\0,&\text{resto}\end{cases}$', "Interpreter", "latex");

% b)
t = -5:0.002:5;
x = zeros(size(t));
x(t <= 0.2) = 1;
figure(14); plot(t, x, "LineWidth", 1.5, "color", "#007AFF");
title('$x(t)=\begin{cases}1, & t\le0.2\\0, & \mathrm{resto}\end{cases}$', 'Interpreter', 'latex');

% c)
t = -5:0.002:5;
x = zeros(size(t));
x(0 < t & t <= 1) = 0.5;
x(1 < t & t <= 2) = 1 - 0.5 * t(1 < t & t <= 2);
figure(15); plot(t, x, "LineWidth", 1.5, "color", "#007AFF");
title('$x(t)=\begin{cases}0.5, & 0<t\le1\\1-0.5t,&1<t\le2\\0,& \mathrm{resto}\end{cases}$', "Interpreter", "latex");

% Ejercicio 2
% i)
T = length(x)*0.002;
N = 50;
dt = 0.002;
ak = cfourier(x, T, N, dt);
ak = T * ak;
k = 0:length(ak)-1;
w = 2*pi*k/T;
figure(16); stem(w, ak, '.', "LineWidth", 1.5, "color", "#007AFF", "MarkerSize", 10);

% ii)
Ti = floor(length(x)/2);
x = [zeros(1, Ti) x zeros(1, Ti)];

% iii)
for i = 1:5
    N = 2*N;
    T = 2*T;
    ak = cfourier(x, T, N, dt);
    ak = T * ak;
    k = 0:length(ak)-1;
    w = 2*pi*k/T;
    figure; stem(w, ak, '.', "LineWidth", 1.5, "color", "#007AFF", "MarkerSize", 4);
end

% Ejercicio 5


% Obtener todas las figuras abiertas:
figs = get(0, 'children');
figs = flip(figs);

% Recorrer todas las figuras:
for i = 1:length(figs)
    % Seleccionar la figura actual:
    figure(figs(i));

    % Crear el nombre del archivo:
    filename = sprintf('Figura%d.png', i);

    % Guardar la figura en un archivo PNG:
    print(filename, '-dpng');
end

close all;
