import pickle
from pathlib import Path
from typing import Tuple

import bentoml
import xgboost as xgb
from sklearn.feature_extraction import DictVectorizer  # type: ignore

__author__ = "Martin Uribe"
__email__ = "clamytoe@gmail.com"
__stage__ = "dev"
__version__ = "2.0.2"


def find_latest_model(
    dir: str = ".", model_type: str = "xgboost", ext: str = "bin"
) -> Path:
    """Locates the latest pickled model

    Args:
        dir (str, optional): directory to look for the file. Defaults to ".".
        model_type (str, optional): name of the model saved. Defaults to "xgboost".
        ext (str, optional): extention of the pickle file. Defaults to "bin".

    Returns:
        Path: the model returned as a pathlib Path object
    """
    files = Path(dir).glob(f"{model_type}*.{ext}")
    _, file_path = max((f.stat().st_mtime, f) for f in files)

    return Path(file_path)


def load_model(file: Path) -> Tuple[DictVectorizer, xgb.Booster]:
    """Loads the model from the pickle file

    Args:
        file (Path): pathlib object representing the pickled model

    Returns:
        Tuple[DictVectorizer, xgb.Booster]: the loaded DictVectorizer and model
    """
    with file.open("rb") as pkl:
        dv, model = pickle.load(pkl)

    return dv, model


def save_bentoml_model(model: xgb.Booster, dv: DictVectorizer):
    """Saves a bentoml model from the xgb model and DictVectorizer

    Args:
        model (xgb.Booster): the XGBoost model
        dv (DictVectorizer): the DictVectorizer
    """
    bento_model = bentoml.xgboost.save_model(
        "covid_risk_model",
        model,
        labels={
            "owner": __author__,
            "email": __email__,
            "stage": __stage__,
            "version": __version__,
        },
        custom_objects={"dictVectorizer": dv},
        signatures={
            "predict": {
                "batchable": True,
                "batch_dim": 0,
            }
        },
    )
    print(bento_model)


def main():
    """Main entry point for the script"""
    pkl_file = find_latest_model()
    dv, model = load_model(pkl_file)
    save_bentoml_model(model, dv)


if __name__ == "__main__":
    main()
