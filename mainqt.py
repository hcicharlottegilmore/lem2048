

# CURRENT BEST

# import sys
# import os
# import random
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy
# )
# from PyQt6.QtGui import QPixmap
# from PyQt6.QtCore import Qt

# # 2048 Game Grid Class
# class Grid:
#     def __init__(self, size=4):
#         self.size = size
#         self.cells = self.generate_empty_grid()
#         self.add_random_tile()
#         self.add_random_tile()

#     def generate_empty_grid(self):
#         return [[0] * self.size for _ in range(self.size)]

#     def add_random_tile(self):
#         empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.cells[i][j] == 0]
#         if empty_cells:
#             i, j = random.choice(empty_cells)
#             self.cells[i][j] = 2 if random.random() < 0.9 else 4

#     def move_left(self):
#         for row in self.cells:
#             self.compress(row)
#             self.merge(row)
#             self.compress(row)
#         self.add_random_tile()

#     def move_right(self):
#         for row in self.cells:
#             row.reverse()
#             self.compress(row)
#             self.merge(row)
#             self.compress(row)
#             row.reverse()
#         self.add_random_tile()

#     def move_up(self):
#         self.transpose()
#         self.move_left()
#         self.transpose()

#     def move_down(self):
#         self.transpose()
#         self.move_right()
#         self.transpose()

#     def compress(self, row):
#         new_row = [num for num in row if num != 0] + [0] * (self.size - len([num for num in row if num != 0]))
#         row[:] = new_row

#     def merge(self, row):
#         for i in range(self.size - 1):
#             if row[i] == row[i + 1] and row[i] != 0:
#                 row[i] *= 2
#                 row[i + 1] = 0

#     def transpose(self):
#         self.cells = [list(row) for row in zip(*self.cells)]


# class GameWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.grid = Grid(4)
#         self.initUI()

#     def initUI(self):
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
#         self.labels = [[QLabel(self) for _ in range(4)] for _ in range(4)]
        
#         for i in range(4):
#             row_layout = QHBoxLayout()
#             for j in range(4):
#                 label = self.labels[i][j]
#                 label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#                 label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
#                 row_layout.addWidget(label)
#             self.layout.addLayout(row_layout)

#         self.update_grid()

#     def update_grid(self):
#         for i in range(4):
#             for j in range(4):
#                 value = self.grid.cells[i][j]
#                 self.labels[i][j].setText(str(value) if value != 0 else "")
#                 self.labels[i][j].setStyleSheet(f"background-color: {self.get_color(value)}; font-size: 40px;")

#     def get_color(self, value):
#         colors = {
#             0: "#f2e0cc", 2: "#c2713c", 4: "#3f1233", 8: "#7fff00",
#             16: "#44d0de", 32: "#00ff7f", 64: "#00ffff", 128: "#007fff",
#             256: "#0000ff", 512: "#7f00ff", 1024: "#ff00ff", 2048: "#ff007f"
#         }
#         return colors.get(value, "#ff007f")

#     def move(self, direction):
#         if direction == "left":
#             self.grid.move_left()
#         elif direction == "right":
#             self.grid.move_right()
#         elif direction == "up":
#             self.grid.move_up()
#         elif direction == "down":
#             self.grid.move_down()
#         self.update_grid()


# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Load Map Files
#         self.maps_folder = "maps"
#         self.maps = sorted([os.path.join(self.maps_folder, f) for f in os.listdir(self.maps_folder) if f.endswith((".png", ".jpg"))])
#         self.current_index = -1  # Start at welcome screen

#         self.setWindowTitle("2048 & Maps")
#         self.setGeometry(100, 100, 1000, 600)

#         # Main Layouts
#         self.main_layout = QHBoxLayout(self)

#         # Left Panel (Map Display)
#         self.map_label = QLabel()
#         self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.map_label.setStyleSheet("background-color: white;")
#         self.load_map()

#         # Right Panel (Stacked Widget for Pages)
#         self.right_panel = QStackedWidget()

#         # Create Pages
#         self.pages = [
#             QLabel("WELCOME\nPress SPACE to continue"),
#             QLabel("DETAILED INSTRUCTIONS\n(Read carefully)"),
#             QLabel(),  # Placeholder for 2048 image
#             QLabel("START PAGE\nPress SPACE to begin"),
#             GameWidget(),  # The 2048 game
#             QLabel("THANK YOU\nExperiment completed!")
#         ]

