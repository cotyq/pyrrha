function [xnode,icone] = aux_mesh_subd(xnode,icone,level)
    for l = 1 : level
        % first subdivide rectangular mesh into smaller elements
        % each rectangle forms now 4 new rectangles
        % updates both xnode and icone
        xnode_mod = xnode;
        icone_mod = icone;
        N = size(xnode,1);

        % for each element
        for i = 1 : size(icone,1)
            if icone(i,4) == -1
                % TRIANGULAR ELEMENTS

                % get current element nodes
                N1 = icone(i,1);
                N2 = icone(i,2);
                N3 = icone(i,3);

                % create new nodes at the midpoint of each two points
                a = (xnode(icone(i,1),:) + xnode(icone(i,2),:))/2;
                b = (xnode(icone(i,2),:) + xnode(icone(i,3),:))/2;
                c = (xnode(icone(i,3),:) + xnode(icone(i,1),:))/2;

                % checks if new node already was inserted
                % if not exist, update xnode and node counter
                % if exist, update only index of already inserted node
                idxa = find(ismember(xnode_mod,a,'rows'), 1);
                if (isempty(idxa))
                    xnode_mod = [xnode_mod; a];
                    N = N + 1; Na = N;
                else
                    Na = idxa;
                end

                idxb = find(ismember(xnode_mod,b,'rows'), 1);
                if (isempty(idxb))
                    xnode_mod = [xnode_mod; b];
                    N = N + 1; Nb = N;
                else
                    Nb = idxb;
                end

                idxc = find(ismember(xnode_mod,c,'rows'), 1);
                if (isempty(idxc))
                    xnode_mod = [xnode_mod; c];
                    N = N + 1; Nc = N;
                else
                    Nc = idxc;
                end

                % updates icone removing former element and inserting the 4 new
                % elements
                [~,aux]=ismember(icone_mod,[N1 N2 N3 -1],'rows');
                idx = find(aux == 1);
                icone_mod = [
                    icone_mod(1:idx-1,:);
                    N1, Na,  Nc,  -1;
                    Na, N2,  Nb,  -1;
                    Na, Nb,  Nc,  -1;
                    Nc, Nb,  N3,  -1;
                    icone_mod(idx+1:end,:)
                    ];

            else
                % QUADRANGULAR ELEMENTS

                % get current element nodes
                N1 = icone(i,1);
                N2 = icone(i,2);
                N3 = icone(i,3);
                N4 = icone(i,4);

                % create new nodes at the midpoint of each two points
                a = (xnode(icone(i,1),:) + xnode(icone(i,2),:))/2;
                b = (xnode(icone(i,2),:) + xnode(icone(i,3),:))/2;
                c = (xnode(icone(i,3),:) + xnode(icone(i,4),:))/2;
                d = (xnode(icone(i,4),:) + xnode(icone(i,1),:))/2;

                % checks if new node already was inserted
                % if not exist, update xnode and node counter
                % if exist, update only index of already inserted node
                idxa = find(ismember(xnode_mod,a,'rows'), 1);
                if (isempty(idxa))
                    xnode_mod = [xnode_mod; a];
                    N = N + 1; Na = N;
                else
                    Na = idxa;
                end

                idxb = find(ismember(xnode_mod,b,'rows'), 1);
                if (isempty(idxb))
                    xnode_mod = [xnode_mod; b];
                    N = N + 1; Nb = N;
                else
                    Nb = idxb;
                end

                idxc = find(ismember(xnode_mod,c,'rows'), 1);
                if (isempty(idxc))
                    xnode_mod = [xnode_mod; c];
                    N = N + 1; Nc = N;
                else
                    Nc = idxc;
                end

                idxd = find(ismember(xnode_mod,d,'rows'), 1);
                if (isempty(idxd))
                    xnode_mod = [xnode_mod; d];
                    N = N + 1; Nd = N;
                else
                    Nd = idxd;
                end

                % mid point of two mid points...always is unique
                e = (a + c)/2; N = N + 1; Ne = N;
                xnode_mod = [xnode_mod; e];

                % updates icone removing former element and inserting the 4 new
                % elements
                [~,aux]=ismember(icone_mod,[N1,N2,N3,N4],'rows');
                idx = find(aux == 1);
                icone_mod = [
                    icone_mod(1:idx-1,:);
                    N1, Na,  Ne,  Nd;
                    Na, N2,  Nb,  Ne;
                    Ne, Nb,  N3,  Nc;
                    Nd, Ne,  Nc,  N4;
                    icone_mod(idx+1:end,:)
                    ];

            end
        end

        xnode = xnode_mod;
        icone = icone_mod;
    end
end
