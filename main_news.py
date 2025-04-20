# todo
# naver news crawling

# 정치 : https://news.naver.com/section/100
# 경제 : https://news.naver.com/section/101
# 사회 : https://news.naver.com/section/102
# 생활/문화 : https://news.naver.com/section/103
# IT/과학 : https://news.naver.com/section/105
# 세계 : https://news.naver.com/section/104
# 랭킹 : https://news.naver.com/main/ranking/popularDay.naver?mid=etc&sid1=111





import getNaverNewsList
from file_manager import FileManager
import datetime
import pandas as pd

file_manager = FileManager()

def call_news_main():
    print("main")

    today = datetime.datetime.now().strftime("%Y%m%d")
    folder_path = file_manager.make_folder(today)
    total_news = []
    for i in range(6):
        news = getNaverNewsList.naver_news(f"https://news.naver.com/section/10{i}")
        total_news = total_news + news

    output_filename = f'today_news_{today}.csv'
    file_manager.check_and_delete_file(folder_path+'/'+output_filename)

    df = pd.DataFrame(total_news)
    df.to_csv(folder_path+'/'+output_filename, index=False, encoding='utf-8-sig')
    print("done")


if __name__ == '__main__':
    call_news_main()