function [OK,message] = aux_check_values(A,B,str)
    NrNan = sum(isnan(B(:)));
    NrInf = sum(isinf(B(:)));
    
    OK = true;
    message = '';
    
    if (NrNan > 0)
        message = [message, str, ' Contiene valores NaN.\n'];
        OK = false;
    end
        
    if (NrInf > 0)
        message = [message, str, ' Contiene valores infinitos.\n'];
        OK = false;
    end
        
    if (NrNan == 0 && NrInf == 0)
        error =  norm(A-B,2) / norm(A,2);
        if (error > 1e-6)
            OK = false;
            message = [message, str, ' Valores incorrectos.\n'];
        end
    end
end

