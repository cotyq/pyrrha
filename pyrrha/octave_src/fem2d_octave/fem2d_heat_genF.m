function [localF] = fem2d_heat_genF(nodes,G)
    if (size(nodes,1) == 3)
        A = 0.5*det([1 nodes(1,1) nodes(1,2);
                     1 nodes(2,1) nodes(2,2);
                     1 nodes(3,1) nodes(3,2);]);
        
        localF = ones(3,1)*G*A/3;
    else
        A1 = 0.5*det([1 nodes(1,1) nodes(1,2);
                     1 nodes(2,1) nodes(2,2);
                     1 nodes(3,1) nodes(3,2);]);
        A2 = 0.5*det([1 nodes(1,1) nodes(1,2);
                     1 nodes(3,1) nodes(3,2);
                     1 nodes(4,1) nodes(4,2);]);
        A = A1+A2;
        
        localF = ones(4,1)*G*A/4;
    end
end