function [idx] = aux_find_element(xnode,icone,Px,Py)
    idx = -1;
    
    for i = 1 : size(icone,1)
        if (icone(i,4) == -1)
            [N] = fem2d_heat_blerp(xnode(icone(i,1:3),:),Px,Py);
            [N1] = aux_check_fn_value(N(1));
            [N2] = aux_check_fn_value(N(2));
            [N3] = aux_check_fn_value(N(3));
            
            if (N1 >= 0 && N1 <= 1 && ...
                N2 >= 0 && N2 <= 1 && ...
                N3 >= 0 && N3 <= 1)
            
                idx = i;
                break;
            end
        else
           [N] = fem2d_heat_blerp(xnode(icone(i,:),:),Px,Py);
            [N1] = aux_check_fn_value(N(1));
            [N2] = aux_check_fn_value(N(2));
            [N3] = aux_check_fn_value(N(3));
            [N4] = aux_check_fn_value(N(4));

            if (N1 >= 0 && N1 <= 1 && ...
                N2 >= 0 && N2 <= 1 && ...
                N3 >= 0 && N3 <= 1 && ...
                N4 >= 0 && N4 <= 1)
            
                idx = i;
                break;
            end
        end
    end
end

