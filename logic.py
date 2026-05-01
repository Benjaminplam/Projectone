from PyQt6.QtWidgets import *
from gui import *
import csv



class Logic(QMainWindow, Ui_MainWindow):
    # Class hold all the logic for the Voting App
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


        self.pushButton_enter.clicked.connect(self.ballot_verification)


        # Buttons are disabled till ballot is validated
        self.button_vote.clicked.connect(self.vote)
        self.button_vote.setEnabled(False)
        self.button_can1.setEnabled(False)
        self.button_can2.setEnabled(False)
        self.button_can3.setEnabled(False)


        # opens a file vote_count.csv if it not already open
        self.vote_tracking_file()


    def ballot_verification(self)-> None:
        # Validates ballot numbers before collecting vote information
        ballot_number = self.lineEdit_ballotnumber.text()

        try:
            int(ballot_number)

        except ValueError:
            self.label_error_ballot.setText("Please enter a valid ballot number")
            return


        if len(ballot_number) != 5:
            self.label_error_ballot.setText("Ballot must have 5 digits")
            return

        self.label_error_ballot.clear()

        self.ballot_tracking()

    def ballot_tracking(self)-> None:
        # Tracks Ballot numbers and the party that has been selected
        ballot_number = self.lineEdit_ballotnumber.text()

        if self.button_dem.isChecked():
            election = "Democrat"
        elif self.button_rep.isChecked():
            election = "Republican"
        else:
            election = "N/A"

        with open("data.csv", 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow([ballot_number, election])



        # Enables all the voting features after verification of ballot number.
        self.button_vote.setEnabled(True)
        self.button_can1.setEnabled(True)
        self.button_can2.setEnabled(True)
        self.button_can3.setEnabled(True)

        self.label_can1.setText("John Smith")
        self.label_can2.setText("Jane Smith")
        self.label_write_in.clear()
        self.label_write_in.setReadOnly(False)

        # disables the ballot section
        self.pushButton_enter.setEnabled(False)
        self.lineEdit_ballotnumber.setReadOnly(True)
        self.button_dem.setEnabled(False)
        self.button_rep.setEnabled(False)



    def vote (self)-> None:
        # Collects the Vote for either Candidate or Write-in, The value is passed to the function vote_count and closes app.
        if self.button_can1.isChecked():
            candidate = "John Smith"
        elif self.button_can2.isChecked():
            candidate = "Jane Smith"
        elif self.button_can3.isChecked():
            if self.label_write_in.text().strip() == "":
                self.label_error_vote.setText("Please select a candidate")
                return
            candidate = "Write-In"

        else:
            self.label_error_vote.setText("Please select a candidate")
            return



        self.vote_count(candidate)
        self.close()



    def vote_count(self, candidate: str)-> None:
        # Tracks count of votes after each vote in a file.
        votes = []

        with open("vote_count.csv",'r') as file:
            reader = csv.reader(file)
            votes = list(reader)

        for vote in votes:
            if vote[0] == candidate:
                count = int(vote[1])

                count = count + 1

                vote[1] = str(count)

        with open("vote_count.csv",'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(votes)


    def vote_tracking_file(self)-> None:
        # opens a file, this function is called in the Class logic.
        try:
            with open("vote_count.csv",'r') as file:
                pass
        except FileNotFoundError:
            with open("vote_count.csv",'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["John Smith", 0])
                writer.writerow(["Jane Smith", 0])
                writer.writerow(["Write-In", 0])

