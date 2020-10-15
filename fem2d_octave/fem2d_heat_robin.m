function [K,F] = fem2d_heat_robin(K,F,ROB,xnode)
    for i=1:size(ROB,1)
        x=xnode(ROB(i,1),:)-xnode(ROB(i,2),:); % Side Coordinaates
        l = sqrt(x*transpose(x));                  % Side Size
        side = [ROB(i,1) ROB(i,2)];            % Side Nodes
        hT = ROB(i,3)*ROB(i,4);
        K(side,side) = K(side,side)+ROB(i,3)*l/6*[2 1;1 2];
        F(side) = F(side) + (l*hT/2)*ones(2,1);     
    end
end