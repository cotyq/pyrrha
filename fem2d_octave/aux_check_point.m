function [result] = aux_check_point(pA, pB, pC)
    % checks wether the point pC is in between pA and pB or not
    % uses a triangular difference as a pseudo-intersection check 

    d1 = norm(pA - pC) + norm(pB - pC);
    d2 = norm(pA - pB);
    
    result = (abs(d1 - d2) < 1e-10);
end

