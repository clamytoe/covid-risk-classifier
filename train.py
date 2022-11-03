import json
import pickle
import random
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd  # type: ignore
import xgboost as xgb
from sklearn.feature_extraction import DictVectorizer  # type: ignore
from sklearn.metrics import roc_auc_score  # type: ignore
from sklearn.model_selection import train_test_split  # type: ignore

# datasets
DATA_DATASET = Path("data", "2022VAERSDATA.csv")
VAX_DATASET = Path("data", "2022VAERSVAX.csv")

# codecs: latin, latin1, cp1252, ISO-8859-1
CODEC = "cp1252"

# keep only covid vaxs
VAX_TYPES = ["COVID19", "COVID19-2"]
DATES = ["RECVDATE", "RPT_DATE", "DATEDIED", "VAX_DATE", "ONSET_DATE", "TODAYS_DATE"]
DROP_FEATURES = [
    "BIRTH_DEFECT",
    "CAGE_MO",
    "CAGE_YR",
    "DATEDIED",
    "ER_ED_VISIT",
    "ER_VISIT",
    "FORM_VERS",
    "HOSPDAYS",
    "HOSPITAL",
    "LAB_DATA",
    "NUMDAYS",
    "ONSET_DATE",
    "RECOVD",
    "RECVDATE",
    "RPT_DATE",
    "SPLTTYPE",
    "SYMPTOM_TEXT",
    "TODAYS_DATE",
    "VAX_DATE",
    "VAX_LOT",
    "VAX_NAME",
    "VAX_ROUTE",
    "VAX_SITE",
    "VAX_TYPE",
    "V_ADMINBY",
    "V_FUNDBY",
    "X_STAY",
]
BINARIZE_FEATURES = ["allergies", "cur_ill", "history", "other_meds", "prior_vax"]
BINARY_FEATURES = ["died", "l_threat", "disable", "ofc_visit"]
OTHER_FEATURES = ["v_fundby"]
NONE_VALUES = {
    '"none" per patient',
    '"unidentified" per grandmother',
    "(does not apply)",
    ",none",
    "-",
    "- nka",
    "- nkda",
    "- none",
    "- none known",
    "--- 1/6/2022 10:48 pm --- nka",
    "-na-",
    "...",
    "2no",
    "?",
    "allergies: nka",
    "decline",
    "denied",
    "denies",
    "denies any allergies to medications,foods",
    "denies.",
    "did not indicate.",
    "did not provide any information.",
    "dka.",
    "do not know",
    "don't know",
    "done",
    "i do not",
    "i don't know",
    "i don't want to add anything.",
    "kna",
    "known",
    "m/a",
    "mkda",
    "mom reported no allergies",
    "mom stated no on admission",
    "mone",
    "n / a",
    "n'a",
    "n-a",
    "n./a",
    "n.a",
    "n.a.",
    "n.k.a",
    "n.k.d. a",
    "n.k.d.a",
    "n.k.d.a.",
    "n/",
    "n/a",
    "n/a - none",
    "n/a per mother",
    "n/a to the best of my knowledge",
    "n/a unknown",
    "n/a.",
    "n/a. pt did not verbalize any allergies.",
    "n/k",
    "n/k/a",
    "n0",
    "n?a",
    "na",
    "na/",
    "nak",
    "ndka",
    "ndka, nka",
    "ndka.",
    "never",
    "nil",
    "nk",
    "nka",
    "nka  knda",
    "nka  reported by father",
    "nka / nkda",
    "nka as per mother",
    "nka nkda",
    "nka no food or drug allergies otherwise noted",
    "nka reported",
    "nka to meds, unknown to others",
    "nka until this 3rd (booster) vaccine",
    "nka, knda, no known environmental or food allergies.",
    "nka, none reported.",
    "nka.",
    "nka/nkda",
    "nkda",
    "nkda  nkfa",
    "nkda at the time",
    "nkda listed in patient profile.",
    "nkda listed on form.",
    "nkda nka",
    "nkda nkfa",
    "nkda no food allergies either",
    "nkda no known food allergies",
    "nkda no other allergies",
    "nkda or allergies reported",
    "nkda or to foods.",
    "nkda reported",
    "nkda, food allergies, or other products",
    "nkda, food allergy, or other allergy",
    "nkda, kkfa",
    "nkda, nka",
    "nkda, nkea.",
    "nkda, nkfa",
    "nkda, no environmental allergies, no food allergies",
    "nkda, no food allergies",
    "nkda, no known allergies",
    "nkda, no known food allergies",
    "nkda, no known food or product allergies",
    "nkda, no known other allergies.",
    "nkda, no reported food allergies",
    "nkda, none",
    "nkda.",
    "nkda/ no known foord allergies",
    "nkda/nka",
    "nkda/nkfa",
    "nkda/no know allergies",
    "nkda; nka",
    "nkda; nkfa",
    "nkda; nkfa.",
    "nkda; no allergies to food or any other products",
    "nkda= no",
    "nkda`",
    "nkdfa",
    "nkfda",
    "nkma",
    "nkma / no food allergies",
    "nkma and no food",
    "nkma.",
    "nkma/nka",
    "nknda",
    "nkne",
    "nknown",
    "no",
    "no  not that aware of.",
    "no according to patient questionnaire",
    "no active allergies",
    "no adverse reactions reported",
    "no allegies",
    "no allergic reactions to vaccines.",
    "no allergies",
    "no allergies any medications and food",
    "no allergies at the moment.",
    "no allergies at the time",
    "no allergies at the time of vaccination.",
    "no allergies currently.",
    "no allergies documented",
    "no allergies found so far.",
    "no allergies indicated",
    "no allergies listed at time of vaccine.",
    "no allergies listed for medications,food components, vaccine components, or latex",
    "no allergies noted",
    "no allergies on file",
    "no allergies per mom",
    "no allergies per patient informed consent form",
    "no allergies per screening checklist",
    "no allergies per vaccination checklist",
    "no allergies reported",
    "no allergies reported by parent.",
    "no allergies reported.",
    "no allergies s at the moment.",
    "no allergies stated;nka",
    "no allergies to any food or medications were reported.",
    "no allergies to any food or medications.",
    "no allergies to any food or other products.",
    "no allergies to any medications or food or any products that i'm aware of.",
    "no allergies to anything",
    "no allergies to food or medications",
    "no allergies to medication or food",
    "no allergies to medication or food that i know of.",
    "no allergies to medication to food, or other products.",
    "no allergies to medications",
    "no allergies to medications and food",
    "no allergies to medications or food",
    "no allergies to medications, food or other products.",
    "no allergies to medications, food, or other products noted at the time of vaccination.",
    "no allergies to medications, food, or other products.",
    "no allergies to medications, foods, or other products.",
    "no allergies to meds or foods",
    "no allergies to my knowledge.",
    "no allergies to previous vaccines",
    "no allergies, food or other products.",
    "no allergies, nkda",
    "no allergies.",
    "no allergy",
    "no allergy reported.",
    "no allergy's",
    "no documented allergies",
    "no documented known allergies",
    "no drug allergies",
    "no drug allergies known",
    "no e",
    "no food allergy, no drug allergy",
    "no food or drug allergies",
    "no food or drug allergies reported.",
    "no food, drug, latex, or venom allergies.none per pt.",
    "no history of allergic reaction to covid-19 vaccines, polysorbate, or any vaccine or injectable medication.",
    "no history of allergic reactions per patient's vaccine consent form",
    "no know",
    "no know allergies.",
    "no know allergy",
    "no know drug  or food allergies",
    "no know drug allergies",
    "no know drug allergy",
    "no know drug or food allergy",
    "no known",
    "no known  allergies on file.",
    "no known alergies",
    "no known allegies",
    "no known allergies",
    "no known allergies according to consent form",
    "no known allergies according to our records",
    "no known allergies at this time.",
    "no known allergies discussed",
    "no known allergies documented.",
    "no known allergies informed by mother",
    "no known allergies listed",
    "no known allergies listed on pqcf form",
    "no known allergies no known medication allergies",
    "no known allergies noted",
    "no known allergies noted on file",
    "no known allergies on file at the pharmacy",
    "no known allergies per her profile",
    "no known allergies per mom.",
    "no known allergies per parent",
    "no known allergies per patient",
    "no known allergies per profile",
    "no known allergies reported",
    "no known allergies reported.",
    "no known allergies stated by patient.",
    "no known allergies to any medication, food, or other products",
    "no known allergies to any of the above",
    "no known allergies to anything",
    "no known allergies to food or medication",
    "no known allergies to food or medications",
    "no known allergies to food, medications or other products.",
    "no known allergies to medication",
    "no known allergies to medication or foods",
    "no known allergies to medication, food, or other products.",
    "no known allergies to medications foods or environmental agents",
    "no known allergies to medications or food",
    "no known allergies to medications or food.",
    "no known allergies to medications, food or other products noted at the time of vaccination.",
    "no known allergies to medications, food or other products.",
    "no known allergies to medications, food, or other products as reported by patient",
    "no known allergies to medications, food, or other products noted at the time of vaccination.",
    "no known allergies to medications, food, or other products noted.",
    "no known allergies to medications, foods, or other products.",
    "no known allergies, no known drug allergies",
    "no known allergies, per var patient didn't list any allergies",
    "no known allergies.",
    "no known allergies. no prior reactions two first and second doses of moderna.",
    "no known allergy",
    "no known allergy reported",
    "no known allergys",
    "no known documented allergies.",
    "no known drug allergie",
    "no known drug allergies",
    "no known drug allergies noted",
    "no known drug allergies or food allergies",
    "no known drug allergies, no known food allergies",
    "no known drug allergies.",
    "no known drug allergies; no known food allergies",
    "no known drug allergy",
    "no known drug allergy, others unknown.",
    "no known drug allergy.",
    "no known drug allergy;",
    "no known drug or food allergies",
    "no known drug or food allergies.",
    "no known drug or food allergy",
    "no known drug, food, latex, or venom allergies.",
    "no known drug, food, or other allergies.",
    "no known drug, food, other product allergies.",
    "no known drug/food allergies",
    "no known durg allergy",
    "no known food allergies or drug allergies.",
    "no known food or drug allergies",
    "no known food or drug allergies.",
    "no known food or medication allergies.",
    "no known food, drug, latex, or venom allergies",
    "no known food, drug, latex, or venom allergies.",
    "no known food, drug, latex, or venom allergy",
    "no known food/drug allergies",
    "no known food/environmental or drug allergies",
    "no known med allergies",
    "no known medical or food allergies",
    "no known medication allergies",
    "no known medication allergies, cats, dogs. nuts, seafood",
    "no known medication or other allergies",
    "no known meds, food or other products",
    "no known or stated drug, food, or other allergies",
    "no listed allergies",
    "no medication allergies  reported",
    "no medication or food allergies",
    "no medication or food allergies known.",
    "no medication or food allergies.",
    "no new allergies. or sensitivities",
    "no none allergies",
    "no not really",
    "no official allergies; allergy test to take place 02/2022",
    "no other reactions before vaccine.",
    "no per pt",
    "no reported allergies",
    "no reported allergies at time of vaccination",
    "no reported allergies.",
    "no reported drug and food allergies",
    "no seasional allergies",
    "no sever allergies noted.",
    "no stated",
    "no true allergies",
    "no true allergies.",
    "no vaccine or injectable medication allergies.",
    "no, according to written and verbal questions asked",
    "no.",
    "no.   not that i know of at time of booster vaccine",
    "no.no.",
    "no/unknown",
    "nobe",
    "noe",
    "nome",
    "non",
    "non known",
    "non known of",
    "non known. non stated",
    "non listed or given",
    "non reported",
    "non stated",
    "non that i am aware of",
    "nona",
    "none",
    "none  given",
    "none  i 'm  aware of",
    "none  known",
    "none  that i am aware of.",
    "none (nkda)",
    "none / denies",
    "none acknowledged",
    "none as per mother",
    "none as stated by father",
    "none as stated by patient.",
    "none at the time but now taking antihistamine and vitamin d",
    "none at time",
    "none at time of vaccination",
    "none aware",
    "none aware of",
    "none aware of.",
    "none declared",
    "none detected. blood test done 3/8/2022",
    "none disclosed",
    "none disclosed at time of assessment.",
    "none disclosed.",
    "none documented",
    "none ever before",
    "none for now",
    "none for the moment",
    "none given",
    "none indicated",
    "none indicated on patient intake form.",
    "none indicated on screening questionnaire",
    "none indicated on the system",
    "none indicated on vaccination form",
    "none indicatedd",
    "none know",
    "none know of",
    "none know,",
    "none knowm",
    "none known",
    "none known allergies",
    "none known at the time",
    "none known at the time.",
    "none known at this time",
    "none known at this time.",
    "none known at time of vaccination",
    "none known at time of vaccine admin",
    "none known before now.",
    "none known of",
    "none known of at that time",
    "none known prior to vaccination",
    "none known. family history of food allergies.",
    "none known/encounter at time of vaccination.",
    "none known/reported",
    "none listed",
    "none listed by patient/parent",
    "none listed in todays chart note for todays visit or medical history.",
    "none listed on consent",
    "none listed on consent form",
    "none listed on immunization form",
    "none listed.",
    "none mentioned",
    "none none",
    "none noted",
    "none noted at the time",
    "none noted in emr",
    "none noted on chart",
    "none noted on consent form",
    "none noted on consent form.",
    "none noted on form",
    "none noted on pre-screening vaccination paperwork for flu and covid shots.",
    "none noted on var",
    "none noted.",
    "none of any kind",
    "none of which i'm aware",
    "none on file",
    "none on file, pt stated no allergies also",
    "none on file, said wasn't allergic to anything",
    "none or unknown",
    "none per consent form",
    "none per guardian",
    "none per guardians",
    "none per informed consent",
    "none per mother",
    "none per patient",
    "none per patient profile",
    "none per patient's mother",
    "none per pt",
    "none per pt hx",
    "none per screening form",
    "none per vaccine administration record",
    "none per var form",
    "none previously",
    "none prior",
    "none prior to moderna vaccine",
    "none provided",
    "none recorded",
    "none report",
    "none reported",
    "none reported / nka",
    "none reported at appointment.",
    "none reported at the time",
    "none reported at time of vaccination",
    "none reported at time of vaccination.",
    "none reported by client",
    "none reported by father",
    "none reported by mother/patient.",
    "none reported by parent",
    "none reported by patient",
    "none reported by pt",
    "none reported by the patient",
    "none reported on case report from hospital",
    "none reported on pre-vaccination checklist",
    "none reported on vars form",
    "none reported via cdc pre vaccination checklist",
    "none reported.",
    "none so far.",
    "none specified",
    "none stated and patient filled out none on sheet",
    "none stated by patient",
    "none stated by patient.",
    "none stated on var",
    "none that  is known of",
    "none that am aware",
    "none that are known.",
    "none that i am aware of",
    "none that i can think of, huh, please, i've tried to share unto those in misc top - down own public official's. it's just senseless this has been allowed to go on for 20 plus years & yeah, i'm not the only one that's locally witnessed it. sigh, i just want my home life back (however), you know. housing solution's could have been last 20 plus year's - (using existing plentiful space's) sro's (single room occupancy) conversions 2/ large bathroom at the end of hallway as well as 2 rooms on each floor (w/ wall out between them) thus converting them 2 support services as well as 2 room's converted into a small kitchen area like in office like building's for just each floor's guest (each guest must have a floor id stating their room #. plus small kitchen area's on each floor via some room's converted into such, thus, so everyone is not piling all into the 1st floor lobby, & i know because i've stay in sro's before year's ago. this could have been done the last 20 plus years throughout cities but would have required involved from real estate industry (itself)!",
    "none that i know",
    "none that i know of or have experienced.",
    "none that i know of.",
    "none that i'm aware of",
    "none that i'm aware of.",
    "none that know of",
    "none that we are aware",
    "none that we are aware of",
    "none that we know of",
    "none that were reported",
    "none to  other vaccine or injectable meds",
    "none to immunizations",
    "none to knowledge",
    "none to knowlegde",
    "none to my knowledge",
    "none to my knowledge.",
    "none to note",
    "none to report",
    "none to rph knowledge",
    "none to vaccines",
    "none voiced",
    "none was reported at this present time",
    "none were listed",
    "none yet",
    "none!",
    "none,",
    "none, but now maybe j&j",
    "none, just the hives now for the past 2-3 weeks",
    "none, nkda",
    "none, patient confirmed",
    "none.",
    "none. *please note, i am not sure of the exact date the condition i am reporting began.",
    "none. healthy before this psycho vaccine   you will pay for what you?re doing to people",
    "none. i have never had an allergic reaction to any vaccines ever and have always kept up to date on all the vaccinations recommended by my doctor and the cdc. i also have no food allergies and no medication allergies.",
    "none. no personal nor family history of allergies ever.",
    "none. there was no reaction.",
    "none..",
    "none/ unknown",
    "nonenone",
    "nonexistent",
    "nonne",
    "nono",
    "nonr",
    "nons",
    "nonw",
    "noone",
    "nope",
    "not  known",
    "not able to determine",
    "not according to her consent form",
    "not allergic",
    "not allergic  any of the ingredients in the vaccine",
    "not allergic to anything",
    "not allergies",
    "not any",
    "not any to date",
    "not applicable",
    "not applicable (reporting due to administering booster dose earlier than patient was suppose to get it)",
    "not applicable in relation to vaccine error.",
    "not applicable.",
    "not assessed",
    "not at this time.",
    "not available",
    "not aware",
    "not aware of",
    "not aware of any",
    "not aware of any allergies",
    "not before this",
    "not currently",
    "not i know.",
    "not known",
    "not known per mom and dad",
    "not known.",
    "not listed",
    "not on file",
    "not prior to vaccination",
    "not provided",
    "not reported",
    "not sure",
    "not sure.",
    "not that i am aware of",
    "not that i am aware of.",
    "not that i am aware off.",
    "not that i an aware of",
    "not that i know",
    "not that i know of",
    "not that i know of; no",
    "not that i'm aware of.",
    "not that patient know of.",
    "nothing",
    "nothing i know of",
    "nothing known",
    "nothing per mother",
    "nothing that i am aware of.",
    "nothing that i know of",
    "nothing that i'm aware of.",
    "nothing was reported",
    "notjing",
    "noun",
    "now",
    "np",
    "patient denies any allergies to medications, food, or other products.",
    "pt reported no known allergies",
    "reports none",
    "she is not allergic to any medication, food, or product.",
    "the patient had no known allergies.",
    "there are not any known drug allergies",
    "ukn",
    "uknown",
    "unable to assess",
    "unable to reach parent to obtain information",
    "unk",
    "unkinown",
    "unkknown",
    "unknow",
    "unknown",
    "unknown (possible moderna allergy from this event)",
    "unknown -- none reported",
    "unknown -answered no for prior serious allergic reactions",
    "unknown but the hospital may have her records",
    "unknown history, not our patient.",
    "unknown to filer",
    "unknown to my knowledge-not in chart",
    "unknown to reporter",
    "unknown, parent unable to provide information",
    "unknown- can't reach patient again",
    "unknown-no severe allergies noted",
    "unknown.",
    "unknown.  no allergy known to pfizer product given.",
    "unknown.  no pfizer product allergies.",
    "unknown. not listed",
    "unknown/ not listed",
    "unknown; none disclosed",
    "unknownf",
    "unknows",
    "unkown",
    "unsure",
    "was not assessed",
    "zero",
}


