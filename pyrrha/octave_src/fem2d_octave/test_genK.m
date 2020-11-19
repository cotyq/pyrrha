function [OK1] = test_genK()
    fd = fopen('results.txt', 'a');
    module = 'fem2d_heat_genK.m';
    fprintf('Validando %s...\n', module);

    load('data_system1.mat');
    
    %% ELEMENTOS CUADRANGULARES
    fprintf('Elementos cuadrangulares:\n');

    e = 3001;
	elem = icone(e,:);
    nodes = xnode(elem,:);
    
    [localK1] = fem2d_heat_genK(nodes,model.kx,model.ky);
    OK_run = true;  % To indicate if user's module has programming issues.
    OK_K = false;   % To indicate if user's module has values issues.
    message = '';

    try
        [localK2] = temp_fem2d_heat_genK(nodes,model.kx,model.ky);
    catch
        message = 'Se produjo un error durante la ejecución de fem2d_heat_genK.\n';
        localK2 = [];

        OK_run = false;
    end

    % If no error was encountered when running user's code.
    if (OK_run)
        message = '';

        [OK_K, message_K] = aux_check_module(localK1,localK2,'[K]');
        message = strcat(message, message_K);
        
        if (OK_K)
            message = strcat('[K] OK\n', message);
        end
    end
    
    OK1 = OK_K;
    fprintf(message);
    
    %% ELEMENTOS TRIANGULARES
    fprintf('Elementos triangulares:\n');

	e = 3002;
	elem = icone(e,1:3);
    nodes = xnode(elem,:);
    
    [localK1] = fem2d_heat_genK(nodes,model.kx,model.ky);
    OK_run = true;  % To indicate if user's module has programming issues.
    OK_K = false;   % To indicate if user's module has values issues.
    message = '';

    try
        [localK2] = temp_fem2d_heat_genK(nodes,model.kx,model.ky);
    catch
        message = 'Se produjo un error durante la ejecución de fem2d_heat_genK.\n';
        localK2 = [];

        OK_run = false;
    end

    % If no error was encountered when running user's code.
    if (OK_run)
        message = '';

        [OK_K, message_K] = aux_check_module(localK1,localK2,'[K]');
        message = strcat(message, message_K);
        
        if (OK_K)
            message = strcat('[K] OK\n', message);
        end
    end
    
    OK2 = OK_K;
    fprintf(message);

    %% RESULT
    OK = OK1*OK2;

    fprintf(fd, '%i : %s\n', OK, module);
    disp('------------------------------------------');
    fclose(fd);
end
