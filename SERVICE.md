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

## What does this do?

This classifier will predict the likelyhood of someone dying from taking the covid vaccination.
The dataset was collected from the [Vaccine Adverse Event Reporting System (VAERS)](https://vaers.hhs.gov/), which is an arm of the [U.S. Department of Health & Human Services (HHS)](https://www.hhs.gov/).

If you are interested in the actual raw data, the datasets can be downloaded from the VAERS Data Sets: [https://vaers.hhs.gov/data/datasets.html](https://vaers.hhs.gov/data/datasets.html).

These are the two datasets that were used:

* 2022VAERSDATA.csv
* 2022VAERSVAX.csv

> **Consult with your primary healthcare provider for any medical decisions.**
I am not a healthcare professional, nor do I work in the healthcare industry.
This is solely and academic exercise and the results should not be relied upon for any healthcare decisions.

## Input data

The model takes json as input.
The actual schema used can be found down below in the POST section of the Service APIs area.
Here is a description of what each feature means:

* `state`: Two letter abbreviation for the United States state or territory:
  * ak, al, ar, as, az, ca, co, ct, dc, de, fl, ga, gu, hi, ia, id, il, in, ks, ky, la,\
  ma, md, me, mh, mi, mn, mo, mp, ms, mt, nc, nd, ne, nh, nj,
  nm, nv, \
  ny, oh, ok, or, pa, pr, pw, ri, sc, sd, tn, tx, ut, va, vi, vt, wa, wi, wv, wy
* `age_yrs`: Numerical age of the patient.
  * The model was trained on ages between:
    * 0 - 107
* `sex`: One letter abbreviation for their gender.
  * f: Female
  * m: Male
  * u: Unknown
* `l_threat`: Boolean value indicating whether the patient currently has a life-threatening illness.
  * 0 or flase
  * 1 or true
* `disable`: Boolean value indicating whether the patient is disabled.
  * 0 or flase
  * 1 or true
* `other_meds`: Boolean value indicating whether the patient is taking any other medications.
  * 0 or flase
  * 1 or true
* `cur_ill`: Boolean value indicating whether the patient is currently sick.
  * 0 or flase
  * 1 or true
* `history`: Boolean value indicating whether the patient has any chronic or long-standing health conditions.
  * 0 or flase
  * 1 or true
* `prior_vax`: Boolean value indicating whether the patient has had any prior adverse vaccine reactions.
  * 0 or flase
  * 1 or true
* `ofc_visit`: Boolean value indicating whether the patient had to visit their doctor or other healthcare provider for any illness instead of just to get the shot.
  * 0 or flase
  * 1 or true
* `allergies`: Boolean value indicating whether the patient had any known allergies to medications, food, or other products.
  * 0 or flase
  * 1 or true
* `vax_name`: The name of the vaccination that they plan on taking.
  * janssen
  * moderna
  * novavax
  * pfizer\biontech
  * unknown
* `vax_dose_series`: Numerical value indicating the dose/booster that this would be.
  * The model was trained on doses between:
    * 0 - 7

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
```
