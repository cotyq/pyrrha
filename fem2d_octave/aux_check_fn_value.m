function [N_out] = aux_check_fn_value(N_in)
    if (abs(N_in) < 1e-12)
        N_out = 0;
    elseif (abs(1 - N_in) < 1e-12)
        N_out = 1;
    else
        N_out = N_in;
    end
end

