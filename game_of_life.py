import tkinter as tk
import random as r
import copy

class Application(tk.Frame):
    """Game of Life simulation.
    """
    def __init__(self, master = tk.Tk()):
        super().__init__(master)
        self.master = master
        self.grid_data = None
        self.new_window = None
        self.starvation_condition = 0
        self.overpopulation_condition = 0
        self.birth_condition = 0
        self.set_menu()

    def set_menu(self):
        """Set items in menu bar.
        """
        menubar = tk.Menu(self.master)

        # File menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.display_new)
        filemenu.add_command(label="Exit", command=self.master.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        # Edit menu
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Step forward 1 time", command=self.simulate_step)
        # editmenu.add_command(label="Step forward X times", command=self.do_nothing)
        menubar.add_cascade(label="Edit", menu=editmenu)

        self.master.config(menu=menubar)

    def display_new(self):
        """Display dialog asking user for necessary information to create new simulations
        """
        if self.new_window is None or not self.new_window.top.winfo_exists():
            self.new_window = NewSettingsWindow(self)
        else:
            self.new_window.top.lift(self.master)

    def get_new_parameters(self):
        """Get new parameters input from new simulation setting window.
        """
        # Get parameters
        size = self.new_window.size_entry.get()
        survival_chance = self.new_window.survival_entry.get()
        self.starvation_condition = self.new_window.starvation_entry.get()
        self.overpopulation_condition = self.new_window.overpopulation_entry.get()
        self.birth_condition = self.new_window.birth_entry.get()

        # Validate inputs
        try:
            size = int(size)
            survival_chance = float(survival_chance)
            self.starvation_condition = int(self.starvation_condition)
            self.overpopulation_condition = int(self.overpopulation_condition)
            self.birth_condition = int(self.birth_condition)
        except ValueError:
            return

        # Generate grid data
        self.grid_data = self.generate_starting_map(size, size, survival_chance)
        self.display_grid(self.grid_data)

        # Destroy popup window
        self.new_window.master.destroy()
        self.new_window = None

    def display_grid(self, grid_data):
        """Display grid in main window.

        Arguments:
            grid_data {[boolean]} -- Grid data
        """
        for r in range(len(grid_data)):
            grid_row = grid_data[r]
            for c in range(len(grid_row)):
                # Set background color based on value
                background_color = None
                if grid_data[r][c] is True:
                    background_color = "white"
                else:
                    background_color = "black"

                frame = tk.Frame(self.master, background=background_color, width=10, height=10)
                frame.grid(row=r,column=c)

    def generate_starting_map(self, width, length, survival_chance):
        """Generate starting map
        
        Returns:
            [Array] -- Starting map
        """
        map = []
        for line in range(length):
            map_line = []
            for cell in range(width):
                if r.random() <= survival_chance:
                    map_line.append(True)
                else:
                    map_line.append(False)
            map.append(map_line)
        return map

    def count_living_neighbours(self, map, x, y):
        """Count living neighbours
        
        Arguments:
            map [Array] -- Cell map,
            x [int] -- x position,
            y [int] -- y position
        
        Returns:
            [int] -- Living neighbours count
        """
        count = 0
        length = len(map)
        width = len(map[0])

        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbour_x = x + i
                neighbour_y = y + j

                # Skip middle
                if i is 0 and j is 0:
                    continue

                # Skip edge cases
                if neighbour_x < 0 or neighbour_y < 0:
                    continue
                if neighbour_x >= width or neighbour_y >= length:
                    continue

                count += 1

        return count

    def simulate_step(self):
        """Simulate single step (cells live and die)
        
        Returns:
            [Array] -- New cell map
        """
        old_map = self.grid_data
        new_map = copy.deepcopy(old_map)

        if (old_map is None):
            return

        for y in range(len(old_map)):
            for x in range(len(old_map[y])):
                living_neighbours = self.count_living_neighbours(old_map, x, y)
                cell = old_map[y][x]
                
                # if living cell
                if cell is True:
                    # if cell has fewer living neighbours than starvation condition, it dies
                    if living_neighbours < self.starvation_condition:
                        print("starve")
                        new_map[y][x] = False
                    # if cell has more living neighbours than overpopulation condition, it dies
                    elif living_neighbours > self.overpopulation_condition:
                        print("overpopulation")
                        new_map[y][x] = False
                    # else survives
                    else:
                        new_map[y][x] = True

                # if dead cell
                else:
                    # if cell has same number of living neighbours as birth condition, it becomes alive
                    if living_neighbours is self.birth_condition:
                        print("birth")
                        new_map[y][x] = True
                    # else stays dead
                    else:
                        new_map[y][x] = False

        self.grid_data = new_map
        self.display_grid(new_map)

class NewSettingsWindow():
    """Display popup window used to generate a new simulation.
    """
    def __init__(self, application):
        self.main_window = application
        self.master = tk.Toplevel()
        self.master.title("New")

        # Size
        size_label = tk.Label(self.master, text="Size")
        size_label.grid(row=0, column=0)
        self.size_entry = tk.Entry(self.master)
        self.size_entry.grid(row=0, column=1)

        # Survival chance
        survival_label = tk.Label(self.master, text="Survival chance")
        survival_label.grid(row=1, column=0)
        self.survival_entry = tk.Entry(self.master)
        self.survival_entry.grid(row=1, column=1)

        # Starvation condition
        starvation_label = tk.Label(self.master, text="Starvation condition")
        starvation_label.grid(row=2, column=0)
        self.starvation_entry = tk.Entry(self.master)
        self.starvation_entry.grid(row=2, column=1)

        # Overpopulation condition
        overpopulation_label = tk.Label(self.master, text="Overpopulation condition")
        overpopulation_label.grid(row=3, column=0)
        self.overpopulation_entry = tk.Entry(self.master)
        self.overpopulation_entry.grid(row=3, column=1)

        # Birth condition
        birth_label = tk.Label(self.master, text="Birth condition")
        birth_label.grid(row=4, column=0)
        self.birth_entry = tk.Entry(self.master)
        self.birth_entry.grid(row=4, column=1)

        # Submit
        submit_button = tk.Button(self.master, text ="Generate", command = self.main_window.get_new_parameters)
        submit_button.grid(row=5, column=1)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
