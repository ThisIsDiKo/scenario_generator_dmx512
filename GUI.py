from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
from copy import deepcopy
from NewScenarioDialog import CustomDialog

from Scenario import Scenario, Slide
import pickle


class Panel(QWidget):
    def __init__(self):
        super().__init__()

        try:
            with open("styles.css", "r") as fh:
                self.setStyleSheet(fh.read())
        except:
            pass


        self.lastPosEntered = 0
        self.lastVelocityEntered = 0

        self.scenario = None
        self.slide = Slide()

        self.rows = 5
        self.cols = 10
        self.currentSlide = 0
        self.numOfSlides = 0
        self.timingIncrement = 200

        self.btnNew = QPushButton('NEW')
        self.btnOpen = QPushButton('OPEN')
        self.btnSave = QPushButton('SAVE')
        self.btnSaveAs = QPushButton('SAVE AS')
        self.lblNumOfRows = QLabel('0')
        self.lblNumOfCols = QLabel('0')


        self.btnSave.clicked.connect(self.save_clicked)
        self.btnOpen.clicked.connect(self.open_clicked)

        self.fileLayout = QHBoxLayout()
        self.fileLayout.addWidget(self.btnNew)
        self.fileLayout.addWidget(self.btnOpen)
        self.fileLayout.addWidget(self.btnSave)
        self.fileLayout.addWidget(self.btnSaveAs)
        self.fileLayout.addSpacing(10)
        self.fileLayout.addWidget(QLabel('ROWS:'))
        self.fileLayout.addWidget(self.lblNumOfRows)
        self.fileLayout.addSpacing(10)
        self.fileLayout.addWidget(QLabel('COLS:'))
        self.fileLayout.addWidget(self.lblNumOfCols)
        self.fileLayout.addSpacing(10)
        self.fileLayout.addWidget(QLabel('TYPE:'))
        self.fileLayout.addWidget(QLabel('SQUARE'))

        self.btnNew.clicked.connect(self.newScenarioClicked)

        self.btnPrevSlide = QPushButton("BACK")
        self.btnNextSlide = QPushButton("NEXT")
        self.txtCurSlide = QLineEdit(str(self.currentSlide))
        self.txtCurSlide.setFixedWidth(100)
        self.lblNumOfSlides = QLabel(str(self.numOfSlides))
        self.lblNumOfSlides.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.txtTimeIncrement = QLineEdit('0')
        self.txtTimeIncrement.setFixedWidth(100)
        self.txtTime = QLineEdit('0')
        self.txtTime.setFixedWidth(100)

        self.btnInsertSlide = QPushButton('Insert')
        self.btnAppendSlide = QPushButton('Append')
        self.btnAcceptSlide = QPushButton('Accept')
        self.btnDeleteSlide = QPushButton('Delete')

        self.txtCurSlide.editingFinished.connect(self.txtEditingFinished)
        self.txtTime.editingFinished.connect(self.time_change)
        self.btnPrevSlide.clicked.connect(self.prevSlideClicked)
        self.btnNextSlide.clicked.connect(self.nextSlideClicked)
        self.btnAppendSlide.clicked.connect(self.appendSlideClicked)
        self.btnAcceptSlide.clicked.connect(self.acceptSlideClicked)
        self.btnInsertSlide.clicked.connect(self.insert_clicked)
        self.btnDeleteSlide.clicked.connect(self.delete_clicked)

        self.controlBtnsLayout = QHBoxLayout()
        self.controlBtnsLayout.addWidget(self.btnPrevSlide)
        self.controlBtnsLayout.addWidget(self.btnNextSlide)
        self.controlBtnsLayout.addWidget(self.txtCurSlide)
        self.controlBtnsLayout.addWidget(QLabel('of'))
        self.controlBtnsLayout.addWidget(self.lblNumOfSlides)
        self.controlBtnsLayout.addStretch()
        self.controlBtnsLayout.addWidget(QLabel('timing inc'))
        self.controlBtnsLayout.addWidget(self.txtTimeIncrement)
        self.controlBtnsLayout.addWidget(QLabel('timing'))
        self.controlBtnsLayout.addWidget(self.txtTime)
        self.controlBtnsLayout.addStretch()
        self.controlBtnsLayout.addWidget(self.btnInsertSlide)
        self.controlBtnsLayout.addWidget(self.btnAppendSlide)
        self.controlBtnsLayout.addWidget(self.btnAcceptSlide)
        self.controlBtnsLayout.addWidget(self.btnDeleteSlide)

        self.mainLayout = QVBoxLayout()



        self.panelsLayout = QHBoxLayout()
        self.positionTable = QGridLayout()
        self.velocityTable = QGridLayout()

        self.positionLayout = QVBoxLayout()
        self.velocityLayout = QVBoxLayout()

        self.btnsPositionLayout = QHBoxLayout()
        self.btnsVelocityLayout = QHBoxLayout()

        self.txtPosition = QLineEdit('0')
        self.txtPosition.setFixedWidth(60)
        self.btnSetPosition = QPushButton('Set')
        self.btnSetPosition.clicked.connect(self.setPositionClicked)
        self.btnsPositionLayout.addWidget(self.txtPosition)
        self.btnsPositionLayout.addWidget(self.btnSetPosition)
        self.btnsPositionLayout.addStretch()

        self.txtVelocity = QLineEdit('0')
        self.txtVelocity.setFixedWidth(60)
        self.btnSetVelocity = QPushButton('Set')
        self.btnSetVelocity.clicked.connect(self.setVelocityClicked)
        self.btnsVelocityLayout.addWidget(self.txtVelocity)
        self.btnsVelocityLayout.addWidget(self.btnSetVelocity)
        self.btnsVelocityLayout.addStretch()

        self.positionLayout.addLayout(self.btnsPositionLayout)
        self.positionLayout.addLayout(self.positionTable)

        self.velocityLayout.addLayout(self.btnsVelocityLayout)
        self.velocityLayout.addLayout(self.velocityTable)

        self.panelsLayout.setProperty("gridLayout", "panelsLayout")
        self.panelsLayout.addLayout(self.positionLayout)
        self.panelsLayout.insertSpacing(1, 20)
        self.panelsLayout.addLayout(self.velocityLayout)
        #self.redrawPanels()

        self.btnDebug = QPushButton('Debug')
        self.btnDebug.clicked.connect(self.debug_clicked)
        self.btnProcess = QPushButton('Process')
        self.btnProcess.clicked.connect(self.generate_clicked)


        self.mainLayout.addLayout(self.fileLayout)
        self.mainLayout.addSpacing(5)
        self.mainLayout.addLayout(self.controlBtnsLayout)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addLayout(self.panelsLayout)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.btnDebug)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.btnProcess)

        self.setLayout(self.mainLayout)
        self.setWindowTitle('Scenario generator panel')
        self.show()

    def delete_clicked(self):
        slideIndex = int(self.txtCurSlide.text()) - 1
        self.currentSlide = slideIndex+1
        if slideIndex == 0 and self.scenario.get_num_of_slides() == 1:
            print('cant delete single slide')
            return
        elif slideIndex == 0:
            nextSlide = 1
        else:
            nextSlide = slideIndex - 1

        self.slide = self.scenario.get_slide(nextSlide)
        self.scenario.delete_slide(slideIndex)
        self.updateSlideNum()
        self.txtCurSlide.setText(str(slideIndex+1))
        self.lblNumOfSlides.setText(str(self.scenario.get_num_of_slides()))


    def insert_clicked(self):
        slideIndex = int(self.txtCurSlide.text())
        slide = deepcopy(self.scenario.get_slide(slideIndex-1))
        self.scenario.insert_slide(slideIndex, slide)

        self.slide = slide

        self.nextSlideClicked()
        self.lblNumOfSlides.setText(str(self.scenario.get_num_of_slides()))

    def save_clicked(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Scenario files (*.bsc)")
        if fileName:
            print(fileName)
            pickle.dump(self.scenario, open(fileName, "wb"))

    def open_clicked(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Scenario files (*.bsc)",)
        if fileName:
            print(fileName)
            self.scenario = pickle.load(open(fileName, "rb"))

            if self.scenario.get_rows() < 1 or self.scenario.get_cols() < 1:
                print('Wrong Scenario')
                return
            else:
                self.scenario.print_info()
                self.rows = self.scenario.get_rows()
                self.cols = self.scenario.get_cols()
                self.redrawPanels()

                slideIndex = 1
                slide = self.scenario.get_slide(slideIndex-1)
                self.txtCurSlide.setText(str(slideIndex))
                self.numOfSlides = self.scenario.get_num_of_slides()
                print("num os slides {0}".format(self.numOfSlides))
                self.lblNumOfSlides.setText(str(self.numOfSlides))

                if slide is not None:
                    self.slide = slide
                    self.slide.print()
                    self.txtTime.setText(str(self.slide.get_timing()))
                    for i in range(self.rows):
                        for j in range(self.cols):
                            self.listOfPos[i][j].setText(str(self.slide.get_position()[i][j]))
                            self.listOfVel[i][j].setText(str(self.slide.get_velocity()[i][j]))


    def debug_clicked(self):
        self.scenario.print_info()

    def generate_clicked(self):
        print('generate clicked')
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "txt scenario (*.txt)")
        if fileName:
            print(fileName)
            with open(fileName, 'w') as f:
                for slide in self.scenario.slides:
                    msg = ""
                    msg += str(slide.timing)
                    msg += ":"
                    for i in range(len(slide.get_position())):
                        for j in range(len(slide.get_position()[0])):
                            msg += str(slide.get_position()[i][j])
                            msg += ","
                            msg += str(slide.get_velocity()[i][j])
                            if j != (len(slide.get_position()[0]) - 1):
                                msg += ";"
                        if i != (len(slide.get_position()) - 1):
                            msg += '\n'
                    f.write(msg)

    def acceptSlideClicked(self):
        pass
    
    def appendSlideClicked(self):
        slideIndex = self.scenario.get_num_of_slides()
        self.timingIncrement = int(self.txtTimeIncrement.text())
        timing = self.scenario.get_slide(slideIndex-1).get_timing() + self.timingIncrement
        self.slide = deepcopy(self.scenario.get_slide(slideIndex-1))
        self.slide.set_timing(timing)
        self.scenario.append_slide(self.slide)

        self.txtTime.setText(str(timing))
        self.txtCurSlide.setText(str(slideIndex+1))
        self.lblNumOfSlides.setText(str(self.scenario.get_num_of_slides()))
        self.numOfSlides = self.scenario.get_num_of_slides()

        for i in range(self.rows):
            for j in range(self.cols):
                self.listOfPos[i][j].setText(str(self.slide.get_position()[i][j]))
                self.listOfVel[i][j].setText(str(self.slide.get_velocity()[i][j]))


    def time_change(self):
        slideIndex = int(self.txtCurSlide.text()) - 1
        slideTiming = int(self.txtTime.text())
        if slideIndex > 0:
            if slideTiming < self.scenario.get_slide(slideIndex-1).get_timing():
                print('wrong time')
                self.txtTime.setText(str(self.scenario.get_slide(slideIndex-1).get_timing()))
                return

            prevSlideTiming = self.scenario.get_slide(slideIndex).get_timing()
            deltaTiming = slideTiming - prevSlideTiming
            self.scenario.get_slide(slideIndex).set_timing(slideTiming)

            self.scenario.update_timings(startindex=slideIndex+1, delta=deltaTiming)

    def newScenarioClicked(self):
        dlg = CustomDialog(self)
        if dlg.exec_():
            print("Success!")
            print(dlg.txtColsNumber.text())
            print(dlg.txtRowsNumber.text())

            try:
                self.rows = int(dlg.txtRowsNumber.text())
                self.cols = int(dlg.txtColsNumber.text())

            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("????????????")
                msg.setInformativeText('?????????????? ???????????????? ????????????????')
                msg.setWindowTitle("????????????")
                msg.exec_()

            self.redrawPanels()
            self.init_scenario()
        else:
            print("Cancel!")

    def txtEditingFinished(self):
        self.currentSlide = int(self.txtCurSlide.text())
        print(self.txtCurSlide.text())

    def prevSlideClicked(self):
        self.currentSlide = int(self.txtCurSlide.text())
        if self.currentSlide > 1:
            self.currentSlide -= 1
        self.updateSlideNum()

    def nextSlideClicked(self):
        self.currentSlide = int(self.txtCurSlide.text())
        if self.currentSlide < self.numOfSlides:
            self.currentSlide += 1
        self.updateSlideNum()

    def updateNumOfSlides(self):
        self.lblNumOfSlides.setText(str(self.numOfSlides))

    def updateSlideNum(self):
        self.txtCurSlide.setText(str(self.currentSlide))
        #?????????????? ?????????? ???? ???????????????? ?? ?????????????????????? ?????? ???????????????????????????? ????????????
        slideIndex = int(self.txtCurSlide.text())-1

        slide = self.scenario.get_slide(slideIndex)
        if slide is not None:
            self.slide = slide
            self.slide.print()
            self.txtTime.setText(str(self.slide.get_timing()))
            for i in range(self.rows):
                for j in range(self.cols):
                    self.listOfPos[i][j].setText(str(self.slide.get_position()[i][j]))
                    self.listOfVel[i][j].setText(str(self.slide.get_velocity()[i][j]))
        else:
            print('?????????????? ???????????? ??????????')



    def redrawPanels(self):
        self.listOfPos = []
        self.listOfVel = []

        self.lblNumOfRows.setText(str(self.rows))
        self.lblNumOfCols.setText(str(self.cols))

        self.clearLayout(self.positionTable)
        self.clearLayout(self.velocityTable)



        for i in range(self.rows):
            tP = []
            tV = []
            for j in range(self.cols):
                lableP = QLineEdit('0')
                # lableP.classes = "cssPanelLabel"
                lableP.setProperty('cssPanelLabel', 'position')
                lableP.setFixedSize(40, 20)
                lableP.editingFinished.connect(lambda: self.position_updated(i, j))
                #lableP.mouseDoubleClicked.connect(lambda: self.panel_double_click(i, j, 'pos'))

                lableV = QLineEdit('100')
                lableV.setProperty('cssPanelLabel', 'velocity')
                lableV.setFixedSize(40, 20)
                lableV.editingFinished.connect(self.updatePanels)
                tP.append(lableP)
                tV.append(lableV)
            self.listOfPos.append(tP)
            self.listOfVel.append(tV)

        for i in range(self.rows):
            for j in range(self.cols):
                self.positionTable.addWidget(self.listOfPos[i][j], i+1, j)
                self.velocityTable.addWidget(self.listOfVel[i][j], i+1, j)



        self.currentSlide = 0
        self.txtCurSlide.setText(str(self.currentSlide+1))

    def panel_double_click(self, row, col, panel):
        if panel == 'pos':
            self.listOfPos[row][col].setText(str(self.lastPosEntered))

    def position_updated(self, row, col):
        self.lastPosEntered = int(self.listOfPos[row][col].text())
        self.updatePanels()

    def init_scenario(self):
        position = []
        velocity = []

        self.scenario = Scenario()
        self.scenario.set_cols(self.cols)
        self.scenario.set_rows(self.rows)

        for i in range(self.rows):
            tP = []
            tV = []
            for j in range(self.cols):
                tP.append(0)
                tV.append(0)
            position.append(tP)
            velocity.append(tV)

        self.slide.set_timing(0)
        self.slide.set_position(position)
        self.slide.set_velocity(velocity)
        self.scenario.set_slide(self.slide, 0)
        self.lblNumOfSlides.setText(str(self.scenario.get_num_of_slides()))

    def setPositionClicked(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.listOfPos[i][j].setText(self.txtPosition.text())

        self.updatePanels()

    def setVelocityClicked(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.listOfVel[i][j].setText(self.txtVelocity.text())

        self.updatePanels()

    def updatePanels(self):
        print("updating panels")
        try:
            self.slide.set_timing(int(self.txtTime.text()))
            for i in range(self.rows):
                for j in range(self.cols):
                    self.slide.position[i][j] = int(self.listOfPos[i][j].text())
                    self.slide.velocity[i][j] = int(self.listOfVel[i][j].text())
        except:
            print("error in updating")

        currentSlideIndex = int(self.txtCurSlide.text()) - 1
        self.scenario.set_slide(self.slide, currentSlideIndex)

        self.slide.print()

    def clearLayout(self, layout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            if not item:
                continue
            w = item.widget()
            if w:
                w.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Panel()
    sys.exit(app.exec_())
