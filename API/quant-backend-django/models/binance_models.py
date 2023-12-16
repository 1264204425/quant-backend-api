from pydantic import BaseModel, Field


class GetBinanceKlineModel(BaseModel):
    symbol: str = Field(..., description="交易对",example="BTCUSDT")
    time_interval: str = Field(..., description="时间间隔",example="5m")
    start_time: str = Field(..., description="开始时间",example="2021-01")
    end_time: str = Field(..., description="结束时间",example="2021-01")