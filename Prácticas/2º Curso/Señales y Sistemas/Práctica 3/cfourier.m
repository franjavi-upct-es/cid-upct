function ak = cfourier(x,T,N,dt)
t = -T/2:dt:T/2-dt;
ak = zeros(1,2*N+1);
for k = -N:N
	ak(k+N+1) = 1/T*sum(x.*exp(-j*k*2*pi/T*t))*dt;
end
