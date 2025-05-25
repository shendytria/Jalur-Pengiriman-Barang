import tkinter as tk
from tkinter import ttk
import time
from collections import deque
from PIL import Image, ImageTk
import tkinter.font as tkFont

# Data koordinat node dan graf
node_pos = {
    "Gudang": (100, 300), "Jl. Raya Darmo": (250, 200), "Jl. Mayjen Sungkono": (250, 400),
    "Jl. Tunjungan": (400, 150), "Jl. Pemuda": (400, 250), "Jl. Diponegoro": (400, 450),
    "Jl. Basuki Rahmat": (550, 300), "Jl. Embong Malang": (550, 150), "Jl. Panglima Sudirman": (700, 200),
    "Jl. Gubernur Suryo": (700, 400), "Jl. Kertajaya": (300, 100), "Jl. Ngagel": (500, 100),
    "Jl. Dr. Soetomo": (600, 350), "Jl. Walikota Mustajab": (350, 350), "Jl. Kusuma Bangsa": (450, 50),
    "Jl. Arjuno": (200, 500), "Jl. Dipatiukur": (600, 500), "Jl. Simpang Dukuh": (750, 300)
}

graph = {
    "Gudang": ["Jl. Raya Darmo", "Jl. Mayjen Sungkono", "Jl. Arjuno"],
    "Jl. Raya Darmo": ["Gudang", "Jl. Tunjungan", "Jl. Pemuda", "Jl. Kertajaya"],
    "Jl. Mayjen Sungkono": ["Gudang", "Jl. Diponegoro", "Jl. Basuki Rahmat", "Jl. Walikota Mustajab"],
    "Jl. Tunjungan": ["Jl. Raya Darmo", "Jl. Basuki Rahmat", "Jl. Embong Malang", "Jl. Ngagel"],
    "Jl. Pemuda": ["Jl. Raya Darmo", "Jl. Basuki Rahmat", "Jl. Walikota Mustajab"],
    "Jl. Diponegoro": ["Jl. Mayjen Sungkono", "Jl. Basuki Rahmat", "Jl. Dr. Soetomo"],
    "Jl. Basuki Rahmat": ["Jl. Tunjungan", "Jl. Pemuda", "Jl. Diponegoro", "Jl. Panglima Sudirman", "Jl. Dr. Soetomo"],
    "Jl. Embong Malang": ["Jl. Tunjungan", "Jl. Panglima Sudirman", "Jl. Ngagel"],
    "Jl. Panglima Sudirman": ["Jl. Basuki Rahmat", "Jl. Embong Malang", "Jl. Gubernur Suryo", "Jl. Simpang Dukuh"],
    "Jl. Gubernur Suryo": ["Jl. Panglima Sudirman", "Jl. Dr. Soetomo", "Jl. Dipatiukur", "Jl. Simpang Dukuh"],
    "Jl. Kertajaya": ["Jl. Raya Darmo", "Jl. Ngagel", "Jl. Kusuma Bangsa"],
    "Jl. Ngagel": ["Jl. Kertajaya", "Jl. Tunjungan", "Jl. Kusuma Bangsa", "Jl. Embong Malang"],
    "Jl. Dr. Soetomo": ["Jl. Gubernur Suryo", "Jl. Dipatiukur", "Jl. Diponegoro", "Jl. Basuki Rahmat"],
    "Jl. Walikota Mustajab": ["Jl. Pemuda", "Jl. Mayjen Sungkono"],
    "Jl. Kusuma Bangsa": ["Jl. Kertajaya", "Jl. Ngagel"],
    "Jl. Arjuno": ["Gudang", "Jl. Dipatiukur"],
    "Jl. Dipatiukur": ["Jl. Arjuno", "Jl. Gubernur Suryo", "Jl. Dr. Soetomo"],
    "Jl. Simpang Dukuh": ["Jl. Panglima Sudirman", "Jl. Gubernur Suryo"]
}