#         # Format pages
#         for page in self.pages:
#             if isinstance(page, QLabel):  # Format text pages
#                 page.setAlignment(Qt.AlignmentFlag.AlignCenter)
#                 page.setStyleSheet("background-color: white; font-size: 30px; color: black;")
#             self.right_panel.addWidget(page)

#         # Load 2048 Image Page
#         self.pages[2].setPixmap(QPixmap("2048_image.png").scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

#         # Add to Main Layout
#         self.main_layout.addWidget(self.map_label, 2)  # Map on Left
#         self.main_layout.addWidget(self.right_panel, 1)  # Pages on Right

#         # Start with welcome screen
#         self.right_panel.setCurrentWidget(self.pages[0])
#         self.map_label.hide()  # Hide the map at the start

#     def load_map(self):
#         """Loads the current map into the left-side QLabel and scales dynamically."""
#         if 0 <= self.current_index < len(self.maps):
#             pixmap = QPixmap(self.maps[self.current_index])
#             self.map_label.setPixmap(pixmap.scaled(
#                 self.map_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))


#     def set_fullscreen_layout(self):
#         """Expands the right panel to fullscreen for non-map/2048 pages."""
#         self.main_layout.setStretchFactor(self.map_label, 0)  # Hide map
#         self.main_layout.setStretchFactor(self.right_panel, 1)  # Right panel takes full width

#     def set_split_layout(self):
#         """Ensures a 50-50 screen split for the map and 2048 game pages."""
#         self.main_layout.setStretchFactor(self.map_label, 1)  # Map takes half
#         self.main_layout.setStretchFactor(self.right_panel, 1)  # Right panel takes half


#     def next_screen(self):
#         """Handles the transitions through pages and ensures layout adapts properly."""
#         current_widget = self.right_panel.currentWidget()

#         if current_widget == self.pages[0]:  # Welcome -> Detailed Instructions
#             self.right_panel.setCurrentWidget(self.pages[1])
#             self.set_fullscreen_layout()

#         elif current_widget == self.pages[1]:  # Instructions -> 2048 Image
#             self.right_panel.setCurrentWidget(self.pages[2])
#             self.set_fullscreen_layout()

#         elif current_widget == self.pages[2]:  # 2048 Image -> Start Page
#             self.right_panel.setCurrentWidget(self.pages[3])
#             self.set_fullscreen_layout()

#         elif current_widget == self.pages[3]:  # Start Page -> Experiment (Maps + 2048)
#             self.current_index = 0  # Move to first map
#             self.load_map()
#             self.right_panel.setCurrentWidget(self.pages[4])
#             self.map_label.show()
#             self.set_split_layout()

#         elif self.current_index < len(self.maps) - 1:  # Map cycle
#             self.current_index += 1
#             self.load_map()

#         else:  # Last map -> Thank You Screen
#             self.right_panel.setCurrentWidget(self.pages[5])
#             self.map_label.hide()
#             self.set_fullscreen_layout()


#     def keyPressEvent(self, event):
#         """Handles key input for navigation and 2048 game movement."""
#         key = event.key()

#         if key == Qt.Key.Key_Space:  
#             self.next_screen()
#         elif self.right_panel.currentWidget() == self.pages[4]:  
#             if key == Qt.Key.Key_Left:
#                 self.pages[4].move("left")
#             elif key == Qt.Key.Key_Right:
#                 self.pages[4].move("right")
#             elif key == Qt.Key.Key_Up:
#                 self.pages[4].move("up")
#             elif key == Qt.Key.Key_Down:
#                 self.pages[4].move("down")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())



















# import sys
# import os
# import random
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy
# )
# from PyQt6.QtGui import QPixmap
# from PyQt6.QtCore import Qt


# # 2048 Game Grid Class
# class Grid:
#     def __init__(self, size=4):
#         self.size = size
#         self.cells = self.generate_empty_grid()
#         self.add_random_tile()
#         self.add_random_tile()

#     def generate_empty_grid(self):
#         return [[0] * self.size for _ in range(self.size)]

#     def add_random_tile(self):
#         empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.cells[i][j] == 0]
#         if empty_cells:
#             i, j = random.choice(empty_cells)
#             self.cells[i][j] = 2 if random.random() < 0.9 else 4

#     def move_left(self):
#         for row in self.cells:
#             self.compress(row)
#             self.merge(row)
#             self.compress(row)
#         self.add_random_tile()

