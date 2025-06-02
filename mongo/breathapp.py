import time
import tkinter as tk
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['breath_test']
collection = db['results']

class BreathTest:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Breath Test")
        self.name = tk.StringVar()
        self.time_taken = 0
        self.start_time = 0
        self.start_page()

    def start_page(self):
        self.clear_window()
        tk.Label(self.window, text="Breath Test", font=("Arial", 24)).pack()
        tk.Label(self.window, text="Enter your name:").pack()
        tk.Entry(self.window, textvariable=self.name).pack()
        tk.Button(self.window, text="Start Test", command=self.start_test).pack()
        tk.Button(self.window, text="Leaderboard", command=self.leaderboard_page).pack()

    def start_test(self):
        self.clear_window()
        tk.Label(self.window, text="Take a deep breath...").pack()
        self.window.update()
        time.sleep(2)

        tk.Label(self.window, text="Hold your breath...").pack()
        tk.Label(self.window, text="Note: If you can't hold your breath,  press the button below").pack()
        self.window.update()

        tk.Label(self.window, text="Inhaling...").pack()
        for i in range(5, 0, -1):
            tk.Label(self.window, text=str(i)).pack()
            self.window.update()
            time.sleep(1)

        tk.Label(self.window, text="Holding breath...").pack()
        self.start_time = time.time()
        self.button = tk.Button(self.window, text="Stop Timer", command=lambda: self.calculate_capacity())
        self.button.pack()
        self.window.update()

        self.timer_label = tk.Label(self.window, text="Time: 0.00 seconds")
        self.timer_label.pack()
        self.update_timer()

        tk.Button(self.window, text="Home", command=self.start_page).pack()
        tk.Button(self.window, text="Leaderboard", command=self.leaderboard_page).pack()

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        self.current_time = "{:.2f}".format(elapsed_time)
        self.timer_label.config(text=f"Time: {self.current_time} seconds")
        self.window.after(100, self.update_timer)

    def calculate_capacity(self):
        self.time_taken = float(self.current_time)
        capacity = (self.time_taken / 60) * 100
        if capacity > 100:
            capacity = 100
        self.save_result(capacity)
        self.result_page(capacity)

    def save_result(self, capacity):
        result = {
            "name": self.name.get(),
            "time_taken": self.time_taken,
            "capacity": capacity
        }
        collection.insert_one(result)

    def result_page(self, capacity):
        self.clear_window()
        tk.Label(self.window, text=f"Your lung capacity is: {capacity:.2f}%").pack()
        if capacity > 80:
            tk.Label(self.window, text="Your lung capacity is excellent!").pack()
        elif capacity > 60:
            tk.Label(self.window, text="Your lung capacity is good!").pack()
        elif capacity > 40:
            tk.Label(self.window, text="Your lung capacity is average!").pack()
        else:
            tk.Label(self.window, text="Your lung capacity is below average!").pack()
        tk.Label(self.window, text=f"Time taken: {self.time_taken:.2f} seconds").pack()
        tk.Button(self.window, text="Home", command=self.start_page).pack()
        tk.Button(self.window, text="Leaderboard", command=self.leaderboard_page).pack()

    def leaderboard_page(self):
        self.clear_window()
        total_tests = collection.count_documents({})
        best_result = collection.find().sort("time_taken", -1).limit(1)
        tk.Label(self.window, text="Leaderboard").pack()
        tk.Label(self.window, text=f"Total tests taken: {total_tests}").pack()
        for result in best_result:
            tk.Label(self.window, text=f"Best record: {result['time_taken']:.2f} seconds by {result['name']} with lung capacity: {result['capacity']:.2f}%").pack()
        tk.Button(self.window, text="Home", command=self.start_page).pack()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    breath_test = BreathTest()
    breath_test.run()