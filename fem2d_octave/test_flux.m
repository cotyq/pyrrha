function [OK] = test_flux()
    fd = fopen('results.txt', 'a');
    module = 'fem2d_heat_flux.m';
    fprintf('Validando %s...\n', module);
    
    load('data_system1.mat');

    N = size(xnode,1);
    PHI = rand(N,1);
    
    [Q1] = fem2d_heat_flux(xnode,icone,model,PHI);
    OK_run = true;  % To indicate if user's module has programming issues.
    OK_Q = false;   % To indicate if user's module has values issues.
    message = '';

    try
        [Q2] = temp_fem2d_heat_flux(xnode,icone,model,PHI);
    catch
        message = 'Se produjo un error durante la ejecución de fem2d_heat_flux.\n';
        Q2 = [];

        OK_run = false;
    end

    % If no error was encountered when running user's code.
    if (OK_run)
        message = '';

        [OK_Q, message_Q] = aux_check_module(Q1,Q2,'[Q]');
        message = strcat(message, message_Q);
        
        if (OK_Q)
            message = strcat('[Q] OK\n', message);
        end
    end
    
    fprintf(message);

    %% RESULT
    OK = OK_Q;
    
    fprintf(fd, '%i : %s\n', OK, module);
    disp('------------------------------------------');
    fclose(fd);
end
