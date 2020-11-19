function [OK] = test_robin()
    fd = fopen('results.txt', 'a');
    module = 'fem2d_heat_robin.m';
    fprintf('Validando %s...\n', module);

    load('data_system1.mat');

    N = size(xnode,1);
    K = aux_gen_rspd_matrix(N);
    F = rand(N,1);

    [K1,F1] = fem2d_heat_robin(K,F,ROB,xnode);
    OK_run = true;  % To indicate if user's module has programming issues.
    OK_K = false;   % To indicate if user's module has values issues.
    OK_F = false;   % To indicate if user's module has values issues.
    message = '';

    try
        [K2,F2] = temp_fem2d_heat_robin(K,F,ROB,xnode);
    catch
        message = 'Se produjo un error durante la ejecución de fem2d_heat_robin.\n';
        K2 = [];
        F2 = [];

        OK_run = false;
    end

    % If no error was encountered when running user's code.
    if (OK_run)
        message = '';
        
        [OK_K, message_K] = aux_check_module(K1,K2,'[K]');
        message = strcat(message, message_K);
        [OK_F, message_F] = aux_check_module(F1,F2,'[F]');
        message = strcat(message, message_F);

        if (OK_K)
            message = strcat('[K] OK\n', message);
        end
        
        if (OK_F)
            message = strcat('[F] OK\n', message);
        end
    end
    
    fprintf(message);
    
    %% RESULT
    OK = OK_K && OK_F;

    fprintf(fd, '%i : %s\n', OK, module);
    disp('------------------------------------------');
    fclose(fd);
end
