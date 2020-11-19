close all; clear all;

fd = fopen('results.txt', 'w');
fclose(fd);

test_genC;
test_genF;
test_genK;
test_neumann;
test_robin;
test_pcond;
test_dirichlet;
test_flux;
test_explicit;
test_implicit;

fprintf('Fin del script.\n');

