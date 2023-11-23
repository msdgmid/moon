import pyupbit

access = "pvTGkFvv8VqlbfzvxPMA1RgufwstWayPRaevxYtZ"          # 본인 값으로 변경
secret = "HlLG74h6T4uJyOxGUlzZsjgJzLfMCwBFOzQeI7Cl"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # KRW-BTC 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회