#     def move_right(self):
#         for row in self.cells:
#             row.reverse()
#             self.compress(row)
#             self.merge(row)
#             self.compress(row)
#             row.reverse()
#         self.add_random_tile()

#     def move_up(self):
#         self.transpose()
#         self.move_left()
#         self.transpose()

#     def move_down(self):
#         self.transpose()
#         self.move_right()
#         self.transpose()

#     def compress(self, row):
#         new_row = [num for num in row if num != 0] + [0] * (self.size - len([num for num in row if num != 0]))
#         row[:] = new_row

#     def merge(self, row):
#         for i in range(self.size - 1):
#             if row[i] == row[i + 1] and row[i] != 0:
#                 row[i] *= 2
#                 row[i + 1] = 0

#     def transpose(self):
#         self.cells = [list(row) for row in zip(*self.cells)]


# class GameWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.grid = Grid(4)
#         self.initUI()

#     def initUI(self):
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
#         self.labels = [[QLabel(self) for _ in range(4)] for _ in range(4)]
        
#         for i in range(4):
#             row_layout = QHBoxLayout()
#             for j in range(4):
#                 label = self.labels[i][j]
#                 label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#                 label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
#                 row_layout.addWidget(label)
#             self.layout.addLayout(row_layout)

#         self.update_grid()

#     def update_grid(self):
#         for i in range(4):
#             for j in range(4):
#                 value = self.grid.cells[i][j]
#                 self.labels[i][j].setText(str(value) if value != 0 else "")
#                 self.labels[i][j].setStyleSheet(f"background-color: {self.get_color(value)}; font-size: 40px;")

#     def get_color(self, value):
#         colors = {
#             0: "#f2e0cc", 2: "#c2713c", 4: "#3f1233", 8: "#7fff00",
#             16: "#44d0de", 32: "#00ff7f", 64: "#00ffff", 128: "#007fff",
#             256: "#0000ff", 512: "#7f00ff", 1024: "#ff00ff", 2048: "#ff007f"
#         }
#         return colors.get(value, "#ff007f")

#     def move(self, direction):
#         if direction == "left":
#             self.grid.move_left()
#         elif direction == "right":
#             self.grid.move_right()
#         elif direction == "up":
#             self.grid.move_up()
#         elif direction == "down":
#             self.grid.move_down()
#         self.update_grid()


# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Load Map Files
#         self.maps_folder = "maps"
#         self.maps = sorted([os.path.join(self.maps_folder, f) for f in os.listdir(self.maps_folder) if f.endswith((".png", ".jpg"))])
#         self.current_index = -1  # Start at welcome screen

#         self.setWindowTitle("2048 & Maps")
#         self.setGeometry(100, 100, 1000, 600)

#         # Main Layouts
#         self.main_layout = QHBoxLayout(self)

#         # Left Panel (Map Display)
#         self.map_label = QLabel()
#         self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.map_label.setStyleSheet("background-color: white;")
#         self.load_map()

#         # Right Panel (Stacked Widget for 2048, Blank, Welcome, and Thank You Screens)
#         self.right_panel = QStackedWidget()

#         # Welcome Screen
#         self.welcome_screen = QLabel("WELCOME")
#         self.welcome_screen.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.welcome_screen.setStyleSheet("background-color: white; font-size: 60px; color: black;")
#         self.right_panel.addWidget(self.welcome_screen)

#         # 2048 Game Screen
#         self.game_widget = GameWidget()
#         self.right_panel.addWidget(self.game_widget)

#         # Blank Screen
#         self.blank_widget = QLabel(" ")
#         self.blank_widget.setStyleSheet("background-color: white;")
#         self.right_panel.addWidget(self.blank_widget)

#         # Thank You Screen
#         self.thank_you_screen = QLabel("THANK YOU")
#         self.thank_you_screen.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.thank_you_screen.setStyleSheet("background-color: white; font-size: 60px; color: black;")
#         self.right_panel.addWidget(self.thank_you_screen)

#         # Add to Main Layout
#         self.main_layout.addWidget(self.map_label, 2)  # Map on Left
#         self.main_layout.addWidget(self.right_panel, 1)  # Game on Right

#         # Ensure equal screen split
#         self.main_layout.setStretchFactor(self.map_label, 1)
#         self.main_layout.setStretchFactor(self.right_panel, 1)

