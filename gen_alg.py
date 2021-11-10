# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'genetic_algorithm.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from populacja import Populacja, ESelection, EMutation, ECross
from FitnessFunction import FitnessFunction
import matplotlib.pyplot as plt
import time



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(311, 470)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(100, 430, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.selectionMethodCombo = QtWidgets.QComboBox(Dialog)
        self.selectionMethodCombo.setGeometry(QtCore.QRect(10, 240, 291, 22))
        self.selectionMethodCombo.setObjectName("selectionMethodCombo")
        self.selectionMethodCombo.addItem("")
        self.selectionMethodCombo.addItem("")
        self.selectionMethodCombo.addItem("")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 220, 111, 16))
        self.label.setObjectName("label")
        self.populationAmount = QtWidgets.QLineEdit(Dialog)
        self.populationAmount.setGeometry(QtCore.QRect(10, 10, 291, 22))
        self.populationAmount.setObjectName("populationAmount")
        self.numberOfEpoch = QtWidgets.QLineEdit(Dialog)
        self.numberOfEpoch.setGeometry(QtCore.QRect(10, 70, 291, 22))
        self.numberOfEpoch.setText("")
        self.numberOfEpoch.setObjectName("numberOfEpoch")
        self.eliteStrategyAmount = QtWidgets.QLineEdit(Dialog)
        self.eliteStrategyAmount.setGeometry(QtCore.QRect(10, 100, 291, 22))
        self.eliteStrategyAmount.setObjectName("eliteStrategyAmount")
        self.crossProbability = QtWidgets.QLineEdit(Dialog)
        self.crossProbability.setGeometry(QtCore.QRect(10, 130, 291, 22))
        self.crossProbability.setObjectName("crossProbability")
        self.mutationProbability = QtWidgets.QLineEdit(Dialog)
        self.mutationProbability.setGeometry(QtCore.QRect(10, 160, 291, 22))
        self.mutationProbability.setObjectName("mutationProbability")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 300, 101, 16))
        self.label_2.setObjectName("label_2")
        self.crossMethodCombo = QtWidgets.QComboBox(Dialog)
        self.crossMethodCombo.setGeometry(QtCore.QRect(10, 320, 291, 22))
        self.crossMethodCombo.setObjectName("crossMethodCombo")
        self.crossMethodCombo.addItem("")
        self.crossMethodCombo.addItem("")
        self.crossMethodCombo.addItem("")
        self.crossMethodCombo.addItem("")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 350, 111, 16))
        self.label_3.setObjectName("label_3")
        self.mutationMethodCombo = QtWidgets.QComboBox(Dialog)
        self.mutationMethodCombo.setGeometry(QtCore.QRect(10, 370, 291, 22))
        self.mutationMethodCombo.setObjectName("mutationMethodCombo")
        self.mutationMethodCombo.addItem("")
        self.mutationMethodCombo.addItem("")
        self.mutationMethodCombo.addItem("")
        self.inversionProbability = QtWidgets.QLineEdit(Dialog)
        self.inversionProbability.setGeometry(QtCore.QRect(10, 190, 291, 22))
        self.inversionProbability.setObjectName("inversionProbability")
        self.numberOfBits = QtWidgets.QLineEdit(Dialog)
        self.numberOfBits.setGeometry(QtCore.QRect(10, 40, 291, 22))
        self.numberOfBits.setObjectName("numberOfBits")
        self.maximizationCheckBox = QtWidgets.QCheckBox(Dialog)
        self.maximizationCheckBox.setGeometry(QtCore.QRect(10, 400, 111, 20))
        self.maximizationCheckBox.setObjectName("maximizationCheckBox")
        self.selectionParameter = QtWidgets.QLineEdit(Dialog)
        self.selectionParameter.setGeometry(QtCore.QRect(10, 270, 291, 22))
        self.selectionParameter.setObjectName("selectionParameter")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(lambda: self.runGen(int(self.numberOfEpoch.text()),int(self.populationAmount.text()), float(self.selectionParameter.text()))) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def generateFiles(self, epoki):
        values = []
        bestValues = []
        means = []
        standardDeviations = []
        f = FitnessFunction()
        for populacja in epoki:
            for osobnik in populacja.population:
                decoded = osobnik.decode(f.a, f.b, f.a, f.b)
                #wartości funkcji dla każdego osobnika w danej populacji
                values.append(f.value(decoded[0], decoded[1]))
            else:
                #najlepsza wartość funkcji dla danej populacji
                best = populacja.findBest().decode(f.a, f.b, f.a, f.b)
                bestValues.append(f.value(best[0], best[1]))
                #średnia wartość funkcji dla danej populacji
                means.append(sum(values)/len(values))
                nominator = 0
                for value in values:
                    nominator += pow(value - means[-1], 2)
                #odchylenie standardowe dla danej populacji
                standardDeviations.append(pow(nominator/len(values), 0.5))
                values.clear()

        bestValuesFile = open("best_values.txt", "w")
        meansFile = open("means.txt", "w")
        standardDeviationsFile = open("standard_deviations.txt", "w")
        for i in range(len(bestValues)):
            bestValuesFile.write(str(i) + ": " + str(bestValues[i]) + "\n")
            meansFile.write(str(i) + ": " + str(means[i]) + "\n")
            standardDeviationsFile.write(str(i) + ": " + str(standardDeviations[i]) + "\n")

        bestValuesFile.close()
        meansFile.close()
        standardDeviationsFile.close()

        plt.plot(bestValues)
        plt.title("DROP-WAVE FUNCTION - best values per iteration")
        plt.xlabel('Iterations')
        plt.ylabel('Best values')
        plt.savefig("best_values.png")
        plt.clf()
        plt.cla()

        plt.plot(means)
        plt.title("DROP-WAVE FUNCTION - mean values per iteration")
        plt.xlabel('Iterations')
        plt.ylabel('Means')
        plt.savefig("means.png")
        plt.clf()
        plt.cla()

        plt.plot(standardDeviations)
        plt.title("DROP-WAVE FUNCTION - standard deviations per iteration")
        plt.xlabel('Iterations')
        plt.ylabel('Standard deviations')
        plt.savefig("standard_deviations.png")
        plt.clf()
        plt.cla()


    def runGen(self, epNo, poNo, selPar):
        print("poczatek testu")
        epoki=[]
        startTime = time.time()
        for e in ESelection:
            if (e.value == self.selectionMethodCombo.currentIndex()+1):
                selectionMethod = e
        for e in ECross:
            if (e.value == self.crossMethodCombo.currentIndex()+1):
                crossMethod = e
        for e in EMutation:
            if (e.value == self.mutationMethodCombo.currentIndex()+1):
                mutationMethod = e

        for x in range(epNo):
            if x == 0:
                epoki.append(Populacja(poNo, int(self.numberOfBits.text())))
            else:
                epoki.append(epoki[x - 1]
                             .nowa_epoka(selectionMethod,
                                         selPar,
                                         crossMethod,
                                         float(self.crossProbability.text()),
                                         mutationMethod,
                                         float(self.mutationProbability.text()),
                                         float(self.inversionProbability.text()),
                                         int(self.eliteStrategyAmount.text())))
        endTime = time.time()
        self.generateFiles(epoki)
        best = epoki[epNo-1].findBest()
        f = FitnessFunction()
        decoded = best.decode(f.a, f.b, f.a, f.b)
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Message")
        messageBox.setText("Solution: " + str(f.value(decoded[0], decoded[1])) + "\nFound at: x = ("
                           + str(int(decoded[0])) + ", " + str(int(decoded[1])) +")\nReal values: " +
                           str(decoded[0]) + ", " + str(decoded[1]) + "\nExecution time: " + str(endTime-startTime))
        messageBox.exec_()


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.selectionMethodCombo.setItemText(0, _translate("Dialog", ESelection.BEST.name))
        self.selectionMethodCombo.setItemText(1, _translate("Dialog", ESelection.ROULETTE.name))
        self.selectionMethodCombo.setItemText(2, _translate("Dialog", ESelection.TOURNAMENT.name))
        self.label.setText(_translate("Dialog", "Selection method:"))
        self.populationAmount.setPlaceholderText(_translate("Dialog", "Population amount"))
        self.numberOfEpoch.setPlaceholderText(_translate("Dialog", "Epoch number"))
        self.eliteStrategyAmount.setPlaceholderText(_translate("Dialog", "Elite strategy amount"))
        self.crossProbability.setPlaceholderText(_translate("Dialog", "Cross probability"))
        self.mutationProbability.setPlaceholderText(_translate("Dialog", "Mutation probability"))
        self.label_2.setText(_translate("Dialog", "Cross method:"))
        self.crossMethodCombo.setItemText(0, _translate("Dialog", ECross.ONEPOINT.name))
        self.crossMethodCombo.setItemText(1, _translate("Dialog", ECross.TWOPOINT.name))
        self.crossMethodCombo.setItemText(2, _translate("Dialog", ECross.TREEPOINT.name))
        self.crossMethodCombo.setItemText(3, _translate("Dialog", ECross.HOMOGENOUS.name))
        self.label_3.setText(_translate("Dialog", "Mutation method:"))
        self.mutationMethodCombo.setItemText(0, _translate("Dialog", EMutation.ONEPOINT.name))
        self.mutationMethodCombo.setItemText(1, _translate("Dialog", EMutation.TWOPOINT.name))
        self.mutationMethodCombo.setItemText(2, _translate("Dialog", EMutation.EDGE.name))
        self.inversionProbability.setPlaceholderText(_translate("Dialog", "Inversion probability"))
        self.numberOfBits.setPlaceholderText(_translate("Dialog", "Number of bits"))
        self.maximizationCheckBox.setText(_translate("Dialog", "Maximization"))
        self.selectionParameter.setPlaceholderText(_translate("Dialog", "Selection parameter"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


