import tkinter as tk
from tkinter import ttk, messagebox
from degrees import shortest_path, person_id_for_name, people, movies, load_data

# ---- GUI ----
class DegreesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Degrees of Separation")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Başlık
        ttk.Label(root, text="Degrees of Separation", font=("Helvetica", 18, "bold")).pack(pady=20)

        # Dataset seçimi
        self.dataset_var = tk.StringVar(value="small")
        frame_dataset = ttk.Frame(root)
        frame_dataset.pack(pady=5)
        ttk.Label(frame_dataset, text="Dataset: ").pack(side=tk.LEFT)
        ttk.Radiobutton(frame_dataset, text="Small", variable=self.dataset_var, value="small").pack(side=tk.LEFT)
        ttk.Radiobutton(frame_dataset, text="Large", variable=self.dataset_var, value="large").pack(side=tk.LEFT)

        # İsimler
        frame_names = ttk.Frame(root)
        frame_names.pack(pady=10)

        ttk.Label(frame_names, text="Source Name: ").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.source_entry = ttk.Entry(frame_names, width=30)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_names, text="Target Name: ").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.target_entry = ttk.Entry(frame_names, width=30)
        self.target_entry.grid(row=1, column=1, padx=5, pady=5)

        # Çalıştır butonu
        ttk.Button(root, text="Find Path", command=self.find_path).pack(pady=15)

        # Sonuç Text kutusu
        self.result_text = tk.Text(root, width=70, height=10, wrap="word")
        self.result_text.pack(pady=10)
        self.result_text.config(state=tk.DISABLED)

        # Veriyi yükle
        self.load_dataset()

    def load_dataset(self):
        directory = self.dataset_var.get()
        try:
            load_data(directory)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dataset: {e}")

    def find_path(self):
        self.load_dataset()
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)

        source_name = self.source_entry.get().strip()
        target_name = self.target_entry.get().strip()

        source_id = person_id_for_name(source_name)
        if source_id is None:
            messagebox.showerror("Error", f"Person '{source_name}' not found.")
            return

        target_id = person_id_for_name(target_name)
        if target_id is None:
            messagebox.showerror("Error", f"Person '{target_name}' not found.")
            return

        path = shortest_path(source_id, target_id)
        if path is None:
            self.result_text.insert(tk.END, f"No connection found between {source_name} and {target_name}.\n")
        else:
            self.result_text.insert(tk.END, f"{len(path)} degrees of separation:\n\n")
            path = [(None, source_id)] + path
            for i in range(len(path)-1):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i+1][1]]["name"]
                movie = movies[path[i+1][0]]["title"]
                self.result_text.insert(tk.END, f"{i+1}: {person1} and {person2} starred in {movie}\n")

        self.result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    gui = DegreesGUI(root)
    root.mainloop()
