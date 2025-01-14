# import tkinter as tk
# from tkinter import messagebox
# from PIL import Image, ImageTk
# import os

# # Function to display the current map
# def show_map(map_file):
#     try:
#         image = Image.open(map_file)
#         image = image.resize((400, 400))  # Resize map for display
#         photo = ImageTk.PhotoImage(image)
#         map_label.config(image=photo)
#         map_label.image = photo  # Keep reference to avoid garbage collection
#     except Exception as e:
#         messagebox.showerror("Error", f"Could not load map: {e}")

# # Function to display the 2048 game or blank space
# def update_screen():
#     current_map = maps[current_index]
#     show_map(current_map)

#     # Check if the map should show the 2048 game
#     if current_map in game_maps:
#         game_label.config(text="2048 Game Here!")
#         # Insert 2048 game logic here (e.g., call a start_game() function)
#     else:
#         game_label.config(text="")

# # Function to go to the next map
# def next_map():
#     global current_index
#     current_index = (current_index + 1) % len(maps)  # Cycle through maps
#     update_screen()

# # Function to go to the previous map
# def previous_map():
#     global current_index
#     current_index = (current_index - 1) % len(maps)  # Cycle backward
#     update_screen()

# # Initialize the main window
# root = tk.Tk()
# root.title("Maps and 2048")
# root.geometry("800x500")

# # Map and 2048 game areas
# map_label = tk.Label(root, bg="gray", width=50, height=25)
# map_label.grid(row=0, column=1, padx=10, pady=10)

# game_label = tk.Label(root, bg="white", width=50, height=25, text="")
# game_label.grid(row=0, column=0, padx=10, pady=10)

# # Navigation buttons
# button_frame = tk.Frame(root)
# button_frame.grid(row=1, column=1, pady=10)

# prev_button = tk.Button(button_frame, text="Previous", command=previous_map)
# prev_button.pack(side=tk.LEFT, padx=5)

# next_button = tk.Button(button_frame, text="Next", command=next_map)
# next_button.pack(side=tk.LEFT, padx=5)

# # List of maps
# maps_folder = "maps"  # Folder where maps are stored
# maps = [os.path.join(maps_folder, f) for f in os.listdir(maps_folder) if f.endswith(('.jpg', '.png'))]
# game_maps = ["maps/map_with_game.jpg"]  # Maps where the 2048 game should appear
# current_index = 0

# # Start with the first map
# update_screen()

# # Start the main loop
# root.mainloop()




import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Function to display the current map
def show_map(map_file):
    try:
        image = Image.open(map_file)
        # Get the current size of the map_label widget
        label_width = map_label.winfo_width()
        label_height = map_label.winfo_height()
        # Resize the image to fit the widget
        image = image.resize((label_width, label_height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        map_label.config(image=photo)
        map_label.image = photo  # Keep reference to avoid garbage collection
    except Exception as e:
        messagebox.showerror("Error", f"Could not load map: {e}")

# Function to display the 2048 game or blank space
# def update_screen():
#     current_map = maps[current_index]
#     show_map(current_map)

#     # Check if the map should show the 2048 game
#     if current_map in game_maps:
#         # Render the 2048 game dynamically in the left pane
#         for widget in game_label.winfo_children():
#             widget.destroy()  # Clear previous content
#         grid = Grid(4)  # Create a 4x4 game grid
#         panel = GamePanel(grid)
#         game = Game(grid, panel)

#         # Embed the game panel in the left pane
#         panel.background.pack(in_=game_label)
#         game.add_start_cells()
#         panel.paint()
#     else:
        # Reset the left pane to a blank placeholder
        game_label.config(text="No game here.")
        game_label.pack()


def update_screen():
    current_map = maps[current_index]
    show_map(current_map)

    # Check if the map should show the 2048 game
    if current_map in game_maps:
        # Render the 2048 game dynamically in the left pane
        for widget in game_label.winfo_children():
            widget.destroy()  # Clear previous content
        grid = Grid(4)  # Create a 4x4 game grid
        panel = GamePanel(grid)
        game = Game(grid, panel)

        # Embed the game panel in the left pane
        panel.background.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        game.add_start_cells()
        panel.paint()
    else:
        # Reset the left pane to a blank placeholder
        for widget in game_label.winfo_children():
            widget.destroy()  # Clear any existing widgets
        blank_label = tk.Label(game_label, text="No game here.", bg="white")
        blank_label.grid(row=0, column=0, padx=10, pady=10)


# Function to go to the next map
def next_map():
    global current_index
    current_index = (current_index + 1) % len(maps)  # Cycle through maps
    update_screen()

# Function to go to the previous map
def previous_map():
    global current_index
    current_index = (current_index - 1) % len(maps)  # Cycle backward
    update_screen()

# Initialize the main window
root = tk.Tk()
root.title("Maps and 2048")
root.geometry("800x500")

# Map and 2048 game areas
map_label = tk.Label(root, bg="gray", width=400, height=400)
map_label.grid(row=0, column=1, padx=10, pady=10)

game_label = tk.Label(root, bg="white", width=400, height=400)
game_label.grid(row=0, column=0, padx=10, pady=10)

# Navigation buttons
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=1, pady=10)

prev_button = tk.Button(button_frame, text="Previous", command=previous_map)
prev_button.pack(side=tk.LEFT, padx=5)

next_button = tk.Button(button_frame, text="Next", command=next_map)
next_button.pack(side=tk.LEFT, padx=5)

# List of maps
maps_folder = "maps"  # Folder where maps are stored
maps = [os.path.join(maps_folder, f) for f in os.listdir(maps_folder) if f.endswith(('.jpg', '.png'))]
game_maps = ["maps/map_with_game.jpg"]  # Maps where the 2048 game should appear
current_index = 0

# Handle empty or invalid maps
if not maps:
    messagebox.showerror("Error", "No valid maps found in the 'maps' folder.")
    root.quit()

# Start with the first map
update_screen()

# Update on window resize
root.bind('<Configure>', lambda event: update_screen())

# Start the main loop
root.mainloop()