#         # Start with welcome screen
#         self.right_panel.setCurrentWidget(self.welcome_screen)
#         self.map_label.hide()  # Hide the map at the start

#     def load_map(self):
#         """Loads the current map into the left-side QLabel and scales dynamically."""
#         if 0 <= self.current_index < len(self.maps):
#             pixmap = QPixmap(self.maps[self.current_index])
#             self.map_label.setPixmap(pixmap.scaled(
#                 self.map_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

#     def next_map(self):
#         """Moves through welcome screen, maps, and thank-you screen in order, hiding map when necessary."""
        
#         if self.current_index == -1:  # If we are at the welcome screen
#             self.current_index = 0  # Move to the first map
#             self.load_map()
#             self.toggle_2048()
#             self.map_label.show()  # Show map again
        
#         elif self.current_index < len(self.maps) - 1:  # Normal map cycle
#             self.current_index += 1
#             self.load_map()
#             self.toggle_2048()
        
#         else:  # If we have reached the last map, show the "Thank You" screen
#             self.current_index = len(self.maps)  # Move past the last map
#             self.right_panel.setCurrentWidget(self.thank_you_screen)
#             self.map_label.hide()  # Hide the map

#     # def toggle_2048(self):
#     #     """Shows 2048 on every other map, otherwise shows a blank screen."""
#     #     if self.current_index % 2 == 0:
#     #         self.right_panel.setCurrentWidget(self.game_widget)
#     #     else:
#     #         self.right_panel.setCurrentWidget(self.blank_widget)

#     def toggle_2048(self):
#         """Shows 2048 on every other map, otherwise shows a blank screen."""
#         if self.current_index % 2 == 0:
#             self.right_panel.setCurrentWidget(self.game_widget)  # Show game on maps 1, 3, 5...
#         else:
#             self.right_panel.setCurrentWidget(self.blank_widget)  # Hide game with blank screen on maps 2, 4...


#     def keyPressEvent(self, event):
#         """Handles arrow key input for 2048 game movement and space bar for next map."""
#         key = event.key()

#         if key == Qt.Key.Key_Space:  # Space bar to switch screens/maps
#             self.next_map()
#         elif self.right_panel.currentWidget() == self.game_widget:
#             if key == Qt.Key.Key_Left:
#                 self.game_widget.move("left")
#             elif key == Qt.Key.Key_Right:
#                 self.game_widget.move("right")
#             elif key == Qt.Key.Key_Up:
#                 self.game_widget.move("up")
#             elif key == Qt.Key.Key_Down:
#                 self.game_widget.move("down")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())











#TESTING  - cover complete, not playable

# import sys
# import os
# import random
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy
# )
# from PyQt6.QtGui import QPixmap
# from PyQt6.QtCore import Qt, QRect

# # 2048 Game Grid Class
# class Grid:
#     def __init__(self, size=4):
#         self.size = size
#         self.cells = self.generate_empty_grid()
#         self.add_random_tile()
#         self.add_random_tile()

#     def generate_empty_grid(self):
#         return [[0] * self.size for _ in range(self.size)]

#     def add_random_tile(self):
#         empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.cells[i][j] == 0]
#         if empty_cells:
#             i, j = random.choice(empty_cells)
#             self.cells[i][j] = 2 if random.random() < 0.9 else 4

#     def move_left(self):
#         for row in self.cells:
#             self.compress(row)
#             self.merge(row)
#             self.compress(row)
#         self.add_random_tile()

#     def move_right(self):
#         for row in self.cells:
#             row.reverse()
#             self.compress(row)
#             self.merge(row)
#             self.compress(row)
#             row.reverse()
#         self.add_random_tile()

#     def move_up(self):
#         self.transpose()
#         self.move_left()
#         self.transpose()

#     def move_down(self):
#         self.transpose()
#         self.move_right()
#         self.transpose()

#     def compress(self, row):
#         new_row = [num for num in row if num != 0] + [0] * (self.size - len([num for num in row if num != 0]))
#         row[:] = new_row

#     def merge(self, row):
#         for i in range(self.size - 1):
#             if row[i] == row[i + 1] and row[i] != 0:
#                 row[i] *= 2
#                 row[i + 1] = 0

#     def transpose(self):
#         self.cells = [list(row) for row in zip(*self.cells)]


# class GameWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.grid = Grid(4)
#         self.initUI()

