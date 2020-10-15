# Change Log

## [1.2.2](https://gitlab.com/csgentile/FEM/tree/master/fem2d_heat) (2019-09-16)

### Added
- New functions for testing:
> - aux\_check\_values.m >>> used to check matrix/vector values and determine whether they are valid (not infinite or NaN) and also they are below the error threshold.
> - aux\_check\_module.m >>> used to perform several common tasks in every module (dimensions and values)
> - aux\_gen\_rspd\_matrix.m >>> used to generate random, symmetric and positive definite matrices.

### Changed
- Random test matrices changed using new algorithm (aux\_gen\_rspd\_matrix).
- Improved all tests logic for more robust results.

