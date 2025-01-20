

import sys
import os
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# 2048 Game Grid
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

# 2048 Game Widget
class GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = Grid(4)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.labels = [[QLabel(self) for _ in range(4)] for _ in range(4)]
        for row in self.labels:
            row_layout = QHBoxLayout()
            for label in row:
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setFixedSize(100, 100)
                row_layout.addWidget(label)
            self.layout.addLayout(row_layout)
        self.update_grid()

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.grid.cells[i][j]
                self.labels[i][j].setText(str(value) if value != 0 else "")
                self.labels[i][j].setStyleSheet(f"background-color: {self.get_color(value)}; font-size: 20px;")

    def get_color(self, value):
        colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#3c3a32")

    def keyPressEvent(self, event):
        """Handle arrow key input for game movement"""
        key = event.key()
        if key == Qt.Key.Key_Left:
            self.grid.move_left()
        elif key == Qt.Key.Key_Right:
            self.grid.move_right()
        elif key == Qt.Key.Key_Up:
            self.grid.move_up()
        elif key == Qt.Key.Key_Down:
            self.grid.move_down()
        self.update_grid()

# Main Application Window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Load Map Files
        self.maps_folder = "maps"
        self.maps = sorted([os.path.join(self.maps_folder, f) for f in os.listdir(self.maps_folder) if f.endswith((".png", ".jpg"))])
        self.current_index = 0

        self.setWindowTitle("2048 & Maps")
        self.setGeometry(100, 100, 1000, 600)

        # Main Layouts
        self.main_layout = QHBoxLayout(self)

        # Left Panel (Map Display)
        self.map_label = QLabel()
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.load_map()

        # Right Panel (Stacked Widget for 2048 or Blank)
        self.right_panel = QStackedWidget()
        self.game_widget = GameWidget()  # 2048 Game
        self.blank_widget = QLabel(" ")
        self.blank_widget.setStyleSheet("background-color: white;")
        self.right_panel.addWidget(self.game_widget)
        self.right_panel.addWidget(self.blank_widget)

        # Add to Main Layout
        self.main_layout.addWidget(self.map_label, 2)  # Map on Left
        self.main_layout.addWidget(self.right_panel, 1)  # Game on Right

        # Buttons Layout
        self.buttons_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.buttons_layout.addWidget(self.prev_button)
        self.buttons_layout.addWidget(self.next_button)

        # Fullscreen Button
        self.fullscreen_button = QPushButton("Toggle Fullscreen")
        self.buttons_layout.addWidget(self.fullscreen_button)

        # Bottom Layout
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.addLayout(self.main_layout)
        self.bottom_layout.addLayout(self.buttons_layout)
        self.setLayout(self.bottom_layout)

        # Button Actions
        self.prev_button.clicked.connect(self.prev_map)
        self.next_button.clicked.connect(self.next_map)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

    def load_map(self):
        """Loads the current map into the left-side QLabel."""
        if self.maps:
            pixmap = QPixmap(self.maps[self.current_index])
            self.map_label.setPixmap(pixmap.scaled(self.map_label.width(), self.map_label.height(), Qt.AspectRatioMode.KeepAspectRatio))

    def next_map(self):
        """Cycles through maps and toggles 2048 every other map."""
        self.current_index = (self.current_index + 1) % len(self.maps)
        self.load_map()
        self.toggle_2048()

    def prev_map(self):
        """Cycles backward through maps and toggles 2048 every other map."""
        self.current_index = (self.current_index - 1) % len(self.maps)
        self.load_map()
        self.toggle_2048()

    def toggle_2048(self):
        """Shows 2048 on every other map, otherwise shows a blank screen."""
        if self.current_index % 2 == 0:
            self.right_panel.setCurrentWidget(self.game_widget)
        else:
            self.right_panel.setCurrentWidget(self.blank_widget)

    def toggle_fullscreen(self):
        """Toggles fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

