import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from main import Proccess, node
from json_manager import JSONManager

class SocialGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Social Network GUI")
        self.geometry("1200x750")
        self.minsize(1100, 700)

        self.proc = None
        self.file_path = None
        self.json_mgr = JSONManager()

        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Button(top, text="Open TXT", command=self.load_file).pack(side="left", padx=5)
        ttk.Button(top, text="Load JSON Data", command=self.load_json_to_app).pack(side="left", padx=5)
        self.file_label = ttk.Label(top, text="No file loaded")
        self.file_label.pack(side="left", padx=10)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabs = {}
        for name in [
            "Friends",
            "Connection Check",
            "Shortest Path",
            "Friend Suggestion",
            "Groups",
            "Popular Person",
            "Intersection",
            "Network Data",
            "User Distances (BFS)",
            "Edit Network"
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
        self._edit_network_tab()

    def load_file(self):
        path = filedialog.askopenfilename(
            title="Select text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            self.file_path = path
            with open(path, "r", encoding="utf-8") as f:
                self.proc = Proccess(f)
            self.file_label.config(text=path)
            self.clear_all_outputs()
            messagebox.showinfo("Loaded", "File loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_json_to_app(self):
        data = self.json_mgr.load_data()
        if not data.get("users"):
            messagebox.showwarning("Empty", "JSON file is empty.")
            return
        
        lines = []
        # ۱. ابتدا همه کاربران (حتی کاربران بدون دوست) اضافه می‌شوند
        for u in data["users"]:
            lines.append(f"{u}\n")
            
        # ۲. سپس روابط دوستی اضافه می‌شوند
        for u1, u2 in data.get("connections", []):
            lines.append(f"{u1} {u2}\n")
            
        self.proc = Proccess(lines)
        self.file_label.config(text="Loaded from JSON")
        self.clear_all_outputs()
        messagebox.showinfo("Loaded", f"JSON loaded successfully with {len(data['users'])} users.")

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
            messagebox.showwarning("No data", "Please load TXT or JSON first.")
            return False
        return True

    def node_from_name(self, name):
        return node(name.strip())

    def write_output(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", text)
        widget.config(state="disabled")

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
        text = "\n".join(sorted([x.name for x in friends])) or "No friends found."
        self.write_output(self.friends_out, text)

    def _same_group_tab(self):
        frame = self.tabs["Connection Check"]
        _, entries = self.make_entry_row(frame, ["User A:", "User B:"])
        self.grp_a, self.grp_b = entries
        ttk.Button(frame, text="Check Connection", command=self.check_group).pack(pady=8)
        self.group_out = tk.Text(frame, height=18, wrap="word")
        self.group_out.pack(fill="both", expand=True)

    def check_group(self):
        if not self.ensure_proc():
            return
        a = self.node_from_name(self.grp_a.get())
        b = self.node_from_name(self.grp_b.get())
        found = self.proc.are_connected(a, b)
        res_text = f"✅ کاربران '{a.name}' و '{b.name}' با هم مرتبط هستند." if found else f"❌ کاربران '{a.name}' و '{b.name}' ارتباطی ندارند."
        self.write_output(self.group_out, res_text)

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
            if not path:
                self.write_output(self.path_out, "مسیری یافت نشد.")
            else:
                names = [x.name for x in path]
                self.write_output(self.path_out, " -> ".join(names))
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
        res = self.proc.find_friend(u)
        text = "\n".join(sorted([x.name for x in res])) or "No suggestions."
        self.write_output(self.suggest_out, text)

    def _groups_tab(self):
        frame = self.tabs["Groups"]
        ttk.Button(frame, text="Compute Groups", command=self.show_groups).pack(pady=8)
        self.groups_out = tk.Text(frame, height=18, wrap="word")
        self.groups_out.pack(fill="both", expand=True)

    def show_groups(self):
        if not self.ensure_proc():
            return
        groups = self.proc.group()
        lines = [f"Group {i}: " + ", ".join(sorted([x.name for x in g])) for i, g in enumerate(groups, 1)]
        self.write_output(self.groups_out, "\n".join(lines))

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
        res = self.proc.intersecion(a, b)
        self.write_output(self.intersection_out, "\n".join(sorted([x.name for x in res])) or "No common friends.")

    def _network_tab(self):
        frame = self.tabs["Network Data"]
        ttk.Button(frame, text="Show Network Data", command=self.show_network).pack(pady=8)
        self.network_out = tk.Text(frame, height=18, wrap="word")
        self.network_out.pack(fill="both", expand=True)

    def show_network(self):
        if not self.ensure_proc():
            return
        lnn, e, ratio, biggest_group, popular = self.proc.network()
        text = (
            f"Nodes: {lnn}\n"
            f"Edges: {e}\n"
            f"Ratio: {ratio}\n"
            f"Biggest Group: {', '.join(sorted([x.name for x in biggest_group]))}\n"
            f"Popular Person(s): {', '.join([x.name for x in popular])}"
        )
        self.write_output(self.network_out, text)

    def _bfs_tab(self):
        frame = self.tabs["User Distances (BFS)"]
        _, entries = self.make_entry_row(frame, ["Start node:"])
        self.bfs_name = entries[0]
        ttk.Button(frame, text="Calculate Distances", command=self.show_bfs).pack(pady=8)
        self.bfs_out = tk.Text(frame, height=18, wrap="word")
        self.bfs_out.pack(fill="both", expand=True)

    def show_bfs(self):
        if not self.ensure_proc():
            return
        s = self.node_from_name(self.bfs_name.get())
        if s not in self.proc.g:
            messagebox.showerror("Error", "User not found.")
            return

        bf = self.proc.BFS(s)
        
        dist_dict = {}
        for d, nodes in bf.items():
            if isinstance(nodes, set):
                for n in nodes:
                    dist_dict[n.name] = d
            else:
                dist_dict[nodes.name] = d

        all_users = set(x.name for x in self.proc.g.keys())
        lines = [f"فاصله کاربر '{s.name}' از تمام افراد شبکه:\n" + "-"*40]
        
        sorted_reachable = sorted(dist_dict.items(), key=lambda x: x[1])
        for name, d in sorted_reachable:
            if name != s.name:
                lines.append(f"{name} ، {d}")
                
        unreachable = sorted(all_users - set(dist_dict.keys()))
        for name in unreachable:
            if name != s.name:
                lines.append(f"{name} ، بینهایت")

        self.write_output(self.bfs_out, "\n".join(lines))

    def _edit_network_tab(self):
        frame = self.tabs["Edit Network"]
        _, entries1 = self.make_entry_row(frame, ["User Name:"])
        self.edit_user_entry = entries1[0]
        
        btn_frame1 = ttk.Frame(frame)
        btn_frame1.pack(fill="x", pady=5)
        ttk.Button(btn_frame1, text="Add User", command=self.add_user_action).pack(side="left", padx=5)
        ttk.Button(btn_frame1, text="Remove User", command=self.remove_user_action).pack(side="left", padx=5)

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

        _, entries2 = self.make_entry_row(frame, ["User A:", "User B:"])
        self.conn_a, self.conn_b = entries2

        btn_frame2 = ttk.Frame(frame)
        btn_frame2.pack(fill="x", pady=5)
        ttk.Button(btn_frame2, text="Add Connection", command=self.add_conn_action).pack(side="left", padx=5)
        ttk.Button(btn_frame2, text="Remove Connection", command=self.remove_conn_action).pack(side="left", padx=5)

    def add_user_action(self):
        u = self.edit_user_entry.get().strip()
        if self.json_mgr.add_user(u):
            messagebox.showinfo("Success", f"User '{u}' added.")
            self.load_json_to_app()
        else:
            messagebox.showwarning("Warning", "User exists or name is empty.")

    def remove_user_action(self):
        u = self.edit_user_entry.get().strip()
        if self.json_mgr.remove_user(u):
            messagebox.showinfo("Success", f"User '{u}' removed.")
            self.load_json_to_app()
        else:
            messagebox.showwarning("Warning", "User not found.")

    def add_conn_action(self):
        a = self.conn_a.get().strip()
        b = self.conn_b.get().strip()
        if self.json_mgr.add_connection(a, b):
            messagebox.showinfo("Success", f"Connection '{a} - {b}' added.")
            self.load_json_to_app()
        else:
            messagebox.showwarning("Warning", "Check if users exist.")

    def remove_conn_action(self):
        a = self.conn_a.get().strip()
        b = self.conn_b.get().strip()
        if self.json_mgr.remove_connection(a, b):
            messagebox.showinfo("Success", f"Connection '{a} - {b}' removed.")
            self.load_json_to_app()
        else:
            messagebox.showwarning("Warning", "Connection not found.")

if __name__ == "__main__":
    app = SocialGUI()
    app.mainloop()
