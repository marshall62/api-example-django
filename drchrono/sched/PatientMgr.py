from drchrono.sched.ModelObjects import ModelObjects

class PatientMgr:

    @staticmethod
    def get_patients_from_name(fname, lname, ssn4=None):
        m = ModelObjects()
        l = []
        for p in m.patients:
            if p.first_name.lower() == fname.lower() and p.last_name.lower() == lname.lower():
                if ssn4 and p.ssn4 == ssn4:
                    l.append(p)
                elif not ssn4:
                    l.append(p)
        return l

    @staticmethod
    def get_patient_by_id ( id):
        m = ModelObjects()
        return m.patients_map.get(id)