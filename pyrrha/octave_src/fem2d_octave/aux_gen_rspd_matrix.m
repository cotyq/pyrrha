function [M] = aux_gen_rspd_matrix(n)
    % Function to generate a Random Symmetric Positive Definite Matrix of
    % n rows by n columns (square)
    
    A = rand(n);
    M = A + A' + sqrt(n)*eye(n);
end