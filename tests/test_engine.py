import pytest
sp=pytest.importorskip("sympy")
from classpad.core.engine import ClassPadEngine
from classpad.core.models import Settings
@pytest.fixture
def engine(): return ClassPadEngine(Settings())
@pytest.mark.parametrize(("source","expected"), [("2+3","5"),("7*8","56"),("2^10","1024"),("5!","120"),("1/2+1/3","5/6"),("sqrt(8)","2*sqrt(2)"),("sin(pi/6)","1/2"),("10C3","120"),("i^2","-1")])
def test_exact(engine,source,expected): assert str(engine.evaluate(source).exact)==expected
def test_solve_and_integrate(engine):
    assert engine.apply("solve","x^2-5x+6=0",variable="x").exact == [2,3]
    assert str(engine.apply("integrate","(x-6)^2",variable="x").exact.expand()) == "x**3/3 - 6*x**2 + 36*x"
def test_assignment(engine): engine.evaluate("x:=5"); assert engine.evaluate("2x+3").exact==13
