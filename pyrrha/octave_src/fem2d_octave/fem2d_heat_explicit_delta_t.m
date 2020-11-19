function [dt] = fem2d_heat_explicit_delta_t(xnode,icone,model)
    alpha = mean(model.kx,model.ky)/(model.rho*model.cp);

    delta = [];
    
    for e = 1 : model.nelem
        if icone(e,4) == -1
            ele = icone(e,1:3);
            d1 = norm(xnode(ele(1),:)-xnode(ele(2),:),2);
            d2 = norm(xnode(ele(2),:)-xnode(ele(3),:),2);
            d3 = norm(xnode(ele(3),:)-xnode(ele(1),:),2);
            % promedio de los 3 lados dividido 2
            delta = [delta (d1+d2+d3)/6];
        else
            ele = icone(e,:);
            d1 = norm(xnode(ele(1),:)-xnode(ele(2),:),2);
            d2 = norm(xnode(ele(2),:)-xnode(ele(3),:),2);
            d3 = norm(xnode(ele(3),:)-xnode(ele(4),:),2);
            d4 = norm(xnode(ele(4),:)-xnode(ele(1),:),2);
            % promedio de los 4 lados dividido 2
            delta = [delta (d1+d2+d3+d4)/8];
        end
    end
    dx = min(delta);
    % valor límite (crítico)
    % dt = 0.5*dx^2/(2*alpha);
    dt = 0.25*dx^2/(2*alpha);
end

