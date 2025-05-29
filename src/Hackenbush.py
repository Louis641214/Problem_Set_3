import tkinter as tk
import random


class Segment:
    def __init__(self, canvas, x1, y1, x2, y2, id):
        self.canvas = canvas
        self.id = id
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.rect = canvas.create_line(x1, y1, x2, y2, width=3, fill='green')
        self.node1 = canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill='black')
        self.node2 = canvas.create_oval(x2 - 3, y2 - 3, x2 + 3, y2 + 3, fill='black')
        self.connected = True

    def remove(self):
        self.canvas.delete(self.rect)
        self.canvas.delete(self.node1)
        self.canvas.delete(self.node2)


class HackenbushGame:
    def __init__(self, window, player1, player2):
        self.window = window
        self.window.title('Hackenbush Game')
        self.window.geometry('800x600')
        self.window.resizable(False, False)

        self.players = [player1, player2]
        self.current_player_index = random.choice([0, 1])

        self.canvas = tk.Canvas(self.window, bg='white', width=800, height=500)
        self.canvas.pack(pady=10)

        self.message = tk.Label(self.window, text='')
        self.message.pack()

        self.end_button = tk.Button(self.window, text='End Game', command=self.window.destroy)

        self.segments = {}
        self.connections = {}

        self.create_structure_with_loops_without_overlapping()
        self.update_message()

    def create_structure_with_loops_without_overlapping(self):
        seg_id = 0
        base_y = 480
        total_segments = random.randint(13, 20)
        layer_height = 50
        max_width = 700
        start_x = 50

        base_x = start_x + max_width // 2
        self.segments[seg_id] = Segment(self.canvas, base_x, base_y, base_x, base_y - layer_height, seg_id)
        self.connections[seg_id] = []
        last_layer = [seg_id]
        seg_id += 1

        layers = []
        layers.append(last_layer)
        created_segments = [0]
        positions = {0: base_x}
        used_pairs = set()

        while seg_id < int(total_segments * 0.8):
            new_layer = []
            num_positions = len(last_layer) * 2
            x_spacing = max_width // (num_positions + 1)
            x_positions = [start_x + x_spacing * (i + 1) for i in range(num_positions)]

            pos_index = 0
            for parent_id in last_layer:
                num_children = random.randint(1, 2)
                for _ in range(num_children):
                    if seg_id >= int(total_segments * 0.8) or pos_index >= len(x_positions):
                        break
                    x0, y0 = positions[parent_id], self.canvas.coords(self.segments[parent_id].rect)[3]
                    x1 = x_positions[pos_index]
                    y1 = y0 - layer_height
                    pos_index += 1

                    self.segments[seg_id] = Segment(self.canvas, x0, y0, x1, y1, seg_id)
                    self.connections[parent_id].append(seg_id)
                    self.connections[seg_id] = []
                    new_layer.append(seg_id)
                    created_segments.append(seg_id)
                    positions[seg_id] = x1
                    seg_id += 1

            if not new_layer:
                break
            last_layer = new_layer
            layers.append(new_layer)

        extra_links = total_segments - seg_id
        added = 0
        attempts = 0
        while added < extra_links and attempts < 500:
            a, b = random.sample(created_segments, 2)
            pair_key = tuple(sorted((a, b)))
            if a != b and pair_key not in used_pairs and b not in self.connections[a]:
                if abs(positions[a] - positions[b]) > 60:
                    cross = False
                    for seg in self.segments.values():
                        if self.lines_cross((positions[a], self.canvas.coords(self.segments[a].rect)[3],
                                             positions[b], self.canvas.coords(self.segments[b].rect)[3]),
                                            (seg.x1, seg.y1, seg.x2, seg.y2)):
                            cross = True
                            break
                    if not cross:
                        loop_seg = Segment(self.canvas, positions[a], self.canvas.coords(self.segments[a].rect)[3],
                                           positions[b], self.canvas.coords(self.segments[b].rect)[3], seg_id)
                        self.segments[seg_id] = loop_seg
                        self.connections[a].append(seg_id)
                        self.connections[b].append(seg_id)
                        self.connections[seg_id] = [a, b]
                        used_pairs.add(pair_key)
                        seg_id += 1
                        added += 1
            attempts += 1

        self.canvas.bind('<Button-1>', self.on_click)

    def lines_cross(self, line1, line2):
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

        A = (line1[0], line1[1])
        B = (line1[2], line1[3])
        C = (line2[0], line2[1])
        D = (line2[2], line2[3])

        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    def on_click(self, event):
        clicked = self.find_segment(event.x, event.y)
        if clicked is not None:
            self.remove_segment(clicked)
            self.check_floating()
            if not self.has_moves():
                self.message.config(text=f'{self.players[self.current_player_index]} wins!')
                self.end_button.pack(pady=10)
            else:
                self.current_player_index = 1 - self.current_player_index
                self.update_message()

    def find_segment(self, x, y):
        for seg_id, seg in self.segments.items():
            if self.canvas.find_withtag('current') and seg.connected:
                current = self.canvas.find_withtag('current')[0]
                if seg.rect == current:
                    return seg_id
        return None

    def remove_segment(self, seg_id):
        self.segments[seg_id].remove()
        self.segments[seg_id].connected = False

    def check_floating(self):
        connected = set()

        def dfs(node):
            connected.add(node)
            for child in self.connections.get(node, []):
                if self.segments[child].connected and child not in connected:
                    dfs(child)

        if self.segments[0].connected:
            dfs(0)

        for seg_id, seg in self.segments.items():
            if seg.connected and seg_id not in connected:
                seg.remove()
                seg.connected = False

    def has_moves(self):
        return any(seg.connected for seg in self.segments.values())

    def update_message(self):
        self.message.config(text=f"{self.players[self.current_player_index]}'s turn")
