import tkinter as tk
import random

# === Game Data ===
WORDS = ["random", "while-loop", "if-else", "strings", "list"]
MAX_ATTEMPTS = 6

class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Hangman – Python GUI")
        self.root.geometry("600x500")
        self.root.configure(bg="#0f172a")

        self.word = ""
        self.attempts = MAX_ATTEMPTS
        self.used = set()
        self.guessed = []

        # Title
        tk.Label(root, text="🎮 Hangman", font=("Arial", 22, "bold"), bg="#0f172a", fg="#22d3ee").pack(pady=10)
        tk.Label(root, text=f"Guess the hidden word. You have {MAX_ATTEMPTS} wrong tries.", 
                 font=("Arial", 12), bg="#0f172a", fg="#94a3b8").pack(pady=5)

        # Stats
        self.stats = tk.Label(root, text="", font=("Arial", 12), bg="#0f172a", fg="#e5e7eb")
        self.stats.pack(pady=5)

        # Word display
        self.word_display = tk.Label(root, text="", font=("Courier", 28, "bold"), bg="#0f172a", fg="#ebebe5")
        self.word_display.pack(pady=10)

        # Message
        self.msg = tk.Label(root, text="", font=("Arial", 14), bg="#0f172a")
        self.msg.pack(pady=5)

        
        # Onscreen keyboard (QWERTY style layout)
        self.kb_frame = tk.Frame(root, bg="#0f172a")
        self.kb_frame.pack(pady=10)

        self.kb_buttons = {}
        rows = [
            "`1234567890-=",
            "QWERTYUIOP[]#",
            "ASDFGHJKL;'",
            "\\ZXCVBNM,./"
        ]
        offsets = [0, 0, 1, 1]  # thoda center alignment jaisa feel dene ke liye

        for r, row_keys in enumerate(rows):
            for c, ch in enumerate(row_keys):
                btn = tk.Button(self.kb_frame, text=ch, width=4, height=2,
                                command=lambda c=ch: self.handle_guess(c.lower()),
                                bg="#111827", fg="white", relief="raised", font=("Arial", 10, "bold"))
                btn.grid(row=r, column=c + offsets[r], padx=3, pady=3)
                self.kb_buttons[ch.lower()] = btn


        # Reset button
        tk.Button(root, text="↻ New Word", font=("Arial", 12, "bold"),
                  command=self.reset_game, bg="#111827", fg="white", padx=10, pady=5).pack(pady=10)

        self.reset_game()

    def reset_game(self):
        self.word = random.choice(WORDS)
        self.attempts = MAX_ATTEMPTS
        self.used = set()
        self.guessed = ["_"] * len(self.word)
        self.msg.config(text="", fg="#e5e7eb")

        for btn in self.kb_buttons.values():
            btn.config(state="normal", bg="#111827")

        self.update_display()

    def update_display(self):
        self.word_display.config(text=" ".join(self.guessed))
        self.stats.config(text=f"Attempts left: {self.attempts}    Used letters: {', '.join(sorted(self.used)) if self.used else '–'}")

    def handle_guess(self, letter):
        if letter in self.used or self.attempts <= 0 or "_" not in self.guessed:
            return

        self.used.add(letter)
        btn = self.kb_buttons[letter]
        btn.config(state="disabled")

        if letter in self.word:
            for i, ch in enumerate(self.word):
                if ch == letter:
                    self.guessed[i] = letter
            btn.config(bg="#34d399")  # green
            self.msg.config(text="✅ Good guess!", fg="#34d399")
        else:
            self.attempts -= 1
            btn.config(bg="#f87171")  # red
            self.msg.config(text=f"❌ Wrong! {self.attempts} attempts left.", fg="#f87171")

        self.update_display()
        self.check_end()

    def check_end(self):
        if "_" not in self.guessed:
            self.msg.config(text=f"🎉 Congratulations! You guessed the word: {self.word}", fg="#34d399")
            self.end_lock()
        elif self.attempts == 0:
            self.msg.config(text=f"💀 Game Over! The word was: {self.word}", fg="#f87171")
            self.end_lock()

    def end_lock(self):
        for btn in self.kb_buttons.values():
            btn.config(state="disabled")

# Run the app
root = tk.Tk()
app = HangmanApp(root)
root.mainloop()

