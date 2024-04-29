clear all;
close all;

% Ejercicio 1

ft = inline('fftshift(fftn(x))');

load splat.mat
sound(y, Fs);
fs = Fs;
x = y.';
X = ft(x);
n = (1:length(x))/fs;
figure(1);
stem(n, x);title('Tiempo "Splat"'); xlabel('s'); ylabel('x(t)');

omega = linspace(-3*pi, 3*pi, 3*length(X));
figure(2); subplot(2,1,1);
plot(omega, [abs(X) abs(X) abs(X)]); xlabel('w'); ylabel('TF (x(t))'); title('T.F dominio continuo de la secuencia');
w = linspace(-length(X)/2, length(X)/2, length(X));
 subplot(2, 1,2); plot(w, abs(X)); xlabel('w'); ylabel('TF (x(t))'); title('T.F dominio continuo');

load laughter.mat
sound(y, Fs);
fs = Fs;
x = y.';
X = ft(x);
n = (1:length(x))/fs;
figure(3);
stem(n, x);title('Tiempo "Laughter"'); xlabel('s'); ylabel('x(t)');

omega = linspace(-3*pi, 3*pi, 3*length(X));
figure(4); title('T.F dominio continuo'); subplot(2, 1,1);
plot(omega, [abs(X) abs(X) abs(X)]); xlabel('w'); ylabel('TF (x(t))');title('T.F dominio continuo de la secuencia');
w = linspace(-length(X)/2, length(X)/2, length(X));
 subplot(2, 1,2); plot(w, abs(X)); xlabel('w'); ylabel('TF (x(t))'); title('T.F dominio continuo');

load handel.mat
sound(y, Fs);
fs = Fs;
x = y.';
X = ft(x);
n = (1:length(x))/fs;
figure(5);
stem(n, x);title('Tiempo "Handel"'); xlabel('s'); ylabel('x(t)');

omega = linspace(-3*pi, 3*pi, 3*length(X));
figure(6); title('T.F dominio continuo'); subplot(2, 1,1);
plot(omega, [abs(X) abs(X) abs(X)]); xlabel('w'); ylabel('TF (x(t))');title('T.F dominio continuo de la secuencia');
w = linspace(-length(X)/2, length(X)/2, length(X));
 subplot(2, 1,2); plot(w, abs(X)); xlabel('w'); ylabel('TF (x(t))');title('T.F dominio continuo');

% Ejercicio 2