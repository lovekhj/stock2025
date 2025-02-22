from io import BytesIO
import requests
import json
# from datetime import datetime, time, date
import pandas as pd
import datetime
import time
import os
from file_manager import FileManager

# 미리셋팅
# pip install requests pandas

file_manager = FileManager()

def get_krx_stock_list():
    """KRX 주식시장의 전종목 시세를 가져오는 함수"""
    print("*" * 80)
    print("KRX 주식시장의 전종목 시세를 가져오는 함수")
    print("*" * 80)
    
    
    # 오늘 날짜 생성 (YYYYMMDD 형식)
    today = datetime.datetime.now().strftime("%Y%m%d")
    # 폴더 만들기
    folder_path = file_manager.make_folder(today)
    
    # otp 데이터 가져오기
    gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    headers = {
        "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Refer": "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101",
        "Connection": "keep-alive"
        }
    query_str_params = {
        "locale": "ko_KR",
        "mktId": "ALL",
        "trdDd": today,
        "share": "1",
        "money": "1",
        "csvxls_isNo": "false",
        "name": "fileDown",
        "url": "dbms/MDC/STAT/standard/MDCSTAT01501"
    }

    try:

        # return df
        res = requests.get(gen_otp_url, query_str_params, headers=headers)
        time.sleep(1.0)  # 1초
        res.raise_for_status()
        down_data = {"code": res.content}
        print("OTP 코드 발급 완료")

        # 데이터 다운로드 요청
        down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
        down_headers = headers.copy()
        down_headers['Content-Type'] = 'application/x-www-form-urlencoded'

        down_csv = requests.post(down_url, data=down_data, headers=down_headers)
        down_csv.raise_for_status()
        print("데이터 다운로드 완료")
        time.sleep(1.0)

        # 다운 받은 csv파일을 pandas의 read_csv 함수를 이용하여 읽어 들임.
        # read_csv 함수의 argument에 적합할 수 있도록 BytesIO함수를 이용하여 바이너 스트림 형태로

        # 데이터프레임 생성
        df = pd.read_csv(BytesIO(down_csv.content), encoding='EUC-KR')
        print("df==>", df)
        # CSV 파일로 저장
        output_filename = f'krx_stock_list_{today}.csv'
        # 동일 파일 삭제
        file_manager.check_and_delete_file(folder_path+'/'+ output_filename)

        df.to_csv(folder_path+'/'+ output_filename, index=False, encoding='utf-8-sig')
        print(f"데이터가 {output_filename}로 저장되었습니다.")
        
    except requests.exceptions.RequestException as e:
        print(f"데이터 요청 중 오류가 발생했습니다: {e}")
        return None
    except Exception as e:
        print(f"처리 중 오류가 발생했습니다: {e}")
        return None

if __name__ == "__main__":
    get_krx_stock_list()
