function X = fftdt(x)

x = x(:); % convertir en vector columna
N = length(x);
if (log2(N)==round(log2(N)))
    fasores = exp(-j*2*pi/N*[0:(N-1)]');
    X = mfft(x, fasores);
else
    error('La longitud de x debe ser potencia de 2')
end
