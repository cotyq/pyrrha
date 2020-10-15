function [OK1] = test_genF()
    fd = fopen('results.txt', 'a');
    module = 'fem2d_heat_genF.m';
    fprintf('Validando %s...\n', module);

    load('data_system1.mat');
    
    %% ELEMENTOS CUADRANGULARES
    fprintf('Elementos cuadrangulares:\n');
    
    e = 3001;
	elem = icone(e,:);
    nodes = xnode(elem,:);
    
    [localF1] = fem2d_heat_genF(nodes,model.G(e));
    OK_run = true;  % To indicate if user's module has programming issues.
    OK_F = false;   % To indicate if user's module has values issues.
    message = '';

    try
        [localF2] = temp_fem2d_heat_genF(nodes,model.G(e));
    catch
        message = 'Se produjo un error durante la ejecución de fem2d_heat_genF.\n';
        localF2 = [];

        OK_run = false;
    end

    % If no error was encountered when running user's code.
    if (OK_run)
        message = '';

        [OK_F, message_F] = aux_check_module(localF1,localF2,'[F]');
        message = strcat(message, message_F);
        
        if (OK_F)
            message = strcat('[F] OK\n', message);
        end
    end
    
    OK1 = OK_F;
    fprintf(message);
    
    %% ELEMENTOS TRIANGULARES
    fprintf('Elementos triangulares:\n');

	e = 3002;
	elem = icone(e,1:3);
    nodes = xnode(elem,:);
    
    [localF1] = fem2d_heat_genF(nodes,model.G(e));
    OK_run = true;  % To indicate if user's module has programming issues.
    OK_F = false;   % To indicate if user's module has values issues.
    message = '';

    try
        [localF2] = temp_fem2d_heat_genF(nodes,model.G(e));
    catch
        message = 'Se produjo un error durante la ejecución de fem2d_heat_genF.\n';
        localF2 = [];

        OK_run = false;
    end

    % If no error was encountered when running user's code.
    if (OK_run)
        message = '';

        [OK_F, message_F] = aux_check_module(localF1,localF2,'[F]');
        message = strcat(message, message_F);
        
        if (OK_F)
            message = strcat('[F] OK\n', message);
        end
    end
    
    OK2 = OK_F;
    fprintf(message);
    
    %% RESULT
    OK = OK1*OK2;

    fprintf(fd, '%i : %s\n', OK, module);
    disp('------------------------------------------');
    fclose(fd);
end
