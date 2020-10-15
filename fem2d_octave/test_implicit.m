function [OK] = test_implicit()
    fd = fopen('results.txt', 'a');
    module = 'fem2d_heat_implicit.m';
    fprintf('Validando %s...\n', module);

    load('data_system1.mat');
    
    N = size(xnode,1);
    K = aux_gen_rspd_matrix(N);
    F = rand(N,1);
    C = K;
    
    [dt] = 0.00001;
    model.maxit = 50;
    model.tol = 1e-5;
    model.verbose = 0;
    
    [PHI1, Q1] = fem2d_heat_implicit(K,C,F,xnode,icone,model,dt);
    OK_run = true;  % To indicate if user's module has programming issues.
    OK_PHI = false; % To indicate if user's module has values issues.
    OK_Q = false;   % To indicate if user's module has values issues.
    message = '';

    try
        [PHI2, Q2] = temp_fem2d_heat_implicit(K,C,F,xnode,icone,model,dt);
    catch
        message = 'Se produjo un error durante la ejecución de fem2d_heat_implicit.\n';
        PHI2 = [];
        Q2 = [];

        OK_run = false;
    end

    % If no error was encountered when running user's code.
    if (OK_run)
        message = '';
        
        [OK_PHI, message_PHI] = aux_check_module(PHI1,PHI2,'[PHI]');
        message = strcat(message, message_PHI);
        [OK_Q, message_Q] = aux_check_module(Q1,Q2,'[ Q ]');
        message = strcat(message, message_Q);

        if (OK_PHI)
            message = strcat('[PHI] OK\n', message);
        end
        
        if (OK_Q)
            message = strcat('[ Q ] OK\n', message);
        end
    end
    
    OK = OK_PHI && OK_Q;
    fprintf(message);

    fprintf(fd, '%i : %s\n', OK, module);
    disp('-------------------------------------');
    fclose(fd);
end
