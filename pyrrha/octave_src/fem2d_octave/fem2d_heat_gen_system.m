function [K,C,F] = fem2d_heat_gen_system(K,C,F,xnode,icone,model)
    % Check if Mass Matrix needs to be calculated and assembled
    if (model.c ~= 0 || model.ts == 0 || model.ts == 1)
        calc_mass = true;
    else
        calc_mass = false;
    end
    
    % Matrices and vectors elementary -- assembly
    for e = 1 : model.nelem
        if (icone(e,4) == -1)
            elem = icone(e,1:3);
        else
            elem = icone(e,:);
        end
        nodes = xnode(elem,:);
        
        % Calculate and assembly local Diffusion Matrix and Termical Flux Vector
        [localK] = fem2d_heat_genK(nodes,model.kx,model.ky);
        [localF] = fem2d_heat_genF(nodes,model.G(e));
        K(elem,elem) = K(elem,elem) + localK;
        F(elem) = F(elem) + localF;
    
        % Calculate and assembly local Mass Matrix
        if calc_mass
            [localC] = fem2d_heat_genC(nodes);
            C(elem,elem) = C(elem,elem) + localC;
        end
    end
    
    K = K + model.c*C; % System Matrix
end

