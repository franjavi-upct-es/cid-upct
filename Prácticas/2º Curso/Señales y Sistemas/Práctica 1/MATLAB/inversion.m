function [y,n2]=inversion(x,n)
ind = length(x):-1:1;
y = x(ind); % Cambiamos el orden del vector x
n2 = -n(ind); % calculamos los índices de n
