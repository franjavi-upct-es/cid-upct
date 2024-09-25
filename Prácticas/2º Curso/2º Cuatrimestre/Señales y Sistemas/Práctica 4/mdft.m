function [Xout] = mdft(xin)

% [Xout] = mdft(xin)
% funcion que calcula la DFT con la notacion matricial.

% Inicializacion
xin = (xin(:)).';
N   = length(xin);
Vo  = ones(N,1);
f   = exp(-j*2*pi/N*([0:(N-1)]'));

Vk   = Vo;
Xout = zeros(N,1);

%iteración
         
for k=0:(N-1)
    Xout(k+1) = xin*Vk;
    Vk        = Vk .* f;
end

