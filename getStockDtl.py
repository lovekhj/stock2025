import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml

## pip install lxml

def get_stock_info(code):
    url = f'https://finance.naver.com/item/main.naver?code={code}'  # URL 변경
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://finance.naver.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류 체크
        response.encoding = 'euc-kr'
        soup = BeautifulSoup(response.text, 'lxml')

        print("soup ==>", soup)

        # 종목 기본 정보
        stock_name_element = soup.select_one('div.wrap_company h2 a')
        stock_name = stock_name_element.text.strip() if stock_name_element else 'N/A'

        # 현재가 정보
        current_price_element = soup.select_one('div.today span.blind')
        current_price = current_price_element.text.strip() if current_price_element else 'N/A'
        
        # 전일대비 정보
        price_diff_element = soup.select_one('div.today span.blind:nth-child(2)')
        price_diff = price_diff_element.text.strip() if price_diff_element else 'N/A'
        
        # 전일가 계산
        prev_price_element = soup.select_one("#chart_area > div.rate_info > table > tbody > tr:nth-child(1) > td.first > em")
        print("prev_price==>", prev_price_element.text)
        # try:
        #     if current_price != 'N/A' and price_diff != 'N/A':
        #         current_price_num = int(current_price.replace(',', ''))
        #         price_diff_num = int(price_diff.replace(',', '').replace('+', '').replace('-', ''))
        #         if '-' in price_diff:
        #             prev_price = current_price_num + price_diff_num
        #         else:
        #             prev_price = current_price_num - price_diff_num
        #         prev_price = format(prev_price, ',')
        #     else:
        #         prev_price = 'N/A'
        # except ValueError:
        #     prev_price = 'N/A'
        
        # 거래량, 거래대금 정보
        volume_element = soup.select_one('span#_quant')
        volume = volume_element.text.strip() if volume_element else 'N/A'
        
        trading_value_element = soup.select_one('span#_amount')
        trading_value = trading_value_element.text.strip() if trading_value_element else 'N/A'
        
        # PER, 추정PER 정보
        per_element = soup.select_one('#_per')
        per = per_element.text.strip().split('\n')[0] if per_element else 'N/A'
        
        est_per_element = soup.select_one('table.per_table tbody tr td:nth-child(2)')
        estimated_per = est_per_element.text.strip().split('\n')[0] if est_per_element else 'N/A'
        
        # 시가총액 정보
        market_cap_element = soup.select_one('#_market_sum')
        market_cap = market_cap_element.text.strip() if market_cap_element else 'N/A'
        
        # 투자의견, 목표주가 정보 (컨센서스)
        consensus_element = soup.select_one('#tab_con1 > div:nth-child(4) > table > tbody > tr:nth-child(1) > td > span.f_up > em')
        consensus = consensus_element.text.strip() if consensus_element else 'N/A'
        
        target_price_element = soup.select_one('#tab_con1 > div:nth-child(4) > table > tbody > tr:nth-child(1) > td > em')
        print("target_price_element==>", target_price_element)
        target_price = target_price_element.text.strip() if target_price_element else 'N/A'
        
        stock_data = {
            '종목코드': code,
            '종목명': stock_name,
            '현재가': current_price,
            '전일가': prev_price,
            '전일대비': price_diff,
            '거래량': volume,
            '거래대금': trading_value,
            'PER': per,
            '추정PER': estimated_per,
            '시가총액': market_cap.replace('\n','').replace('\t',''),
            '투자의견': consensus,
            '목표주가': target_price
        }
        
        # 데이터 검증
        print("\n수집된 데이터:")
        for key, value in stock_data.items():
            print(f"{key}: {value}")
        
        return pd.DataFrame([stock_data])

    except requests.RequestException as e:
        print(f"네트워크 요청 중 오류 발생: {str(e)}")
        return None
    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {str(e)}")
        return None

# 사용 예시
if __name__ == "__main__":
    stock_code = "005930"  # 삼성전자
    df = get_stock_info(stock_code)
    if df is not None:
        print("\n최종 DataFrame:")
        print(df)
        # CSV 파일로 저장
        df.to_csv(f'stock_info_{stock_code}.csv', index=False, encoding='utf-8-sig')
        print(f"\nCSV 파일 저장 완료: stock_info_{stock_code}.csv")