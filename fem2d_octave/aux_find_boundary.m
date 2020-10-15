function [boundary] = aux_find_boundary(xnode,icone,pA,pB,mode)
    boundary = [];
    
    % mode == 1 --> finds all nodes that belong to the boundary defined by [pA,pB]
    if mode == 1
        for i = 1 : size(xnode, 1)
           pC = xnode(i,:);

           if aux_check_point(pA, pB, pC)
               boundary = [ boundary; i ];
           end
        end
    end
    
    % mode == 2 --> finds all node-pairs that belong to the boundary defined by [pA,pB]
    if mode == 2
        for i = 1 : size(icone,1)
            if icone(i,4) == -1
                pC1 = xnode(icone(i,1),:);
                pC2 = xnode(icone(i,2),:);
                pC3 = xnode(icone(i,3),:);
                
                if aux_check_point(pA, pB, pC1) && aux_check_point(pA, pB, pC2)
                    boundary = [ boundary; icone(i,1), icone(i,2) ];
                end
                
                if aux_check_point(pA, pB, pC2) && aux_check_point(pA, pB, pC3)
                    boundary = [ boundary; icone(i,2), icone(i,3) ];
                end
                
                if aux_check_point(pA, pB, pC3) && aux_check_point(pA, pB, pC1)
                    boundary = [ boundary; icone(i,3), icone(i,1) ];
                end
            else
                pC1 = xnode(icone(i,1),:);
                pC2 = xnode(icone(i,2),:);
                pC3 = xnode(icone(i,3),:);
                pC4 = xnode(icone(i,4),:);
                
                if aux_check_point(pA, pB, pC1) && aux_check_point(pA, pB, pC2)
                    boundary = [ boundary; icone(i,1), icone(i,2) ];
                end
                
                if aux_check_point(pA, pB, pC2) && aux_check_point(pA, pB, pC3)
                    boundary = [ boundary; icone(i,2), icone(i,3) ];
                end
                
                if aux_check_point(pA, pB, pC3) && aux_check_point(pA, pB, pC4)
                    boundary = [ boundary; icone(i,3), icone(i,4) ];
                end
                
                if aux_check_point(pA, pB, pC4) && aux_check_point(pA, pB, pC1)
                    boundary = [ boundary; icone(i,4), icone(i,1) ];
                end
            end
        end
    end
end

