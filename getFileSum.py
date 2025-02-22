import pandas as pd
import os
import datetime
from file_manager import FileManager


# pip install openpyxl

file_manager = FileManager()

def getFileSum():
    # 오늘 날짜 생성 (YYYYMMDD 형식)
    today = datetime.datetime.now().strftime("%Y%m%d")
    # 폴더 만들기
    folder_path = file_manager.make_folder(today)
    # CSV 파일로 저장
    output_filename = f'total_{today}.xlsx'
    
    # 동일 파일 삭제
    file_manager.check_and_delete_file(folder_path+'/'+ output_filename)

    # 파일 경로 설정
    krx_file = folder_path + f'/krx_stock_list_{today}.csv'
    theme_file = folder_path + f'/naver_themes_list_{today}.csv'
    theme_dtl_file = folder_path + f'/naver_themes_dtl_list_{today}.csv'
    stock_dtl_file = folder_path + f'/stock_dtl_list_{today}.csv'


    # 각 CSV 파일 읽기
    try:
        # KRX 주식 목록 읽기 (필요한 컬럼만 선택)
        krx_df = pd.read_csv(krx_file, usecols=['종목코드', '종목명', '시장구분', '상장주식수'])
        
        # 테마 목록 읽기
        theme_df = pd.read_csv(theme_file)
        
        # 테마 상세 목록 읽기
        theme_dtl_df = pd.read_csv(theme_dtl_file)

        # 종목 상세 목록 읽기
        stock_dtl_df = pd.read_csv(stock_dtl_file)
        
        # Excel 파일로 저장
        with pd.ExcelWriter(folder_path + '/' +output_filename, engine='openpyxl') as writer:
            krx_df.to_excel(writer, sheet_name='주식종목', index=False)
            stock_dtl_df.to_excel(writer, sheet_name='주식종목상세', index=False)
            theme_df.to_excel(writer, sheet_name='테마', index=False)
            theme_dtl_df.to_excel(writer, sheet_name='테마상세', index=False)
        
        print(f"'{output_filename}' 파일이 성공적으로 생성되었습니다.")

    except FileNotFoundError as e:
        print(f"파일을 찾을 수 없습니다: {e.filename}")
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")



if __name__ == "__main__":
    getFileSum()
