import re
import math
import hashlib
import requests
import tkinter as tk
from tkinter import messagebox

# Password Strength Functions
def general_validation(password):
    score = 0
    feedback = []
    
    size = len(password)
    upper = re.search(r'[A-Z]', password)
    lower = re.search(r'[a-z]', password)
    digit = re.search(r'[0-9]', password)
    special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    
    # Size points
    if size > 12:
        score += 3
    elif 8 < size <= 12:
        score += 2
    elif size == 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
    
    # Other points
    if upper:
        score += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")
    if lower:
        score += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")
    if digit:
        score += 1
    else:
        feedback.append("Password should contain at least one digit.")
    if special:
        score += 1
    else:
        feedback.append("Password should contain at least one special character.")
    
    return score, feedback

def calculate_entropy(password):
    character_set_size = 0
    if re.search(r'[a-z]', password):
        character_set_size += 26
    if re.search(r'[A-Z]', password):
        character_set_size += 26
    if re.search(r'[0-9]', password):
        character_set_size += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        character_set_size += 32
    
    length = len(password)
    if character_set_size == 0:
        return 0
    
    entropy = length * math.log2(character_set_size)
    
    if entropy < 40:
        return 1
    elif 40 <= entropy <= 60:
        return 2
    else:
        return 3

def check_pwned_password(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    
    try:
        url = f'https://api.pwnedpasswords.com/range/{prefix}'
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return True, int(count)
        return False, 0
    except requests.RequestException:
        return False, 0

def grade_password(score_final):
    if score_final >= 12:
        return "Excellent"
    elif 9 <= score_final < 12:
        return "Good"
    elif 6 <= score_final < 9:
        return "Fair"
    elif 0 <= score_final < 6:
        return "Weak"
    else:
        return "Very Weak"

# GUI Creation
class PasswordCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("400x400")

        # Input Field
        self.password_label = tk.Label(root, text="Enter your password:")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.pack()

        # Check Password Button
        self.check_button = tk.Button(root, text="Check Password", command=self.check_password)
        self.check_button.pack(pady=10)

        # Results Display
        self.result_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 10), wraplength=350, justify="left")
        self.feedback_label.pack(pady=10)

    def check_password(self):
        password = self.password_entry.get()

        # Check strength components
        score_general, feedback = general_validation(password)
        score_entropy = calculate_entropy(password)
        is_pwned, count = check_pwned_password(password)
        score_integrity = -5 if is_pwned else 5

        # Final score and grade
        score_final = score_general + score_entropy + score_integrity
        grade = grade_password(score_final)

        # Display results
        result_text = f"General Validation Score: {score_general}\n" \
                      f"Entropy Score: {score_entropy}\n" \
                      f"Password Integrity Score: {score_integrity}\n" \
                      f"Final Score: {score_final}\n" \
                      f"Password Grade: {grade}"
        self.result_label.config(text=result_text)

        # Feedback display
        integrity_feedback = f"Warning: Password has been pwned {count} times!" if is_pwned \
            else "Password is safe (not found in breaches)."
        feedback_text = "\n".join(feedback) + "\n" + integrity_feedback
        self.feedback_label.config(text=f"Feedback:\n{feedback_text}")

        # Alert if pwned
        if is_pwned:
            messagebox.showwarning("Pwned Password", f"Your password has been found in {count} breaches!")

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCheckerGUI(root)
    root.mainloop()