def import_datasets(data_dataset: str, vax_dataset: str) -> pd.DataFrame:
    data = pd.read_csv(data_dataset, parse_dates=DATES, encoding=CODEC, engine="python")
    vdata = pd.read_csv(vax_dataset, encoding=CODEC)

    # merge datasets based on id
    data.set_index("VAERS_ID", inplace=True)
    vdata.set_index("VAERS_ID", inplace=True)
    df = pd.merge(data, vdata, left_index=True, right_index=True)

    df = df[df["VAX_TYPE"].isin(VAX_TYPES)]

    return df


def cleanup_dataset(df: pd.DataFrame) -> pd.DataFrame:
    # drop unused features
    df.drop(DROP_FEATURES, axis=1, inplace=True)

    # get column headings
    df.columns = df.columns.str.lower()
    categorical = list(df.dtypes[df.dtypes == "object"].index)
    numerical = list(df.dtypes[df.dtypes != "object"].index)

    # turn all categorical headings to lowercase
    for c in categorical:
        df[c] = df[c].str.lower()

    # take care of null values
    df["vax_dose_series"].fillna("0", inplace=True)
    df["vax_dose_series"] = df["vax_dose_series"].replace({"unk": np.nan, "7+": 7})

    # conver to 0 and 1
    df[BINARY_FEATURES] = df[BINARY_FEATURES].fillna("n")
    df[BINARY_FEATURES] = df[BINARY_FEATURES].replace({"n": 0, "y": 1})
    df[BINARIZE_FEATURES] = df[BINARIZE_FEATURES].fillna(0)
    df["allergies"] = df["allergies"].apply(lambda x: 0 if x in NONE_VALUES else x)

    # fill missing age with mean
    df["age_yrs"].fillna(df["age_yrs"].mean(), inplace=True)

    # column rename
    df.rename(columns={"vax_manu": "vax_name"}, inplace=True)

    # convert features into binary values
    for bin_feat in BINARIZE_FEATURES:
        bin_feat = bin_feat.lower()
        df[bin_feat].fillna(0, inplace=True)
        df[bin_feat] = df[bin_feat].apply(lambda x: 1 if x != 0 else 0)

    # remove numerical feature from categorical list and add to numerical
    numerical.append(categorical.pop())

    # remove died and vax_manu from categorical list
    categorical.remove("died")
    categorical.remove("vax_manu")

    # fill temporary -1 placeholder for vax_dose_series based on its current distrubution
    dose_distrubution = df.vax_dose_series.value_counts(normalize=True)
    missing_doses = df.vax_dose_series.isnull()
    df.loc[missing_doses, "vax_dose_series"] = np.random.choice(
        dose_distrubution.index, size=len(df[missing_doses]), p=dose_distrubution.values
    )

    # convert str numbers to integers
    df[["age_yrs", "vax_dose_series"]] = df[["age_yrs", "vax_dose_series"]].astype(
        np.int16
    )

    # fill missing state values based on its current distrubution
    state_distrubution = df.state.value_counts(normalize=True)
    missing_states = df.state.isnull()
    df.loc[missing_states, "state"] = np.random.choice(
        state_distrubution.index,
        size=len(df[missing_states]),
        p=state_distrubution.values,
    )

    return df


