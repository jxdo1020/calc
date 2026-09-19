import math
import pytest
from classpad.core.statistics import binomial_cdf, binomial_pdf, inverse_normal, linear_regression, normal_cdf, normal_pdf, one_variable
def test_known_dataset():
    result=one_variable([1,2,3,4,5]); assert result["mean"] == result["Med"] == 3
    assert result["σx"] == pytest.approx(math.sqrt(2)); assert result["sx"] == pytest.approx(math.sqrt(2.5))
def test_linear_regression(): assert linear_regression([1,2,3],[3,5,7]) == pytest.approx({"a":2,"b":1,"r":1})
def test_distributions():
    assert normal_pdf(0) == pytest.approx(1/math.sqrt(2*math.pi))
    assert normal_cdf(-1,1) == pytest.approx(.682689492, rel=1e-8)
    assert inverse_normal(.5) == pytest.approx(0,abs=1e-10)
    assert binomial_pdf(10,.5,3) == pytest.approx(120/1024)
    assert binomial_cdf(3,.5,3) == 1