#     def initUI(self):
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
#         self.labels = [[QLabel(self) for _ in range(4)] for _ in range(4)]
        
#         for i in range(4):
#             row_layout = QHBoxLayout()
#             for j in range(4):
#                 label = self.labels[i][j]
#                 label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#                 label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
#                 row_layout.addWidget(label)
#             self.layout.addLayout(row_layout)

#         # White Overlay (Initially Hidden)
#         self.overlay = QLabel(self)
#         self.overlay.setStyleSheet("background-color: white;")
#         self.overlay.setGeometry(self.rect())  # Ensure it covers the full game area
#         self.overlay.hide()  # Initially hidden

#         self.update_grid()

#     def resizeEvent(self, event):
#         """Resize overlay dynamically with the game widget."""
#         self.overlay.setGeometry(self.rect())

#     def update_grid(self):
#         for i in range(4):
#             for j in range(4):
#                 value = self.grid.cells[i][j]
#                 self.labels[i][j].setText(str(value) if value != 0 else "")
#                 self.labels[i][j].setStyleSheet(f"background-color: {self.get_color(value)}; font-size: 40px;")

#     def get_color(self, value):
#         colors = {
#             0: "#f2e0cc", 2: "#c2713c", 4: "#3f1233", 8: "#7fff00",
#             16: "#44d0de", 32: "#00ff7f", 64: "#00ffff", 128: "#007fff",
#             256: "#0000ff", 512: "#7f00ff", 1024: "#ff00ff", 2048: "#ff007f"
#         }
#         return colors.get(value, "#ff007f")

#     def move(self, direction):
#         if direction == "left":
#             self.grid.move_left()
#         elif direction == "right":
#             self.grid.move_right()
#         elif direction == "up":
#             self.grid.move_up()
#         elif direction == "down":
#             self.grid.move_down()
#         self.update_grid()


# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Load Map Files
#         self.maps_folder = "maps"
#         self.maps = sorted([os.path.join(self.maps_folder, f) for f in os.listdir(self.maps_folder) if f.endswith((".png", ".jpg"))])
#         self.current_index = -1  # Start at welcome screen

#         self.setWindowTitle("2048 & Maps")
#         self.setGeometry(100, 100, 1000, 600)

#         # Main Layouts
#         self.main_layout = QHBoxLayout(self)

#         # Left Panel (Map Display)
#         self.map_label = QLabel()
#         self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.map_label.setStyleSheet("background-color: white;")
#         self.load_map()

#         # Right Panel (Stacked Widget for Pages)
#         self.right_panel = QStackedWidget()

#         # Create Pages
#         self.pages = [
#             QLabel("WELCOME\nPress SPACE to continue"),
#             QLabel("DETAILED INSTRUCTIONS\n(Read carefully)"),
#             QLabel(),  # Placeholder for 2048 image
#             QLabel("START PAGE\nPress SPACE to begin"),
#             GameWidget(),  # The 2048 game
#             QLabel("THANK YOU\nExperiment completed!")
#         ]

#         # Format pages
#         for page in self.pages:
#             if isinstance(page, QLabel):  # Format text pages
#                 page.setAlignment(Qt.AlignmentFlag.AlignCenter)
#                 page.setStyleSheet("background-color: white; font-size: 30px; color: black;")
#             self.right_panel.addWidget(page)

#         # Load 2048 Image Page
#         self.pages[2].setPixmap(QPixmap("2048_image.png").scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

#         # Add to Main Layout
#         self.main_layout.addWidget(self.map_label, 1)  # Map takes half
#         self.main_layout.addWidget(self.right_panel, 1)  # Game takes half

#         # Start with welcome screen
#         self.right_panel.setCurrentWidget(self.pages[0])
#         self.map_label.hide()  # Hide the map at the start

#     def load_map(self):
#         """Loads the current map into the left-side QLabel and scales dynamically."""
#         if 0 <= self.current_index < len(self.maps):
#             pixmap = QPixmap(self.maps[self.current_index])
#             self.map_label.setPixmap(pixmap.scaled(
#                 self.map_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

#     def toggle_overlay(self):
#         """Toggles the overlay for maps 2 and 4 only."""
#         if self.current_index in [1, 3]:  # Map indexes are 0-based
#             self.pages[4].overlay.show()
#         else:
#             self.pages[4].overlay.hide()

