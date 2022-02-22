"""Tests for the Patient model."""


def test_create_patient():
    """Check a patient is created correctly given a name."""
    from inflammation.models import Patient

    name = 'Alice'
    p = Patient(name=name)

    assert p.name == name


def test_patient_is_person():
    """Check if a patient is a person. """
    from inflammation.models import Person, Patient
    bob = Patient('Bob')
    assert isinstance(bob, Person)


def test_create_doctor():
    """Check a doctor is created correctly given a name."""
    from inflammation.models import Doctor
    name = "Evan"
    evan = Doctor(name)
    assert evan.name == name


def test_doctor_is_person():
    """Check if a doctor is a person."""
    from inflammation.models import Doctor, Person
    evan = Doctor("Evan")
    assert isinstance(evan, Person)


def test_add_patients():
    """Check patients are being added correctly by a doctor. """
    from inflammation.models import Doctor, Patient
    evan = Doctor("Evan")
    alice = Patient("Alice")
    evan.add_patient(alice)
    assert evan.patients is not None
    assert len(evan.patients) == 1


def test_no_duplicates():
    """Check adding the same patient to the same doctor twice does not result in duplicates. """
    from inflammation.models import Doctor, Patient
    doc = Doctor("Sheila Wheels")
    alice = Patient("Alice")
    doc.add_patient(alice)
    doc.add_patient(alice)
    assert len(doc.patients) == 1