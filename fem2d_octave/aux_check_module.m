function [OK, message] = aux_check_module(A,B,str)
    OK_val = false;
    message = '';
        
    % Check dimensions
    [OK_dim,message_dim] = aux_check_dim(A,B,str);
    message = strcat(message, message_dim);
        
    % If dimensions were OK, then check values
    if (OK_dim)
        [OK_val,message_val] = aux_check_values(A,B,str);
        message = strcat(message, message_val);
    end

    OK = OK_dim && OK_val;
end

