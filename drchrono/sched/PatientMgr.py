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
        return m.patients_map.get(int(id))

    @classmethod
    def update_patient(cls, patient, new_data=None, summary=True):
        if summary:
            ModelObjects().save_patient_summary(patient)
        else: ModelObjects().save_patient(patient, new_data)

