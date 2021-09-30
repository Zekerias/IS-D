#!/usr/bin/python
#-*- coding:utf-8 -*-

#Interactive self-dictionary [IS-D]
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QMainWindow, \
 QLabel,QPushButton,QLineEdit,QComboBox,QMenu,QAction,qApp,\
     QListWidget,QListWidgetItem,QShortcut, QSystemTrayIcon
from PyQt5.QtCore import  Qt,QRectF,Qt
from PyQt5.QtGui import QFont,QPainterPath,QRegion,QKeySequence,QIcon
import sqlite3
from googletrans import Translator

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Electronic self-dictionary")
        self.setGeometry(1520, 440,400,600)
     #   self.setGeometry(1520, 440,400,600)
        self.setStyleSheet("background: rgba(10, 10, 10, 1)")
        
        ########################################################################
        #TrayMenu
        self.tray_icon = QSystemTrayIcon(QIcon("Icon/EI.png"), self)
        self.tray_icon.setToolTip(u'IS-D')
        self.tray_icon.setVisible(True)
        quit_action = QAction("Exit", self)
        quit_action
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.setFont(QFont('arials', 10))
        tray_menu.addAction(quit_action)
        tray_menu.setStyleSheet('background: #001111; color: green;border-radius: 4px')
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.tray_icon.activated.connect(self.onoff) 
        #Working place
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.Key = QLineEdit(self)
        self.Key.setGeometry(50,5,120,20)
        self.Key.setVisible(True)
        self.Key.setStyleSheet("border-radius:10px;background:#666666")
        self.Key.setFont(QFont('Times',13))
        self.Key.setToolTip("Enter a word in your native language")
        self.Key.setAlignment(Qt.AlignCenter)
        self.Word = QLineEdit(self)
        self.Word.setGeometry(230,5,120,20)
        self.Word.setVisible(True)
        self.Word.setStyleSheet("border-radius:10px;background: #666666;")
        self.Word.setFont(QFont('Times',13))
        self.Word.setAlignment(Qt.AlignCenter)
        self.Word.setToolTip('Enter a word in the selected language')
        self.LangClicked = QComboBox(self)
        self.LangClicked.setGeometry(5,0,45,40)
        self.LangClicked.setStyleSheet('''background:#2a7827;border-radius:10px;''')
        self.LangClicked.setVisible(True)
        self.LangClicked.setFocusPolicy(Qt.NoFocus)
        self.LangClicked.setToolTip('Select the language for which you are entering the translation')
        self.SettingsButton  = QPushButton('Del',self)
        self.SettingsButton.setFont(QFont('Times',13))
        self.SettingsButton.setGeometry(351,-1,40,41)
        self.SettingsButton.setStyleSheet('''QPushButton{
           border-radius:10px;
            border:2px solid #2a7827;
            background:#2a7827
           }
        QPushButton:pressed{
            background-color: black;
            border:2px solid #2a7827;
           }
            ''')

        self.SettingsButton.setVisible(True)
        self.SettingsButton.setToolTip('Settings')
        self.PlusButton = QPushButton('+',self)
        self.PlusButton.setFont(QFont('Arial', 20))
        self.PlusButton.setGeometry(180,0,40,40)
        self.PlusButton.setVisible(True)
        self.PlusButton.setToolTip('Add new translation')
        self.shortcut_add= QShortcut(QKeySequence(Qt.Key_Return),self)
        self.shortcut_add.activated.connect(self.AddNewTranslate)
        self.PlusButton.setStyleSheet('''
        QPushButton{
            border-radius:10px;
            border:2px solid #2a7827;
            background:#2a7827
            }
        QPushButton:pressed{
            background-color: black;
            border:2px solid #2a7827;
            }
            ''')

        self.Find = QLineEdit(self)
        
        self.Find.setGeometry(10,560,170,30)
        self.Find.setVisible(True)
        self.Find.setStyleSheet("border-radius:10px;box-shadow;background:#666666")
        self.Find.setFont(QFont('Times',15))
        self.Find.setAlignment(Qt.AlignCenter)
        self.Output = QLabel(self)
        self.Output.setAlignment(Qt.AlignCenter)
        self.Output.setGeometry(210,560,170,30)
        self.Output.setVisible(True)
        self.Output.setStyleSheet("border-radius:10px;box-shadow;background:#666666; text-align: center")
        self.Output.setFont(QFont('Times',15))
        radius = 10.0
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        self.ListBox = QListWidget(self)
        self.ListBox.setVisible(True)
        self.ListBox.setGeometry(0,40,400,510)
        self.ListBox.setFont(QFont('Times',15))
        self.ListBox.setFocusPolicy(Qt.NoFocus)
        self.ListBox.setStyleSheet('''QListWidget{
            color:white;background: rgba(10, 10, 10, 1);border:0px
            }
            QListWidget:pressed{
            background-color: black;
            border:2px solid #2a7827;
            }
            QListView::item:selected{
            border-radius:10px;
            border : 0px solid black;
            background : green;
            }
            QScrollBar{
                background:green;border-color:balck solid;
            }''')
       
