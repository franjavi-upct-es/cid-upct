function [y,n2]=compresion(x,n,a)
ind = find(mod(n,a)==0); % Valores de n m�ltiplo de a
y = x(ind); % Valores de x para n m�ltiplo de a
n2 = n(ind)/a; % Variable independiente