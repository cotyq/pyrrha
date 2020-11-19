function [] = fem2d_heat_graph_mesh(PHI,Q,xnode,icone,mode,graph)
    figure('Name', 'Resultados');
    
    if (mode == 0 || mode == 2)
        vm = 2;
    elseif (mode == 1 || mode == 3)
        vm = 3;
    else
        vm = 2;
        mode = 0;
    end
    
    if (graph < 0 || graph > 5)
        graph = 0;
    end
    
    err = 1;
    
    for i = 1 : size(PHI,2) - 1
        err = [err; norm(PHI(:,i+1)-PHI(:,i),2)/norm(PHI(:,i),2)];
    end
    
    X = xnode(:,1);
    Y = xnode(:,2);
    
    triangles = [];
    rectangles = [];
    for i = 1 : size(icone,1)
        if icone(i,4) == -1
            triangles = [triangles; icone(i,1:3)]; %#ok<*AGROW>
        end
    end
    
    trimesh = triangles;
    for i = 1 : size(icone,1)
        if icone(i,4) ~= -1
            i1 = icone(i,1);
%             i2 = icone(i,2);
            i3 = icone(i,3);
            i4 = icone(i,4);
            trimesh = [trimesh; icone(i,1:3); i1,i3,i4];
            rectangles = [rectangles; icone(i,:)];
        end
    end
    
    xmax = max(xnode(:,1));
    xmin = min(xnode(:,1));
    ymax = max(xnode(:,2));
    ymin = min(xnode(:,2));
    zmax = max(max(PHI));
    zmin = min(min(PHI));
    
    ratio = (xmax-xmin)/(ymax-ymin);
    
    %% Temperature (scalar)
    if graph == 0        
        for i = 1 : size(PHI,2)
            clf;
        	
            Z = PHI(:,i);
        
            hold on;
            patch('Vertices',[X Y Z],'Faces',trimesh,'FaceVertexCData',Z);
            hold off;
            shading interp;
            
            if (mode < 2)
                hold on;
                patch('Vertices',[X Y Z],'Faces',triangles,'FaceVertexCData',Z,...
                'FaceColor','none');
                
                patch('Vertices',[X Y Z],'Faces',rectangles,'FaceVertexCData',Z,...
                'FaceColor','none');
                hold off;
            end
            
            if (i > 1)
                title(sprintf('nit: %d - error: %e',i-1,err(i)));
            end

            view(vm);
            grid on;
            pbaspect([ratio 1 1]);
            zlim([zmin-0.001, zmax+0.001]);
            drawnow;
            pause(0.000001);
        end
            
        colorbar;
    end
    
    %% Heat Flux (vectorial)
    if graph == 1
        maxq = max(max(abs(Q)));
        
        if (maxq > 0 && maxq < 5)
            scale = 1/maxq;
        elseif (maxq >= 5 && maxq < 10)
            scale = 2/maxq;
        elseif (maxq >= 10 && maxq < 100)
            scale = 3/maxq;
        elseif (maxq >= 100 && maxq < 1000)
            scale = 4/maxq;
        elseif (maxq >= 1000)
            scale = 5/maxq;
        else
            scale = 1;
        end
        
        for i = 1 : size(PHI,2)
            clf;
            Z = PHI(:,i);
            
            if (mode < 2)
                hold on;
                patch('Vertices',[X Y Z],'Faces',triangles,'FaceVertexCData',Z,...
                    'FaceColor','none');
                patch('Vertices',[X Y Z],'Faces',rectangles,'FaceVertexCData',Z,...
                    'FaceColor','none');
                hold off;
                shading interp;
            end
                
            hold on;
            Qx = Q(:,2*(i-1)+1);
            Qy = Q(:,2*(i-1)+2);
            Qz = zeros(size(Qx,1),1);
            quiver3(xnode(:,1), xnode(:,2), Z, Qx, Qy, Qz,...
                scale, 'color', 'black');
            hold off;
            if (i > 1)
                title(sprintf('nit: %d - error: %e',i-1,err(i)));
            end

            xlim([xmin-(xmax-xmin)*.1, xmax+(xmax-xmin)*.1]);
            ylim([ymin-(ymax-ymin)*.1, ymax+(ymax-ymin)*.1]);
            zlim([zmin-(zmax-zmin)*.1, zmax+(zmax-zmin)*.1]);
            grid on;
            pbaspect([ratio 1 1]);
            view(vm);
            drawnow;
            pause(0.000001);
        end
        colorbar;
    end
    
    %% Heat Flux x-axis (scalar)
    if graph == 2
        zmax = max(max(Q));
        zmin = min(min(Q));
        
        for i = 1 : size(PHI,2)
            clf;
            Z = Q(:,2*(i-1)+1);
            hold on;
            patch('Vertices',[X Y Z],'Faces',triangles,'FaceVertexCData',Z);
            patch('Vertices',[X Y Z],'Faces',rectangles,'FaceVertexCData',Z);
            hold off;
            shading interp;

            if (mode < 2)
                hold on;
                patch('Vertices',[X Y Z],'Faces',triangles,'FaceVertexCData',Z,...
                'FaceColor','none');
                patch('Vertices',[X Y Z],'Faces',rectangles,'FaceVertexCData',Z,...
                'FaceColor','none');
                hold off;
            end
            
            if (i > 1)
                title(sprintf('nit: %d - error: %e',i-1,err(i)));
            end
            
            grid on;
            zlim([zmin zmax]);
            pbaspect([ratio 1 1]);
            view(vm);
            drawnow;
            pause(0.000001);
        end
        colorbar;
    end
    
    %% Heat Flux y-axis (scalar)
    if graph == 3
        zmax = max(max(Q));
        zmin = min(min(Q));
        
        for i = 1 : size(PHI,2)
            clf;
            Z = Q(:,2*(i-1)+2);

            hold on;
            patch('Vertices',[X Y Z],'Faces',triangles,'FaceVertexCData',Z);
            patch('Vertices',[X Y Z],'Faces',rectangles,'FaceVertexCData',Z);
            hold off;
            shading interp;

            if (mode < 2)
                hold on;
                patch('Vertices',[X Y Z],'Faces',triangles,'FaceVertexCData',Z,...
                'FaceColor','none');
                patch('Vertices',[X Y Z],'Faces',rectangles,'FaceVertexCData',Z,...
                'FaceColor','none');
                hold off;
            end
            
            if (i > 1)
                title(sprintf('nit: %d - error: %e',i-1,err(i)));
            end

            grid on;
            zlim([zmin zmax]);
            pbaspect([ratio 1 1]);
            view(vm);
            drawnow;
            pause(0.000001);
        end
        colorbar;
    end
    
    %% Heat Flux magnitude (scalar)
    if graph == 4
        Z = zeros(size(PHI));
        for i = 1 : size(PHI,2)
            Qx = Q(:,2*(i-1)+1);
            Qy = Q(:,2*(i-1)+2);
            
            for j = 1 : size(Qx,1)
                Z(j,i) = norm([Qx(j), Qy(j)],2);
            end
        end
        
        zmax = max(max(Z));
        zmin = min(min(Z));
        
        for i = 1 : size(PHI,2)
            clf;
            hold on;
            patch('Vertices',[X Y Z(:,i)],'Faces',triangles,'FaceVertexCData',Z(:,i));
            patch('Vertices',[X Y Z(:,i)],'Faces',rectangles,'FaceVertexCData',Z(:,i));
            hold off;
            shading interp;

            if (mode < 2)
                hold on;
                patch('Vertices',[X Y Z(:,i)],'Faces',triangles,'FaceVertexCData',Z(:,i),...
                'FaceColor','none');
                patch('Vertices',[X Y Z(:,i)],'Faces',rectangles,'FaceVertexCData',Z(:,i),...
                'FaceColor','none');
                hold off;
            end
            
            if (i > 1)
                title(sprintf('nit: %d - error: %e',i-1,err(i)));
            end

            if (i > 1)
                title(sprintf('nit: %d - error: %e',i-1,err(i)));
            end

            grid on;
            zlim([zmin zmax]);
            pbaspect([ratio 1 1]);
            view(vm);
            drawnow;
            pause(0.000001);
        end
        colorbar;
    end
end


