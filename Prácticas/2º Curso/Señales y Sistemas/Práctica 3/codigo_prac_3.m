clear all;
close all;

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
title('$x(t)=x(t)=e^{j2\pi t}+e^{-j3\pi t}$', 'Interpreter', 'latex')

% Ejercicio 2
T = 4;dt = 0.001;

% Crear el rango de tiempo para un periodo
t = -T/2:dt:T/2-dt;

% Inicializar la señal x con ceros
x = zeros(1, length(t));

% Encontrar los índices de tiempo donde 0<|t|<0.5 y asignar el valor 2 a x en esos índices
ti = find(abs(t)<=0.5); x(ti) = 2;

% Encontrar los índices de tiempo donde 0.5<|t|<1 y asignar el valor 0 a x en esos índices
ti = find(abs(t)> 0.5); x(ti) = 0;

% (a)
x = zeros(1, length(t));
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

close all;

% Ejercicio 3

% Definir el periodo y el paso de tiempo
T = 2; dt = 0.001; N=5;
t = -T/2:dt:T/2-dt;

% (a)
x = zeros(1, length(t));
ti = find(abs(t)<=0.5); x(ti) = 2;
ti = find(abs(t)> 0.5); x(ti) = 0;
ak = cfourier(x, T, N, dt)


