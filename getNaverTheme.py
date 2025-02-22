import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import datetime


# pip install requests beautifulsoup4 pandas


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


def get_theme_data(page_num):
    url_basic = f"https://finance.naver.com/sise"
    url = f"https://finance.naver.com/sise/theme.naver?&page={page_num}"
    response = requests.get(url)
    response.encoding = 'euc-kr'  # 한글 인코딩 설정
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 테마 테이블 찾기
    theme_table = soup.find('table', {'class': 'type_1'})
    theme_rows = theme_table.find_all('tr')[2:]  # 헤더 제외
    
    themes_data = []
    
    for row in theme_rows:
        cols = row.find_all('td')
        if len(cols) > 1:  # 빈 행 제외
            print("cols==>", cols)
            theme_url = url_basic + cols[0].find('a')['href']
            print("theme_url==>", theme_url)
            
            theme_name = cols[0].find('a').text.strip()
            change_rate = cols[1].text.strip()
            
            themes_data.append({
                '테마명': theme_name,
                '전일대비': change_rate,
                '상세url': theme_url,

            })
    
    return themes_data



if __name__ == "__main__":
    # 모든 페이지의 데이터 수집
    all_themes_data = []
    for page in range(1, 9):  # 1페이지부터 8페이지까지
    # for page in range(1, 2):  # 1페이지부터 8페이지까지
        page_data = get_theme_data(page)
        all_themes_data.extend(page_data)
        time.sleep(1)  # 서버 부하 방지를 위한 지연

    # print(all_themes_data)
    for item in all_themes_data:
        print(item)

    # 오늘 날짜 생성 (YYYYMMDD 형식)
    today = datetime.datetime.now().strftime("%Y%m%d")

    # 폴더 만들기
    folder_path = make_folder(today)

    # CSV 파일로 저장
    output_filename = f'naver_themes_list_{today}.csv'
    
    # 동일 파일 삭제
    chk_file(folder_path+'/'+ output_filename)

    # # DataFrame 생성 및 CSV 저장
    df = pd.DataFrame(all_themes_data)
    df.to_csv(folder_path+'/'+ output_filename, index=False, encoding='utf-8-sig')
    print(f"데이터가 {output_filename}로 저장되었습니다.")