#     def next_screen(self):
#         """Handles the transitions through pages and ensures layout adapts properly."""
#         current_widget = self.right_panel.currentWidget()

#         if current_widget == self.pages[0]:  # Welcome -> Detailed Instructions
#             self.right_panel.setCurrentWidget(self.pages[1])
#         elif current_widget == self.pages[1]:  # Instructions -> 2048 Image
#             self.right_panel.setCurrentWidget(self.pages[2])
#         elif current_widget == self.pages[2]:  # 2048 Image -> Start Page
#             self.right_panel.setCurrentWidget(self.pages[3])
#         elif current_widget == self.pages[3]:  # Start Page -> Experiment (Maps + 2048)
#             self.current_index = 0
#             self.load_map()
#             self.right_panel.setCurrentWidget(self.pages[4])
#             self.map_label.show()
#             self.toggle_overlay()
#         elif self.current_index < len(self.maps) - 1:
#             self.current_index += 1
#             self.load_map()
#             self.toggle_overlay()
#         else:
#             self.right_panel.setCurrentWidget(self.pages[5])
#             self.map_label.hide()

#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key.Key_Space:
#             self.next_screen()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())








# game working but overlay behind and no pages

# import sys
# import os
# import random
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy
# )
# from PyQt6.QtGui import QPixmap
# from PyQt6.QtCore import Qt

# # 2048 Game Grid Class
# class Grid:
#     def __init__(self, size=4):
#         self.size = size
#         self.cells = self.generate_empty_grid()
#         self.add_random_tile()
#         self.add_random_tile()

#     def generate_empty_grid(self):
#         return [[0] * self.size for _ in range(self.size)]

#     def add_random_tile(self):
#         empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.cells[i][j] == 0]
#         if empty_cells:
#             i, j = random.choice(empty_cells)
#             self.cells[i][j] = 2 if random.random() < 0.9 else 4

#     def move_left(self):
#         for row in self.cells:
#             self.compress(row)
#             self.merge(row)
#             self.compress(row)
#         self.add_random_tile()

#     def move_right(self):
#         for row in self.cells:
#             row.reverse()
#             self.compress(row)
#             self.merge(row)
#             self.compress(row)
#             row.reverse()
#         self.add_random_tile()

#     def move_up(self):
#         self.transpose()
#         self.move_left()
#         self.transpose()

#     def move_down(self):
#         self.transpose()
#         self.move_right()
#         self.transpose()

#     def compress(self, row):
#         new_row = [num for num in row if num != 0] + [0] * (self.size - len([num for num in row if num != 0]))
#         row[:] = new_row

#     def merge(self, row):
#         for i in range(self.size - 1):
#             if row[i] == row[i + 1] and row[i] != 0:
#                 row[i] *= 2
#                 row[i + 1] = 0

#     def transpose(self):
#         self.cells = [list(row) for row in zip(*self.cells)]


# class GameWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.grid = Grid(4)
#         self.initUI()

#     def initUI(self):
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
#         self.labels = [[QLabel(self) for _ in range(4)] for _ in range(4)]
        
#         for i in range(4):
#             row_layout = QHBoxLayout()
#             for j in range(4):
#                 label = self.labels[i][j]
#                 label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#                 label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
#                 row_layout.addWidget(label)
#             self.layout.addLayout(row_layout)

#         # White Overlay (Initially Hidden)
#         self.overlay = QLabel(self)
#         self.overlay.setStyleSheet("background-color: white;")
#         self.overlay.setGeometry(self.rect())  # Ensure it covers the full game area
#         self.overlay.hide()  # Initially hidden

#         # Ensure overlay does NOT block interaction
#         self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
#         self.overlay.lower()  # Send it to the back

#         self.update_grid()

#     def resizeEvent(self, event):
#         """Resize overlay dynamically with the game widget."""
#         super().resizeEvent(event)  # Ensure QWidget resizes correctly
#         self.overlay.setGeometry(self.rect())  # Adjust overlay size

#     def update_grid(self):
#         for i in range(4):
#             for j in range(4):
#                 value = self.grid.cells[i][j]
#                 self.labels[i][j].setText(str(value) if value != 0 else "")
#                 self.labels[i][j].setStyleSheet(f"background-color: {self.get_color(value)}; font-size: 40px;")

