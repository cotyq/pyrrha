function [DIR,NEU,ROB] = aux_clean_boundary(DIR,NEU,ROB)
    % Remove duplicates
    DIR = unique(DIR, 'rows');
    NEU = unique(NEU, 'rows');
    ROB = unique(ROB, 'rows');
end