#Process{

        self.PlusButton.clicked.connect(self.AddNewTranslate)

        self.SettingsButton.clicked.connect(self.Delete)
        self.LangClicked.addItem("EN")
        self.LangClicked.addItem("ES")
        self.LangClicked.addItem("EPO")
        self.LangClicked.currentIndexChanged.connect(self.selectionchange)
        
        self.MakeTranslate = QPushButton('T',self)
        self.MakeTranslate.setFont(QFont('Arial', 20))
        self.MakeTranslate.setGeometry(180,560,30,30)
        self.MakeTranslate.setVisible(True)
        self.MakeTranslate.setToolTip('Add new translation')
        self.MakeTranslate.clicked.connect(self.translation)
        self.shortcut_t= QShortcut(QKeySequence('Alt+T'),self)
        self.shortcut_t.activated.connect(self.translation)
        self.MakeTranslate.setStyleSheet('''
        QPushButton{
            border-radius:10px;
            border:2px solid #2a7827;
            background:#2a7827
            }
        QPushButton:pressed{
            background-color: black;
            border:2px solid #2a7827;
            }
            ''')
        
    def translation(self):
        translator = Translator(service_urls=['translate.google.com'])
        FindPlane=str(self.Find.text())
        print(FindPlane)
        trad = translator.translate(f'{FindPlane}',dest='ru')
        traductor= str(trad.text[:1].upper()+trad.text[1:])
        self.Output.setText(traductor)

    def selectionchange(self):
        global lang
        lang = self.LangClicked.currentText()

        cur.execute(f'SELECT keyword FROM data WHERE lang = "{lang}"')
        Data = cur.fetchall()
        self.ListBox.clear()
        for row in Data:
            rowdata=list(row)
            for item_text in rowdata:
                item = QListWidgetItem(item_text)
                item.setTextAlignment(Qt.AlignHCenter)
                self.ListBox.addItem(item)
        
    def AddNewTranslate(self):
        if str(self.Key.text()) != '':
            lewd = str(self.Key.text())
            print('Adding new word')
        else:
            print('Wrong word')
            return
            
        if str(self.Word.text()) !='':
            outlaw = str(self.Word.text())
            print('Adding new translation')
        else:
            print('Wrong translation')
            return
        
        cur.execute(f"""INSERT INTO data VALUES('{lewd}-{outlaw}','{lang}');""")
        conn.commit()
        Data = f'{lewd}-{outlaw}'
        item = QListWidgetItem(Data)
        item.setTextAlignment(Qt.AlignHCenter)
        self.ListBox.addItem(item)
        self.Key.clear()
        self.Word.clear()
    def Delete(self):
        listItems=self.ListBox.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.ListBox.takeItem(self.ListBox.row(item))
            deleteble = item.text()
            cur.execute("""SELECT keyword FROM data""")
            cur.execute(f"DELETE FROM data WHERE keyword = '{deleteble}';")
            conn.commit()

    def onoff(self):

        global flag
        if flag:
            self.hide() 
            flag = 0
        else:
            self.show()
            flag = 1
 
 

 
            
#       }

if __name__ == "__main__": 
    import sys
    global conn
    global cur
    global Data
    global state
    flag =  1
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    lang = 'EN'
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS data(
    keyword TEXT,
    lang TEXT);
    """)
    cur.execute(f"""SELECT keyword FROM data WHERE lang = '{lang}'""")
    Data = cur.fetchall()
    for row in Data:
        rowdata=list(row)
        for item_text in rowdata:
            item = QListWidgetItem(item_text)
            item.setTextAlignment(Qt.AlignHCenter)
            mw.ListBox.addItem(item)
    mw.show()
    sys.exit(app.exec())
   