path_adjustments = {
    ("Jl. Raya Darmo", "Jl. Pemuda"): [(0, 5), (0, -5), "#4B5EAA"],
    ("Jl. Tunjungan", "Jl. Basuki Rahmat"): [(5, 0), (-5, 0), "#4B5EAA"],
    ("Jl. Pemuda", "Jl. Basuki Rahmat"): [(5, 0), (-5, 0), "#4B5EAA"],
    ("Jl. Ngagel", "Jl. Tunjungan"): [(0, 5), (5, 0), "#4B5EAA"],
    ("Jl. Kertajaya", "Jl. Ngagel"): [(5, 0), (-5, 0), "#4B5EAA"],
    ("Jl. Panglima Sudirman", "Jl. Gubernur Suryo"): [(0, 5), (0, -5), "#4B5EAA"],
    ("Jl. Panglima Sudirman", "Jl. Simpang Dukuh"): [(5, 0), (-5, 0), "#4B5EAA"],
    ("Jl. Walikota Mustajab", "Jl. Simpang Dukuh"): [(5, 0), (-5, 0), "#4B5EAA"],
    ("Jl. Dr. Soetomo", "Jl. Walikota Mustajab"): [(0, 5), (0, -5), "#4B5EAA"],
}

def bfs(start, goal):
    queue = deque([[start]])
    visited = set()
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return path
        for neighbor in graph.get(node, []):
            queue.append(path + [neighbor])
    return None

def dfs(start, goal):
    stack = [[start]]
    visited = set()
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    stack.append(new_path)
    return None

class CourierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulasi Kurir Kota")
        self.root.geometry("1000x800")
        self.root.configure(bg="#F3F4F6")

        # Canvas
        self.canvas = tk.Canvas(root, width=1000, height=600, bg="#E5E7EB", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.canvas.create_rectangle(0, 0, 1000, 600, fill="#D1D5DB", outline="")
        self.canvas.create_text(500, 20, text="Peta Kota", font=("Helvetica", 16, "bold"), fill="#1F2937")

        self.current_location = "Gudang"
        self.is_delivery_started = False  # Untuk melacak apakah pengiriman sudah dimulai

        # Control frame
        self.control_frame = tk.Frame(root, bg="#FFFFFF", relief=tk.RAISED, borderwidth=2, highlightbackground="#D1D5DB", highlightthickness=2)
        self.control_frame.pack(pady=10, padx=20, fill=tk.X)

        # Mode selection (Terpisah atau Gabungan)
        self.mode_frame = tk.Frame(self.control_frame, bg="#FFFFFF")
        self.mode_frame.pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(self.mode_frame, text="MODE VISUALISASI:", font=("Helvetica", 12, "bold"), bg="#FFFFFF", fg="#1F2937").pack(side=tk.LEFT)
        self.mode_var = tk.StringVar(value="Terpisah")
        self.mode_dropdown = ttk.Combobox(self.mode_frame, textvariable=self.mode_var, 
                                          values=["Terpisah", "Gabungan"], state="readonly", width=10, font=("Helvetica", 10))
        self.mode_dropdown.pack(side=tk.LEFT, padx=5)

        # Method selection (hanya aktif jika mode Terpisah)
        self.method_frame = tk.Frame(self.control_frame, bg="#FFFFFF")
        self.method_frame.pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(self.method_frame, text="PILIH METODE:", font=("Helvetica", 12, "bold"), bg="#FFFFFF", fg="#1F2937").pack(side=tk.LEFT)
        self.method_var = tk.StringVar(value="BFS")
        self.method_dropdown = ttk.Combobox(self.method_frame, textvariable=self.method_var, 
                                            values=["BFS", "DFS"], state="readonly", width=10, font=("Helvetica", 10))
        self.method_dropdown.pack(side=tk.LEFT, padx=5)

        # Destination (awalnya "Tujuan Awal")
        self.sel_frame1 = tk.Frame(self.control_frame, bg="#FFFFFF")
        self.sel_frame1.pack(side=tk.LEFT, padx=15, pady=5)
        self.destination_label = tk.Label(self.sel_frame1, text="TUJUAN AWAL:", font=("Helvetica", 12, "bold"), bg="#FFFFFF", fg="#1F2937")
        self.destination_label.pack(side=tk.LEFT)
        self.destination_var = tk.StringVar()
        self.dropdown = ttk.Combobox(self.sel_frame1, textvariable=self.destination_var, 
                                     values=list(node_pos.keys()), state="readonly", width=20, font=("Helvetica", 10))
        self.dropdown.pack(side=tk.LEFT, padx=5)
        self.dropdown.set("Pilih Tujuan")

        # Buttons
        self.btn_frame = tk.Frame(self.control_frame, bg="#FFFFFF")
        self.btn_frame.pack(side=tk.LEFT, padx=20, pady=5)
        self.start_button = tk.Button(self.btn_frame, text="MULAI PENGIRIMAN", command=self.start_delivery,
                                      bg="#10B981", fg="white", font=("Helvetica", 10, "bold"), relief=tk.FLAT, padx=20, pady=10,
                                      activebackground="#059669", bd=0, highlightthickness=0)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.continue_button = tk.Button(self.btn_frame, text="LANJUTKAN PERJALANAN", command=self.continue_to_new_destination,
                                         bg="#3B82F6", fg="white", font=("Helvetica", 10, "bold"), relief=tk.FLAT, padx=20, pady=10,
                                         state=tk.DISABLED, activebackground="#2563EB", bd=0, highlightthickness=0)
        self.continue_button.pack(side=tk.LEFT, padx=5)

        self.home_button = tk.Button(self.btn_frame, text="KEMBALI KE GUDANG", command=self.return_home,
                                     bg="#EF4444", fg="white", font=("Helvetica", 10, "bold"), relief=tk.FLAT, padx=20, pady=10,
                                     state=tk.DISABLED, activebackground="#DC2626", bd=0, highlightthickness=0)
        self.home_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.btn_frame, text="RESET SEMUA", command=self.reset_courier,
                                      bg="#6B7280", fg="white", font=("Helvetica", 10, "bold"), relief=tk.FLAT, padx=20, pady=10,
                                      activebackground="#4B5563", bd=0, highlightthickness=0)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Status frame
        self.status_frame = tk.Frame(root, bg="#FFFFFF", relief=tk.RAISED, borderwidth=2, highlightbackground="#D1D5DB", highlightthickness=2)
        self.status_frame.pack(pady=5, padx=20, fill=tk.X)
        self.status_label = tk.Label(self.status_frame, text="Status: Kurir siap di Gudang", font=("Helvetica", 12), bg="#FFFFFF", fg="#1F2937", anchor="w")
        self.status_label.pack(side=tk.LEFT, padx=10)
        self.location_label = tk.Label(self.status_frame, text="Lokasi Saat Ini: Gudang", font=("Helvetica", 12, "bold"), bg="#FFFFFF", fg="#2563EB", anchor="e")
        self.location_label.pack(side=tk.RIGHT, padx=10)

        # Journey log
        self.log_frame = tk.Frame(root, bg="#FFFFFF", relief=tk.RAISED, borderwidth=2, highlightbackground="#D1D5DB", highlightthickness=2)
        self.log_frame.pack(pady=5, padx=20, fill=tk.X)
        tk.Label(self.log_frame, text="Riwayat Perjalanan:", font=("Helvetica", 12, "bold"), bg="#FFFFFF", fg="#1F2937").pack(anchor="w", padx=10, pady=2)
        self.journey_log = tk.Text(self.log_frame, height=5, width=80, font=("Helvetica", 10), bg="#F9FAFB", fg="#1F2937", relief=tk.FLAT, borderwidth=2)
        self.journey_log.pack(padx=10, pady=5, fill=tk.X)
        self.journey_log.insert(tk.END, "Gudang")
        self.journey_log.config(state=tk.DISABLED)

        self.tooltip = None
        self.load_images()
        self.draw_map()

        x, y = node_pos["Gudang"]
        self.kurir = self.canvas.create_image(x, y, image=self.courier_img, tags="kurir")
        self.path_lines = []
        self.path_glows = []
        self.journey_history = ["Gudang"]

    def load_images(self):
        try:
            self.courier_img = self.create_svg_motorcycle_rider(40, 40)
            self.house_img = self.create_svg_house_with_items(50, 50)
        except Exception as e:
            print(f"Error loading images: {e}")
            self.courier_img = None
            self.house_img = None

    def create_svg_motorcycle_rider(self, width, height):
        img = tk.PhotoImage(width=width, height=height)
        for y in range(height//2, height-8):
            for x in range(8, width-10):
                if 0 <= x < width and 0 <= y < height:
                    img.put("#1E40AF", (x, y))
        for y in range(5, height//2):
            for x in range(width//3, 2*width//3):
                if 0 <= x < width and 0 <= y < height:
                    img.put("#F97316", (x, y))
        for y in range(2, 12):
            for x in range(width//2-6, width//2+6):
                if 0 <= x < width and 0 <= y < height:
                    img.put("#FBBF24", (x, y))
        for y in range(height//3, height//2):
            for x in range(width-12, width-2):
                if 0 <= x < width and 0 <= y < height:
                    img.put("#7C2D12", (x, y))
        wheel_centers = [(12, height-8), (width-12, height-8)]
        for cx, cy in wheel_centers:
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    if dx*dx + dy*dy <= 25 and 0 <= cx + dx < width and 0 <= cy + dy < height:
                        img.put("#111827", (cx + dx, cy + dy))
        return img

    def create_svg_house_with_items(self, width, height):
        img = tk.PhotoImage(width=width, height=height)
        wall_color = "#FCD34D"
        roof_color = "#DC2626"
        door_color = "#1E3A8A"
        window_frame = "#FFFFFF"
        window_pane = "#60A5FA"
        package_color = "#92400E"
        grass_color = "#34C759"
        
        for y in range(4*height//5, height):
            for x in range(width):
                if 0 <= x < width and 0 <= y < height:
                    img.put(grass_color, (x, y))
        wall_top, wall_bottom = height//3, 4*height//5
        wall_left, wall_right = width//6, 5*width//6
        for y in range(wall_top, wall_bottom):
            for x in range(wall_left, wall_right):
                if 0 <= x < width and 0 <= y < height:
                    img.put(wall_color, (x, y))
        roof_peak = height//8
        for y in range(roof_peak, wall_top):
            roof_width = (y - roof_peak) * 2
            for x in range(width//2 - roof_width, width//2 + roof_width):
                if wall_left <= x < wall_right and 0 <= x < width and 0 <= y < height:
                    img.put(roof_color, (x, y))
        door_width, door_height = width//6, height//4
        door_x, door_y = width//2 - door_width//2, wall_bottom - door_height
        for y in range(door_y, wall_bottom):
            for x in range(door_x, door_x + door_width):
                if 0 <= x < width and 0 <= y < height:
                    img.put(door_color, (x, y))
        window_width, window_height = width//8, height//8
        window_positions = [(wall_left + 10, wall_top + 10), (wall_right - window_width - 10, wall_top + 10)]
        for wx, wy in window_positions:
            for y in range(wy, wy + window_height):
                for x in range(wx, wx + window_width):
                    if 0 <= x < width and 0 <= y < height:
                        img.put(window_pane, (x, y))
            for y in range(wy-2, wy + window_height + 2):
                for x in range(wx-2, wx + window_width + 2):
                    if (y in (wy-2, wy + window_height + 1) or x in (wx-2, wx + window_width + 1)) and 0 <= x < width and 0 <= y < height:
                        img.put(window_frame, (x, y))
        package_width, package_height = width//8, height//10
        for y in range(wall_bottom - package_height, wall_bottom):
            for x in range(wall_right + 5, wall_right + 5 + package_width):
                if 0 <= x < width and 0 <= y < height:
                    img.put(package_color, (x, y))
        return img

    def draw_map(self):
        drawn_paths = set()
        for node, neighbors in graph.items():
            x1, y1 = node_pos[node]
            for neighbor in neighbors:
                if (node, neighbor) not in drawn_paths and (neighbor, node) not in drawn_paths:
                    x2, y2 = node_pos[neighbor]
                    key = (node, neighbor)
                    reverse_key = (neighbor, node)
                    if key in path_adjustments:
                        (off_x1, off_y1), (off_x2, off_y2), color = path_adjustments[key]
                        self.canvas.create_line(x1 + off_x1, y1 + off_y1, x2 + off_x2, y2 + off_y2, 
                                                fill=color, width=10, smooth=True, capstyle=tk.ROUND)
                        self.canvas.create_line(x1 + off_x1, y1 + off_y1, x2 + off_x2, y2 + off_y2, 
                                                fill="#FCD34D", width=2, dash=(5, 5))
                    elif reverse_key in path_adjustments:
                        (off_x2, off_y2), (off_x1, off_y1), color = path_adjustments[reverse_key]
                        self.canvas.create_line(x1 + off_x1, y1 + off_y1, x2 + off_x2, y2 + off_y2, 
                                                fill=color, width=10, smooth=True, capstyle=tk.ROUND)
                        self.canvas.create_line(x1 + off_x1, y1 + off_y1, x2 + off_x2, y2 + off_y2, 
                                                fill="#FCD34D", width=2, dash=(5, 5))
                    else:
                        self.canvas.create_line(x1, y1, x2, y2, fill="#4B5EAA", width=10, capstyle=tk.ROUND)
                        self.canvas.create_line(x1, y1, x2, y2, fill="#FCD34D", width=2, dash=(5, 5))
                    drawn_paths.add((node, neighbor))
                    drawn_paths.add((neighbor, node))
        for node, pos in node_pos.items():
            x, y = pos
            if node == "Gudang":
                if self.house_img:
                    self.canvas.create_image(x, y, image=self.house_img)
            else:
                self.canvas.create_oval(x-12, y-12, x+12, y+12, fill="#60A5FA", outline="#1E3A8A", width=2)
                self.canvas.create_oval(x-8, y-8, x+8, y+8, fill="#93C5FD", outline="")
            self.canvas.create_text(x, y+30, text=node, font=("Helvetica", 10, "bold"), fill="#1F2937")

    def draw_combined_paths(self, bfs_route=None, dfs_route=None):
        for line in self.path_lines:
            self.canvas.delete(line)
        for glow in self.path_glows:
            self.canvas.delete(glow)
        self.path_lines = []
        self.path_glows = []

        if bfs_route:
            bfs_coords = []
            for node in bfs_route:
                x, y = node_pos[node]
                bfs_coords.extend([x, y])
            self.path_glows.append(self.canvas.create_line(bfs_coords, fill="#FCD34D", width=8, dash=(4, 4), capstyle=tk.ROUND))
            self.path_lines.append(self.canvas.create_line(bfs_coords, fill="#10B981", width=5, capstyle=tk.ROUND, joinstyle=tk.ROUND))

        if dfs_route:
            dfs_coords = []
            for node in dfs_route:
                x, y = node_pos[node]
                dfs_coords.extend([x, y])
            self.path_glows.append(self.canvas.create_line(dfs_coords, fill="#FCD34D", width=8, dash=(4, 4), capstyle=tk.ROUND))
            self.path_lines.append(self.canvas.create_line(dfs_coords, fill="#EF4444", width=5, capstyle=tk.ROUND, joinstyle=tk.ROUND))

    def animate_courier(self, route, method_name, callback=None):
        route_coords = []
        for node in route:
            x, y = node_pos[node]
            route_coords.extend([x, y])
        route_text = f"{method_name}: " + " → ".join(route)
        self.status_label.config(text=f"Rute {route_text}")
        self.disable_buttons()
        for i in range(len(route) - 1):
            start_x, start_y = node_pos[route[i]]
            end_x, end_y = node_pos[route[i + 1]]
            steps = 40
            self.status_label.config(text=f"Bergerak ({method_name}) dari {route[i]} ke {route[i+1]}")
            for j in range(steps):
                new_x = start_x + (end_x - start_x) * j / steps
                new_y = start_y + (end_y - start_y) * j / steps
                self.canvas.coords(self.kurir, new_x, new_y)
                glow = self.canvas.create_oval(new_x-10, new_y-10, new_x+10, new_y+10, fill="#F97316", outline="", tags="glow")
                self.root.update()
                time.sleep(0.02)
                self.canvas.delete(glow)
        self.current_location = route[-1]
        self.location_label.config(text=f"Lokasi Saat Ini: {self.current_location}")
        for node in route[1:]:
            if node not in self.journey_history or self.journey_history[-1] != node:
                self.journey_history.append(node)
        self.status_label.config(text=f"Kurir sampai di {route[-1]} ({method_name})!")
        self.enable_buttons()
        # Ubah label dropdown menjadi "Tujuan Berikutnya" setelah animasi selesai
        if self.current_location != "Gudang":
            self.destination_label.config(text="TUJUAN BERIKUTNYA:")
        if callback:
            self.root.after(500, callback)

    def update_journey_log(self, bfs_route=None, dfs_route=None):
        self.journey_log.config(state=tk.NORMAL)
        self.journey_log.delete(1.0, tk.END)
        if bfs_route and dfs_route:
            bfs_text = "BFS: " + " → ".join(bfs_route) + "\n"
            dfs_text = "DFS: " + " → ".join(dfs_route) + "\n"
            self.journey_log.insert(tk.END, bfs_text + dfs_text + "\nMengikuti jalur BFS")
        else:
            log_text = " → ".join(self.journey_history)
            self.journey_log.insert(tk.END, log_text)
        self.journey_log.config(state=tk.DISABLED)

    def reset_courier(self):
        x, y = node_pos["Gudang"]
        self.canvas.coords(self.kurir, x, y)
        for line in self.path_lines:
            self.canvas.delete(line)
        for glow in self.path_glows:
            self.canvas.delete(glow)
        self.path_lines = []
        self.path_glows = []
        self.current_location = "Gudang"
        self.is_delivery_started = False
        self.location_label.config(text=f"Lokasi Saat Ini: {self.current_location}")
        self.journey_history = ["Gudang"]
        self.update_journey_log()
        self.dropdown.set("Pilih Tujuan")
        self.destination_label.config(text="TUJUAN AWAL:")  # Kembalikan label ke "Tujuan Awal"
        self.enable_buttons()
        self.status_label.config(text="Status: Kurir siap di Gudang")

    def get_search_method(self):
        method = self.method_var.get()
        return bfs if method == "BFS" else dfs

    def start_delivery(self):
        destination = self.destination_var.get()
        if destination == "Pilih Tujuan" or destination == self.current_location:
            self.status_label.config(text="Pilih tujuan yang berbeda dari lokasi saat ini!")
            return

        mode = self.mode_var.get()
        if mode == "Gabungan":
            bfs_route = bfs("Gudang", destination)
            dfs_route = dfs("Gudang", destination)
            if not bfs_route or not dfs_route:
                self.status_label.config(text=f"Tidak ada rute dari Gudang ke {destination}!")
                return
            self.draw_combined_paths(bfs_route, dfs_route)
            self.update_journey_log(bfs_route, dfs_route)
            self.animate_courier(bfs_route, "BFS")
            self.is_delivery_started = True
        else:
            search_method = self.get_search_method()
            route = search_method("Gudang", destination)
            if route:
                self.draw_combined_paths(route if self.method_var.get() == "BFS" else None, 
                                         route if self.method_var.get() == "DFS" else None)
                self.animate_courier(route, self.method_var.get())
                self.is_delivery_started = True
            else:
                self.status_label.config(text=f"Tidak ada rute dari Gudang ke {destination}!")

    def continue_to_new_destination(self):
        destination = self.destination_var.get()  # Gunakan dropdown yang sama
        if destination == "Pilih Tujuan" or destination == self.current_location:
            self.status_label.config(text="Pilih tujuan yang berbeda dari lokasi saat ini!")
            return

        mode = self.mode_var.get()
        if mode == "Gabungan":
            bfs_route = bfs(self.current_location, destination)
            dfs_route = dfs(self.current_location, destination)
            if not bfs_route or not dfs_route:
                self.status_label.config(text=f"Tidak ada rute dari {self.current_location} ke {destination}!")
                return
            self.draw_combined_paths(bfs_route, dfs_route)
            self.update_journey_log(bfs_route, dfs_route)
            self.animate_courier(bfs_route, "BFS")
        else:
            search_method = self.get_search_method()
            route = search_method(self.current_location, destination)
            if route:
                self.draw_combined_paths(route if self.method_var.get() == "BFS" else None, 
                                         route if self.method_var.get() == "DFS" else None)
                self.animate_courier(route, self.method_var.get())
            else:
                self.status_label.config(text=f"Tidak ada rute dari {self.current_location} ke {destination}!")

    def return_home(self):
        if self.current_location != "Gudang":
            mode = self.mode_var.get()
            if mode == "Gabungan":
                bfs_route = bfs(self.current_location, "Gudang")
                dfs_route = dfs(self.current_location, "Gudang")
                if not bfs_route or not dfs_route:
                    self.status_label.config(text="Tidak ada rute kembali ke Gudang!")
                    return
                self.draw_combined_paths(bfs_route, dfs_route)
                self.update_journey_log(bfs_route, dfs_route)
                self.animate_courier(bfs_route, "BFS", self.delivery_completed)
            else:
                search_method = self.get_search_method()
                route = search_method(self.current_location, "Gudang")
                if route:
                    self.draw_combined_paths(route if self.method_var.get() == "BFS" else None, 
                                             route if self.method_var.get() == "DFS" else None)
                    self.animate_courier(route, self.method_var.get(), self.delivery_completed)
                else:
                    self.status_label.config(text="Tidak ada rute kembali ke Gudang!")
        else:
            self.status_label.config(text="Kurir sudah di Gudang!")

    def delivery_completed(self):
        self.status_label.config(text="Pengiriman selesai! Kurir kembali ke Gudang.")
        self.destination_label.config(text="TUJUAN AWAL:")  # Kembalikan label ke "Tujuan Awal"
        self.is_delivery_started = False
        self.enable_buttons()

    def disable_buttons(self):
        self.start_button.config(state=tk.DISABLED)
        self.continue_button.config(state=tk.DISABLED)
        self.home_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)

    def enable_buttons(self):
        self.reset_button.config(state=tk.NORMAL)
        if self.current_location == "Gudang":
            self.start_button.config(state=tk.NORMAL)
            self.continue_button.config(state=tk.DISABLED)
            self.home_button.config(state=tk.DISABLED)
        else:
            self.start_button.config(state=tk.DISABLED)
            self.continue_button.config(state=tk.NORMAL)
            self.home_button.config(state=tk.NORMAL)

root = tk.Tk()
app = CourierApp(root)
root.mainloop()