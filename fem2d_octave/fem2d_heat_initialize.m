function [K,C,F] = fem2d_heat_initialize(nnodes)
    % Inicialización de las variables principales del Sistema
    K = sparse(nnodes,nnodes);
    C = sparse(nnodes,nnodes);
    F = sparse(nnodes,1);
end

