from drchrono.datastore.APIGateway import APIGateway

def test_gw_singl ():
    # verify is true singleton
    g = APIGateway(False)
    assert g != None
    g2 = APIGateway(False)
    assert g == g2
    assert g is g2


def test_dr ():
    g = APIGateway(False)
    rec = g._load_dr_from_api()
    print (rec)
    assert rec['first_name'] == 'David'
    assert rec['last_name'] == 'Marshall'

def test_pats ():
    g = APIGateway(False)
    rec = g._load_dr_from_api()
    g.doctor = rec
    recs = g._load_pts_from_api()
    for r in recs:
        print(r)
    assert len(recs) > 0

def test_appt ():
    g = APIGateway(False)
    rec = g._load_dr_from_api()
    g.doctor = rec
    recs = g._load_appts_from_api()
    for r in recs:
        print(r)
    assert len(recs) > 0

def test_gw_load ():
    APIGateway.instance = None # remove its inner so that we can make a new one with loading true
    gw = APIGateway()
    assert gw.doctor != None
    assert gw.office != None
    assert gw.patients != None
    assert gw.patients_map != None
    assert gw.appointments != None
    assert gw.appointments_map != None
    assert len(gw.patients) > 0
    for i,p in enumerate(gw.patients):
        print(i,p)

# @pytest.mark.skip
def test_gw_maps ():
    gw = APIGateway()
    patmap = gw.patients_map
    assert type(patmap) == dict
    assert len(patmap.keys()) > 0
    assert len(patmap.keys()) == len(gw.patients)

    aptmap = gw.appointments_map
    assert type(aptmap) == dict
    assert len(aptmap.keys()) == len(gw.appointments)


