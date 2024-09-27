from PyQt5.QtWidgets import *
from PyQt5 import uic
import random


class MyGUI(QMainWindow):
    
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("main.ui", self)
        self.show()
        self.guess_counter = 0
        self.games_played = 0
        self.scoreboard_data = []
        self.guess_btn.clicked.connect(self.check_guess)
        self.restart_btn.clicked.connect(self.restart)

        self.set_game()
        buttons = [100, 1000, 10000, 100000, 100000]
        for num in buttons:
            # Dynamically get the button object (e.g., self.btn_100, self.btn_1000, etc.)
            button = getattr(self, f'btn_{num}')

            # Connect the button's clicked signal to a slot (in this case, 'on_button_clicked')
            button.clicked.connect(lambda _, num=num: self.set_game(num))

        self.scoreboard.setColumnCount(2)
        self.scoreboard.setHorizontalHeaderLabels(["Name", "Count"])

    def set_game(self, num=100):
        self.restart()
        self.get_random_num(num)
        self.instructions.setText(f"Guess a number between 1 and {num} | {self.random_num}")
        return self

    def get_random_num(self, num):
        self.num_max = num
        self.random_num = random.randint(1, num)
        return self

    def check_guess(self, num):
        guess_num = int(self.guess_input.text())
        if guess_num > self.random_num:
            self.message_handler("Too High")
            self.increase_count()
        elif guess_num < self.random_num:
            self.message_handler("Too Low")
            self.increase_count()
        else:
            self.win()

        self.guess_input.setText("")
        return self
    
    def win(self):
        self.message_handler("Correct")
        self.name_label.setEnabled(True)
        self.name_input.setEnabled(True)
        self.name_btn.setEnabled(True)

        if self.name_btn.clicked.connect(self.add_winner):
            self.name_label.setEnabled(False)
            self.name_input.setEnabled(False)
            self.name_btn.setEnabled(False)

    def add_winner(self):
        player_name = self.name_input.text()
        row_count = self.scoreboard.rowCount()
        self.scoreboard.insertRow(row_count)
        self.scoreboard.setItem(row_count, 0, QTableWidgetItem(player_name))
        self.scoreboard.setItem(row_count, 1, QTableWidgetItem(str(self.guess_counter)))
        self.set_game()
        return True
        
    def increase_count(self):
        self.guess_counter += 1
        self.guess_count_text.setText(str(self.guess_counter))
        return self

    def message_handler(self, msg):
        message = QMessageBox()
        message.setText(msg)
        message.exec_()
        return self

    def restart(self):
        self.guess_counter = 0
        self.guess_count_text.setText(str(self.guess_counter))
        # self.message_handler("Game is restarting...")
        return self

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()
