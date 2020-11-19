function [xnode_sort,icone_sort] = aux_mesh_sort(xnode, icone)
    [xnode_sort,idx] = sortrows(xnode);
    
    icone_sort = (-1)*ones(size(icone));
    
    for i = 1 : size(icone,1)
        P1 = icone(i,1);
        P2 = icone(i,2);
        P3 = icone(i,3);
        P4 = icone(i,4);
        
        [i1,~,~] = find(idx == P1);
        [i2,~,~] = find(idx == P2);
        [i3,~,~] = find(idx == P3);
        if (P4 ~= -1)
            [i4,~,~] = find(idx == P4);
        else
            i4 = -1;
        end
        
        icone_sort(i,:) = [i1, i2, i3, i4];
    end
    
    icone_sort = sortrows(icone_sort);
end

