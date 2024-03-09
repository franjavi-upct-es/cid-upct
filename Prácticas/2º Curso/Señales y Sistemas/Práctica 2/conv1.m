function y = conv1(x, h)
	% N es la longitud de la secuencia x
	N = length(x);
	% M es la longitud de la secuencia h
	M = length(h);
	% Inicializa la secuencia de salida y con ceros
	y = zeros(1, N+M-1);
	% Itera sobre cada elemento de la secuencia de salida
	for n = 1:N+M-1
		% Itera sobre los elementos de x y h que se superponen para el elemento actual de y
		for k = max(1, n+1-M):min(n, N)
			% Suma el producto de los elementos correspondientes de x y h a la secuencia de salida
			y(n) = y(n) + x(k) * h(n-k+1);
		end
	end
end
