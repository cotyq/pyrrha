function [localF] = fem2d_heat_genF(nodes,G)
% Descripción: módulo para calcular el vector de flujo térmico F para cada
% elemento, producto de la presencia de una fuente de calor en dicho elemento.
% La integral se resuelve mediante cuadratura de punto medio, y se requiere
% evaluar el área del elemento.

% Entrada:
% * nodes: nodos (x,y) del elemento. Los elementos admisibles son de 3 o 4 nodos.
% * G: fuente de calor.

% Salida:
% * localF: vector de flujo térmico (local).
% ----------------------------------------------------------------------

    localF = [];
    
end