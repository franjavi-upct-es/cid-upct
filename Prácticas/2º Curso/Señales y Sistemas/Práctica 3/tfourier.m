function [X,w] = tfourier(x,t,dw,wmax)
    % Crear el vector de frecuencias
    w = -wmax:dw:wmax;

    % Inicializar el vector de la Transformada de Fourier
    X = zeros(size(w));

    % Calcular la Transformada de Fourier para cada frecuencia
    for k = 1:length(w)
        X(k) = sum(x .* exp(-1i * w(k) * t));
    end
end
