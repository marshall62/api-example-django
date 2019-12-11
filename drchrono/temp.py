from drchrono.sched.APIGateway import APIGateway

def update_from_api ():
    # get new list of appointments every time browser page calls for updates
    #
    g = APIGateway()
    g.reload_appointments()


    g.reload_patients()
    return True