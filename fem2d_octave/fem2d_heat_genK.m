function [localK] = fem2d_heat_genK(nodes,kx,ky)
    k = [kx 0;0 ky];
    if (size(nodes,1) == 3) % elemento triangular
        J = [nodes(2,1)-nodes(1,1)  nodes(2,2)-nodes(1,2);
             nodes(3,1)-nodes(1,1)  nodes(3,2)-nodes(1,2)];
        DN = [-1 1 0;-1 0 1];
        B = J\DN; % inv(J)*DN;
        A = 0.5;

        localK = (B'*k*B)*det(J)*A;
    else 
        % cuatro puntos de Gauss con peso w=1
        p = sqrt(3)/3;
        pospg = [-p,p];
        localK = zeros(4,4);
        for i=1:2
            for j=1:2
                s = pospg(i);
                t = pospg(j);
                DNnum = [   (-1+t)/4,( 1-t)/4,( 1+t)/4,(-1-t)/4;
                            (-1+s)/4,(-1-s)/4,( 1+s)/4,( 1-s)/4     ];
                J = DNnum*nodes;
                B = J\DNnum; % inv(J)*DNnum;
                localK = localK + B'*k*B*det(J);
            end
        end
    end
end