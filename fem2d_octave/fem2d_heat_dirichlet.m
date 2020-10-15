function [K,F] = fem2d_heat_dirichlet(K,F,DIR)
    for i = 1 : size(DIR,1)
        P = DIR(i,1);
        K(P,:) = 0;
        K(P,P) = 1;
        F(P) = DIR(i,2);
    end
end