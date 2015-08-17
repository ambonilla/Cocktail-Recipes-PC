#!/bin/usr/env/ python
# -*- coding: utf-8 -*-

from PyQt4.QtSql import *

class SQLiteConnector:

   def __init__(self, filename):
      self.db = QSqlDatabase.addDatabase("QSQLITE")
      self.dbName = filename
      self.db.setDatabaseName(self.dbName)
      self.openDB()

   def openDB(self):
      if not self.db.open():
         self.connection = False
      else:
         self.connection = True

   def getTableNames(self):
      if self.connection:
         query = QSqlQuery()
         query.prepare("SELECT name FROM sqlite_master WHERE type='table'")
         output = query.exec_()
         if output:
            tableNames = []
            while query.next():
               tableNames.append(query.value(0).toString())
            return tableNames
         else:
            print query.lastQuery()
            print "@ getTables"
            print query.lastError().text()


   def getColumnNames(self, tableName):
      if self.connection:
         query = QSqlQuery()
         query.prepare("PRAGMA table_info(" + tableName + ")")
         output = query.exec_()
         if output:
            self.columnsList = []
            while query.next():
               self.columnsList.append(query.value(1).toString())
            return self.columnsList
         else:
            print query.lastQuery()
            print "@ getColumnNames"
            print query.lastError().text()

   def getCompleteData(self, tableName):
      if self.connection:
         query = QSqlQuery()
         queryStr = "SELECT "
         for x in self.columnsList:
            queryStr += " " + x + ","
         queryStr = queryStr[:-1] + " FROM " + tableName
         query.prepare(queryStr)
         output = query.exec_()

         if output:
            return query

         else:
            print query.lastQuery()
            print "@ getCompleteData"
            print query.lastError().text()

   def getNameData(self, tableName):
      if self.connection:
         query = QSqlQuery()
         queryStr = "SELECT `name` FROM " + tableName + " ORDER BY `name` ASC"
         query.prepare(queryStr)
         output = query.exec_()

         if output:
            return query

         else:
            print query.lastQuery()
            print "@ getNameData"
            print query.lastError().text()


   def getIngredients(self, tableName, name):
      if self.connection:
         query = QSqlQuery()
         queryStr = "SELECT `ingredients` FROM " + tableName + " WHERE `name` = ?"
         query.prepare(queryStr)
         query.addBindValue(name)
         output = query.exec_()

         if output:
            query.next()
            return query.value(0).toString()

         else:
            print query.lastQuery()
            print "@ getNameData"
            print query.lastError().text()


   def getPreparation(self, tableName, name):
      if self.connection:
         query = QSqlQuery()
         queryStr = "SELECT `description` FROM " + tableName + " WHERE `name` = ?"
         query.prepare(queryStr)
         query.addBindValue(name)
         output = query.exec_()

         if output:
            query.next()
            return query.value(0).toString()

         else:
            print query.lastQuery()
            print "@ getNameData"
            print query.lastError().text()


