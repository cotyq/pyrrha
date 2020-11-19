function [DIR,NEU,ROB] = fem2d_heat_set_boundary(xnode,icone,BC)
    DIR = [];
    NEU = [];
    ROB = [];

    for i = 1 : size(BC,1)
        % DIRICHLET
        if BC(i,1) == 1
            pA = BC(i,2:3);
            pB = BC(i,4:5);
            phi = BC(i,6);

            [boundary] = aux_find_boundary(xnode,icone,pA,pB,1);
            aux = [boundary ones(size(boundary,1),1)*phi];
            DIR = [DIR; aux];
        end

        % NEUMANN
        if BC(i,1) == 2
            pA = BC(i,2:3);
            pB = BC(i,4:5);
            q = BC(i,6);

            [boundary] = aux_find_boundary(xnode,icone,pA,pB,2);
            aux = [boundary ones(size(boundary,1),1)*q];
            NEU = [NEU; aux];
        end

        % ROBIN
        if BC(i,1) == 3
            pA = BC(i,2:3);
            pB = BC(i,4:5);
            h = BC(i,6);
            phi_inf = BC(i,7);

            [boundary] = aux_find_boundary(xnode,icone,pA,pB,2);
            a = ones(size(boundary,1),1)*h;
            b = ones(size(boundary,1),1)*phi_inf;
            aux = [boundary a b];
            ROB = [ROB; aux];
        end
    end
end
