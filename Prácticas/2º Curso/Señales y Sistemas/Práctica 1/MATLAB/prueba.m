N = 5; % Define el valor de N
n = -100:100; % Define el intervalo completo
y = sin(0.6 * n); % Define la señal y[n]

% Define la función de desplazamiento
desplazamiento = @(x, N) [x(N+1:end), zeros(1, N)];

% Crea la señal z[n] = y[n] - y[n-N]
y_desplazada = desplazamiento(y, -N);
z = y - y_desplazada;

% Crea una nueva figura
figure

% Muestra la señal y[n] en el intervalo [-20:20]
subplot(2,1,1)
stem(n(n>=-20 & n<=20), y(n>=-20 & n<=20), '.', 'LineWidth', 2)
title('Señal y[n]')

% Muestra la señal z[n] en el intervalo [-20:20]
subplot(2,1,2)
stem(n(n>=-20 & n<=20), z(n>=-20 & n<=20), '.', 'LineWidth', 2)
title('Señal z[n]')
