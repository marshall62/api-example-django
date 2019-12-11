#from drchrono.Scheduler import Scheduler
from drchrono.temp import update_from_api

def test1 ():
    # x = Scheduler.get_appointments(None)
    x = update_from_api()
    assert x
