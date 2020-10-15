function [PUN] = fem2d_heat_set_pcond(xnode,icone,PUN)
    % First step, try to find the element of each punctual source
    for i = 1 : size(PUN,1)
        Px = PUN(i,3);
        Py = PUN(i,4);
        
        [idx] = aux_find_element(xnode,icone,Px,Py);
        PUN(i,1) = idx;
    end
    
    % Second step, clean all those sources that don't belong to any element
    PUN_old = PUN;
    PUN = [];
    for i = 1 : size(PUN_old,1)
        if (PUN_old(i,1) ~= -1)
            PUN = [PUN; PUN_old(i,:)];
        end
    end
end

