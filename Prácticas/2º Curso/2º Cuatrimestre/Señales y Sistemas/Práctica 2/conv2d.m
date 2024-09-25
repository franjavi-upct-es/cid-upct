function y = conv2d(x, h)
    % Obtén las dimensiones de las matrices de entrada
    [xRows, xCols] = size(x);
    [hRows, hCols] = size(h);

    % Inicializa la matriz de salida
    y = zeros(xRows + hRows - 1, xCols + hCols - 1);

    % Realiza la convolución
    for i = 1:xRows
        for j = 1:xCols
            for m = 1:hRows
                for n = 1:hCols
                    y(i+m-1, j+n-1) = y(i+m-1, j+n-1) + x(i, j) * h(m, n);
                end
            end
        end
    end
end
