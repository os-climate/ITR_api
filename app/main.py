import json
import os

from typing import List, Optional

import pandas as pd
import numpy as np
import uvicorn
from ITR.interfaces import PortfolioCompany, EScope, ETimeFrames, ScoreAggregations

from fastapi import FastAPI, File, Form, UploadFile, Body, HTTPException, Request
from pydantic import BaseModel
import mimetypes
import ITR
from ITR.portfolio_aggregation import PortfolioAggregationMethod

app = FastAPI(
    title="ITR Temperature Alignment tool API",
    description="This tool helps companies and financial institutions to assess the temperature alignment of current "
                "targets, commitments, and investment and lending portfolios.",
    version="0.2.0",
)

mimetypes.init()

APP_ROOT = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = os.path.join(APP_ROOT, 'data')


@app.middleware("http")
async def add_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "deny"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Pragma"] = "no-cache"
    return response

with open(os.path.join(APP_ROOT, 'config.json')) as f_config:
    config = json.load(f_config)


class ResponseTemperatureScore(BaseModel):
    aggregated_scores: Optional[ScoreAggregations]
    scores: List[dict]
    companies: List[dict]


@app.post("/temperature_score/", response_model=ResponseTemperatureScore, response_model_exclude_none=True)
def calculate_temperature_score(
        companies: List[PortfolioCompany] = Body(
            ...,
            description="A portfolio containing the companies. If you want to use other fields later on or for grouping "
                        "you can include these in the 'user_fields' object."),
        default_score: float = Body(
            default=config["default_score"],
            gte=0,
            description="The default score to fall back on when there's no target available."),
        data_providers: Optional[List[str]] = Body(
            default=[],
            description="A list of data provider names to use. These names should be available in the list that can be "
                        "retrieved through the /data_providers/ endpoint."),
        aggregation_method: Optional[PortfolioAggregationMethod] = Body(
            default=config["aggregation_method"],
            description="The aggregation method to use."),
        grouping_columns: Optional[List[str]] = Body(
            default=None,
            description="A list of column names that should be grouped on."),
        include_columns: Optional[List[str]] = Body(
            default=[],
            description="A list of column names that should be included in the output."),
        anonymize_data_dump: Optional[bool] = Body(
            default=False,
            description="Whether or not the resulting data set should be anonymized or not."),
        aggregate: Optional[bool] = Body(
            default=True,
            description="Whether to calculate aggregations or not."),
        scopes: Optional[List[EScope]] = Body(
            default=[],
            description="The scopes that should be included in the results."),
        time_frames: Optional[List[ETimeFrames]] = Body(
            default=[],
            description="The time frames that should be included in the results.")
) -> ResponseTemperatureScore:
    """
    Calculate the temperature score for a given set of parameters.
    """
    try:
        dataproviders_config = config["data_providers"]
        for dataprovider in dataproviders_config:
            dataprovider["parameters"]["company_path"] = os.path.join(APP_ROOT, dataprovider["parameters"]["company_path"])
            dataprovider["parameters"]["sector_path"] = os.path.join(APP_ROOT, dataprovider["parameters"]["sector_path"])
        data_providers = ITR.utils.get_data_providers(dataproviders_config, data_providers)
        portfolio_data = ITR.utils.get_data(data_providers, companies)
        scores, aggregations = ITR.utils.calculate(
            portfolio_data=portfolio_data,
            fallback_score=default_score,
            time_frames=time_frames,
            scopes=scopes,
            aggregation_method=aggregation_method,
            grouping=grouping_columns,
            anonymize=anonymize_data_dump,
            aggregate=aggregate
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=repr(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

    # Include columns
    include_columns = ["company_name", "scope", "time_frame", "temperature_score"] + \
                      [column for column in include_columns if column in scores.columns]

    return ResponseTemperatureScore(
        aggregated_scores=aggregations,
        scores=scores.where(pd.notnull(scores), None).to_dict(orient="records"),
        companies=scores[include_columns].replace({np.nan: None}).to_dict(orient="records")
    )


class ResponseDataProvider(BaseModel):
    name: str
    type: str


@app.get("/data_providers/", response_model=List[ResponseDataProvider])
def get_data_providers() -> List[ResponseDataProvider]:
    """
    Get a list of the available data providers.
    """
    return [ResponseDataProvider(name=data_provider["name"], type=data_provider["type"])
            for data_provider in config["data_providers"]]


@app.post("/parse_portfolio/", response_model=List[dict])
def parse_portfolio(file: bytes = File(...), skiprows: int = Form(...)):
    """
    Parse a portfolio Excel file and return it as a list of dictionaries.

    *Note: This endpoint is only for use in the frontend*
    """
    df = pd.read_excel(file, skiprows=int(skiprows))

    return df.replace(r'^\s*$', np.nan, regex=True).dropna(how='all').replace({np.nan: None}).to_dict(orient="records")




if __name__ == "__main__":
    uvicorn.run("main:app", host=config["server"]["host"], port=config["server"]["port"],
                log_level=config["server"]["log_level"], reload=config["server"]["reload"])
