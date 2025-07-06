import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
from utils import extract_frames
from detection import detect_objects
from logger import save_transcript

# --- Minimal custom style for scrollbars and widgets ---
def style_scrollbar(widget):
    try:
        import tkinter.ttk as ttk
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Vertical.TScrollbar', gripcount=0,
                        background='#e0e0e0', darkcolor='#e0e0e0', lightcolor='#e0e0e0',
                        troughcolor='#f7f7f7', bordercolor='#f7f7f7', arrowcolor='#888')
        style.configure('Horizontal.TScrollbar', gripcount=0,
                        background='#e0e0e0', darkcolor='#e0e0e0', lightcolor='#e0e0e0',
                        troughcolor='#f7f7f7', bordercolor='#f7f7f7', arrowcolor='#888')
    except Exception:
        pass

class SurveillanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Surveillance Transcription")
        self.root.geometry("500x650")
        self.root.configure(bg="#232323")

        # Header
        header = tk.Label(root, text="AI SURVEILLANCE", font=("Segoe UI", 22, "bold"), bg="#232323", fg="#6be445")
        header.pack(pady=(18, 8))

        # Search bar for transcript
        search_frame = tk.Frame(root, bg="#232323")
        search_frame.pack(pady=(0, 10), padx=32, fill=tk.X)
        search_label = tk.Label(search_frame, text="Search transcript", font=("Segoe UI", 10), bg="#232323", fg="#bbb")
        search_label.pack(anchor="w")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 12), bg="#333", fg="#eee", bd=0, relief=tk.FLAT)
        search_entry.pack(fill=tk.X, ipady=8, pady=(2, 0))
        search_entry.bind('<KeyRelease>', self._search_transcript)
    def _search_transcript(self, event=None):
        # Highlight all matches in the transcript box
        query = self.search_var.get().strip().lower()
        self.transcript_box.tag_remove('search', '1.0', tk.END)
        if not query:
            return
        start = '1.0'
        while True:
            pos = self.transcript_box.search(query, start, stopindex=tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(query)}c"
            self.transcript_box.tag_add('search', pos, end)
            start = end
        self.transcript_box.tag_config('search', background='#6be445', foreground='#232323')

        # Upload button with roundness
        self.upload_btn = tk.Button(
            root, text="Upload Video", command=self.upload_video,
            font=("Segoe UI", 13, "bold"), bg="#333", fg="#fff",
            activebackground="#444", activeforeground="#fff",
            relief=tk.FLAT, bd=0, padx=0, pady=0, cursor="hand2",
            highlightthickness=0
        )
        self.upload_btn.pack(pady=(10, 10), ipadx=0, ipady=0)
        self.upload_btn.configure(borderwidth=0, highlightbackground="#232323")
        self.upload_btn.bind('<Enter>', lambda e: self.upload_btn.config(bg="#444"))
        self.upload_btn.bind('<Leave>', lambda e: self.upload_btn.config(bg="#333"))
        # Add roundness using a canvas
        self._round_button(self.upload_btn, width=180, height=40, radius=20)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = tk.Canvas(root, width=420, height=18, bg="#232323", highlightthickness=0, bd=0)
        self.progress.pack(pady=(0, 10))
        self.progress_bar = self.progress.create_rectangle(0, 0, 0, 18, fill="#6be445", outline="")

        # Transcript box frame for border effect
        frame = tk.Frame(root, bg="#232323", bd=0, highlightthickness=0)
        frame.pack(padx=32, pady=(0, 18), fill=tk.BOTH, expand=True)
        self.transcript_box = scrolledtext.ScrolledText(
            frame, wrap=tk.WORD, font=("Segoe UI", 12), width=50, height=18,
            bg="#181818", fg="#eee", insertbackground="#eee", bd=0, relief=tk.FLAT
        )
        self.transcript_box.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
        self.transcript_box.configure(highlightthickness=1, highlightbackground="#444", highlightcolor="#444")
        style_scrollbar(self.transcript_box)

    def _round_button(self, button, width=180, height=40, radius=20):
        # Place button on a canvas for roundness
        canvas = tk.Canvas(button.master, width=width, height=height, bg="#232323", highlightthickness=0, bd=0)
        canvas.place(in_=button, relx=0.5, rely=0.5, anchor="center", x=0, y=0)
        canvas.create_oval(0, 0, height, height, fill="#333", outline="#333")
        canvas.create_oval(width-height, 0, width, height, fill="#333", outline="#333")
        canvas.create_rectangle(height//2, 0, width-height//2, height, fill="#333", outline="#333")
        button.lift()

    def upload_video(self):
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
        )
        if not file_path:
            return
        try:
            self.transcript_box.delete(1.0, tk.END)
            self._set_progress(0)
            self.root.update()
            frames = extract_frames(file_path, frame_interval=30)
            detections = []
            total = len(frames)
            for i, (timestamp, frame) in enumerate(frames):
                self.root.update()
                try:
                    labels = detect_objects(frame)
                except Exception as e:
                    labels = []
                detections.append((timestamp, labels))
                self._set_progress((i+1)/total)
            output_path = os.path.join("output", "transcript.txt")
            save_transcript(detections, output_path)
            # Show transcript in box
            with open(output_path, "r") as f:
                transcript = f.read()
            # Animation: fade in transcript
            self.transcript_box.delete(1.0, tk.END)
            self._set_progress(0)
            self._animate_transcript(transcript)
        except Exception as e:
            self._set_progress(0)
            messagebox.showerror("Error", str(e))

    def _set_progress(self, frac):
        # Update the progress bar (0.0 to 1.0)
        width = 420
        self.progress.coords(self.progress_bar, 0, 0, int(width*frac), 18)
        self.progress.update()

    def _animate_transcript(self, text, idx=0):
        # Simple fade-in animation for transcript text
        if idx < len(text):
            self.transcript_box.insert(tk.END, text[idx])
            self.transcript_box.see(tk.END)
            self.transcript_box.update()
            self.root.after(1, lambda: self._animate_transcript(text, idx+1))

if __name__ == "__main__":
    root = tk.Tk()
    app = SurveillanceApp(root)
    root.mainloop()
