function [localC] = fem2d_heat_genC(nodes)
% Descripción: módulo para calcular y evaluar de forma numérica la matriz de
% masa C. Se utilizan funciones de forma en coordenadas naturales y se 
% resuelve la integral de forma numérica utilizando cuadratura de Gauss.

% Entrada:
% * nodes: nodos (x,y) del elemento. Los elementos admisibles son de 3 o 4 nodos.

% Salida:
% * localC: matriz de masa para elemento (local).
% ----------------------------------------------------------------------

    localC = [];
    
end