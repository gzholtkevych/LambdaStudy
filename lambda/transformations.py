from typing import Tuple, Set, Optional
from instances import Var, Term, Occurrence  


def substitute(t1: Term, x: Var, t2: Term) -> Term:
    """
    The function substitutes each free occurrence of the variable with
    some term in another term.

    Args:
        t1: the term whose free variable is substituting
        x:  the variable that is substituted
        t2: the term that substitutes

    Returns:
        the term t1[x:=t2]
        
    Remark:
        if x is not a free variable of t1 then the function returns t1
    """
    if type(t1) != Term or type(x) != Var or type(t2) != Term:
        raise TypeError("substitute() error! Bad type of argument(s)")
    if x not in t1.fvars:
        return t1
    if t1.kind == "atom":
        return t2
    if t1.kind == "application":
        t10 = substitute(t1[0], x, t2)
        t11 = substitute(t1[1], x, t2)
        return Term.app(t10, t11)
    # t1.kind == "abstraction"
    t11 = substitute(t1[1], x, t2)
    return Term.abs(t1[0], t11)

def rename(t: Term, x: Var, y: Var) -> Term:
    """
    The function renames The function renames the binding variable of
    a term using a fresh variable.

    Args:
        t: the term in which the binding variable is renamed
        x: the variable for renaming
        y: a fresh variable

    Returns:
        the term after renaming
        
    Remarks:
        1) x should be bound in t
        2) y should be fresh for t
    """
    if type(t) != Term or type(x) != Var or type(y) != Var:
        raise TypeError("rename() error! Bad type of argument(s)")
    if y in t.vars:
        raise ValueError(
            "rename() error! the third argument is not a fresh variable")
    if t.kind == "atom":
        return t
    if t.kind == "application":
        t0 = rename(t[0], x, y)
        if t[0] != t0:
            return Term.app(t0, t[1])
        t1 = rename(t[1], x, y)
        if t[1] != t1:
            return Term.app(t[0], t1)
        return t
    # t.kind == "abstraction"
    if t[0] == x:
        t1 = substitute(t[1], x, Term.atm(y))
        return Term.abs(y, t1)
    t1 = rename(t[1], x, y)
    if t[1] != t1:
        return Term.abs(t[0], t1)
    return t


def get_fresh_variable(*ts: Tuple[Term, ...]) -> Var:
    """
    The function finds some common fresh variable for each of its arguments.
    
    Args:
        *ts:  terms for which a common fresh variable is finding

    Returns:
        a common fresh variable 
    """
    if not ts:
        return Var('v0')
    if any(type(t) != Term for t in ts):
        return TypeError(
            "get_fresh_variable() error! Bad type of argument(s)")
    ic = 0
    vs = set()
    vs.union(*(t.vars for t in ts))
    while True:
        x = Var(f"v{ic}")
        if x not in vs:
            return x
        ic += 1


# def subterm(t: Term, occ: Occurrence) -> Optional[Term]:
    
