function y = conv1(x, h)
    N = length(x);
    M = length(h);
    y = zeros(1, N+M-1);
    for n = 1:N+M-1
        for k = max(1, n+1-M):min(n, N)
            y(n) = y(n) + x(k) * h(n-k+1);
        end
    end
end
