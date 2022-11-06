from locust import HttpUser, between, task

from service import CovidRisk

sample: CovidRisk = {
    "state": "sd",
    "age_yrs": 42.0,
    "sex": "f",
    "disable": 0,
    "other_meds": 0,
    "cur_ill": 1,
    "history": 0,
    "prior_vax": 0,
    "ofc_visit": 0,
    "allergies": 0,
    "vax_name": "moderna",
    "vax_dose_series": 2,
}  # type: ignore


class CovidRiskTestUser(HttpUser):
    """Load tester for the Covid Risk Classifier

    Usage:
        Start locust load testing client with:
            locust -H http://localhost:3000
        Open browser at http://0.0.0.0:8089, adjust desired number of users and spawn
        rate for the load test from the Web UI and start swarming.
    """

    @task
    def classify(self):
        self.client.post("/classify", json=sample)

    wait_time = between(0.01, 2)
