import drchrono.dates as d
import pytest

def test_tm ():
    t = '2019-12-11T21:33:00'
    r = d.time_format(t)
    assert '9:33 PM' == r

    t = '2019-12-11T00:33:00'
    r = d.time_format(t)
    assert '12:33 AM' == r

    t = '2019-12-11T23:33:00'
    r = d.time_format(t)
    assert '11:33 PM' == r

    t = '2019-12-11T23:59:59'
    r = d.time_format(t)
    assert '11:59 PM' == r

    t = '2019-12-11T00:00:00'
    r = d.time_format(t)
    assert '12:00 AM' == r

    with pytest.raises(ValueError):
        t = '2019-12-11T24:00:00'
        r = d.time_format(t)
