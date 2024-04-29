function X = mfft(x,fasores)

N = length(x);

if (N==2)
    X   = zeros(2,1);
    X(1)= x(1) + x(2);
    X(2)= x(1) - x(2);
else
    G = mfft(x(1:2:end),fasores(1:2:end));
    H = mfft(x(2:2:end),fasores(1:2:end));
    X =[G; G] + [H; H].*fasores;
end