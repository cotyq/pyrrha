function [OK1] = test_genC()
    fd = fopen('results.txt', 'a');
    module = 'fem2d_heat_genC.m';
    fprintf('Validando %s...\n', module);

    load('data_system1.mat');
    
    %% ELEMENTOS CUADRANGULARES
    fprintf('Elementos cuadrangulares:\n');

	elem = icone(3001,:);
    nodes = xnode(elem,:);
    
    [localC1] = fem2d_heat_genC(nodes);
    OK_run = true;  % To indicate if user's module has programming issues.
    OK_C = false;   % To indicate if user's module has values issues.
    message = '';

    try
        [localC2] = temp_fem2d_heat_genC(nodes);
    catch
        message = 'Se produjo un error durante la ejecución de fem2d_heat_genC.\n';
        localC2 = [];

        OK_run = false;
    end

    % If no error was encountered when running user's code.
    if (OK_run)
        message = '';

        [OK_C, message_C] = aux_check_module(localC1,localC2,'[C]');
        message = strcat(message, message_C);
        
        if (OK_C)
            message = strcat('[C] OK\n', message);
        end
    end
    
    OK1 = OK_C;
    fprintf(message);
    
    %% ELEMENTOS TRIANGULARES
    fprintf('Elementos triangulares:\n');
	
    elem = icone(3002,1:3);
    nodes = xnode(elem,:);
    
    [localC1] = fem2d_heat_genC(nodes);
    OK_run = true;  % To indicate if user's module has programming issues.
    OK_C = false;   % To indicate if user's module has values issues.
    message = '';

    try
        [localC2] = temp_fem2d_heat_genC(nodes);
    catch
        message = 'Se produjo un error durante la ejecución de fem2d_heat_genC.\n';
        localC2 = [];

        OK_run = false;
    end

    % If no error was encountered when running user's code.
    if (OK_run)
        message = '';

        [OK_C, message_C] = aux_check_module(localC1,localC2,'[C]');
        message = strcat(message, message_C);
        
        if (OK_C)
            message = strcat('[C] OK\n', message);
        end
    end
    
    OK2 = OK_C;
    fprintf(message);
    
    %% RESULT
    OK = OK1*OK2;
    
    fprintf(fd, '%i : %s\n', OK, module);
    disp('------------------------------------------');
    fclose(fd);
end
