function [OK] = test_neumann()
    fd = fopen('results.txt', 'a');
    module = 'fem2d_heat_neumann.m';
    fprintf('Validando %s...\n', module);

    load('data_system1.mat');

    N = size(xnode,1);
    F = rand(N,1);

    [F1] = fem2d_heat_neumann(F,NEU,xnode);
    OK_run = true;  % To indicate if user's module has programming issues.
    OK_F = false;   % To indicate if user's module has values issues.
    message = '';

    try
        [F2] = temp_fem2d_heat_neumann(F,NEU,xnode);
    catch
        message = 'Se produjo un error durante la ejecución de fem2d_heat_neumann.\n';
        F2 = [];

        OK_run = false;
    end

    % If no error was encountered when running user's code.
    if (OK_run)
        message = '';

        [OK_F, message_F] = aux_check_module(F1,F2,'[F]');
        message = strcat(message, message_F);
        
        if (OK_F)
            message = strcat('[F] OK\n', message);
        end
    end
    
    OK = OK_F;
    fprintf(message);

    fprintf(fd, '%i : %s\n', OK, module);
    disp('------------------------------------------');
    fclose(fd);
end
