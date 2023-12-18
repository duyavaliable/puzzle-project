import tkinter as tk
from tkinter import ttk
from queue import PriorityQueue

class PuzzleNode:
    def __init__(self, state, moves=0, prev=None):
        self.state = state
        self.moves = moves
        self.prev = prev

    def __lt__(self, other):
        return self.moves < other.moves

class SlidingPuzzleSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.rows = len(puzzle)
        self.cols = len(puzzle[0])
        self.goal_state = tuple(range(1, self.rows * self.cols)) + (0,)

    def get_neighbors(self, node):
        neighbors = []
        zero_idx = node.state.index(0)
        zero_row, zero_col = zero_idx // self.cols, zero_idx % self.cols

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dr, dc in directions:
            new_row, new_col = zero_row + dr, zero_col + dc

            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                new_idx = new_row * self.cols + new_col
                new_state = list(node.state)
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                neighbors.append(PuzzleNode(tuple(new_state), node.moves + 1, node))

        return neighbors

    def solve(self):
        start_node = PuzzleNode(self.flatten(self.puzzle))
        visited = set()
        pq = PriorityQueue()
        pq.put(start_node)

        while not pq.empty():
            current_node = pq.get()

            if current_node.state == self.goal_state:
                return self.construct_path(current_node)

            if current_node.state in visited:
                continue

            visited.add(current_node.state)

            for neighbor in self.get_neighbors(current_node):
                if neighbor.state not in visited:
                    pq.put(neighbor)

        return None

    def flatten(self, puzzle):
        return tuple(cell for row in puzzle for cell in row)

    def construct_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.prev
        return path[::-1]

class PuzzleSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle Solver")

        self.puzzle = [[0 for _ in range(3)] for _ in range(3)]
        self.goal_state = tuple(range(1, 3 * 3)) + (0,)

        self.create_input_widgets()
        self.create_buttons()

    def create_input_widgets(self):
        self.entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = tk.Entry(self.root, width=8, font=('Arial', 14))  # Increase width and font size
                entry.grid(row=i, column=j)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def display_solution(self, solution_path):
        solution_window = tk.Toplevel(self.root)
        solution_window.title("Solution Steps")

        canvas = tk.Canvas(solution_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(solution_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        solution_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=solution_frame, anchor=tk.NW)

        for step, state in enumerate(solution_path):
            label = tk.Label(solution_frame, text=f"Step {step}:", font=('Arial', 12, 'bold'))  # Increase font size
            label.pack()
            for row in range(0, len(self.puzzle)):
                row_data = ' '.join(map(str, state[row * len(self.puzzle): row * len(self.puzzle) + len(self.puzzle)]))
                tk.Label(solution_frame, text=row_data, font=('Arial', 12)).pack()  # Increase font size
            tk.Label(solution_frame, text="").pack()

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width=400, height=400)  # Adjusted size

        solution_frame.bind("<Configure>", on_frame_configure)

    def create_buttons(self):
        start_button = tk.Button(self.root, text="Start", command=self.start_solving)
        start_button.grid(row=3, column=0)

        stop_button = tk.Button(self.root, text="Stop", command=self.stop_solving)
        stop_button.grid(row=3, column=1)

    def get_puzzle_input(self):
        for i in range(3):
            for j in range(3):
                try:
                    self.puzzle[i][j] = int(self.entries[i][j].get())
                except ValueError:
                    self.puzzle[i][j] = 0

    def start_solving(self):
        self.get_puzzle_input()

        solver = SlidingPuzzleSolver(self.puzzle)
        solution_path = solver.solve()

        if solution_path:
            self.display_solution(solution_path)
        else:
            print("No solution found!")

    def stop_solving(self):
        # Implement logic to stop solving midway if possible
        pass

    def display_solution(self, solution_path):
        solution_window = tk.Toplevel(self.root)
        solution_window.title("Solution Steps")

        canvas = tk.Canvas(solution_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(solution_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        solution_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=solution_frame, anchor=tk.NW)

        for step, state in enumerate(solution_path):
            label = tk.Label(solution_frame, text=f"Step {step}:")
            label.pack()
            for row in range(0, len(self.puzzle)):
                row_data = ' '.join(map(str, state[row * len(self.puzzle): row * len(self.puzzle) + len(self.puzzle)]))
                tk.Label(solution_frame, text=row_data).pack()
            tk.Label(solution_frame, text="").pack()

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width=300, height=300)

        solution_frame.bind("<Configure>", on_frame_configure)

    def flatten(self, puzzle):
        return tuple(cell for row in puzzle for cell in row)

def main():
    root = tk.Tk()
    app = PuzzleSolverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()