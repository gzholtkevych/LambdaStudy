from typing import Dict, Union, Set
from typing_extensions import Self


class Var(str):
    
    __declared: Dict[str, Self] = {}
    
    def __new__(cls, name: str) -> Self:
        if type(name) != str:
            raise TypeError("Var() error! Bad type of argument")
        if not (name.isidentifier() and name[: 1].islower()):
            raise ValueError("Var error! Bad value of argument")
        try:
            return Var.__declared[name]
        except KeyError:
            Var.__declared[name] = super().__new__(cls, name)
            return Var.__declared[name]

    def __str__(self) -> str:
        return super().__str__()

    def __eq__(self, another: Self) -> bool:
        return super().__eq__(another) if type(another) == Var else False

    def __ne__(self, another: Self) -> bool:
        return not (self == another)
    
    def __hash__(self) -> int:
        return super().__hash__()
    

class Term(tuple):
    
    def __new__(cls, *args) -> Self:
        if len(args) == 1 and type(args[0]) == Var:
            return super().__new__(cls, args)
        if len(args) == 2 and type(args[0]) == Term and type(args[1]) == Term:
            return super().__new__(cls, args)
        if len(args) == 2 and type(args[0]) == Var and type(args[1]) == Term:
            return super().__new__(cls, args)
        raise ValueError("Term() error! Bad argument(s)")
        
    @classmethod
    def atm(cls, x: Union[str, Var]) -> Self:
        if type(x) == Var:
            return cls(x)
        try:
            x = Var(x)
            return cls(x)
        except:
            raise ValueError("atm() error! Bad argument")
        
    @classmethod
    def app(cls, t1: Self, t2: Self) -> Self:
        if type(t1) == Term:
            try:
                return cls(t1, t2)
            except:
                raise TypeError("app() error! Bad type of argument")
        raise TypeError("app() error! Bad type of argument")
    
    @classmethod
    def abs(cls, x: Union[str, Var],  t: Self) -> Self:
        if type(x) == str:
            try:
                x = Var(x)
            except:
                raise TypeError("abs() error! Bad type of argument")
        if type(x) == Var:
            try:
                return cls(x, t)
            except:
                raise TypeError("abs() error! Bad type of argument")
        raise TypeError("abs() error! Bad type of argument")

    @property
    def kind(self) -> str:
        if len(self) == 1:
            return "atom"
        if type(self[0]) == Term:
            return "application"
        return "abstraction"

    def __str__(self) -> str:
        if self.kind == "atom":
            return f"{str(self[0])}"
        if self.kind == "application":
            return f"({str(self[0])} {str(self[1])})"
        # self.kind == "abstraction"
        return f"(λ {str(self[0])}.{str(self[1])})"

    def __eq__(self, another: Self) -> bool:
        if type(another) != Term:
            return False
        if self.kind == "atom":
            return self[0] == another[0]
        # self.kind == "application" or  self.kind == "abstraction"
        return self[0] == another[0] and self[1] == another[1]
    
    def __ne__(self, another: Self) -> bool:
        return not (self == another)

    @property
    def vars(self) -> Set[Var]:
        if self.kind == "atom":
            return {self[0], }
        if self.kind == "application":
            return self[0].vars | self[1].vars
        # self.kind == "abstraction"
        return {self[0], } | self[1].vars
    
    @property
    def fvars(self) -> Set[Var]:
        if self.kind == "atom":
            return {self[0], }
        if self.kind == "application":
            return self[0].fvars | self[1].fvars
        # self.kind == "abstraction"
        temp = self[1].fvars
        temp.discard(self[0])
        return temp


class Occurrence(str):
    
    def __new__(cls, s: str) -> Self:
        if type(s) != str:
            raise TypeError(
                "Occurrence() error! Bad type of argument")
        if s and any(ch != "0" and ch != "1" for ch in s):
            raise ValueError(
                "Occurrence() error! Bad value of argument")
        return super().__new__(cls, s)
    
    def __str__(self)-> str:
        return f"@{super().__str__()}"