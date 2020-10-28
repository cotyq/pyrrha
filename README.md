# Pymetheus

## Comandos

### Generar template a partir de una clase base

```
pymetheus --generate FiniteElement2D CustomElement2D
```

### Testear clase implementada

Testear la clase completa.
```
pymetheus --test CustomElement2D
```

Testear un método en particular.
```
pymetheus --test CustomElement2D heat_neumann
```