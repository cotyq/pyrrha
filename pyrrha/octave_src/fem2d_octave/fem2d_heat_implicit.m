function [PHI_vec,Q_vec] = fem2d_heat_implicit(K,C,F,xnode,icone,model,dt)
    auxA = dt/(model.rho*model.cp);

    PHI = model.PHI_n;
    PHI_n = model.PHI_n;
    PHI_vec = PHI;
    Q_vec = zeros(model.nnodes,2);
    
    Kn = (1/auxA)*C + K;
    
    for n = 1 : model.maxit
        Fn = F + (1/auxA)*C*PHI_n;
        PHI = Kn\Fn;

        % Error relativo entre las últimas dos iteraciones
        err = norm(PHI-PHI_n,2)/norm(PHI,2);
        
        % actualizo phi(n+1) será phi(n) para el siguiente paso
        PHI_n = PHI;
        PHI_vec = [PHI_vec PHI];
        
        [Q] = fem2d_heat_flux(xnode,icone,model,PHI);
        Q_vec = [Q_vec, Q];
        
        % para informar por consola el grado de avance del esquema temporal
        if model.verbose
            [model] = aux_ts_progress(model, n, err);
        end
        
        if err < model.tol
            if model.verbose
                disp('Método terminado por tolerancia de error.');
            end
            
            return;
        end
    end

    if model.verbose
        disp('Método terminado por límite de iteraciones.');
    end
end
