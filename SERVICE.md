# Covid Risk Classifier

```bash
 ▄████▄   ██▓    ▄▄▄       ███▄ ▄███▓▓██   ██▓▄▄▄█████▓ ▒█████  ▓█████ 
▒██▀ ▀█  ▓██▒   ▒████▄    ▓██▒▀█▀ ██▒ ▒██  ██▒▓  ██▒ ▓▒▒██▒  ██▒▓█   ▀ 
▒▓█    ▄ ▒██░   ▒██  ▀█▄  ▓██    ▓██░  ▒██ ██░▒ ▓██░ ▒░▒██░  ██▒▒███   
▒▓▓▄ ▄██▒▒██░   ░██▄▄▄▄██ ▒██    ▒██   ░ ▐██▓░░ ▓██▓ ░ ▒██   ██░▒▓█  ▄ 
▒ ▓███▀ ░░██████▒▓█   ▓██▒▒██▒   ░██▒  ░ ██▒▓░  ▒██▒ ░ ░ ████▓▒░░▒████▒
░ ░▒ ▒  ░░ ▒░▓  ░▒▒   ▓▒█░░ ▒░   ░  ░   ██▒▒▒   ▒ ░░   ░ ▒░▒░▒░ ░░ ▒░ ░
  ░  ▒   ░ ░ ▒  ░ ▒   ▒▒ ░░  ░      ░ ▓██ ░▒░     ░      ░ ▒ ▒░  ░ ░  ░
░          ░ ░    ░   ▒   ░      ░    ▒ ▒ ░░    ░      ░ ░ ░ ▒     ░   
░ ░          ░  ░     ░  ░       ░    ░ ░                  ░ ░     ░  ░
░                                     ░ ░                              
```

## How likely are you to die if you take the vax?

That is the question that I am going to attempt to tackle here.
I must admit that I am not a healthcare professional or work in the healthcare industry.
This is solely and academic exercise and the results should not be relied upon for any healthcare decisions.

> Consult with your primary healthcare provider for any medical decisions.

## Problem description

In order to attempt to answer the question, I used data that I collected from the [Vaccine Adverse Event Reporting System (VAERS)](https://vaers.hhs.gov/), which is an arm of the [U.S. Department of Health & Human Services (HHS)](https://www.hhs.gov/).

The datasets can be downloaded from: [VAERS Data Sets](https://vaers.hhs.gov/data/datasets.html).
When I was exploring the subject, I downloaded the complete dataset, but I only ended up using the data for the year 2022.

## Input data

The service takes json as input and requires the following fields in order to give the best restults:

* `state`: Two letter abbreviation for the your state.
  * valid entries:
    ['mn', 'ky', 'tn', 'tx', 'sd', 'mo', 'ny', 'mt', 'fl', 'wi', 'wa',
     'mi', 'nj', 'nv', 'ar', 'il', 'pa', 'ms', 'ok', 'md', 'az', 'oh',
     'ia', 'co', 'al', 'or', 'ma', 'ca', 'la', 'id', 'pr', 'nh', 'ri',
     'in', 'ga', 'nc', 'va', 'hi', 'ks', 'me', 'ct', 'ut', 'wv', 'ne',
     'sc', 'vt', 'de', 'nm', 'ak', 'nd', 'wy', 'gu', 'dc', 'as', 'vi',
     'mh', 'pw', 'mp']
* `age_yrs`: Numerical age of the patient.
  * valid entries: The model was trained on ages between 0-107
* `sex`: One letter abbreviation for their gender.
  * valid entries: ['f', 'm', 'u']
* `l_threat`: Boolean value indicating whether the patient currently has a life-threatening illness.
  * valid entries: [0, 1] or [false, true]
* `disable`: Boolean value indicating whether the patient is disabled.
  * valid entries: [0, 1] or [false, true]
* `other_meds`: Boolean value indicating whether the patient is taking any other medications.
  * valid entries: [0, 1] or [false, true]
* `cur_ill`: Boolean value indicating whether the patient is currently sick.
  * valid entries: [0, 1] or [false, true]
* `history`: Boolean value indicating whether the patient has any chronic or long-standing health conditions.
  * valid entries: [0, 1] or [false, true]
* `prior_vax`: Boolean value indicating whether the patient has had any prior adverse vaccine reactions.
  * valid entries: [0, 1] or [false, true]
* `ofc_visit`: Boolean value indicating whether the patient had to visit their doctor or other healthcare provider for any illness instead of just to get the shot.
  * valid entries: [0, 1] or [false, true]
* `allergies`: Boolean value indicating whether the patient had any known allergies to medications, food, or other products.
  * valid entries: [0, 1] or [false, true]
* `vax_name`: The name of the vaccination that they plan on taking.
  * valid entries: ['moderna', 'pfizer\biontech', 'janssen', 'unknown', 'novavax']
* `vax_dose_series`: Numerical value indicating dose this will be.
  * valid entries: The model was trained on doses between 0-7

## Sample data

Here are a couple of examples along with the predicted and actual values:

```json
{
  "state": "tn",
  "age_yrs": 87,
  "sex": "f",
  "l_threat": 0,
  "disable": 0,
  "other_meds": 0,
  "cur_ill": 0,
  "history": 0,
  "prior_vax": 0,
  "ofc_visit": 0,
  "allergies": 0,
  "vax_name": "moderna",
  "vax_dose_series": 2
}
predicted: 0.997665286064148
   actual: 1
---
{
  "state": "pr",
  "age_yrs": 24,
  "sex": "f",
  "l_threat": 0,
  "disable": 0,
  "other_meds": 0,
  "cur_ill": 0,
  "history": 0,
  "prior_vax": 0,
  "ofc_visit": 0,
  "allergies": 0,
  "vax_name": "moderna",
  "vax_dose_series": 3
}
predicted: 0.010604704730212688
   actual: 0
---
```