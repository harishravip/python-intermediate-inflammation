"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains 
inflammation data for a single patient taken over a number of days 
and each column represents a single day across all patients.
"""

import numpy as np


def load_csv(filename: str) -> np.ndarray:
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load
    """
    return np.loadtxt(fname=filename, delimiter=',')


def daily_mean(data: np.ndarray) -> np.ndarray:
    """Calculate the daily mean of a 2D inflammation data array.

    :param data: A 2D data array with inflammation data
        (each row contains measurements for a single patient across all days).
    :return : An array of mean values of measurements for each day.
    """
    return np.mean(data, axis=0)


def daily_max(data: np.ndarray) -> np.ndarray:
    """Calculate the daily max of a 2D inflammation data array.

    :param data: A 2D data array with inflammation data
        (each row contains measurements for a single patient across all days).
    :return : An array of maximum values of measurements for each day.
    """
    return np.max(data, axis=0)


def daily_min(data: np.ndarray) -> np.ndarray:
    """Calculate the daily min of a 2D inflammation data array.

    :param data: A 2D data array with inflammation data
        (each row contains measurements for a single patient across all days).
    :return : An array of minimum values of measurements for each day.
    """
    return np.min(data, axis=0)


def daily_sd(data: np.ndarray) -> np.ndarray:
    """Calculate the daily standard deviation of a 2D inflammation data array.

    :param data: A 2D data array with inflammation data
        (each row contains measurements for a single patient across all days).
    :return : An array of standard deviation values of measurements for each day.
    """
    return np.nanstd(data, axis=0, keepdims=False)


def patient_normalise(data: np.ndarray) -> np.ndarray:
    """
    Normalise patient data from a 2D inflammation data array.
    NaN values are ignored, and normalised to 0.
    Negative values are rounded to 0.

    :param data: A 2D data array with inflammation data
        (each row contains measurements for a single patient across all days).
    :return : An array of normalized values of measurements for each day.
    """
    if not isinstance(data, np.ndarray):
        raise TypeError('data input should be ndarray')
    if len(data.shape) != 2:
        raise ValueError('inflammation array should be 2-dimensional')
    if np.any(data < 0):
        raise ValueError('inflammation values should be non-negative')
    max_data = np.nanmax(data, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        normalised = data / max_data[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    return normalised


class Observation:
    """
       A class to represent an inflammation observation.

       Attributes
       ----------
       day : int
           Day of observation
       value : str
           full name of the person
    """

    def __init__(self, day, value):
        self.day = day
        self.value = value

    def __str__(self):
        return str(self.value)


class Person:
    """
       A class to represent a person.
       ...

       Attributes
       ----------
       name : str
           first name last name of the patient/doctor.
    """

    def __init__(self, name):
        """
        Constructs all the necessary attributes for the Person object.

        Parameters
        ----------
        name : str
            full name of the person
        """
        self.name = name

    def __str__(self):
        return self.name


class Patient(Person):
    """
       A class to represent a Patient of type Person.

       Attributes
       ----------
       name : str
           full name of the person
       observations : Observation
           inflammation observation

       Methods
       -------
       add_observation(value, day=None):
           Adds inflammation observation for the patient
    """

    def __init__(self, name, observations=None):
        super().__init__(name)
        """
        Constructs all the necessary attributes for the Patient object.

        Parameters
        ----------
            name : str
                first name of the person
            observations: Observation
                inflammation observation
        """
        self.observations = []
        if self.observations is not None:
            self.observations = observations

    def add_observation(self, value: float, day: int = None) -> Observation:
        """

        :param value: observed inflammation value
        :param day: Day of observation
        :return: New Observation
        """
        if day is None:
            try:
                day = self.observations[-1].day + 1
            except IndexError:
                day = 0

        new_observation = Observation(day, value)

        self.observations.append(new_observation)
        return new_observation

    def __str__(self):
        return self.name

    @property
    def last_observation(self):
        return self.observations[-1]


class Doctor(Person):
    """
       A class to represent a Patient of type Person.

       Attributes
       ----------
       name : str
           full name of the doctor

       Methods
       -------
       add_patient(Patient):
           Add patient treated by the doctor
    """

    def __init__(self, name):
        """
        Constructs all the necessary attributes for the Doctor object.

        Parameters
        ----------
            name : str
                first name of the person
        """
        super().__init__(name)
        self.patients = []

    def add_patient(self, patient):
        """
        
        :param patient: Patient of Patient class
        :return: None
        """
        if patient in self.patients:
            return
        self.patients.append(patient)

# alice = Patient('Alice')
# print(alice)
#
# obs = alice.add_observation(3)
# print(obs)
#
# bob = Person('Bob')
# print(bob)
#
# obs = bob.add_observation(4)
# print(obs)
