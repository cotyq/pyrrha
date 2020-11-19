function [] = fem2d_heat_post_process(mode,graph)
%% mode --->  visualization mode:
%             [0] 2D - With mesh (default)
%             [1] 3D - With mesh
%             [2] 2D - Without mesh
%             [3] 3D - Without mesh
%% graph ---> graph selection: 
%             [0] Temperature (scalar)
%             [1] Heat flux (vectorial)
%             [2] Heat fux x-axis (scalar)
%             [3] Heat flux y-axix (scalar)
%             [4] Heat flux magnitude


    load('results.mat');
    fem2d_heat_graph_mesh(full(PHI),Q,xnode,icone,mode,graph);
    
    disp('---------------------------------------------------------------');
    disp('Finalizado el post-procesamiento.');
end