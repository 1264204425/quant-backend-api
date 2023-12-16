import logging
import os
import time
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from models.binance_models import *
from server.binance.get_kline import *
from server.utils import *

env = os.environ
# app = FastAPI(docs_url=None, redoc_url=None)  # 用于禁用swagger文档
app = FastAPI()

# 日志配置
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)
# 输出到控制台
to_console = logging.StreamHandler()
to_console.setFormatter(formatter)
logger.addHandler(to_console)

# 输出到文件中
to_file = logging.FileHandler(filename="log.txt")
to_file.setFormatter(formatter)
logger.addHandler(to_file)

# 配置CORS
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/binance/get_kline", tags=["Binance"])
async def get_kline(
        getBinanceKlineModel: GetBinanceKlineModel
):
    """
    按月获取k线数据

    :param getBinanceKlineModel:
    :return:
    """
    symbol = getBinanceKlineModel.symbol
    time_interval = getBinanceKlineModel.time_interval
    start_time = getBinanceKlineModel.start_time
    end_time = getBinanceKlineModel.end_time

    # 获取当前时间戳做为文件夹名
    current_timestamp = int(time.time())

    # 遍历月份
    start_year = int(start_time.split("-")[0])
    start_month = int(start_time.split("-")[1])
    end_year = int(end_time.split("-")[0])
    end_month = int(end_time.split("-")[1])
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if year == start_year and month < start_month:
                continue
            if year == end_year and month > end_month:
                continue
            date = f"{year}-{month:02d}"
            logger.info(f"symbol:{symbol},date: {date}")
            get_binance_kline(symbol, time_interval, date, f"{BASE_DIR}/data/binance/{current_timestamp}")

    # 清洗数据
    file_path = clear_data(current_timestamp)

    return FileResponse(file_path, media_type='application/octet-stream', filename=f"{start_time}-{end_time}.csv")


if __name__ == '__main__':
    # 启动服务
    host = env.get("HOST") if env.get("HOST") is not None else "0.0.0.0"
    port = int(env.get("PORT")) if env.get("PORT") is not None else 7777
    uvicorn.run(app='app:app', host=host, port=port, reload=True)
