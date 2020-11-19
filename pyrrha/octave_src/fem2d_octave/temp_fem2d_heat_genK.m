function [localK] = fem2d_heat_genK(nodes,kx,ky)
% Descripción: módulo para calcular y evaluar de forma numérica la matriz de
% difusión K. Se utilizan funciones de forma en coordenadas naturales y se 
% resuelve la integral de forma numérica utilizando cuadratura de Gauss.

% Entrada:
% * nodes: nodos (x,y) del elemento. Los elementos admisibles son de 3 o 4 nodos.
% * kx: conductividad térmica orientada en eje-x.
% * ky: conductividad térmica orientada en eje-y.

% Salida:
% * localK: matriz de difusión del elemento (local).
% ----------------------------------------------------------------------

    localK = [];
    
end