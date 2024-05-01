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
figure(1);subplot(2,1,1);
stem(x, "color", "#007AFF"); title('Tiempo "Splat"'); ylabel('x[n]');
subplot(2,1,2);
plot(n,x, "color", "#007AFF"); xlabel('s'); ylabel('x(t)');

omega = linspace(-3*pi, 3*pi, 3*length(X));
figure(2); subplot(2,1,1);
plot(omega, [abs(X) abs(X) abs(X)], "color", "#007AFF"); xlabel('w'); ylabel('TF (x(t))'); title('T.F dominio continuo de la secuencia');
w = linspace(-length(X)/2, length(X)/2, length(X));
subplot(2, 1,2); plot(w, abs(X), "color", "#007AFF"); xlabel('w'); ylabel('TF (x(t))'); title('T.F dominio continuo');

load laughter.mat
sound(y, Fs);
fs = Fs;
x = y.';
X = ft(x);
n = (1:length(x))/fs;
figure(3); subplot(2,1,1);
stem(x, "color", "#007AFF");title('Tiempo "Laughter"'); ylabel('x[n]');
subplot(2,1,2); plot(n,x,"color", "#007AFF"); xlabel('s'); ylabel('x(t)');

omega = linspace(-3*pi, 3*pi, 3*length(X));
figure(4); title('T.F dominio continuo'); subplot(2, 1,1);
plot(omega, [abs(X) abs(X) abs(X)],"color", "#007AFF"); xlabel('w'); ylabel('TF (x(t))');title('T.F dominio continuo de la secuencia');
w = linspace(-length(X)/2, length(X)/2, length(X));
 subplot(2, 1,2); plot(w, abs(X), "color", "#007AFF"); xlabel('w'); ylabel('TF (x(t))'); title('T.F dominio continuo');

load handel.mat
sound(y, Fs);
fs = Fs;
x = y.';
X = ft(x);
n = (1:length(x))/fs;
figure(5);subplot(2,1,1);
stem(x);title('Tiempo "Handel"'); ylabel('x[n]');
subplot(2,1,2);
plot(n,x,"color", "#007AFF"); xlabel('s'); ylabel('x(t)');

omega = linspace(-3*pi, 3*pi, 3*length(X));
figure(6); title('T.F dominio continuo'); subplot(2, 1,1);
plot(omega, [abs(X) abs(X) abs(X)], "color", "#007AFF"); xlabel('w'); ylabel('TF (x(t))');title('T.F dominio continuo de la secuencia');
w = linspace(-length(X)/2, length(X)/2, length(X));
 subplot(2, 1,2); plot(w, abs(X), "color", "#007AFF"); xlabel('w'); ylabel('TF (x(t))');title('T.F dominio continuo');

% Ejercicio 2

N = 64;

x = rand(1, N);

% Calcular DFT usando mdft.m

tic
X_mdft = mdft(x)
toc

% Calcular DFT usando fftdt.m

tic
X_mdft = fftdt(x)
toc

N_values = 2.^(10:17);

array_mdft = zeros(1, length(N_values));
array_fftdt = zeros(1, length(N_values));

% Calcular DFT y coste computacional
for i = 1:length(N_values)
    x = rand(1, N_values(i));

    tic
    X_mdft = mdft(x);
    array_mdft(i) = toc;

    tic
    X_fftdt = fftdt(x);
    array_fftdt(i) = toc;
end

figure(7); plot(N_values, array_mdft, "color", '#FF0000', "LineWidth", 2, N_values, array_fftdt, "color", '#007AFF', "LineWidth", 2);
xlabel('N'); ylabel('Coste computacional (s)'); legend('DFT', 'FFT')

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

n = 0:63;
x1 = rand(1, 64);

% Filtro FIR
x2 = ones(1, 8) / 8

% Definir la función de convolución circular
convcirc = inline('real(ifft(fft(x1, N) .* fft(x2, N), N))', 'x1', 'x2', 'N');

isqual(length(x1) + length(x2) - 1, conv(x1, x2))
