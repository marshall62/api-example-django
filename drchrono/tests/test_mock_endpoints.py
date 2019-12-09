from drchrono.endp.mock_endpoints import *

class TestMockEndpoints:

    def setup_class (cls):
        cls.dep = Doctor_MockEndpoint()
        cls.doc2 = cls.dep.create({'first_name': 'Gomer', 'last_name': 'Pyle'})
        cls.doc3 = cls.dep.create({'first_name': 'David', 'last_name': 'Pyle'})

        cls.aep = Appointment_MockEndpoint()
        cls.pep = Patient_MockEndpoint()

    def test_fetch (self):
        x = self.dep.fetch(id=self.doc2['id'])
        assert x['first_name'] == 'Gomer'

    def test_list (self):
        all = self.dep.list(first_name='Gomer', last_name='Pyle')
        assert 1 == len(all)
        assert 'Gomer' == all[0]['first_name']

        all = self.dep.list(first_name='David')
        assert 2 == len(all)
        for d in all:
            assert 'David' == d['first_name']

    def test_update (self):
        id = self.doc3['id']
        self.dep.update(id=id,data={}, partial=True, last_name='Smith')
        assert 'Smith' == self.doc3['last_name']

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
        recs = self.pep.list(first_name='Homer')
        assert len(recs) == len(ps)
        for r in recs:
            assert r['status'] == 'BLEEDING' and r['first_name'] == 'Homer'



