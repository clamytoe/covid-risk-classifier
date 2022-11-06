import bentoml
from bentoml.io import JSON
from loguru import logger
from pydantic import BaseModel

logger.add(
    "covid_risk_classifier.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="1 MB",
    compression="zip",
)


class CovidRisk(BaseModel):
    """Schema for input data

    Args:
        BaseModel (class): pydantic basemodel
    """

    state: str
    age_yrs: int
    sex: str
    disable: bool
    other_meds: bool
    cur_ill: bool
    history: bool
    prior_vax: bool
    ofc_visit: bool
    allergies: bool
    vax_name: str
    vax_dose_series: int


tag = "covid_risk_model:latest"
model_ref = bentoml.xgboost.get(tag)
dv = model_ref.custom_objects["dictVectorizer"]
model_runner = model_ref.to_runner()
svc = bentoml.Service("covid_risk_classifier", runners=[model_runner])


@svc.api(input=JSON(pydantic_model=CovidRisk), output=JSON())
async def classify(patient_data: CovidRisk) -> JSON:
    """Classifier for the service

    Args:
        patient_data (CovidRisk): json input representing the patient

    Returns:
        JSON: json formatted results of the prediction
    """
    logger.info(f"Processing: {patient_data}")
    patient_info = patient_data.dict()
    vector = dv.transform(patient_info)
    probability = await model_runner.predict.async_run(vector)  # type: ignore

    result = probability[0]
    logger.info(f"Probability: {result}")

    if result > 0.5:
        prediction = {"status": "DANGER", "proba": result}
    elif result > 0.25:
        prediction = {"status": "CAUTION", "proba": result}
    else:
        prediction = {"status": "SAFE", "proba": result}

    logger.info(f"Prediction: {prediction}")
    return prediction  # type: ignore
