import pytest
from classpad.core.parser import ClassPadSyntaxError, normalize, split_assignment, split_equation
@pytest.mark.parametrize(("source", "expected"), [("2x", "2*x"), ("3(x+1)", "3*(x+1)"), ("2π", "2*pi"), ("sqrt(8)", "sqrt(8)"), ("e^x", "E**x"), ("5e^(-0.0173x)", "5*E**(-0.0173*x)"), ("i^2", "I**2")])
def test_normalize(source, expected): assert normalize(source) == expected
def test_splits():
    assert split_assignment("x:=5") == ("x", "5")
    assert split_equation("2x+4=10") == ("2x+4", "10")
def test_rejects_escape_hatches():
    with pytest.raises(ClassPadSyntaxError): normalize("__import__('os')")
