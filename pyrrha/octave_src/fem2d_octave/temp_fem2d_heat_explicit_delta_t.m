function [dt] = fem2d_heat_explicit_delta_t(xnode,icone,model)
% Descripción: módulo para calcular el paso temporal crítico para esquema 
% temporal explícito a partir de las constantes del modelo y las dimensiones
% de los elementos de la malla.

% Entrada:
% * xnode: matriz de nodos con pares (x,y) representando las coordenadas de 
%   cada nodo de la malla.
% * icone: matriz de conectividad. Indica los 3 ó 4 nodos que integran el 
%   elemento, recorridos en cualquier orden pero en sentido antihorario. 
%   En caso de elementos triangulares, la cuarta columna siempre es -1.
% * model: struct con todos los datos del modelo (constantes, esquema numérico, etc.)

% Salida:
% * dt: paso temporal crítico para método explícito.
% ----------------------------------------------------------------------

    dt = [];
    
end

