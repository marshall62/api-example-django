from drchrono.endp.EndpointMgr import EndpointMgr
from drchrono.endp.mock_endpoints import *
import pytest

class TestMockEndpoints:

    def setup_class (cls):
        EndpointMgr()
        cls.dep = Doctor_MockEndpoint()
        cls.doc2 = cls.dep.create({'first_name': 'Gomer', 'last_name': 'Pyle'})
        cls.doc3 = cls.dep.create({'first_name': 'David', 'last_name': 'Pyle'})

        cls.aep = Appointment_MockEndpoint()
        cls.pep = Patient_MockEndpoint()

    def test_fetch (self):
        x = self.dep.fetch(id=self.doc2['id'])
        assert x['first_name'] == 'Gomer'

    def test_list_gen (self):
        g = self.dep.list(first_name='Gomer', last_name='Pyle')
        next(g)
        with pytest.raises(StopIteration):
            next(g)

    def test_list1 (self):
        all = list(self.dep.list(first_name='Gomer', last_name='Pyle'))
        assert 1 == len(all)
        p1 = all[0]
        assert 'Gomer' == p1['first_name'] and 'Pyle' == p1['last_name']

    def test_list2a (self):
        g = self.dep.list(verbose=False, first_name='David')
        all = list(g)
        assert 2 == len(all)
        for d in all:
            assert 'David' == d['first_name']

    def test_list2b (self):
        g = self.dep.list(first_name='David')
        all = list(g)
        assert 2 == len(all)
        for d in all:
            assert 'David' == d['first_name']

    def test_update1 (self):
        id = self.doc3['id']
        self.dep.update(id=id,data={}, partial=True, status='Evil')
        r = self.dep.fetch(id=id)
        assert 'Evil' == r['status']

    def test_update2 (self):
        id = self.doc3['id']
        self.dep.update(id=id,data={'status': 'Asleep'}, partial=True)
        r = self.dep.fetch(id=id)
        assert 'Asleep' == r['status']

    def test_update3 (self):
        id = self.doc3['id']
        self.dep.update(id=id,data={'status': 'Asleep'}, partial=True, last_name='Hooligan')
        r = self.dep.fetch(id=id)
        assert 'Asleep' == r['status']
        assert 'Hooligan' == r['last_name']

    def test_update_full (self):
        id = self.doc3['id']
        self.dep.update(id=id,data={'id': id, 'first_name': 'Benedict', 'last_name': 'Drumpf'}, partial=False)
        r = self.dep.fetch(id=id)
        assert 'Benedict' == r['first_name']
        assert 'Drumpf' == r['last_name']


    def test_appoint_ops (self):
        ps = self.pep.list(last_name='Smith')
        assert len(ps) > 0
        for p in ps:
            assert p['last_name'] == 'Smith'

        for p in ps:
            id = p['id']
            r = self.pep.fetch(id=id)
            assert r['last_name'] == 'Smith'
            self.pep.update(id, data={}, partial=True, first_name='Homer', status='BLEEDING' )
        recs = list(self.pep.list(first_name='Homer'))
        assert len(recs) == len(ps)
        for r in recs:
            assert r['status'] == 'BLEEDING' and r['first_name'] == 'Homer'



