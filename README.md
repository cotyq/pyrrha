![pyrra](https://gitlab.com/dsklar/pyrrha/uploads/f6f763a9ce81995256a6de4809e898e2/image__24_.png)

pyrrha is a tool for helping in the developement and testing of
 Computational Mechanics methods.

This project is based in the Octave & C++ program called "Prometheus
", developed by Carlos Gentile, that allows to generate templates for
 programming Octave implementations of classical Computional Mechanics
  methods. Inspired in these ideas, this project offers the ability to
   generate python templates for the Finite Elements method, and tools for
    evaluating the intermediate steps of its implementation.

The name pyrrha comes from Pyrrha, the wife of Deucalion (the son of Prometheus
), who had a child out of wedlock with Zeus. She is basically the daughter
-in-law and niece of Prometheus (a link that is in some way preserved between
 the original Prometheus application and this package).

## Commands

### Generate template from a base class

```
pyrrha --generate FiniteElement2D CustomElement2D
```

### Test implemented class

Test the whole class
```
pyrrha --test CustomElement2D
```

Test a particular method.
```
pyrrha --test CustomElement2D heat_neumann
```

<div>Icons made by <a href="https://www.flaticon.com/authors/darius-dan" title="Darius Dan">Darius Dan</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
