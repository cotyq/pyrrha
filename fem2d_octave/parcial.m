close all; clear all; more off;

xnode = [
  0.0000000000000000, 0.0000000000000000;
  0.0000000000000000, 0.2000000000000000;
  0.3333333333333333, 0.0000000000000000;
  0.3333333333333333, 0.2000000000000000;
  0.6666666666666666, 0.0000000000000000;
  0.6666666666666666, 0.2000000000000000;
  1.0000000000000000, 0.0000000000000000;
  1.0000000000000000, 0.2000000000000000;
];

icone = [
       1,      3,      2,     -1;
       3,      4,      2,     -1;
       3,      5,      4,     -1;
       5,      6,      4,     -1;
       5,      7,      6,     -1;
       7,      8,      6,     -1;
];

DIR = [
       1, 0.0000000000000000;
       2, 0.0000000000000000;
       7, 200.0000000000000000;
       8, 200.0000000000000000;
];

NEU = [
       1, 3.0000000000000000, 0;
       3, 5.0000000000000000, 0;
       4, 2.0000000000000000, 0;
       5, 7.0000000000000000, 0;
       6, 4.0000000000000000, 0;
       8, 6.0000000000000000, 0;
];

ROB = [
];

PUN = [
];

disp("---------------------------------------------------------------");
disp("Inicializando modelo de datos...");

model.nnodes = size(xnode,1);
model.nelem = size(icone,1);

model.kx = 1.0000000000000000;
model.ky = 1.0000000000000000;
model.c = 0.0000000000000000;

model.G = [
    500.0000000000000000;
    0.0000000000000000;
    -200.0000000000000000;
    0.0000000000000000;
    0.0000000000000000;
    0.0000000000000000;
];

% Esquema Temporal: [0] Explícito, [1] Implícito, [X] Estacionario
model.ts = 2;

% Parámetros para esquemas temporales
model.rho = 1.0000000000000000;
model.cp = 1.0000000000000000;
model.maxit =            1;
model.tol = 1.000000e-05;

% Condición inicial
model.PHI_n = mean(DIR(:,2))*ones(model.nnodes,1);

disp("Iniciando el método numérico...");

% Llamada principal al Método de Elementos Finitos
[PHI,Q] = fem2d_heat(xnode,icone,DIR,NEU,ROB,PUN,model);

disp("Finalizada la ejecución del método numérico.");

disp("---------------------------------------------------------------");
disp("Iniciando el post-procesamiento...");

% mode ---> modo de visualización:
%           [0] 2D - Con malla
%           [1] 3D - Con malla
%           [2] 2D - Sin malla
%           [3] 3D - Sin malla
% graph --> tipo de gráfica:
%           [0] Temperatura (escalar)
%           [1] Flujo de Calor (vectorial)
%           [2] Flujo de Calor eje-x (escalar)
%           [3] Flujo de Calor eje-y (escalar)
%           [4] Magnitud de Flujo de Calor (escalar)
mode = 0;
graph = 0;
fem2d_heat_graph_mesh(full(PHI),Q,xnode,icone,mode,graph);

disp("Finalizado el post-procesamiento.");
