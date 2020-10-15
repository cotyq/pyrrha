function [OK] = test_explicit_delta_t()
    fd = fopen('results.txt', 'a');
    module = "fem2d_heat_explicit_delta_t.m";
    fprintf('Validando %s...\n', module);

    load('data_system1.mat');

    [dt1] = fem2d_heat_explicit_delta_t(xnode,icone,model);

    try
        [dt2] = temp_fem2d_heat_explicit_delta_t(xnode,icone,model);
    catch
        warning('Se produjo un error durante la ejecución de fem2d_heat_explicit_delta_t.');
        dt2 = [];
    end

    message = "";
    OK = true;
    
    if (isempty(dt2))
        dt2 = 0;
    end

    if (dt2 == 0 || dt2 > dt1)
        message = strcat(message, "[dt] incorrecto\n");
        OK = false;
    end

     if (OK)
        message = "OK\n";
    end

    fprintf(message);
    fprintf(fd, "%i : %s\n", OK, module);
    disp("------------------------------------------");
    fclose(fd);
end
