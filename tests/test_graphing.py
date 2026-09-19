import math
import pytest
from classpad.core.graphing import roots, sample_function
def test_quadratic_roots(): assert roots(lambda x:x*x-4,-5,5) == pytest.approx([-2,2],abs=1e-7)
def test_discontinuity_breaks():
    segments=sample_function(lambda x:1/x,-1,1,100,10)
    assert len(segments)>=2
    assert all(math.isfinite(p.y) for s in segments for p in s)
