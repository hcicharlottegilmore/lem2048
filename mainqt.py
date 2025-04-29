


import sys
import os
import random
import csv
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# 2048 Game Grid Class
class Grid:
    def __init__(self, size=4):
        self.size = size
        self.cells = self.generate_empty_grid()
        self.add_random_tile()
        self.add_random_tile()

    def generate_empty_grid(self):
        return [[0] * self.size for _ in range(self.size)]

    def add_random_tile(self):
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.cells[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.cells[i][j] = 2 if random.random() < 0.9 else 4

    def move_left(self):
        for row in self.cells:
            self.compress(row)
            self.merge(row)
            self.compress(row)
        self.add_random_tile()

    def move_right(self):
        for row in self.cells:
            row.reverse()
            self.compress(row)
            self.merge(row)
            self.compress(row)
            row.reverse()
        self.add_random_tile()

    def move_up(self):
        self.transpose()
        self.move_left()
        self.transpose()

    def move_down(self):
        self.transpose()
        self.move_right()
        self.transpose()

    def compress(self, row):
        new_row = [num for num in row if num != 0] + [0] * (self.size - len([num for num in row if num != 0]))
        row[:] = new_row

    def merge(self, row):
        for i in range(self.size - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0

    def transpose(self):
        self.cells = [list(row) for row in zip(*self.cells)]


class GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = Grid(4)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.labels = [[QLabel(self) for _ in range(4)] for _ in range(4)]

        for i in range(4):
            row_layout = QHBoxLayout()
            for j in range(4):
                label = self.labels[i][j]
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                row_layout.addWidget(label)
            self.layout.addLayout(row_layout)

        self.overlay = QLabel(self)
        self.overlay.setStyleSheet("background-color: white;")
        self.overlay.setGeometry(self.rect())
        self.overlay.hide()
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.overlay.lower()

        self.update_grid()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay.setGeometry(self.rect())
        if self.overlay.isVisible():
            self.overlay.raise_()

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.grid.cells[i][j]
                self.labels[i][j].setText(str(value) if value != 0 else "")
                self.labels[i][j].setStyleSheet(f"background-color: {self.get_color(value)}; font-size: 40px;")

    def get_color(self, value):
        colors = {
            0: "#f2e0cc", 2: "#c2713c", 4: "#3f1233", 8: "#7fff00",
            16: "#44d0de", 32: "#00ff7f", 64: "#00ffff", 128: "#007fff",
            256: "#0000ff", 512: "#7f00ff", 1024: "#ff00ff", 2048: "#ff007f"
        }
        return colors.get(value, "#ff007f")

    def move(self, direction):
        if direction == "left":
            self.grid.move_left()
        elif direction == "right":
            self.grid.move_right()
        elif direction == "up":
            self.grid.move_up()
        elif direction == "down":
            self.grid.move_down()
        self.update_grid()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.maps_folder = "maps"
        self.maps = sorted([os.path.join(self.maps_folder, f) for f in os.listdir(self.maps_folder) if f.endswith((".png", ".jpg"))])
        self.current_index = -1

        self.trial_conditions = ['blind'] * 3 + ['2048'] * 3
        random.shuffle(self.trial_conditions)

        with open("trial_assignments.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['trial_index', 'condition'])
            for i, cond in enumerate(self.trial_conditions):
                writer.writerow([i, cond])

        self.setWindowTitle("2048 & Maps")
        self.setGeometry(100, 100, 1000, 600)

        self.main_layout = QHBoxLayout(self)
        self.map_label = QLabel()
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.map_label.setStyleSheet("background-color: white;")
        self.right_panel = QStackedWidget()

        self.pages = [
            QLabel("WELCOME\nPress SPACE to continue"),
            QLabel("DETAILED INSTRUCTIONS\n(Read carefully)\nIn this experiment, you are the LISTENER,\nand your partner is the SPEAKER \nYou will be shown a series of maps adjacent to a 2048 game.\nThis game is playable only during select \nportions of the study.\nOtherwise it will be blank.\nYour objective is to successfully complete \nboth the MAP TASK and the GAME TASK. \nPlease press space to continue."),
            QLabel("In the MAP TASK, you will be conversing \nwith your partner, who will give you directions \nto a specified point on the map. \nYou are both given maps of the same locations, \nwith some slight differences. \nYou will need to communicate with your partner \nto understand how to reach the destination point. \nPlease press space to continue. "),
            QLabel("In the 2048 GAME TASK, your goal is \nto combine numbered tiles to create \nthe tile 2048. Use the arrow keys (\u2190 \u2191 \u2192 \u2193) \nto slide all tiles in the chosen direction. \nWhen two tiles with the same number \ncollide, they merge into one tile \nwith a value equal to their sum. \nEach move introduces a new tile (either 2 or 4) \nat a random empty position on the board. \nAn example will be provided. \nPlease press space to continue. "),
            QLabel(),
            QLabel("START PAGE\nPress SPACE to begin"),
            GameWidget(),
            QLabel("THANK YOU\nExperiment completed!")
        ]

        for page in self.pages:
            if isinstance(page, QLabel):
                page.setAlignment(Qt.AlignmentFlag.AlignCenter)
                page.setStyleSheet("background-color: white; font-size: 30px; color: black;")
            self.right_panel.addWidget(page)

        self.pages[4].setPixmap(QPixmap("2048_image.png").scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio))

        self.main_layout.addWidget(self.map_label, 2)
        self.main_layout.addWidget(self.right_panel, 1)
        self.right_panel.setCurrentWidget(self.pages[0])
        self.map_label.hide()

    def showEvent(self, event):
        super().showEvent(event)
        if self.current_index == 0 and self.map_label.pixmap() is None:
            self.load_map()

    def load_map(self):
        if 0 <= self.current_index < len(self.maps):
            pixmap = QPixmap(self.maps[self.current_index])
            self.map_label.setPixmap(pixmap.scaled(
                self.map_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def toggle_overlay(self):
        if isinstance(self.pages[6], GameWidget) and 0 <= self.current_index < len(self.trial_conditions):
            if self.trial_conditions[self.current_index] == 'blind':
                self.pages[6].overlay.show()
                self.pages[6].overlay.raise_()
            else:
                self.pages[6].overlay.hide()

    def set_fullscreen_layout(self):
        self.main_layout.setStretchFactor(self.map_label, 0)
        self.main_layout.setStretchFactor(self.right_panel, 1)

    def set_split_layout(self):
        self.main_layout.setStretchFactor(self.map_label, 1)
        self.main_layout.setStretchFactor(self.right_panel, 1)

    def next_screen(self):
        current_widget = self.right_panel.currentWidget()

        if current_widget == self.pages[0]:
            self.right_panel.setCurrentWidget(self.pages[1])
            self.set_fullscreen_layout()
        elif current_widget == self.pages[1]:
            self.right_panel.setCurrentWidget(self.pages[2])
            self.set_fullscreen_layout()
        elif current_widget == self.pages[2]:
            self.right_panel.setCurrentWidget(self.pages[3])
            self.set_fullscreen_layout()
        elif current_widget == self.pages[3]:
            self.right_panel.setCurrentWidget(self.pages[4])
            self.set_fullscreen_layout()
        elif current_widget == self.pages[4]:
            self.right_panel.setCurrentWidget(self.pages[5])
            self.set_fullscreen_layout()
        elif current_widget == self.pages[5]:
            self.current_index = 0
            self.load_map()
            self.right_panel.setCurrentWidget(self.pages[6])
            self.map_label.show()
            self.set_split_layout()
            self.toggle_overlay()
        elif self.current_index < len(self.maps) - 1:
            self.current_index += 1
            self.load_map()
            self.toggle_overlay()
        else:
            self.right_panel.setCurrentWidget(self.pages[7])
            self.map_label.hide()
            self.set_fullscreen_layout()

    def previous_screen(self):
        current_widget = self.right_panel.currentWidget()

        if current_widget == self.pages[0]:
            return
        elif current_widget == self.pages[1]:
            self.right_panel.setCurrentWidget(self.pages[0])
            self.set_fullscreen_layout()
        elif current_widget == self.pages[2]:
            self.right_panel.setCurrentWidget(self.pages[1])
            self.set_fullscreen_layout()
        elif current_widget == self.pages[3]:
            self.right_panel.setCurrentWidget(self.pages[2])
            self.set_fullscreen_layout()
        elif current_widget == self.pages[4]:
            self.right_panel.setCurrentWidget(self.pages[3])
            self.set_fullscreen_layout()
        elif current_widget == self.pages[5]:
            self.right_panel.setCurrentWidget(self.pages[4])
            self.set_fullscreen_layout()
        elif current_widget == self.pages[6]:
            self.right_panel.setCurrentWidget(self.pages[5])
            self.set_fullscreen_layout()
        elif current_widget == self.pages[7]:
            self.right_panel.setCurrentWidget(self.pages[6])
            self.set_split_layout()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.next_screen()
        elif event.key() == Qt.Key.Key_Q:
            self.previous_screen()
        elif self.right_panel.currentWidget() == self.pages[6]:
            if event.key() == Qt.Key.Key_Left:
                self.pages[6].move("left")
            elif event.key() == Qt.Key.Key_Right:
                self.pages[6].move("right")
            elif event.key() == Qt.Key.Key_Up:
                self.pages[6].move("up")
            elif event.key() == Qt.Key.Key_Down:
                self.pages[6].move("down")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
