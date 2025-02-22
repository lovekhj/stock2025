import pandas as pd
import os
import datetime

# pip install openpyxl

def make_folder(today):
    # 현재 디렉토리 기준으로 폴더 경로 설정
    folder_path = os.path.join(os.getcwd(), today)

    # 폴더가 없으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"폴더 생성됨: {folder_path}")
    else:
        print(f"이미 존재하는 폴더: {folder_path}")

    return folder_path

def chk_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)
        print(f"{filename} 파일을 삭제했습니다.")
    else:
        print(f"{filename} 파일이 존재하지 않습니다.")


def getFileSum():

    # 오늘 날짜 생성 (YYYYMMDD 형식)
    today = datetime.datetime.now().strftime("%Y%m%d")

    # 폴더 만들기
    folder_path = make_folder(today)

    # CSV 파일로 저장
    output_filename = f'total_{today}.xlsx'
    
    # 동일 파일 삭제
    chk_file(folder_path+'/'+ output_filename)


    # 파일 경로 설정
    krx_file = folder_path + f'/krx_stock_list_{today}.csv'
    theme_file = folder_path + f'/naver_themes_list_{today}.csv'
    theme_dtl_file = folder_path + f'/naver_themes_dtl_list_{today}.csv'


    # 각 CSV 파일 읽기
    try:
        # KRX 주식 목록 읽기 (필요한 컬럼만 선택)
        krx_df = pd.read_csv(krx_file, usecols=['종목코드', '종목명', '시장구분', '상장주식수'])
        
        # 테마 목록 읽기
        theme_df = pd.read_csv(theme_file)
        
        # 테마 상세 목록 읽기
        theme_dtl_df = pd.read_csv(theme_dtl_file)
        
        # Excel 파일로 저장
        with pd.ExcelWriter(folder_path + '/' +output_filename, engine='openpyxl') as writer:
            krx_df.to_excel(writer, sheet_name='items', index=False)
            theme_df.to_excel(writer, sheet_name='theme', index=False)
            theme_dtl_df.to_excel(writer, sheet_name='themeDtl', index=False)
        
        print(f"'{output_filename}' 파일이 성공적으로 생성되었습니다.")

    except FileNotFoundError as e:
        print(f"파일을 찾을 수 없습니다: {e.filename}")
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")


if __name__ == "__main__":
    getFileSum()
