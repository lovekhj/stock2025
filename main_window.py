import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QTextEdit, QLabel,
                           QProgressBar, QTabWidget, QComboBox, QSizePolicy,
                           QDateEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate
import subprocess
import datetime


# pip install PyQt5 pandas openpyxl

class WorkerThread(QThread):
    finished = pyqtSignal(str)
    progress = pyqtSignal(str)
    
    def __init__(self, script_name):
        super().__init__()
        self.script_name = script_name
    
    def run(self):
        try:
            self.progress.emit(f"{self.script_name} 실행 중...")
            
            # 현재 작업 디렉토리 출력
            current_dir = os.getcwd()
            print(f"현재 작업 디렉토리: {current_dir}")
            print(f"실행할 스크립트: {os.path.join(current_dir, self.script_name)}")
            
            process = subprocess.Popen(
                [sys.executable, self.script_name],  # sys.executable로 Python 인터프리터 경로 지정
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                cwd=current_dir  # 현재 디렉토리에서 실행
            )
            
            stdout, stderr = process.communicate()
            
            if stdout:
                print("표준 출력:", stdout)
            if stderr:
                print("표준 에러:", stderr)
            
            if process.returncode == 0:
                self.finished.emit(f"{self.script_name} 실행 완료")
            else:
                self.finished.emit(f"{self.script_name} 실행 실패: {stderr}")
        except Exception as e:
            self.finished.emit(f"오류 발생: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("주식 데이터 관리 시스템")
        self.setGeometry(100, 100, 1600, 1000)
        
        # 메인 위젯과 레이아웃 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # 상단 레이아웃 (버튼과 테이블)
        top_layout = QHBoxLayout()
        
        # 왼쪽 버튼 패널
        button_panel = QWidget()
        button_layout = QVBoxLayout(button_panel)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        # 버튼 생성
        buttons = [
            ("KRX주식정보", 'getKrxStockList.py'),
            ("테마조회", 'getNaverTheme.py'),
            ("테마상세조회", 'getNaverThemDtl.py'),
            ("주식상세조회", 'getStockDtl.py'),
            ("엑셀데이터", 'getFileSum.py'),
            ("조회", None)
        ]
        
        for text, script_name in buttons:
            btn = QPushButton(text)
            btn.setMinimumHeight(50)
            if script_name:
                btn.clicked.connect(lambda checked, sn=script_name: self.run_script(sn))
            else:
                btn.clicked.connect(self.load_excel_data)
            button_layout.addWidget(btn)
        
        button_layout.addStretch()
        button_panel.setMaximumWidth(200)
        top_layout.addWidget(button_panel)
        
        # 오른쪽 패널 (검색조건 + 탭)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)
        
        # 검색 조건 패널
        search_panel = QWidget()
        search_layout = QHBoxLayout(search_panel)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        # 날짜 선택 위젯 추가
        date_label = QLabel("날짜:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)  # 달력 팝업 활성화
        self.date_edit.setDate(QDate.currentDate())  # 오늘 날짜로 초기화
        self.date_edit.setDisplayFormat("yyyy-MM-dd")  # 날짜 표시 형식
        
        # 검색 조건 위젯들
        code_label = QLabel("종목코드:")
        self.code_combo = QComboBox()
        name_label = QLabel("종목명:")
        self.name_combo = QComboBox()
        theme_label = QLabel("테마:")
        self.theme_combo = QComboBox()
        
        # 검색 버튼과 초기화 버튼
        self.search_button = QPushButton("검색")
        self.search_button.setFixedWidth(80)
        self.search_button.clicked.connect(lambda: self.run_script('getFileSum.py'))  # 엑셀데이터 버튼과 동일 기능
        
        self.reset_button = QPushButton("초기화")
        self.reset_button.setFixedWidth(80)
        self.reset_button.clicked.connect(self.reset_filters)
        
        # 콤보박스 설정
        for combo in [self.code_combo, self.name_combo, self.theme_combo]:
            combo.setEditable(True)
            combo.setInsertPolicy(QComboBox.NoInsert)
            combo.setMinimumWidth(150)
        
        # 검색 조건 패널에 위젯 추가 (날짜 선택 추가)
        search_layout.addWidget(date_label)
        search_layout.addWidget(self.date_edit)
        search_layout.addWidget(code_label)
        search_layout.addWidget(self.code_combo)
        search_layout.addWidget(name_label)
        search_layout.addWidget(self.name_combo)
        search_layout.addWidget(theme_label)
        search_layout.addWidget(self.theme_combo)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.reset_button)
        search_layout.addStretch()
        
        # 검색 조건 패널 높이 설정
        search_panel.setFixedHeight(40)
        right_layout.addWidget(search_panel)
        
        # 탭 위젯
        self.tab_widget = QTabWidget()
        # 최소 높이 제거하고 크기 정책 설정
        self.tab_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        right_layout.addWidget(self.tab_widget)
        
        top_layout.addWidget(right_panel, stretch=1)
        
        # 하단 상태 패널
        status_panel = QWidget()
        status_layout = QVBoxLayout(status_panel)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(2)
        
        # 진행 상태 표시줄
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(15)
        status_layout.addWidget(self.progress_bar)
        
        # 상태 메시지 창
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setFixedHeight(80)
        status_layout.addWidget(self.status_text)
        
        # 상태 패널 전체 높이 설정
        status_panel.setFixedHeight(100)
        
        main_layout.addLayout(top_layout, stretch=1)
        main_layout.addWidget(status_panel)
        
        # 최소 창 크기 설정
        self.setMinimumSize(800, 600)
        
        # 작업 스레드 초기화
        self.worker = None
        self.current_df = None

    def add_status_message(self, message):
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_message = f"[{current_time}] {message}"
            
            current_text = self.status_text.toPlainText()
            messages = current_text.split('\n') if current_text else []
            messages.append(new_message)
            if len(messages) > 5:
                messages = messages[-5:]
            
            self.status_text.clear()
            self.status_text.setText('\n'.join(messages))
            
            QApplication.processEvents()
            scrollbar = self.status_text.verticalScrollBar()
            if scrollbar:
                scrollbar.setValue(scrollbar.maximum())
                
        except Exception as e:
            print(f"상태 메시지 업데이트 중 오류: {str(e)}")

    def run_script(self, script_name):
        """Python 스크립트 실행"""
        try:
            self.add_status_message(f"{script_name} 실행 중...")
            self.progress_bar.setValue(0)
            
            # WorkerThread 생성 및 시작
            self.worker = WorkerThread(script_name)
            self.worker.progress.connect(self.add_status_message)
            self.worker.finished.connect(self.on_script_finished)
            self.worker.start()
            
        except Exception as e:
            self.add_status_message(f"스크립트 실행 중 오류 발생: {e}")
            self.progress_bar.setValue(0)

    def on_script_finished(self, result):
        """스크립트 실행 완료 후 처리"""
        try:
            self.add_status_message(f"스크립트 실행 완료: {result}")
            self.progress_bar.setValue(100)
            
            # getFileSum.py 실행 후 자동으로 Excel 파일 로드
            if 'getFileSum.py' in result:
                self.load_excel_data()
            
        except Exception as e:
            self.add_status_message(f"완료 처리 중 오류 발생: {e}")

    def update_combos(self, df):
        """콤보박스 항목 업데이트"""
        try:
            # 종목코드 (6자리 유지)
            if '종목코드' in df.columns:
                unique_codes = sorted(df['종목코드'].unique())
                self.code_combo.clear()
                self.code_combo.addItem('')  # 빈 항목 추가
                self.code_combo.addItems([f"{str(code).zfill(6)}" for code in unique_codes])
            
            # 종목명
            if '종목명' in df.columns:
                unique_names = sorted(df['종목명'].unique())
                self.name_combo.clear()
                self.name_combo.addItem('')
                self.name_combo.addItems([str(name) for name in unique_names])
            
            # 테마
            if '테마' in df.columns:
                unique_themes = sorted(df['테마'].unique())
                self.theme_combo.clear()
                self.theme_combo.addItem('')
                self.theme_combo.addItems([str(theme) for theme in unique_themes])
        
        except Exception as e:
            self.add_status_message(f"콤보박스 업데이트 중 오류 발생: {e}")

    def reset_filters(self):
        """검색 조건 초기화"""
        try:
            # 날짜를 오늘 날짜로 초기화
            self.date_edit.setDate(QDate.currentDate())
            
            # 콤보박스 초기화
            self.code_combo.setCurrentText("")
            self.name_combo.setCurrentText("")
            self.theme_combo.setCurrentText("")
            
            # 테이블 데이터 초기화
            self.load_excel_data()  # 현재 선택된 날짜로 데이터 다시 로드
            
            self.add_status_message("검색 조건과 정렬이 초기화되었습니다.")
            
        except Exception as e:
            self.add_status_message(f"초기화 중 오류 발생: {e}")

    def filter_data(self):
        """선택된 조건으로 데이터 필터링"""
        try:
            if self.current_df is None:
                self.add_status_message("조회할 데이터가 없습니다.")
                return
            
            df = self.current_df.copy()
            
            # 필터 조건 가져오기
            code_filter = self.code_combo.currentText().strip()
            name_filter = self.name_combo.currentText().strip()
            theme_filter = self.theme_combo.currentText().strip()
            
            # 필터 적용
            if code_filter:
                df = df[df['종목코드'].astype(str).str.contains(code_filter, case=False)]
            if name_filter:
                df = df[df['종목명'].astype(str).str.contains(name_filter, case=False)]
            if theme_filter:
                df = df[df['테마'].astype(str).str.contains(theme_filter, case=False)]
            
            # 현재 선택된 탭의 테이블 업데이트
            current_table = self.tab_widget.currentWidget()
            if current_table:
                # 정렬 상태 저장
                sort_column = current_table.horizontalHeader().sortIndicatorSection()
                sort_order = current_table.horizontalHeader().sortIndicatorOrder()
                
                # 새 테이블 생성
                new_table = self.create_table_widget(df)
                
                # 이전 정렬 상태가 있었다면 복원
                if sort_column >= 0:
                    new_table.sortItems(sort_column, sort_order)
                
                # 테이블 교체
                self.tab_widget.removeTab(self.tab_widget.currentIndex())
                self.tab_widget.insertTab(self.tab_widget.currentIndex(), new_table, 
                                        self.tab_widget.tabText(self.tab_widget.currentIndex()))
                
                self.add_status_message(f"검색 결과: {len(df)}건")
            
        except Exception as e:
            self.add_status_message(f"데이터 필터링 중 오류 발생: {e}")

    def update_current_table(self, df):
        """현재 선택된 탭의 테이블 업데이트"""
        current_table = self.tab_widget.currentWidget()
        if current_table:
            current_table.setRowCount(len(df))
            for row in range(len(df)):
                for col in range(len(df.columns)):
                    item = QTableWidgetItem(str(df.iloc[row, col]))
                    current_table.setItem(row, col, item)

    def create_table_widget(self, df):
        """테이블 위젯 생성 및 설정"""
        table = QTableWidget()
        table.setAlternatingRowColors(True)
        
        # 행과 열 설정
        table.setRowCount(len(df))
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns)
        
        # 데이터 채우기
        for row in range(len(df)):
            for col in range(len(df.columns)):
                value = df.iloc[row, col]
                item = QTableWidgetItem()
                
                # 숫자 데이터 처리
                if pd.api.types.is_numeric_dtype(df[df.columns[col]]):
                    try:
                        num_value = float(value)
                        item.setData(Qt.DisplayRole, num_value)
                    except (ValueError, TypeError):
                        item.setData(Qt.DisplayRole, str(value))
                else:
                    # 문자열 데이터 처리
                    str_value = str(value)
                    item.setData(Qt.DisplayRole, str_value)
                
                table.setItem(row, col, item)
        
        # 헤더 설정
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setMinimumHeight(25)
        
        # 행 높이 설정
        table.verticalHeader().setDefaultSectionSize(23)
        
        # 정렬 기능 활성화 (데이터 설정 후)
        table.setSortingEnabled(True)
        
        return table

    def load_excel_data(self):
        try:
            self.add_status_message("Excel 파일 로딩 중...")
            
            # 선택된 날짜로 파일명 생성
            selected_date = self.date_edit.date().toString("yyyyMMdd")
            excel_folder = os.path.join(os.getcwd(), selected_date)
            excel_file = os.path.join(excel_folder, f'total_{selected_date}.xlsx')
            
            # 탭 위젯 초기화
            self.tab_widget.clear()
            self.current_df = None
            
            # 콤보박스 초기화
            self.code_combo.clear()
            self.name_combo.clear()
            self.theme_combo.clear()
            
            if not os.path.exists(excel_folder):
                self.add_status_message(f"오류: 폴더를 찾을 수 없습니다. ({excel_folder})")
                return
                
            if not os.path.exists(excel_file):
                self.add_status_message(f"오류: Excel 파일을 찾을 수 없습니다. ({excel_file})")
                return
            
            excel = pd.ExcelFile(excel_file)
            
            for sheet_name in excel.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                
                # 종목코드 형식 처리
                if '종목코드' in df.columns:
                    df['종목코드'] = df['종목코드'].astype(str).apply(lambda x: x.zfill(6))
                
                self.current_df = df
                self.update_combos(df)
                
                # 테이블 생성 및 데이터 설정
                table = self.create_table_widget(df)
                self.tab_widget.addTab(table, sheet_name)
            
            self.add_status_message(f"Excel 데이터 로드 완료 (총 {len(excel.sheet_names)}개 시트)")
            self.progress_bar.setValue(100)
            
        except Exception as e:
            self.add_status_message(f"Excel 파일 로드 중 오류 발생: {e}")
            self.progress_bar.setValue(0)
            # 에러 발생 시에도 테이블과 콤보박스 초기화
            self.tab_widget.clear()
            self.current_df = None
            self.code_combo.clear()
            self.name_combo.clear()
            self.theme_combo.clear()

    def closeEvent(self, event):
        """프로그램 종료 시 정리 작업"""
        try:
            if self.worker and self.worker.isRunning():
                self.worker.terminate()
                self.worker.wait()
        except Exception as e:
            print(f"프로그램 종료 중 오류 발생: {str(e)}")
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())