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
ti = find(abs(t)>=-1 & abs(t)<0); x(ti) = -2*t(ti);
ti = find(abs(t)>0 & abs(t)<1); x(ti) = 2*t(ti);
figure(3), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=\begin{cases}2t & 0<t<1\\-2t&-1\le t\le0\end{cases}$','Interpreter','latex');

% (d)
ti = find(abs(t)==0); x(ti) = 0.5 * (1/dt);
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
ti = find(abs(t)>=-1 & abs(t)<0); x(ti) = -2*t(ti);
ti = find(abs(t)>0 & abs(t)<1); x(ti) = 2*t(ti);
figure(8), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=\begin{cases}2t & 0<t<1\\-2t&-1\le t\le0\end{cases}$','Interpreter','latex');

% (d)
x = zeros(1, length(t));
ti = find(abs(t)==0); x(ti) = 0.5 * (1/dt);
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
ti = find(abs(t)>=-1 & abs(t)<0); x(ti) = -2*t(ti);
ti = find(abs(t)>0 & abs(t)<1); x(ti) = 2*t(ti);
figure(11), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=\begin{cases}2t & 0<t<1\\-2t&-1\le t\le0\end{cases}$','Interpreter','latex');

% (d)
x = zeros(1, length(t));
ti = find(abs(t)==0); x(ti) = 0.5 * (1/dt);
figure(12), plot([t-T t t+T], [x x x], "LineWidth", 1.5, "color", "#007AFF");
xlabel('Tiempo (t)');
ylabel('x(t)');
title('$x(t)=0.5\delta(t),\,-1\le t<1$', 'Interpreter', 'latex')

% Ejercicio 4

% Definir el periodo y el paso de tiempo
T = 2; dt = 0.001; N=5;
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
ti = find(abs(t)>=-1 & abs(t)<0); x(ti) = -2*t(ti);
ti = find(abs(t)>0 & abs(t)<1); x(ti) = 2*t(ti);
ak_c = cfourier(x, T, N, dt);

% (d)
x = zeros(1, length(t));
ti = find(abs(t)==0); x(ti) = 0.5 * (1/dt);
ak_d = cfourier(x, T, N, dt);

% (e)
x = abs(sin(pi/2.*t));
ak_e = cfourier(x, T, N, dt);

% (f)
x = exp(j*2*pi*t) + exp(-3*j*pi*t);
ak_f = cfourier(x, T, N, dt);

% Ejercicio 6

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
sum_ak2_b = sum(abs(ak_b).^2);
sum_ak2_c = sum(abs(ak_c).^2);
sum_ak2_d = sum(abs(ak_d).^2);
sum_ak2_e = sum(abs(ak_e).^2);
sum_ak2_f = sum(abs(ak_f).^2);

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
% a)
t = -5:0.002:5;
x = zeros(size(t));
ti = find(abs(t) <= 0.6)
x(ti) = 1;
T = length(x)*0.002;
N = 50;
dt = 0.002;
ak = cfourier(x, T, N, dt);
ak = T * ak;
k = 0:length(ak)-1;
w = 2*pi*k/T;
figure(16); stem(w, ak, '.', "LineWidth", 1.5, "color", "#007AFF", "MarkerSize", 10);

% b)
t = -5:0.002:5;
x = zeros(size(t));
ti = find(abs(t) <= 0.2)
x(ti) = 1;
T = length(x)*0.002;
N = 50;
dt = 0.002;
ak = cfourier(x, T, N, dt);
ak = T * ak;
k = 0:length(ak)-1;
w = 2*pi*k/T;
figure(17); stem(w, ak, '.', "LineWidth", 1.5, "color", "#007AFF", "MarkerSize", 10);

% c)
t = -5:0.002:5;
x = zeros(size(t));
ti = find(0 < abs(t) <= 0.1);
x(ti) = 0.5;
ti = find(1 < t & t <= 2);
x(ti) = 1 - 0.5 * t(ti);
T = length(x)*0.002;
N = 50;
dt = 0.002;
ak = cfourier(x, T, N, dt);
ak = T * ak;
k = 0:length(ak)-1;
w = 2*pi*k/T;
figure(18); stem(w, ak, '.', "LineWidth", 1.5, "color", "#007AFF", "MarkerSize", 10);

% ii)
% a)
t = -5:0.002:5;
x = zeros(size(t));
ti = find(abs(t) <= 0.6)
x(ti) = 1;
Ti = floor(length(x)/2);
x = [zeros(1, Ti) x zeros(1, Ti)];
T = length(x)*dt;
N = 50;
dt = 0.002;
ak = cfourier(x, T, N, dt);
ak = T * ak;
k = 0:length(ak)-1;
w = 2*pi*k/T;
figure(19); stem(w, ak, '.', "LineWidth", 1.5, "color", "#007AFF", "MarkerSize", 10);

