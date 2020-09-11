from . import N1_encapsulation_1
import pytest

@pytest.mark.test1
@pytest.mark.parametrize(
    "x,expected",
    [
        ('a','a'),
        (1,1),
        ([1],[1]),
        ({"test":1},{"test":1}),
        ((1,),(1,)),
        ({1},{1}),
    ]
)
@pytest.mark.test1
def test_N1_encapsulation_1(x,expected):
    val=N1_encapsulation_1.MyClass()
    val.set_val(x)
    assert expected==val.get_val()

