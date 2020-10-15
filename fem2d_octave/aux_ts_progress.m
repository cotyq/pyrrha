function [ model ] = aux_ts_progress(model, niter, err)
    e1 = niter / model.maxit * 100;
    e2 = log(err) / log(model.tol) * 100;
    
    progress = round(max(e1, e2));
    
    if (mod(progress, 20) == 0 && progress >= 20 && progress < 40 && ~model.reach20)
        fprintf(' 20 %% completado de la ejecución del Esquema Temporal...\n');
        model.reach20 = true;
    elseif (mod(progress, 40) == 0 && progress >= 40 && progress < 60 && ~model.reach40)
        fprintf(' 40 %% completado de la ejecución del Esquema Temporal...\n');
        model.reach40 = true;
    elseif (mod(progress, 60) == 0 && progress >= 60 && progress < 80 && ~model.reach60)
        fprintf(' 60 %% completado de la ejecución del Esquema Temporal...\n');
        model.reach60 = true;
    elseif (mod(progress, 80) == 0 && progress >= 80 && progress < 100 && ~model.reach80)
        fprintf(' 80 %% completado de la ejecución del Esquema Temporal...\n');
        model.reach80 = true;
    elseif (mod(progress, 100) == 0 && progress >= 100 && ~model.reach100)
        fprintf('100 %% completado de la ejecución del Esquema Temporal...\n');
        model.reach100 = true;
    end
end