% b)
t = -5:0.002:5;
x = zeros(size(t));
ti = find(abs(t) <= 0.2)
x(ti) = 1;
Ti = floor(length(x)/2);
x = [zeros(1, Ti) x zeros(1, Ti)];
T = length(x)*dt;
N = 50;
dt = 0.002;
ak = cfourier(x, T, N, dt);
ak = T * ak;
k = 0:length(ak)-1;
w = 2*pi*k/T;
figure(20); stem(w, ak, '.', "LineWidth", 1.5, "color", "#007AFF", "MarkerSize", 10);

% c)
t = -5:0.002:5;
x = zeros(size(t));
ti = find(0 < abs(t) <= 0.1);
x(ti) = 0.5;
ti = find(1 < t & t <= 2);
x(ti) = 1 - 0.5 * t(ti);
Ti = floor(length(x)/2);
x = [zeros(1, Ti) x zeros(1, Ti)];
T = length(x)*dt;

N = 50;
dt = 0.002;
ak = cfourier(x, T, N, dt);
ak = T * ak;
k = 0:length(ak)-1;
w = 2*pi*k/T;
figure(21); stem(w, ak, '.', "LineWidth", 1.5, "color", "#007AFF", "MarkerSize", 10);

% iii)
% a)
T = 10;
t = -T/2:0.002:T/2-0.002;
x = zeros(size(t));
ti = find(abs(t) <= 0.6)
x(ti) = 1;
N = 50;
dt = 0.002;
% Bucle for para duplicar N y T
for i = 1:2
    Ti = floor(length(x)/2);
    x = [zeros(1, Ti) x zeros(1, Ti)];
    N = 2*N;
    T = 2*T;
    k = -N:N
    % Calcular ak y normalizar
    ak = cfourier(x, T, N, dt);
    ak = T * ak;

    % Definir k y w
    w = 2*pi*k/T;

    % Crear figura y representar las series de Fourier normalizadas
    figure; stem(w, ak, '.', "LineWidth", 1.5, "color", "#007AFF", "MarkerSize", 10);
end

% b)
T = 10;
t = -T/2:0.002:T/2-0.002;
x = zeros(size(t));
ti = find(abs(t) <= 0.2)
x(ti) = 1;
N = 50;
dt = 0.002;
% Bucle for para duplicar N y T
for i = 1:2
    Ti = floor(length(x)/2);
    x = [zeros(1, Ti) x zeros(1, Ti)];
    N = 2*N;
    T = 2*T;
    k = -N:N
    % Calcular ak y normalizar
    ak = cfourier(x, T, N, dt);
    ak = T * ak;

    % Definir k y w
    w = 2*pi*k/T;

    % Crear figura y representar las series de Fourier normalizadas
    figure; stem(w, ak, '.', "LineWidth", 1.5, "color", "#007AFF", "MarkerSize", 10);
end

% c)
T = 10;
t = -T/2:0.002:T/2-0.002;
x = zeros(size(t));
ti = find(0 < abs(t) <= 0.1);
x(ti) = 0.5;
ti = find(1 < abs(t) & abs(t) <= 2);
x(ti) = 1 - 0.5 * t(ti);
N = 50;
dt = 0.002;
% Bucle for para duplicar N y T
for i = 1:2
    Ti = floor(length(x)/2);
    x = [zeros(1, Ti) x zeros(1, Ti)];
    N = 2*N;
    T = 2*T;
    k = -N:N
    % Calcular ak y normalizar
    ak = cfourier(x, T, N, dt);
    ak = T * ak;

    % Definir k y w
    w = 2*pi*k/T;

    % Crear figura y representar las series de Fourier normalizadas
    figure; stem(w, ak, '.', "LineWidth", 1.5, "color", "#007AFF", "MarkerSize", 10);
end

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

% Define the signals
t = -5:0.002:5;
a = zeros(size(t));
b = zeros(size(t));
c = zeros(size(t));

% Define the signals a, b, and c
a(abs(t) <= 0.6) = 1;
b(abs(t) <= 0.2) = 1;
c(0 < t & t <= 1) = 0.5;
c(1 < t & t <= 2) = 1 - 0.5 * t(1 < t & t <= 2);

% Define the frequency range and step size
dt = 0.002;
wmax = 5;

% Calculate the Fourier transforms
[A, w] = tfourier(a, t,dt, wmax);
[B, ~] = tfourier(b, t,dt, wmax);
[C, ~] = tfourier(c, t,dt, wmax);

% Verify the properties
% 1. Linearity
AB = tfourier(a + b, t,dt, wmax);
isequal(AB, A + B)

% 2. Time shifting
t0 = 1; % Define a time shift
B_shift = tfourier(b .* exp(-i * w * t0), t, dt, wmax);
isequal(B_shift, B)

% 3. Inversion
C_inv = tfourier(c(end:-1:1), t, dt, wmax);
isequal(C_inv, C(end:-1:1))

% 4. Conjugation
C_conj = tfourier(conj(c), t, dt, wmax);
isequal(C_conj, conj(C))

% 5. Real part
C_real = tfourier(real(c), t, dt, wmax);
isequal(C_real, real(C))

% 6. Imaginary part
C_imag = tfourier(imag(c), t, dt, wmax);
isequal(C_imag, imag(C))
