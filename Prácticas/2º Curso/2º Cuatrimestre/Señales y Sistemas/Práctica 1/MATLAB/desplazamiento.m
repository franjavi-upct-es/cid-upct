function y=desplazamiento(x,n0)
long=length(x); % Longitud de x
if(n0>=0) % Si n0 es =>0
 y=[zeros(1,n0) x(1:long-n0)]; % desplazamiento a la derecha
else % Si n0 es <0
 n0=-n0;
 y=[x(1+n0:long) zeros(1,n0)]; % desplazamiento a la izquierda
end