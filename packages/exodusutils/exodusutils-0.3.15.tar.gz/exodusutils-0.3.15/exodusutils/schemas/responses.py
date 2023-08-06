from __future__ import annotations

import abc
from typing import Any, Dict, List, Optional

from bson import ObjectId
from minio.api import Minio
from pandas import DataFrame
from pydantic import BaseModel
from pydantic.fields import Field

from exodusutils.schemas import Attribute
from exodusutils.schemas.scores import CVScores, Scores
from exodusutils.schemas.uri import MinioURI

class ModelRespBase(BaseModel, abc.ABC):
    """
    The base class for all model algorithm responses.
    """


class TrainRespBody(ModelRespBase):
    """
    The schema for train response body.
    """
    model_id: str = Field(description="The specified model id")
    name: str = Field(description="Name of the model. This is the display name for the model. E.g. LightGBM Accuracy - 1")
    model_key: str = Field(description='The key for the model object stored in Minio. E.g. "lgbmaccuracy_1234"')
    algo: str = Field(description='Key for the algorithm. E.g. "lgbmaccuracy".')
    cv_scores: Dict[str, List[float]]
    cv_deviations: Dict[str, float]
    cv_averages: Dict[str, float]
    holdout_scores: Optional[Dict[str, float]]
    validation_scores: Optional[Dict[str, float]]

class PredictRespBody(ModelRespBase):
    """
    The schema for prediction response body.
    """

    prediction: str = Field(description="The prediction file uri")

    @classmethod
    def create(cls, name: str, df: DataFrame, minio: Minio) -> PredictRespBody:
        """
        Creates a `PredictRespBody` based on the prediction result dataframe.

        Parameters
        ----------
        name : str
            Name of the model.
        df : DataFrame
            The prediction results as a Pandas DataFrame.
        minio : Minio
            The Minio client.

        Returns
        -------
        PredictRespBody
            The response body.
        """
        key = f"prediction/{name}-{str(ObjectId())}.csv"
        uri = MinioURI(bucket="exodus", key=key)
        return cls(prediction=uri.put_df(minio, df))


class InfoRespBody(BaseModel):
    """
    The schema for info response body.
    """

    name: str = Field(description="Name of the model algorithm")
    description: str = Field(description="Description of the model algorithm")


class FailedResp(BaseModel):
    """
    The schema for failed actions.
    """

    reason: str


class OKResp(BaseModel):
    """
    The return value for train and predict. Notice how this does not contain any information,
    as both actions are done asynchronously.
    """

    msg: str = "OK"
