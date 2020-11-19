function [F] = fem2d_heat_pcond(F,xnode,icone,PUN)
    for n = 1 : size(PUN,1)
        e = PUN(n,1);
        G = PUN(n,2);
        xp = PUN(n,3);
        yp = PUN(n,4);
        if icone(e,4) == -1 % triangular element
            ele = icone(e,1:3);
        else
            ele = icone(e,:);
        end
        nodes = xnode(ele,:);
        N = fem2d_heat_blerp(nodes,xp,yp);
        f = N*G;
        F(ele) = F(ele) + f;
    end
end