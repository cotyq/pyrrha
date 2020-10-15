function [Qn] = fem2d_heat_flux(xnode,icone,model,PHI)
% Descripción: módulo calcular el flujo de calor en todo el dominio. Se aplica
% la Ley de Fourier y se evalúa como fluye el calor en todos los puntos (nodos)
% del dominio.

% Entrada:
% * K: matriz del sistema (difusión + reacción)
% * F: vector de flujo térmico.
% * PHI: vector solución. Cada elemento del vector representa un valor escalar
%   asociado a cada nodo de la malla, y su posición dentro del vector depende 
%   de cómo se especificó cada nodo en xnode.

% Salida:
% * Q: vector de flujo de calor.
% ----------------------------------------------------------------------

    Qn = [];
    
end

