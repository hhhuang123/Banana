import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLabel, 
    QSizePolicy, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QSize, QTimer, QElapsedTimer

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from random import randint


class ContributionWidget(QWidget):
    def __init__(self, date, contributions):
        super().__init__()
        self.date = date
        self.contributions = contributions
        self.setToolTip(f"Date: {self.date.strftime('%Y-%m-%d')}\LearningTime: {self.contributions * 10} m")
    
    def get_contributions(self):
        return self.contributions

    def sizeHint(self):
        return QSize(20, 20)  # Return the preferred size, but it will be overridden by layout resizing

    def paintEvent(self, event):
        painter = QPainter(self)
        color = self.get_color_based_on_contributions(self.contributions)
        painter.fillRect(self.rect(), color)

    def get_color_based_on_contributions(self, contributions):
        # contributions range: [0-20]
        if contributions > 20:
            contributions = 20
        return QColor(235 - contributions * 10, 237, 240 - contributions * 10)
    
    def update_contributions(self, contributions):
        self.contributions = contributions
        self.setToolTip(f"Date: {self.date.strftime('%Y-%m-%d')}\nLearningTime: {self.contributions * 10} m")
        self.update()


class ContributionCalendar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = None
        self.widgets = dict() # date -> ContributionWidget
        self.contributions_data = dict() # date -> contribution
        self.setWindowTitle('Contribution Calendar')
        self.setGeometry(100, 100, 1500, 200)  # Adjust the initial size as needed
        self.initUI()
        self.initTimer()
        # 程序计时器
        self.programTimer = QElapsedTimer()
        self.programTimer.start()

    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__update_contributions)
        self.timer.start(1000) # 10s更新一次

    def __update_contributions(self):
        now = datetime.now().date()
        cnt = self.contributions_data.get(now, 0) + self.__convert_time_to_cnt()
        self.widgets[now].update_contributions(cnt)
        self.__dumps_data()

    def __convert_time_to_cnt(self) -> int:
        return int(self.programTimer.elapsed() / 1000 / 10)

    def __get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout with vertical and horizontal box layouts to keep the calendar centered
        main_vbox = QVBoxLayout(central_widget)
        main_hbox = QHBoxLayout()
        main_hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 这玩意会定期更新的
        self.contributions_data = self.generate_contributions_data()

        # Calendar layout that will contain all the month and day widgets
        calendar_layout = QGridLayout()
        calendar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        calendar_layout.setHorizontalSpacing(3)  # 设置水平间距

        # 初始化日历布局：计算一年前的日期
        one_year_ago = datetime.now() - relativedelta(years=1)
        months_list = [(one_year_ago + relativedelta(months=+i)).date() for i in range(1, 13)]
        horizontal_position = 0 # 月份格子水平布局位置
        for date in months_list:
            horizontal_position += 1
            # Each month has its own grid layout
            month_layout = QGridLayout()

            # 设置小方块之间的距离
            month_layout.setHorizontalSpacing(3)  # 设置水平间距
            month_layout.setVerticalSpacing(3)    # 设置垂直间距

            # Add month label
            month_name = date.strftime('%B')
            month_label = QLabel(f'{month_name}')
            month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            month_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            month_layout.addWidget(month_label, 0, 0, 1, 7)  # Span the label across all days of the week

            # Calculate days in month and start weekday
            month_date = datetime(date.year, date.month, 1)
            next_month = month_date.replace(day=28) + timedelta(days=4)
            days_in_month = (next_month - timedelta(days=next_month.day)).day
            start_day = month_date.weekday()

            for day in range(days_in_month):
                day_date = month_date + timedelta(days=day)
                contributions = self.contributions_data.get(day_date.date(), 0)
                widget = ContributionWidget(day_date, contributions)
                col = (day + start_day) // 7 + 1  # Calculate row
                row = (day + start_day) % 7 +1 # Calculate column
                month_layout.addWidget(widget, row, col)
                self.widgets[day_date.date()] = widget
            # Add month grid to the calendar grid
            calendar_layout.addLayout(month_layout, 1, horizontal_position - 1, 1, 1)
        main_hbox.addLayout(calendar_layout)
        main_vbox.addLayout(main_hbox)
        central_widget.setLayout(main_vbox)

    def generate_contributions_data(self):
        json_file_path = self.__get_resource_path("data\data.json")
        history_data = dict()
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                for data_str, contributions in data.items():
                    date = datetime.strptime(data_str, '%Y-%m-%d').date()
                    history_data[date] = contributions
        except Exception as e:
            print(f"UPDATE CONTRIBUTIONS: {e}")
        else:
            return history_data

    def __dumps_data(self):
        _d = dict()
        for date, contribution_widget in self.widgets.items():
            _d[str(date)] = contribution_widget.get_contributions()
        json_file_path = self.__get_resource_path("data\data.json")
        with open(json_file_path, 'w') as f:
            json.dump(_d, f, indent=4)
        

def main():
    app = QApplication(sys.argv)
    ex = ContributionCalendar()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
