function [x,t] = itfourier(X,w,dw,tmax)
    % Aplicar la Transformada de Fourier a la señal en el dominio de la frecuencia
    [x_tilde, t] = tfourier(X,w,dw,tmax);

    % Escalar la señal y tomar la parte real para obtener la señal en el dominio del tiempo
    x = real(dw/(2*pi) * x_tilde);
end
