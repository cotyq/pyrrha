function [PHI,Q] = fem2d_heat_solve(K,C,F,xnode,icone,model)
    % Esquema temporal: [0] Explícito, [1] Implícito, [X] Estacionario
    if model.ts == 0 % Explicit
        disp('Iniciando esquemas temporales...');
        % Paso temporal del método explícito Explícito (Forward Euler)
        [dt] = fem2d_heat_explicit_delta_t(xnode,icone,model);
        [PHI,Q] = fem2d_heat_explicit(K,C,F,xnode,icone,model,dt);
    elseif model.ts == 1 % Implicit
        disp('Iniciando esquemas temporales...');
        % Paso temporal arbitrario
        dt = model.dt;
        [PHI,Q] = fem2d_heat_implicit(K,C,F,xnode,icone,model,dt);
    else % Estado Estacionario
        disp('Resolución del sistema de ecuaciones...');
        % Resolución del sistema lineal de ecuaciones
        PHI = K\F;
        
        % Cálculo del flujo de calor
        [Q] = fem2d_heat_flux(xnode,icone,model,PHI);
    end
end

