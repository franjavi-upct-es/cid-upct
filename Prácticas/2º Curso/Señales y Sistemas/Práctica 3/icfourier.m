function x = icfourier(ak,T,N,dt)
t = -T/2:dt:T/2-dt;
x = zeros(1,lenght(t));
for k = -N:N
	x = x + ak(k+N+1)*exp(j*k*2*pi/T*t);
end
