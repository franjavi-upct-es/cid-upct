# Apartado 1

from sympy import symbols, And, Or, Implies, Not, Equivalent

p,q,r = symbols('p q r')

print(Implies(And(And(Implies(p,q),Equivalent(q,r)), And(Not(p), Not(r))), (And(Not(p), And(Not(r),Not(q))))).subs({p:True, q:True, r:True}))
print(Implies(And(And(Implies(p,q),Equivalent(q,r)), And(Not(p), Not(r))), (And(Not(p), And(Not(r),Not(q))))).subs({p:True, q:True, r:False}))
print(Implies(And(And(Implies(p,q),Equivalent(q,r)), And(Not(p), Not(r))), (And(Not(p), And(Not(r),Not(q))))).subs({p:True, q:False, r:True}))
print(Implies(And(And(Implies(p,q),Equivalent(q,r)), And(Not(p), Not(r))), (And(Not(p), And(Not(r),Not(q))))).subs({p:True, q:False, r:False}))
print(Implies(And(And(Implies(p,q),Equivalent(q,r)), And(Not(p), Not(r))), (And(Not(p), And(Not(r),Not(q))))).subs({p:False, q:True, r:True}))
print(Implies(And(And(Implies(p,q),Equivalent(q,r)), And(Not(p), Not(r))), (And(Not(p), And(Not(r),Not(q))))).subs({p:False, q:True, r:False}))
print(Implies(And(And(Implies(p,q),Equivalent(q,r)), And(Not(p), Not(r))), (And(Not(p), And(Not(r),Not(q))))).subs({p:False, q:False, r:True}))
print(Implies(And(And(Implies(p,q),Equivalent(q,r)), And(Not(p), Not(r))), (And(Not(p), And(Not(r),Not(q))))).subs({p:False, q:False, r:False}))

# He probado todas las combinaciones posibles, como si fuera una tabla de verdad
# y con los resultados se puede ver que es válida