#     def get_color(self, value):
#         colors = {
#             0: "#f2e0cc", 2: "#c2713c", 4: "#3f1233", 8: "#7fff00",
#             16: "#44d0de", 32: "#00ff7f", 64: "#00ffff", 128: "#007fff",
#             256: "#0000ff", 512: "#7f00ff", 1024: "#ff00ff", 2048: "#ff007f"
#         }
#         return colors.get(value, "#ff007f")

#     def move(self, direction):
#         if direction == "left":
#             self.grid.move_left()
#         elif direction == "right":
#             self.grid.move_right()
#         elif direction == "up":
#             self.grid.move_up()
#         elif direction == "down":
#             self.grid.move_down()
#         self.update_grid()


# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Load Map Files
#         self.maps_folder = "maps"
#         self.maps = sorted([os.path.join(self.maps_folder, f) for f in os.listdir(self.maps_folder) if f.endswith((".png", ".jpg"))])
#         self.current_index = -1  # Start at welcome screen

#         self.setWindowTitle("2048 & Maps")
#         self.setGeometry(100, 100, 1000, 600)

#         # Main Layouts
#         self.main_layout = QHBoxLayout(self)

#         # Left Panel (Map Display)
#         self.map_label = QLabel()
#         self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.map_label.setStyleSheet("background-color: white;")
#         self.load_map()

#         # Right Panel (Stacked Widget for Pages)
#         self.right_panel = QStackedWidget()

#         # Create Pages
#         self.pages = [
#             QLabel("WELCOME\nPress SPACE to continue"),
#             QLabel("DETAILED INSTRUCTIONS\n(Read carefully)"),
#             QLabel(),  # Placeholder for 2048 image
#             QLabel("START PAGE\nPress SPACE to begin"),
#             GameWidget(),  # The 2048 game
#             QLabel("THANK YOU\nExperiment completed!")
#         ]

#         # Format pages
#         for page in self.pages:
#             if isinstance(page, QLabel):  # Format text pages
#                 page.setAlignment(Qt.AlignmentFlag.AlignCenter)
#                 page.setStyleSheet("background-color: white; font-size: 30px; color: black;")
#             self.right_panel.addWidget(page)

#         # Load 2048 Image Page
#         self.pages[2].setPixmap(QPixmap("2048_image.png").scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

#         # Add to Main Layout
#         self.main_layout.addWidget(self.map_label, 1)  # Map takes half
#         self.main_layout.addWidget(self.right_panel, 1)  # Game takes half

#         # Start with welcome screen
#         self.right_panel.setCurrentWidget(self.pages[0])
#         self.map_label.hide()  # Hide the map at the start

#     def load_map(self):
#         """Loads the current map into the left-side QLabel and scales dynamically."""
#         if 0 <= self.current_index < len(self.maps):
#             pixmap = QPixmap(self.maps[self.current_index])
#             self.map_label.setPixmap(pixmap.scaled(
#                 self.map_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

#     def toggle_overlay(self):
#         """Toggles the overlay for maps 2 and 4 only."""
#         if self.current_index in [1, 3]:  # Maps are zero-indexed, so 2nd and 4th maps are at index 1 and 3
#             self.pages[4].overlay.show()
#         else:
#             self.pages[4].overlay.hide()

#     def next_screen(self):
#         """Handles screen transitions and updates layout properly."""
#         if self.current_index == -1:  # Start from welcome screen
#             self.current_index = 0
#             self.load_map()
#             self.right_panel.setCurrentWidget(self.pages[4])
#             self.map_label.show()
#             self.toggle_overlay()
#         elif self.current_index < len(self.maps) - 1:
#             self.current_index += 1
#             self.load_map()
#             self.toggle_overlay()
#         else:  # Last map -> Thank You Screen
#             self.right_panel.setCurrentWidget(self.pages[5])
#             self.map_label.hide()

#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key.Key_Space:
#             self.next_screen()
#         elif self.right_panel.currentWidget() == self.pages[4]:
#             if event.key() == Qt.Key.Key_Left:
#                 self.pages[4].move("left")
#             elif event.key() == Qt.Key.Key_Right:
#                 self.pages[4].move("right")
#             elif event.key() == Qt.Key.Key_Up:
#                 self.pages[4].move("up")
#             elif event.key() == Qt.Key.Key_Down:
#                 self.pages[4].move("down")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())









# ALL GOOD BUT NO EXTRA PAGES