def balance_dataset(df: pd.DataFrame) -> pd.DataFrame:
    dead = df[df.died == 1].died.count()
    shuffled_df = df.sample(frac=1, random_state=1)
    dead_df = shuffled_df[shuffled_df["died"] == 1]
    alive_df = shuffled_df[shuffled_df["died"] == 0].sample(n=dead, random_state=1)

    return pd.concat([dead_df, alive_df])


def split_data(df: pd.DataFrame):
    df_full_train, df_test = train_test_split(
        df, test_size=0.2, random_state=1, stratify=df.died
    )
    df_train, df_val = train_test_split(
        df_full_train, test_size=0.25, random_state=1, stratify=df_full_train.died
    )

    df_train = df_train.reset_index(drop=True)
    df_val = df_val.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)

    y_train = df_train.died.values
    y_val = df_val.died.values
    y_test = df_test.died.values

    del df_train["died"]
    del df_val["died"]
    del df_test["died"]

    return df_full_train, df_test, df_train, df_val, y_train, y_val, y_test


def prep_data_for_xgboost(X: pd.DataFrame, X_test: pd.DataFrame):
    dfull_train = X.reset_index(drop=True)
    yfull_train = (dfull_train.died == 1).astype(int).values
    del dfull_train["died"]

    dicts_full_train = dfull_train.to_dict(orient="records")

    dv = DictVectorizer(sparse=False)
    X_full_train_dv = dv.fit_transform(dicts_full_train)

    dicts_test = X_test.to_dict(orient="records")
    X_test_dv = dv.transform(dicts_test)

    dfulltrain = xgb.DMatrix(
        X_full_train_dv,
        label=yfull_train,
        # feature_names=dv.get_feature_names_out().tolist(),
    )
    dtest = xgb.DMatrix(
        X_test_dv,
        # feature_names=dv.get_feature_names_out().tolist(),
    )

    return dfulltrain, dtest, dv


