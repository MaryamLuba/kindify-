import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import random
import os
import json
from datetime import datetime

class KindnessSpark:
    def __init__(self, root):
        self.root = root
        self.root.title("Kindness Spark")
        self.root.geometry("400x700")
        self.root.configure(bg='#FFF0F5')  # Light pink background

        # Persistent storage paths
        self.BADGES_FILE = 'kindness_badges.json'
        self.PROOFS_FILE = 'kindness_proofs.json'

        # Load previous data
        self.load_data()

        self.kindness_acts = {
            'Home': [
                "🏠 Write a cozy letter to a family member",
                "🧹 Help with chores with a cheerful smile",
                "🍲 Cook a surprise meal with love"
            ],
            'Work': [
                "🌟 Spread sunshine with a genuine compliment",
                "🤝 Be a hero and help a struggling teammate",
                "🍪 Surprise colleagues with homemade treats"
            ],
            'Online': [
                "💌 Send a virtual hug to a friend",
                "🌈 Share a positivity post",
                "💖 Drop a heartwarming comment"
            ],
            'Outdoor': [
                "🛍️ Be a grocery guardian angel",
                "🌱 Plant hope with a new tree",
                "🧹 Clean up with a sparkly smile"
            ]
        }

        self.appreciation_messages = [
            "Aww, you're spreading love! 💕",
            "Your kindness is pure magic! ✨",
            "You're making the world sparkle! 🌟",
            "Kindness champion alert! 🏆",
            "Sending virtual hugs your way! 🤗"
        ]

        # UI Variables
        self.current_kindness = tk.StringVar()
        self.current_category = tk.StringVar()
        self.proof_image = None

        self.create_ui()
        self.generate_kindness_act()

    def create_ui(self):
        # Main Frame
        main_frame = tk.Frame(self.root, bg='#FFF0F5')
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame, text="Kindness Spark", 
                                font=("Arial", 24, "bold"), 
                                bg='#FFF0F5', 
                                fg='#FF1493')
        title_label.pack(pady=10)

        # Category Label
        self.category_label = tk.Label(main_frame, 
                                       textvariable=self.current_category, 
                                       font=("Arial", 12), 
                                       bg='#FFF0F5', 
                                       fg='#4B0082')
        self.category_label.pack()

        # Kindness Act Display
        act_label = tk.Label(main_frame, 
                             textvariable=self.current_kindness, 
                             font=("Arial", 16, "italic"), 
                             bg='#FFF0F5', 
                             fg='#333', 
                             wraplength=350)
        act_label.pack(pady=10)

        # Image Upload Button
        self.image_preview = tk.Label(main_frame, bg='#FFF0F5')
        self.image_preview.pack(pady=10)

        upload_btn = tk.Button(main_frame, text="Upload Proof", 
                               command=self.upload_image, 
                               bg='#FF69B4', 
                               fg='white')
        upload_btn.pack(pady=5)

        # Action Buttons
        btn_frame = tk.Frame(main_frame, bg='#FFF0F5')
        btn_frame.pack(pady=10)

        regenerate_btn = tk.Button(btn_frame, text="Regenerate", 
                                   command=self.generate_kindness_act, 
                                   bg='white', 
                                   fg='#FF1493')
        regenerate_btn.pack(side=tk.LEFT, padx=5)

        complete_btn = tk.Button(btn_frame, text="Complete Act", 
                                 command=self.complete_act, 
                                 bg='#FF1493', 
                                 fg='white')
        complete_btn.pack(side=tk.LEFT, padx=5)

        # Stats
        stats_frame = tk.Frame(main_frame, bg='#FFF0F5')
        stats_frame.pack(pady=10)

        self.completed_label = tk.Label(stats_frame, 
                                   text=f"Completed Acts: {self.completed_acts}", 
                                   bg='#FFF0F5')
        self.completed_label.pack(side=tk.LEFT, padx=5)

        self.badges_label = tk.Label(stats_frame, 
                                text=f"Badges: {sum(self.badges.values())}/3", 
                                bg='#FFF0F5')
        self.badges_label.pack(side=tk.LEFT, padx=5)

    def load_data(self):
        # Load badges
        try:
            with open(self.BADGES_FILE, 'r') as f:
                self.badges = json.load(f)
        except FileNotFoundError:
            self.badges = {
                'starter': False,
                'kindness_champ': False,
                'positivity_master': False
            }

        # Load proofs
        try:
            with open(self.PROOFS_FILE, 'r') as f:
                self.uploaded_proofs = json.load(f)
        except FileNotFoundError:
            self.uploaded_proofs = []

        # Set completed acts count
        self.completed_acts = len(self.uploaded_proofs)

    def save_data(self):
        # Save badges
        with open(self.BADGES_FILE, 'w') as f:
            json.dump(self.badges, f)

        # Save proofs (without full image path to save space)
        proofs_to_save = [{k: v for k, v in proof.items() if k != 'image'} for proof in self.uploaded_proofs]
        with open(self.PROOFS_FILE, 'w') as f:
            json.dump(proofs_to_save, f)

    def generate_kindness_act(self, category=None):
        categories = list(self.kindness_acts.keys())
        chosen_category = category or random.choice(categories)
        
        acts = self.kindness_acts[chosen_category]
        random_act = random.choice(acts)
        
        self.current_kindness.set(random_act)
        self.current_category.set(f"{chosen_category} Challenge")
        self.proof_image = None
        self.image_preview.config(image='')

    def upload_image(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
            )
            if file_path:
                image = Image.open(file_path)
                image.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(image)
                self.image_preview.config(image=photo)
                self.image_preview.image = photo
                self.proof_image = file_path
        except Exception as e:
            messagebox.showerror("Image Upload Error", str(e))

    def complete_act(self):
        if not self.proof_image:
            messagebox.showwarning("Oops!", "Please upload a proof of your kind act!")
            return

        self.completed_acts += 1

        # Store proof
        self.uploaded_proofs.append({
            'act': self.current_kindness.get(),
            'image': self.proof_image,
            'timestamp': datetime.now().isoformat(),
            'category': self.current_category.get()
        })

        # Badge logic
        if self.completed_acts >= 1:
            self.badges['starter'] = True
        if self.completed_acts >= 5:
            self.badges['kindness_champ'] = True
        if self.completed_acts >= 10:
            self.badges['positivity_master'] = True

        # Update UI labels
        self.completed_label.config(text=f"Completed Acts: {self.completed_acts}")
        self.badges_label.config(text=f"Badges: {sum(self.badges.values())}/3")

        # Save data
        self.save_data()

        # Show appreciation
        message = random.choice(self.appreciation_messages)
        messagebox.showinfo("Kindness Celebration!", message)

        # Regenerate act
        self.generate_kindness_act()

def main():
    root = tk.Tk()
    app = KindnessSpark(root)
    root.mainloop()

if __name__ == "__main__":
    main()
