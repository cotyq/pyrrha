function [OK,message] = aux_check_dim(A,B,str)
    [a1,a2] = size(A);
    [b1,b2] = size(B);

    OK = true;
    message = '';
    
    if (isvector(A))
        if (~isvector(B) || a1 ~= b1)
            message = [message, str, ' dimensiones inconsistentes. Se espera un vector columna.\n'];
            OK = false;
        end
    else
        if (isvector(B))
            message = [message, str, ' dimensiones inconsistentes. Se espera una matriz, no un vector.\n'];
            OK = false;
        elseif (a1 ~= b1 || a2 ~= b2)
            message = [message, str, ' dimensiones incorrectas. Nro. distinto de filas y/o columnas.\n'];
            OK = false;
        end
    end
    
    
end