def get_xgboost_model(
    eta: float,
    max_depth: int,
    min_child_weight: int,
    dfulltrain: xgb.DMatrix,
    dtest: xgb.DMatrix,
    y_test: np.ndarray,
) -> Tuple[xgb.Booster, np.ndarray]:
    xgb_params = {
        "eta": eta,
        "max_depth": max_depth,
        "min_child_weight": min_child_weight,
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "nthread": 8,
        "seed": 1,
        "verbosity": 1,
    }
    model = xgb.train(xgb_params, dfulltrain, num_boost_round=200)
    y_pred = model.predict(dtest)
    model_score = roc_auc_score(y_test, y_pred)
    print(f"{model_score=}")

    return model, y_pred


def generate_samples(X_test: pd.DataFrame, y_pred: np.ndarray, y_test: np.ndarray):
    sample_count = X_test.shape[0] + 1
    samples = random.sample(range(0, sample_count), 10)

    for n in samples:
        request = X_test.iloc[n].to_dict()
        print(json.dumps(request, indent=2))
        print(f"predicted: {y_pred[n]}")
        print(f"   actual: {y_test[n]}")
        print("---")


def pickle_model(
    eta: float,
    max_depth: int,
    min_child_weight: int,
    model: xgb.Booster,
    dv: DictVectorizer,
):
    # save model
    output_file = Path(
        f"xgboost_eta={eta}_max_depth={max_depth}_min_child_weight={min_child_weight}.bin"
    )
    with output_file.open("wb") as f_out:
        pickle.dump((dv, model), f_out)
    print(f"saved: {output_file.name}")


def main():
    # xgboost optimized params
    eta = 0.3
    max_depth = 5
    min_child_weight = 1

    # import and prep dataset
    df = import_datasets(DATA_DATASET, VAX_DATASET)
    df = cleanup_dataset(df)
    vax_deaths_df = balance_dataset(df)

    # train, test, val split the dataset
    X_full_train, X_test, *_, y_test = split_data(vax_deaths_df)
    dfulltrain, dtest, dv = prep_data_for_xgboost(X_full_train, X_test)
    model, y_pred = get_xgboost_model(
        eta, max_depth, min_child_weight, dfulltrain, dtest, y_test
    )

    # save model to file
    pickle_model(eta, max_depth, min_child_weight, model, dv)

    # generate sample patients
    # generate_samples(X_test, y_pred, y_test)


if __name__ == "__main__":
    main()
