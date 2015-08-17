#!/bin/usr/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import Qt
from ViewCocktails import Ui_RecipesWindow
from SQLiteConnector import SQLiteConnector

import sys

class ControlCocktail(QMainWindow):


   def __init__(self):
      super(ControlCocktail, self).__init__()
      self.ui = Ui_RecipesWindow()
      self.ui.setupUi(self)
      self.show()

      #Basic GUI done, setting up the ListWidget
      self.CURR_DATABASE = "cocktails"
      self.setupSignals()
      self.setupList()

   def searchCocktail(self, text):
      items = self.ui.cocktailListWidget.findItems(text,Qt.MatchContains)
      tempItemList = []
      if len(items) > 0 and text:
         for item in items:
            tempItemList.append(item.text())
         self.ui.cocktailListWidget.clear()
         self.ui.cocktailListWidget.addItems(tempItemList)
         self.ui.ingredientsLabel.setText("")
         self.ui.preparationLabel.setText("")
      else:
         self.ui.cocktailListWidget.clear()
         self.ui.cocktailListWidget.addItems(self.nameList)


   def setupSignals(self):
      self.ui.lineEdit.textChanged.connect(self.searchCocktail)
      self.ui.cocktailListWidget.currentItemChanged.connect(self.showTotalData)
      self.ui.cocktailListWidget.itemActivated.connect(self.showTotalData)
      self.ui.cocktailListWidget.itemChanged.connect(self.showTotalData)
      self.ui.cocktailListWidget.itemClicked.connect(self.showTotalData)

   def setupList(self):
      self.newConnector = SQLiteConnector(self.CURR_DATABASE)
      if not self.newConnector.connection:
         QMessageBox.critical(self,
               "Error",
               u'Cannot access the Database')
      else:
         nameQuery = self.newConnector.getNameData(self.CURR_DATABASE)
         self.nameList = []
         while nameQuery.next():
            self.nameList.append(nameQuery.value(0).toString())
         self.ui.cocktailListWidget.addItems(self.nameList)

   def showTotalData(self, listWidgetItem):
      try:
         currText = listWidgetItem.text()
         currIngredients = self.newConnector.getIngredients(self.CURR_DATABASE, currText)
         currPreparation = self.newConnector.getPreparation(self.CURR_DATABASE, currText)
         self.ui.ingredientsLabel.setText(currIngredients)
         self.ui.preparationLabel.setText(currPreparation)
      except:
         self.ui.ingredientsLabel.setText("")
         self.ui.preparationLabel.setText("")












def main():
   app = QApplication(sys.argv)
   newControlCocktail = ControlCocktail()
   sys.exit(app.exec_())

if __name__ == "__main__":
   main()
