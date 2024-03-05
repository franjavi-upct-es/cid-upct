clear all;
close all;

x = [1 2 -2];
h = [1 3 0 1 2 1 2];

y = conv(x, h);

figure(1)
stem(y, 'filled', "LineWidth", 1.5, "MarkerSize", 4);
xlabel('n');
ylabel('y[n]');
title('Convolución discreta de x[n] y h[n]')

y1 = conv1(x,h);


figure(2)
stem(y1, "filled", "LineWidth", 1.5, "MarkerSize", 4);
xlabel('n');
ylabel("y[n]")
title('Conv1 y[n]')

y2 = conv2d(x, h);

figure(3)
stem(y2, "filled", "LineWidth", 1.5, "MarkerSize", 4);
xlabel('n');
ylabel("y[n]")
title('Conv2 y[n]')

% Las siguiente funciones recorren todos los elementos de las señales y
% comprueban si sus valores coinciden con valores bnarios (1 sí, 0 no).
disp(all(y == y1)); % 1
disp(all(y == y2)); % 1
disp(all(y1 == y2)); % 1


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


