import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from main import Proccess , node

# assume your Proccess class is already imported here
# from your_module import Proccess, node


class SocialGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Social Network GUI")
        self.geometry("1200x750")
        self.minsize(1100, 700)

        self.proc = None
        self.file_path = None

        self._build_ui()

    def _build_ui(self):
        # top bar
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Button(top, text="Open TXT", command=self.load_file).pack(side="left", padx=5)
        self.file_label = ttk.Label(top, text="No file loaded")
        self.file_label.pack(side="left", padx=10)

        # main notebook
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabs = {}
        for name in [
            "Friends",
            "Same Group",
            "Shortest Path",
            "Friend Suggestion",
            "Groups",
            "Popular Person",
            "Intersection",
            "Network Data",
            "BFS"
        ]:
            frame = ttk.Frame(self.nb, padding=10)
            self.nb.add(frame, text=name)
            self.tabs[name] = frame

        self._friends_tab()
        self._same_group_tab()
        self._shortest_path_tab()
        self._friend_suggestion_tab()
        self._groups_tab()
        self._popular_tab()
        self._intersection_tab()
        self._network_tab()
        self._bfs_tab()

    def load_file(self):
        path = filedialog.askopenfilename(
            title="Select text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            self.file_path = path
            with open(path, "r") as f:
                self.proc = Proccess(f)
            self.file_label.config(text=path)
            self.clear_all_outputs()
            messagebox.showinfo("Loaded", "File loaded and processed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_all_outputs(self):
        for var in [
            getattr(self, "friends_out", None),
            getattr(self, "group_out", None),
            getattr(self, "path_out", None),
            getattr(self, "suggest_out", None),
            getattr(self, "groups_out", None),
            getattr(self, "popular_out", None),
            getattr(self, "intersection_out", None),
            getattr(self, "network_out", None),
            getattr(self, "bfs_out", None),
        ]:
            if var is not None:
                var.config(state="normal")
                var.delete("1.0", "end")
                var.config(state="disabled")

        if hasattr(self, "canvas"):
            self.canvas.delete("all")

    def make_entry_row(self, parent, labels):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=5)
        entries = []
        for text in labels:
            ttk.Label(row, text=text).pack(side="left", padx=(0, 5))
            e = ttk.Entry(row, width=22)
            e.pack(side="left", padx=5)
            entries.append(e)
        return row, entries

    def ensure_proc(self):
        if self.proc is None:
            messagebox.showwarning("No data", "Please load a TXT file first.")
            return False
        return True

    def node_from_name(self, name):
        return node(name.strip())

    def write_output(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", text)
        widget.config(state="disabled")

    # 1) Friends
    def _friends_tab(self):
        frame = self.tabs["Friends"]
        _, entries = self.make_entry_row(frame, ["User name:"])
        self.friends_name = entries[0]
        ttk.Button(frame, text="Show Friends", command=self.show_friends).pack(pady=8)

        self.friends_out = tk.Text(frame, height=18, wrap="word")
        self.friends_out.pack(fill="both", expand=True)

    def show_friends(self):
        if not self.ensure_proc():
            return
        u = self.node_from_name(self.friends_name.get())
        if u not in self.proc.g:
            messagebox.showerror("Error", "User not found.")
            return
        friends = self.proc.g[u]
        if type(friends) is not set:text = f"\n{friends.name}" or "No friends found."
        else:text = "\n".join(sorted([x.name for x in friends])) or "No friends found."
        self.write_output(self.friends_out, text)
  # 3) same group
    def _same_group_tab(self):
        frame = self.tabs["Same Group"]
        _, entries = self.make_entry_row(frame, ["User A:", "User B:"])
        self.grp_a, self.grp_b = entries
        ttk.Button(frame, text="Check Group", command=self.check_group).pack(pady=8)

        self.group_out = tk.Text(frame, height=18, wrap="word")
        self.group_out.pack(fill="both", expand=True)

    def check_group(self):
        if not self.ensure_proc():
            return
        a = self.node_from_name(self.grp_a.get())
        b = self.node_from_name(self.grp_b.get())
        groups = self.proc.group()

        found = False
        for g in groups:
            if a in g and b in g:
                found = True
                break

        self.write_output(self.group_out, str(found))

    # 4) shortest path
    def _shortest_path_tab(self):
        frame = self.tabs["Shortest Path"]
        _, entries = self.make_entry_row(frame, ["Start:", "Stop:"])
        self.sp_a, self.sp_b = entries
        ttk.Button(frame, text="Find Shortest Path", command=self.show_path).pack(pady=8)

        self.path_out = tk.Text(frame, height=18, wrap="word")
        self.path_out.pack(fill="both", expand=True)

    def show_path(self):
        if not self.ensure_proc():
            return
        a = self.node_from_name(self.sp_a.get())
        b = self.node_from_name(self.sp_b.get())
        try:
            path = self.proc.path(a, b)
            names = [x.name for x in reversed(path)]
            self.write_output(self.path_out, " -> ".join(names))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # 5) find_friend
    def _friend_suggestion_tab(self):
        frame = self.tabs["Friend Suggestion"]
        _, entries = self.make_entry_row(frame, ["User name:"])
        self.sug_name = entries[0]
        ttk.Button(frame, text="Suggest Friends", command=self.show_suggestions).pack(pady=8)

        self.suggest_out = tk.Text(frame, height=18, wrap="word")
        self.suggest_out.pack(fill="both", expand=True)

    def show_suggestions(self):
        if not self.ensure_proc():
            return
        u = self.node_from_name(self.sug_name.get())
        if u not in self.proc.g:
            messagebox.showerror("Error", "User not found.")
            return
        res = self.proc.find_friend(u)
        text = "\n".join(sorted([x.name for x in res])) or "No suggestions."
        self.write_output(self.suggest_out, text)

    # 6) groups visualization
    def _groups_tab(self):
        frame = self.tabs["Groups"]
        btns = ttk.Frame(frame)
        btns.pack(fill="x", pady=5)

        ttk.Button(btns, text="Compute Groups", command=self.show_groups).pack(side="left", padx=5)
        ttk.Button(btns, text="Draw Groups", command=self.draw_groups).pack(side="left", padx=5)

        self.groups_out = tk.Text(frame, height=10, wrap="word")
        self.groups_out.pack(fill="x", pady=5)

        # scrollable canvas
        canvas_frame = ttk.Frame(frame)
        canvas_frame.pack(fill="both", expand=True)

        self.group_canvas = tk.Canvas(canvas_frame, bg="white")
        x_scroll = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.group_canvas.xview)
        y_scroll = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.group_canvas.yview)

        self.group_canvas.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

        self.group_canvas.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)


    def show_groups(self):
        if not self.ensure_proc():
            return
        groups = self.proc.group()
        lines = []
        for i, g in enumerate(groups, 1):
            lines.append(f"Group {i}: " + ", ".join(sorted([x.name for x in g])))
        self.write_output(self.groups_out, "\n".join(lines))

    def draw_groups(self):
        if not self.ensure_proc():
            return

        groups = self.proc.group()
        self.group_canvas.delete("all")

        colors = ["#ff9999", "#99ccff", "#99ff99", "#ffcc99", "#cc99ff", "#ffff99"]

        node_w = 90
        node_h = 35
        x_gap = 25
        y_gap = 20

        group_x = 40
        group_y = 40
        col_width = 260

        for gi, g in enumerate(groups):
            g = list(g)
            color = colors[gi % len(colors)]

            self.group_canvas.create_text(
                group_x, group_y - 20,
                text=f"Group {gi + 1} ({len(g)})",
                anchor="w",
                font=("Arial", 11, "bold")
            )

            cols = 2
            for i, n in enumerate(g):
                row = i // cols
                col = i % cols

                nx = group_x + col * (node_w + x_gap)
                ny = group_y + row * (node_h + y_gap)

                self.group_canvas.create_oval(nx, ny, nx + node_w, ny + node_h,
                                            fill=color, outline="black")
                self.group_canvas.create_text(nx + node_w / 2, ny + node_h / 2,
                                            text=n.name)

            rows = (len(g) + cols - 1) // cols
            group_y += rows * (node_h + y_gap) + 80

        # set scroll region
        self.group_canvas.update_idletasks()
        self.group_canvas.configure(scrollregion=self.group_canvas.bbox("all"))

    # 7) popular person
    def _popular_tab(self):
        frame = self.tabs["Popular Person"]
        ttk.Button(frame, text="Find Popular Person", command=self.show_popular).pack(pady=8)

        self.popular_out = tk.Text(frame, height=18, wrap="word")
        self.popular_out.pack(fill="both", expand=True)

    def show_popular(self):
        if not self.ensure_proc():
            return
        ppl = self.proc.popular_person()
        self.write_output(self.popular_out, "\n".join([p.name for p in ppl]))

    # 8) intersection
    def _intersection_tab(self):
        frame = self.tabs["Intersection"]
        _, entries = self.make_entry_row(frame, ["User A:", "User B:"])
        self.int_a, self.int_b = entries
        ttk.Button(frame, text="Find Intersection", command=self.show_intersection).pack(pady=8)

        self.intersection_out = tk.Text(frame, height=18, wrap="word")
        self.intersection_out.pack(fill="both", expand=True)

    def show_intersection(self):
        if not self.ensure_proc():
            return
        a = self.node_from_name(self.int_a.get())
        b = self.node_from_name(self.int_b.get())
        if a not in self.proc.g or b not in self.proc.g:
            messagebox.showerror("Error", "User not found.")
            return
        res = self.proc.intersecion(a, b)
        self.write_output(self.intersection_out, "\n".join(sorted([x.name for x in res])) or "No common friends.")

    # 9) network data + export
    def _network_tab(self):
        frame = self.tabs["Network Data"]
        btns = ttk.Frame(frame)
        btns.pack(fill="x", pady=5)
        ttk.Button(btns, text="Show Network Data", command=self.show_network).pack(side="left", padx=5)
        ttk.Button(btns, text="Export JSON", command=self.export_json).pack(side="left", padx=5)

        self.network_out = tk.Text(frame, height=20, wrap="word")
        self.network_out.pack(fill="both", expand=True)

    def show_network(self):
        if not self.ensure_proc():
            return
        data = self.proc.network()
        lnn, e, ratio, biggest_group, popular = data
        text = (
            f"Nodes: {lnn}\n"
            f"Edges: {e}\n"
            f"Ratio: {ratio}\n"
            f"Biggest Group: {', '.join(sorted([x.name for x in biggest_group]))}\n"
            f"Popular Person(s): {', '.join([x.name for x in popular])}"
        )
        self.write_output(self.network_out, text)

    def export_json(self):
        if not self.ensure_proc():
            return
        path = filedialog.asksaveasfilename(
            title="Save JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if not path:
            return

        lnn, e, ratio, biggest_group, popular = self.proc.network()
        export_data = {
            "nodes": lnn,
            "edges": e,
            "ratio": ratio,
            "biggest_group": [x.name for x in biggest_group],
            "popular_person": [x.name for x in popular]
        }
        with open(path, "w") as f:
            json.dump(export_data, f, indent=4)

        messagebox.showinfo("Saved", "JSON exported successfully.")

    # 10) BFS
    def _bfs_tab(self):
        frame = self.tabs["BFS"]
        _, entries = self.make_entry_row(frame, ["Start node:"])
        self.bfs_name = entries[0]
        ttk.Button(frame, text="Run BFS", command=self.show_bfs).pack(pady=8)

        self.bfs_out = tk.Text(frame, height=20, wrap="word")
        self.bfs_out.pack(fill="both", expand=True)

    def show_bfs(self):
        if not self.ensure_proc():
            return

        s = self.node_from_name(self.bfs_name.get())
        if s not in self.proc.g:
            messagebox.showerror("Error", "User not found.")
            return

        bf = self.proc.BFS(s)
        lines = []
        for d in sorted(bf.keys()):
            lines.append(f"Distance {d}  ->  {len(bf[d]) if type(bf[d]) is set else 1} node(s)")
            if type(bf[d]) is not set:
                lines.append("   " + f"{bf[d].name}")
            else:lines.append("   " + ", ".join([x.name for x in bf[d]]))
            lines.append("")

        self.write_output(self.bfs_out, "\n".join(lines))


if __name__ == "__main__":
    app = SocialGUI()
    app.mainloop()