import sys
import os
import random
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

        # White Overlay (Initially Hidden)
        self.overlay = QLabel(self)
        self.overlay.setStyleSheet("background-color: white;")
        self.overlay.setGeometry(self.rect())  # Ensure it covers the full game area
        self.overlay.hide()  # Initially hidden

        # Ensure overlay does NOT block interaction
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.overlay.lower()  # Send it to the back

        self.update_grid()

    # def resizeEvent(self, event):
    #     """Resize overlay dynamically with the game widget."""
    #     super().resizeEvent(event)  # Ensure QWidget resizes correctly
    #     self.overlay.setGeometry(self.rect())  # Adjust overlay size
        
    def resizeEvent(self, event):
        """Ensure the overlay resizes dynamically and stays above the game when visible."""
        super().resizeEvent(event)  # Keep normal resizing behavior
        self.overlay.setGeometry(self.rect())  # Update overlay size
        if self.overlay.isVisible():
            self.overlay.raise_()  # Ensure overlay stays on top


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

        # Load Map Files
        self.maps_folder = "maps"
        self.maps = sorted([os.path.join(self.maps_folder, f) for f in os.listdir(self.maps_folder) if f.endswith((".png", ".jpg"))])
        self.current_index = -1  # Start at welcome screen

        self.setWindowTitle("2048 & Maps")
        self.setGeometry(100, 100, 1000, 600)

        # Main Layouts
        self.main_layout = QHBoxLayout(self)

        # Left Panel (Map Display)
        self.map_label = QLabel()
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.map_label.setStyleSheet("background-color: white;")
        self.load_map()

        # Right Panel (Stacked Widget for Pages)
        self.right_panel = QStackedWidget()

        # Create Pages
        self.pages = [
            QLabel("WELCOME\nPress SPACE to continue"),
            QLabel("DETAILED INSTRUCTIONS\n(Read carefully)"),
            QLabel(),  # Placeholder for 2048 image
            QLabel("START PAGE\nPress SPACE to begin"),
            GameWidget(),  # The 2048 game
            QLabel("THANK YOU\nExperiment completed!")
        ]

        # Format pages
        for page in self.pages:
            if isinstance(page, QLabel):  # Format text pages
                page.setAlignment(Qt.AlignmentFlag.AlignCenter)
                page.setStyleSheet("background-color: white; font-size: 30px; color: black;")
            self.right_panel.addWidget(page)

        # Load 2048 Image Page
        self.pages[2].setPixmap(QPixmap("2048_image.png").scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

        # Add to Main Layout
        self.main_layout.addWidget(self.map_label, 1)  # Map takes half
        self.main_layout.addWidget(self.right_panel, 1)  # Game takes half

        # Start with welcome screen
        self.right_panel.setCurrentWidget(self.pages[0])
        self.map_label.hide()  # Hide the map at the start

    def load_map(self):
        """Loads the current map into the left-side QLabel and scales dynamically."""
        if 0 <= self.current_index < len(self.maps):
            pixmap = QPixmap(self.maps[self.current_index])
            self.map_label.setPixmap(pixmap.scaled(
                self.map_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def toggle_overlay(self):
        """Toggles the overlay for maps 2 and 4 only."""
        if self.current_index in [1, 3]:  # Maps are zero-indexed, so 2nd and 4th maps are at index 1 and 3
            self.pages[4].overlay.show()
            self.pages[4].overlay.raise_()  # Bring overlay to the front
        else:
            self.pages[4].overlay.hide()

    def next_screen(self):
        """Handles screen transitions and updates layout properly."""
        if self.current_index == -1:  # Start from welcome screen
            self.current_index = 0
            self.load_map()
            self.right_panel.setCurrentWidget(self.pages[4])
            self.map_label.show()
            self.toggle_overlay()
        elif self.current_index < len(self.maps) - 1:
            self.current_index += 1
            self.load_map()
            self.toggle_overlay()
        else:  # Last map -> Thank You Screen
            self.right_panel.setCurrentWidget(self.pages[5])
            self.map_label.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.next_screen()
        elif self.right_panel.currentWidget() == self.pages[4]:
            if event.key() == Qt.Key.Key_Left:
                self.pages[4].move("left")
            elif event.key() == Qt.Key.Key_Right:
                self.pages[4].move("right")
            elif event.key() == Qt.Key.Key_Up:
                self.pages[4].move("up")
            elif event.key() == Qt.Key.Key_Down:
                self.pages[4].move("down")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
