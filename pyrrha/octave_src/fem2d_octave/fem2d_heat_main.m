close all; clear all;

% Load test meshes and boundary conditions
addpath('../meshes');

% sc_fem1;
% sc_fem2;
% sc_fem3;
% sc_fem4;
sc_fem5;
% sc_fem6;
% sc_fem7;
% sc_fem8;

% BC --> Boundary Condition vector. This vector has all the information needed to format
% every node on the mesh that belongs to a certain boundary. User should add one row to
% the vector for each side of the mesh that belongs to boundary. Then the algorithm for
% subdividing the mesh will find every node of each boundary and format it accordingly to
% Finite Difference Method (FDM)
% Format:
% Col. 1    - Type: [1] Dirichlet, [2] Neumann, [3] Robin, [4] Point load
% Cols. 2-3 - P1: 
%          * First point of the line that defines the boundary side (DIR, NEU, ROB)
%          * Point of application of load
% Cols. 4-5 - P2: second point of the line that defines the boundary side (DIR,NEU,ROB)
% Col. 6 - First value:
%          * Fixed (phi - Dirichlet [K])
%          * Heat flux (q - Neumann [W/m²])
%          * Convective heat transfer coefficient (h - Robin [W/m²K])
%          * Temperature source (g - Point load [W])
% Col. 7 - Second value: Reference temperature (phi_inf - Robin [K])

fprintf('---------------------------------------------------------------\n');
fprintf('Inicializando condiciones de contorno...\n');

BC = [  1,0.00,0.00,1.00,0.00,10,20;
        2,1.00,0.00,1.00,0.50,10,20;
        3,0.00,0.50,1.00,0.50,10,20;
        1,0.00,0.00,0.00,0.50,10,20;
        2, 1/3, 1/6, 2/3, 1/6,10,20;
        3, 2/3, 1/6, 2/3, 1/3,10,20;
        1, 1/3, 1/3, 2/3, 1/3,10,20;
        2, 1/3, 1/6, 1/3, 1/3,10,20;    ];

% BC = [  1,0,0,0,2,0,0;
%         2,0,0,2,0,0,0;
%         2,2,0,2,2,5,0;
%         3,0,2,2,2,1.5,10   ];
    
% BC = [  1,0,0,1,0,10,0;
%         1,1,0,0,1,10,0;
%         1,0,1,0,0,10,0;   ];

fprintf('Refinando malla...\n');

[xnode,icone] = aux_mesh_subd(xnode,icone,2);
[xnode,icone] = aux_mesh_sort(xnode,icone);

PUN = [
    -1,5,0.25,0.25;
    -1,5,0.75,0.25;
    -1,5,0.25,0.45;
    -1,5,0.75,0.45;
];
[PUN] = fem2d_heat_set_pcond(xnode,icone,PUN);

[DIR,NEU,ROB] = fem2d_heat_set_boundary(xnode,icone,BC);
[DIR,NEU,ROB] = aux_clean_boundary(DIR,NEU,ROB);

fprintf('Inicializando modelo de datos...\n');

% System's dimentions
model.nnodes = size(xnode,1);
model.nelem = size(icone,1);

% System's constants
model.kx  = 1;          % thermal conductivity (x-axis)
model.ky  = 1;          % thermal conductivity (y-axis)
model.c   = 0;          % reaction coefficient
model.G = 100*ones(model.nelem,1);     % heat source

% Time Scheme: [0] Explicit, [1] Implicit, [X] Stationary
model.ts = 2;

% Time Scheme's parameters
model.rho = 1;          % density
model.cp  = 1;          % specific heat at constant pressure
model.maxit = 900;      % max number of iterations
model.tol = 1e-8;       % error tolerance
model.dt = 0.001;       % time step

% Initial condition
if (size(DIR,1) > 0)
    model.PHI_n = mean(DIR(:,2))*ones(model.nnodes,1);
else
    model.PHI_n = 0*ones(model.nnodes,1);
end

% Time Scheme checkpoints
model.reach20 = false;
model.reach40 = false;
model.reach60 = false;
model.reach80 = false;
model.reach100 = false;
model.verbose = 1;

fprintf('Iniciando el método numérico...\n');

% Main call to Finite Element Method
[PHI,Q] = fem2d_heat(xnode,icone,DIR,NEU,ROB,PUN,model);

results.PHI = PHI;
results.Q = Q;
results.xnode = xnode;
results.icone = icone;
results.model = model;
results.DIR = DIR;
results.NEU = NEU;
results.ROB = ROB;
results.PUN = PUN;

save('results.mat', '-v7', '-struct', 'results');

%% mode ---> modo de visualización:
%            [0] 2D - Con malla (por defecto)
%            [1] 3D - Con malla
%            [2] 2D - Sin malla
%            [3] 3D - Sin malla
%% graph --> tipo de gráfica
%            [0] Temperatura (escalar) (por defecto)
%            [1] Flujo de Calor (vectorial)
%            [2] Flujo de Calor eje-x (escalar)
%            [3] Flujo de Calor eje-y (escalar)
%            [4] Magnitud de Flujo de Calor (escalar)

mode = 1;
graph = 0;
fem2d_heat_post_process(mode,graph);
