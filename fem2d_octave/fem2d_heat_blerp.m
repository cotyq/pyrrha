function [N] = fem2d_heat_blerp(nodes,xp,yp)    
    x1 = nodes(1,1); y1 = nodes(1,2);
    x2 = nodes(2,1); y2 = nodes(2,2);
    x3 = nodes(3,1); y3 = nodes(3,2);
    
    if (size(nodes,1)==3) %elemento triangular
        M = [x2-x1 x3-x1;y2-y1 y3-y1];
        b = [xp-x1;yp-y1];
        st = M\b;
        
        N1 = 1-st(1)-st(2); N2=st(1); N3=st(2);
        N = [N1; N2; N3];
    else
        x4 = nodes(4,1); y4 = nodes(4,2);
        
        M = [1 -1 1 -1;-1 1 1 -1;-1 -1 1 1];
        xy = [x1 y1;x2 y2;x3 y3;x4 y4];
        coef = M*xy;
        a1 = coef(1,1); a2 = coef(1,2);
        b1 = coef(2,1); b2 = coef(2,2);
        c1 = coef(3,1); c2 = coef(3,2);
        d1 = 4*xp-(x1+x2+x3+x4); d2 = 4*yp-(y1+y2+y3+y4);
        
        % Recorrido de posibilidades
        if (a1 == 0)
            if (a2 == 0)
                s = (d1*c2-d2*c1)/(b1*c2-b2*c1);
                t = (b1*d2-b2*d1)/(b1*c2-b2*c1);
            else
                if (c1 == 0)
                    s = d1/b1;
                    t = (b1*d2-b2*d1)/(a2*d1+b1*c2);
                else
                    a = a2*b1;
                    b = c2*b1-a2*d1-b2*c1;
                    c = d2*c1-c2*d1;
                    d = (b^2)-(4*a*c);
                    s1=(-b+sqrt(d))/(2*a);
                    s2=(-b-sqrt(d))/(2*a);
                    if (abs(s1) <= 1)
                        s = s1;
                    else
                        s = s2;
                    end
                    t = (d1-b1*s)/c1;
                end
            end
        else
            if (a2 ~= 0)
                ab = a1*b2-a2*b1;                                           % ab
                if (ab ~= 0)
                    ac = a1*c2-a2*c1;                                       % ac
                    ad = a1*d2-a2*d1;                                       % ad
                    if (ac ~= 0)
                        a = a1*ab;
                        b = c1*ab-a1*ad-b1*ac;
                        c = d1*ac-c1*ad;
                        d = (b^2)-(4*a*c);
                        s1=(-b+sqrt(d))/(2*a);
                        s2=(-b-sqrt(d))/(2*a);
                        if (abs(s1) <= 1)
                            s = s1;
                        else
                            s = s2;
                        end
                        t = (ad-ab*s)/ac;
                    else
                        db = d1*b-d2*b1;
                        s = ad/ab;
                        t = a1*db/(c1*ab+a1*ad);
                    end
                else
                    dc = d1*c2-d2*c1;                                       % dc
                    ac = a1*c2-a2*c1;                                       % ac
                    ad = a1*d2-a2*d1;                                       % ad
                    s = a1*dc/(b1*ac+a1*ad);
                    t = ad/ac;
                end
            else
                if (b2 == 0)
                    s = (d1*c2-d2*c1)/(a1*d2+b1*c2);                        % dc
                    t = d2/c2;                                              % ad    
                else
                    a = a1*b2;
                    b = c1*b2-a1*d2-b1*c2;                      
                    c = d1*c2-c1*d2;                                        % dc
                    d = (b^2)-(4*a*c);
                    s1=(-b+sqrt(d))/(2*a);
                    s2=(-b-sqrt(d))/(2*a);
                    if (abs(s1) <= 1)
                        s = s1;
                    else
                        s = s2;
                    end
                    t = (d2-b2*s)/c2;
                end
            end
        end
        N1 = 0.25*(1-s)*(1-t);
        N2 = 0.25*(1+s)*(1-t);
        N3 = 0.25*(1+s)*(1+t);
        N4 = 0.25*(1-s)*(1+t);
        N = [N1; N2; N3; N4];
    end
end

