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

y2 = conv2(x, h);

disp(all(y == y1));
disp(all(y == y2));


% Obtener todas las figuras abiertas:
figs = get(0, 'children');


% Recorrer todas las figuras:
for i = 1:length(figs)
    % Seleccionar la figura actual:
    figure(figs(i));

    % Crear el nombre del archivo:
    filename = sprintf('Figura%d.png', i);

    % Guardar la figura en un archivo PNG:
    print(filename, '-dpng');
end
