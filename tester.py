from simulambda.instances import *
from simulambda.transformations import *


x, y, z = Var('x'), Var('y'), Var('z')
u, v, w = Var('u'), Var('v'), Var('w')
X, Y, Z = Term.atm(x), Term.atm(y), Term.atm(z)
XZ, YZ = Term.app(X, Z), Term.app(Y, Z)
S = Term.abs(y, Term.abs(z, Term.app(XZ, YZ)))
S1 = rename(S, x, u)
S2 = rename(S1, y, v)
S3 = rename(S2, z, w)
print(f"S3 = {S3}")

v = get_fresh_variable(S2, S3)
print(f"The variable {v} is fresh for {S2} and {S3}")

occ = Occurrence("")
print(f"type(occ) = {type(occ)}; occ = {occ}")

occ = Occurrence("0011")
print(f"occ = {occ}; occ.head = {occ.head}; occ.tail = {occ.tail}")
subt = subterm(S1, occ)
print(f"subterm indicated by {occ} is {subt}")
