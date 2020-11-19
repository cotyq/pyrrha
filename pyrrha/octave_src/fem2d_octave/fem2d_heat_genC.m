function [localC] = fem2d_heat_genC(nodes)
    if (size(nodes,1) == 3) % elemento triangular
        J = [nodes(2,1)-nodes(1,1)  nodes(2,2)-nodes(1,2);
             nodes(3,1)-nodes(1,1)  nodes(3,2)-nodes(1,2)];
        % tres puntos de Gauss con peso w=1/6
        detJ = det(J);
        w = 1/6;
        pospg = [0.5 0;0 0.5;0.5 0.5];
        localC = zeros(3);
        for i=1:3
            s = pospg(i,1);
            t = pospg(i,2);
            Nnum = [1-s-t, s, t];
            localC = localC + w*(Nnum')*Nnum*detJ;
        end
    else
        % cuatro puntos de Gauss con peso w=1
        p = sqrt(3)/3;
        pospg = [-p,p];
        localC = zeros(4);
        for i=1:2
            for j=1:2
                s = pospg(i);
                t = pospg(j);
                Nnum = [    0.25*(1-s)*(1-t)...
                            0.25*(1+s)*(1-t)...
                            0.25*(1+s)*(1+t)...
                            0.25*(1-s)*(1+t)    ];
            
                DNnum = [   (-1+t)/4,( 1-t)/4,( 1+t)/4,(-1-t)/4;
                            (-1+s)/4,(-1-s)/4,( 1+s)/4,( 1-s)/4     ];
                J = DNnum*nodes;
                localC = localC + (Nnum')*Nnum*det(J);
            end
        end
    end
end