# Apartado 2

import sympy as sy

A = set(list("defghijklmn"))
B = set(list("vivadixiesubmarinetransmissionplot"))
C = set(list("franciscojaviermercadermartinez"))
U = set(list("abcdefghijklmnñopqrstuvwxyz"))

# (A\B)^c = (U-(A\B))

sy.simplify_logic((U-(A-B)) & (A & C | B) & (A ^ C))
