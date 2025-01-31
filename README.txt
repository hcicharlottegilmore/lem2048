Documentation for 2048/Maps Program


This program integrates a 2048 game with a sequence of map images. 
It presents different screens to the user, guiding them through an experiment that includes 
displaying maps and allowing interaction with the 2048 game at specific points.

The following software and libraries are required:

- Python 3 (Recommended version: 3.11 or later)

Libraries: 
- `PyQt6` (for GUI )
- `sys`
- `os` 
- `random` 


The program consists of the file mainqt.py. No other scripts are required to run it - 
testing.py is simply there as alternative/ testing versions for me, and the "game" folder was for a previous version. 

Ensure that these files and folders are accessible as well, in the main folder:
- Maps Folder (`maps/`)
- `2048_image.png`


The program runs through a series of initial pages with instructions for the subject on what the experiment will entail. 
Then there are the map/ 2048 pages, where users can interact with the 2048 game on certain pages and not on others.
For the 2048 game, movement is controlled using arrow keys. 

Users progress through these pages using the SPACE key and can use the Q key to go back. 

To run program: 
python mainqt.py


