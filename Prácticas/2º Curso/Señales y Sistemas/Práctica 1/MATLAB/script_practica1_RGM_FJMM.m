close all


x = [0 0 -0.4 -0.75 -0.2 0 0.5 0.8 1.2 0.8 0.4 0 -0.3 0 0];
N = floor(length(x)/2);
n = [-N:N];

figure(1)
stem(n,x,'.')
x(find(n==-3)) % Valor de la señal en el instante n=-3
x(find(n==-3))=-0.6;


% Cuestiones ejercicio 1:
% Generación de señales:
y = (-1.1) .^ n
x2 = x .* y
z = 0.75 .* (x + x2)
E = x .^ 2

% Energía y potencia de la señal x:
energia = sum(x .^ 2)
potencia = (1 / (2 * N + 1)) *  sum(x .^ 2)

% Cuestiones ejercicio 2: Desplazamiento temporal

x = rand(1,15);
n = -7:7;
y = desplazamiento(x,1);
figure(2)
subplot(2,1,1)
stem(n,x,'.')
subplot(2,1,2)
stem(n,y,'.')


y1 = desplazamiento(x,2);
figure(3)
stem(n,y1,'.')

y2 = desplazamiento(x,-3);
figure(4)
stem(n,y2,'.')

% Cuestiones ejercicio 2: Inversión temporal
x1=[1 1 2 3 5 8 13 21 34]; 
n = 0:8;

y1 = inversion(x1,n);
figure(5)
subplot(2,1,1)
stem(n,x1,'.')
subplot(2,1,2)
stem(n,y1,'.')

x2=[1 -2 3 -4 5 -4 3 -2 1]
n = -4:4;

y2 =inversion(x1,n);
figure(6)
subplot(2,1,1)
stem(n,x2,'.')
subplot(2,1,2)
stem(n,y2,'.')
% Lo que ocurre con y2 es que se invierte pero podemos apreciar que no es
% simétrica, al contrario que y1, que si lo es.


% Cuestiones ejercicio 3:
x=randn(1,9);
x=[x x x x x];
N=floor(length(x)/2);
n=[-N:N];

figure(7)
subplot(2,1,1)
stem(n,x,'.')

n2=[-20:20];
i0=find(n==n2(1));


subplot(2,1,2)
stem(n2,x(i0:i0+length(n2)-1))

n=[-100:100];
x = sin(pi / 5 * n)
N_x = (2*pi) / (pi/5)


n=[-20:20];
x = sin(pi / 5 * n)

y = desplazamiento(x,-N)
figure(8)
subplot(2,1,1)
stem(n,x,'.')

subplot(2,1,2)
stem(n2,y)
