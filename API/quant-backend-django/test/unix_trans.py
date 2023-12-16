import datetime

timestamps = [
    1.69353E+12,
    1.69354E+12,
    # 添加更多的时间戳...
]

# 将科学计数法表示的时间戳转换为整数
timestamps_as_int = [int(ts) for ts in timestamps]

# 将整数时间戳转换为ISO日期时间格式
iso_date_times = [datetime.datetime.fromtimestamp(ts / 1e9).isoformat() for ts in timestamps_as_int]

# 打印结果
for ts, iso_dt in zip(timestamps, iso_date_times):
    print(f"Scientific Notation Timestamp: {ts}")
    print(f"ISO Date Time: {iso_dt}")
    print()
