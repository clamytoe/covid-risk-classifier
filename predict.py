import json
from typing import Iterable

import requests

from service import CovidRisk

HOST: dict[str, str] = {
    "aws": "http://54.221.93.161:3000",
    "local": "http://localhost:3000",
}
ACTUAL: list[int] = [0, 1, 0, 1, 1, 0, 0, 1, 0, 0]
PATIENTS: list[dict[str, str | int]] = [
    {
        "state": "mi",
        "age_yrs": 85,
        "sex": "f",
        "disable": 0,
        "other_meds": 0,
        "cur_ill": 0,
        "history": 0,
        "prior_vax": 0,
        "ofc_visit": 0,
        "allergies": 0,
        "vax_name": "pfizer\\biontech",
        "vax_dose_series": 2,
    },
    {
        "state": "tx",
        "age_yrs": 77,
        "sex": "m",
        "disable": 0,
        "other_meds": 1,
        "cur_ill": 0,
        "history": 1,
        "prior_vax": 0,
        "ofc_visit": 0,
        "allergies": 0,
        "vax_name": "pfizer\\biontech",
        "vax_dose_series": 2,
    },
    {
        "state": "ca",
        "age_yrs": 15,
        "sex": "m",
        "disable": 0,
        "other_meds": 1,
        "cur_ill": 1,
        "history": 1,
        "prior_vax": 0,
        "ofc_visit": 0,
        "allergies": 1,
        "vax_name": "pfizer\\biontech",
        "vax_dose_series": 3,
    },
    {
        "state": "mi",
        "age_yrs": 88,
        "sex": "f",
        "disable": 0,
        "other_meds": 0,
        "cur_ill": 0,
        "history": 0,
        "prior_vax": 0,
        "ofc_visit": 0,
        "allergies": 0,
        "vax_name": "pfizer\\biontech",
        "vax_dose_series": 2,
    },
    {
        "state": "wi",
        "age_yrs": 73,
        "sex": "m",
        "disable": 0,
        "other_meds": 0,
        "cur_ill": 0,
        "history": 1,
        "prior_vax": 0,
        "ofc_visit": 0,
        "allergies": 0,
        "vax_name": "janssen",
        "vax_dose_series": 1,
    },
    {
        "state": "mi",
        "age_yrs": 68,
        "sex": "m",
        "disable": 0,
        "other_meds": 0,
        "cur_ill": 0,
        "history": 0,
        "prior_vax": 0,
        "ofc_visit": 1,
        "allergies": 0,
        "vax_name": "pfizer\\biontech",
        "vax_dose_series": 3,
    },
    {
        "state": "ga",
        "age_yrs": 52,
        "sex": "f",
        "disable": 0,
        "other_meds": 0,
        "cur_ill": 0,
        "history": 0,
        "prior_vax": 0,
        "ofc_visit": 0,
        "allergies": 0,
        "vax_name": "pfizer\\biontech",
        "vax_dose_series": 2,
    },
    {
        "state": "tx",
        "age_yrs": 53,
        "sex": "f",
        "disable": 0,
        "other_meds": 0,
        "cur_ill": 0,
        "history": 0,
        "prior_vax": 0,
        "ofc_visit": 0,
        "allergies": 0,
        "vax_name": "pfizer\\biontech",
        "vax_dose_series": 1,
    },
    {
        "state": "ca",
        "age_yrs": 3,
        "sex": "m",
        "disable": 0,
        "other_meds": 0,
        "cur_ill": 0,
        "history": 0,
        "prior_vax": 0,
        "ofc_visit": 0,
        "allergies": 0,
        "vax_name": "moderna",
        "vax_dose_series": 1,
    },
    {
        "state": "tx",
        "age_yrs": 52,
        "sex": "f",
        "disable": 0,
        "other_meds": 1,
        "cur_ill": 0,
        "history": 0,
        "prior_vax": 0,
        "ofc_visit": 0,
        "allergies": 0,
        "vax_name": "moderna",
        "vax_dose_series": 1,
    },
]


def test_service(data: Iterable[tuple[CovidRisk, int]], host: str = "local"):
    """Tests the covid risk classifier service

    It sends ten randomly selected records from the test dataset for
    processing.

    Args:
        data (Iterable[tuple[CovidRisk, int]]): list of CovidRisk json entries
        host (str, optional): type of hosting service used. Defaults to "local"
                              but can also send to AWS as well.
    """
    print(f"Predicting from {host.upper()} server:")
    for patient, actual in data:
        patient = json.dumps(patient)
        response = requests.post(
            f"{HOST[host]}/classify",
            headers={"content-type": "application/json"},
            data=patient,
        ).json()
        print(f"{actual=}", response["status"], response["proba"])


if __name__ == "__main__":
    samples = zip(PATIENTS, ACTUAL)
    test_service(samples, host="local")  # type: ignore
