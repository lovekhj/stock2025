import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd

# url = 'https://finance.naver.com/sise/sise_index_day.naver?code=KOSPI'
# resp = requests.get(url)
# soup = BeautifulSoup(resp.content, 'lxml')

# "상위태그.클래명"  또는 "상위태그.아이디명"

# dates = soup.select("td.date")
# date_lst = [ d.text for d in dates]
# print(date_lst)

# rate_down = soup.select("td.rate_down")
# rate_down_lst = [r.text.strip() for r in rate_down]
# print(rate_down_lst)

# aaa = soup.select("td.number_1")
# # print(aaa)
# for aaaa in aaa:
#     print(aaaa)

# [0::4]는 파이썬의 슬라이싱(slicing) 문법이야
# 리스트의 0번째 인덱스부터 시작해서, 4개씩 건너뛰며 요소를 가져와라 는 뜻이야
# 리스트[start:stop:step]

# prices, rates, volumns, amounts = [],[],[],[]
# prices = [p.text for p in soup.select("td.number_1")[0::4]] # 체결가
# rates = [r.text.strip() for r in soup.select("td.number_1")[1::4]] # 등락률
# volumns = [v.text for v in soup.select("td.number_1")[2::4]] # 거래량
# amounts = [a.text for a in soup.select("td.number_1")[3::4]] # 거래대금
# print(prices, rate, volumns, amounts)

# for i in range(len(prices)):
#     print(date_lst[i], prices[i],rate_down_lst[i], rates[i], volumns[i], amounts[i])

# last_page = soup.select("td.pgRR a")[0]["href"].split("=")[-1]
# print(last_page)

# 참고로 아래 코드에서 append를 사용할 경우 리스트 안에 리스트 형태로 모든 데이터가 들어갑니다. 각 컬럼에 들어갈 값의 리스트이기 때문에 
# 각 리스트는 1차원 리스트가 되어야 하고, 이 때는 append 대신 extend를 사용해주면 됩니다.
# extend는 append와 달리 리스트를 리스트에 넣더라도 내용만 넣어서 1차원 리스트로 만들어줍니다.

dates, prices, diffs, rates, volumns, amounts = [],[],[],[], [],[]
for i in range(223, 225):
    url = f'https://finance.naver.com/sise/sise_index_day.naver?code=KOSPI&page={i}'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')
    
    dates.extend([d.text for d in soup.select("td.date")]) # 날짜
    prices.extend([p.text for p in soup.select("td.number_1")[0::4]]) # 체결가
    diffs.extend([d.text.strip() for d in soup.select("td.rate_down")]) # 전일비
    rates.extend([r.text.strip() for r in soup.select("td.number_1")[1::4]]) # 등락률
    volumns.extend([v.text for v in soup.select("td.number_1")[2::4]]) # 거래량
    amounts.extend([a.text for a in soup.select("td.number_1")[3::4]]) # 거래대금


df_ksp200 = pd.DataFrame({"날짜": dates, '체결가':prices, "전일비":diffs, 
                          "등락율":rates, "거래량":volumns, "거래대금":amounts})
print(df_ksp200)
