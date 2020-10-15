function [] = aux_fem2d_heat_export(xnode,icone,DIR,NEU,ROB,PUN,model,src)
    fd = fopen(src,'w');
    
    fprintf(fd, 'close all; clear all; more off;\n');
    fprintf(fd, '\n');
    
    fprintf(fd, 'xnode = [\n');
    for i = 1 : size(xnode,1)
        fprintf(fd, '  %.16f, %.16f;\n', xnode(i,:));
    end
    fprintf(fd, '];\n');
    fprintf(fd, '\n');
    
    fprintf(fd, 'icone = [\n');
    for i = 1 : size(icone,1)
        fprintf(fd, '  %6d, %6d, %6d, %6d;\n', icone(i,:));
    end
    fprintf(fd, '];\n');
    fprintf(fd, '\n');
    
    fprintf(fd, 'DIR = [\n');
    for i = 1 : size(DIR,1)
        fprintf(fd, '  %6d, %.16f;\n', DIR(i,:));
    end
    fprintf(fd, '];\n');
    fprintf(fd, '\n');
    
    fprintf(fd, 'NEU = [\n');
    for i = 1 : size(NEU,1)
        fprintf(fd, '  %6d, %.16f, %d;\n', NEU(i,:));
    end
    fprintf(fd, '];\n');
    fprintf(fd, '\n');
    
    fprintf(fd, 'ROB = [\n');
    for i = 1 : size(ROB,1)
        fprintf(fd, '  %6d, %.16f, %.16f, %d;\n', ROB(i,:));
    end
    fprintf(fd, '];\n');
    fprintf(fd, '\n');
    
    fprintf(fd, 'PUN = [\n');
    for i = 1 : size(PUN,1)
        fprintf(fd, '  %6d, %.16f, %.16f, %.16f\n', PUN(i,:));
    end
    fprintf(fd, '];\n');
    fprintf(fd, '\n');
    
    fprintf(fd, 'disp(''---------------------------------------------------------------'');\n');
    fprintf(fd, 'disp(''Inicializando modelo de datos...'');\n');
    fprintf(fd, '\n');
    fprintf(fd, 'model.nnodes = size(xnode,1);\n');
    fprintf(fd, 'model.nelem = size(icone,1);\n');
    fprintf(fd, '\n');
    fprintf(fd, 'model.kx = %.16f;\n', model.kx);
    fprintf(fd, 'model.ky = %.16f;\n', model.ky);
    fprintf(fd, 'model.c = %.16f;\n', model.c);
    fprintf(fd, '\n');
    fprintf(fd, 'model.G = [\n');
    for i = 1 : size(model.G,1)
        fprintf(fd, '    %.16f;\n',model.G(i));
    end
    fprintf(fd, '];\n');
    fprintf(fd, '\n');
    fprintf(fd, '%% Esquema Temporal: [0] Explícito, [1] Implícito, [X] Estacionario\n');
    fprintf(fd, 'model.ts = %d;\n', model.ts);
    fprintf(fd, '\n');
    fprintf(fd, '%% Parámetros para esquemas temporales\n');
    fprintf(fd, 'model.rho = %.16f;\n', model.rho);
    fprintf(fd, 'model.cp = %.16f;\n', model.cp);
    fprintf(fd, 'model.maxit = %12d;\n', model.maxit);
    fprintf(fd, 'model.tol = %e;\n', model.tol);
    if (model.ts == 1)
        fprintf(fd, 'model.dt = %.16f;\n', model.dt);
    end

    fprintf(fd, '\n');
    fprintf(fd, '%% Condición inicial\n');
    if (size(DIR,1) > 0)
        fprintf(fd, 'model.PHI_n = mean(DIR(:,2))*ones(model.nnodes,1);\n');
    else
        fprintf(fd, 'model.PHI_n = 0*ones(model.nnodes,1);\n');
    end
    fprintf(fd, '\n');
    fprintf(fd, 'disp(''Iniciando el método numérico...'');\n');
    fprintf(fd, '\n');
    fprintf(fd, '%% Llamada principal al Método de Elementos Finitos\n');
    fprintf(fd, '[PHI,Q] = fem2d_heat(xnode,icone,DIR,NEU,ROB,PUN,model);\n');
    fprintf(fd, '\n');
    fprintf(fd, 'disp(''Finalizada la ejecución del método numérico.'');\n');
    fprintf(fd, '\n');
    fprintf(fd, 'disp(''---------------------------------------------------------------'');\n');
    fprintf(fd, 'disp(''Iniciando el post-procesamiento...'');\n');
    fprintf(fd, '\n');
    fprintf(fd, '%% mode ---> modo de visualización:\n');
    fprintf(fd, '%%           [0] 2D - Con malla\n');
    fprintf(fd, '%%           [1] 3D - Con malla\n');
    fprintf(fd, '%%           [2] 2D - Sin malla\n');
    fprintf(fd, '%%           [3] 3D - Sin malla\n');
    fprintf(fd, '%% graph --> tipo de gráfica:\n');
    fprintf(fd, '%%           [0] Temperatura (escalar)\n');
    fprintf(fd, '%%           [1] Flujo de Calor (vectorial)\n');
    fprintf(fd, '%%           [2] Flujo de Calor eje-x (escalar)\n');
    fprintf(fd, '%%           [3] Flujo de Calor eje-y (escalar)\n');
    fprintf(fd, '%%           [4] Magnitud de Flujo de Calor (escalar)\n');
    fprintf(fd, 'mode = 0;\n');
    fprintf(fd, 'graph = 0;\n');
    fprintf(fd, 'fem2d_heat_graph_mesh(full(PHI),Q,xnode,icone,mode,graph);\n');
    fprintf(fd, '\n');
    fprintf(fd, 'disp(''Finalizado el post-procesamiento.'');\n');
    fclose(fd);
end
