#!/usr/bin/python
#-*- coding:utf-8 -*-

#Interactive self-dictionary [IS-D]
from PyQt5.QtWidgets    import QApplication, QListWidgetItem, QMainWindow, \
    QLabel,QPushButton,QLineEdit,QComboBox,QMenu,QAction,qApp,QApplication,QInputDialog,\
     QListWidget,QListWidgetItem,QShortcut, QSystemTrayIcon,QWidget,QDesktopWidget
from PyQt5.QtCore       import  Qt,QRectF,Qt,QSize,QFile
from PyQt5.QtGui        import QFont,QPainterPath,QRegion,QKeySequence,QIcon,QValidator,QFontDatabase,QPixmap
from googletrans        import Translator
import sqlite3
import sys
import configparser
import json
class Validator(QValidator):
    def validate(self, string, pos):
        return QValidator.Acceptable, string.upper(), pos
class MainWindow(QMainWindow):
    def __init__(self):
        global LC#ComboBox external func
        QMainWindow.__init__(self)
        self.setMaximumSize(400,600)
        self.setMinimumSize(400,600)
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)
        self.setWindowTitle("Interactive self-dictionary")
        self.setStyleSheet("background: rgb(10, 10, 10)")
        self.setWindowIcon(QIcon('Resources/dict.png'))
        ########################################################################
        #TrayMenu
        self.tray_icon = QSystemTrayIcon(QIcon("Resources/dict.png"), self)
        self.tray_icon.setToolTip(u'IS-D')
        self.tray_icon.setVisible(True)
        lang_action = QAction("Primary Language", self)
        lang_list = QAction("List of languages", self)
        quit_action = QAction("Exit", self)
        lang_action.triggered.connect(self.newwidnow)
        lang_list.triggered.connect(self.LanguageList)    
        quit_action.triggered.connect(qApp.quit)  
        tray_menu = QMenu()
        tray_menu.setFont(QFont('asi', 10))
        tray_menu.addAction(lang_action)
        tray_menu.addAction(lang_list)
        tray_menu.addAction(quit_action)
        tray_menu.setStyleSheet('background: #001111; color: green;border-radius: 2px')
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.onoff) 
        #Working place
        self.Key = QLineEdit(self)
        self.Key.setGeometry(50,5,120,30)
        self.Key.setVisible(True)
        self.Key.setStyleSheet("color: green;border-radius:10px;border:2px solid purple;background:black")
        self.Key.setFont(QFont('Times bold',13))
        self.Key.setToolTip("Enter a word in your native language")
        self.Key.setAlignment(Qt.AlignCenter)
        self.Word = QLineEdit(self)
        self.Word.setGeometry(230,5,120,30)
        self.Word.setVisible(True)
        self.Word.setStyleSheet("color: green;border-radius:10px;border:2px solid purple;background:black")
        self.Word.setFont(QFont('Times bold',13))
        self.Word.setAlignment(Qt.AlignCenter)
        self.Word.setToolTip('Enter a word in the selected language')
        self.Find = QLineEdit(self)
        self.Find.setGeometry(10,560,170,30)
        self.Find.setVisible(True)
        self.Find.setStyleSheet("color: green;border-radius:10px;border:2px solid purple;background:black")
        self.Find.setFont(QFont('Times bold',13))
        self.Find.setAlignment(Qt.AlignCenter)
        self.Output = QLabel(self)
        self.Output.setAlignment(Qt.AlignCenter)
        self.Output.setGeometry(220,560,170,30)
        self.Output.setVisible(True)
        self.Output.setStyleSheet("color: green;border-radius:10px;border:2px solid purple;background:black")
        self.Output.setFont(QFont('Times bold',13))
        self.Lang_Clicked = QComboBox(self)
        self.Lang_Clicked.setGeometry(5,0,45,40)
        self.Lang_Clicked.setStyleSheet('''color:black;background:#2a7827;border-radius:10px;''')
        self.Lang_Clicked.setVisible(True)
        self.Lang_Clicked.setFont(QFont('Times bold',9))
        self.Lang_Clicked.setFocusPolicy(Qt.NoFocus)
        self.Lang_Clicked.setToolTip('Select the language for which you are entering the translation')
        self.Delete_Button  = QPushButton(self)
        self.Delete_Button.setFont(QFont('asi',13))
        self.Delete_Button.setGeometry(351,-1,40,41)
        self.Delete_Button.setIcon(QIcon('Resources/delete.png'))
        self.Delete_Button.setIconSize(QSize(35,35))
        self.Delete_Button.setStyleSheet('''QPushButton{
            border-radius:10px;
            border:2px solid #2a7827;
            background:#2a7827
           }
        QPushButton:pressed{
            background-color: black;
            border:2px solid #2a7827;
           }
            ''')
        self.Delete_Button.setVisible(True)
        self.Delete_Button.setToolTip('Delete selected words')
        self.PlusButton = QPushButton('+',self)
        self.PlusButton.setFont(QFont('Arial', 20))
        self.PlusButton.setGeometry(180,0,40,40)
        self.PlusButton.setVisible(True)

        self.PlusButton.setToolTip('Add new translation')
        self.shortcut_add= QShortcut(QKeySequence(Qt.Key_Return),self)
        self.shortcut_add.activated.connect(self.Add_New_Translate)
        self.PlusButton.setStyleSheet('''
        QPushButton{
            color:black;
            border-radius:10px;
            border:2px solid #2a7827;
            background:#2a7827
            }
        QPushButton:pressed{
            background-color: black;
            border:2px solid #2a7827;
            }
            ''')
        radius = 10.0
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        self.List_Widget = QListWidget(self)
        self.List_Widget.setVisible(True)
        self.List_Widget.setGeometry(0,40,400,510)
        self.List_Widget.setFont(QFont('Times bold',15))
        self.List_Widget.setFocusPolicy(Qt.NoFocus)
        self.List_Widget.setStyleSheet('''QListWidget{
            color:green;background: rgb(10, 10, 10);border:0px
            }
            QListWidget:pressed{
            
            background-color: black;
            border:2px solid #2a7827;
            }
            QListView::item:selected{
            color:black;
            border-radius:10px;
            border : 0px solid black;
            background : green;
            }
            QScrollBar{
                background:green;border-color:balck solid;
            }''')
        self.PlusButton.clicked.connect(self.Add_New_Translate)
        self.Delete_Button.clicked.connect(self.Delete)
        LC = self.Lang_Clicked
        self.Lang_Clicked.currentIndexChanged.connect(self.selection_change)
        self.Make_Translate = QPushButton(self)
        self.Make_Translate.setFont(QFont('Arial', 20))
        self.Make_Translate.setGeometry(185,560,30,30)
        self.Make_Translate.setVisible(True)
        self.Make_Translate.setToolTip('Add new translation')
        self.Make_Translate.clicked.connect(self.translation)
        self.Make_Translate.setIcon(QIcon('Resources/translate.png'))
        self.Make_Translate.setIconSize(QSize(35, 35))
        self.shortcut_t= QShortcut(QKeySequence('Alt+T'),self)
        self.shortcut_t.activated.connect(self.translation)
        self.Make_Translate.setStyleSheet('''
        QPushButton{
            color:whire;
            border-radius:10px;
            border:2px solid #2a7827;
            background:#2a7827
            }
        QPushButton:pressed{
            background-color: black;
            border:2px solid #2a7827;
            }
            ''')
 #Process{
    #Translate Button
    def translation(self):
        try:
            translator = Translator(service_urls=['translate.google.com','translate.googleapis.com'])
            FindPlane=str(self.Find.text())
            trad = translator.translate(f'{FindPlane}',dest=f'{lang_destinition}')
            traductor= str(trad.text[:1].upper()+trad.text[1:])
            self.Output.setText(traductor)
        except:
            pass
    #Combobox(DON`T TOUCH, I`l DON`T KNOW HOW THIS WORKS, BUT THIS WORKS IT JUST WORKS)
    def selection_change(self):
        global lang
        global cur
        global conn
        lang = self.Lang_Clicked.currentText()
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS data(
        keyword TEXT,
        lang TEXT);
        """)
        cur.execute(f'SELECT keyword FROM data WHERE lang = "{lang}"')
        Data = cur.fetchall()
        self.List_Widget.clear()    
        for row in Data:
            row_data=list(row)
            for item_text in row_data:
                item = QListWidgetItem(item_text)
                item.setTextAlignment(Qt.AlignHCenter)
                self.List_Widget.addItem(item)
    #Button to add Wprd + Translate to Database and List_Widget
    def Add_New_Translate(self):
        if str(self.Key.text()) != '':
            lewd = str(self.Key.text())
        else:
            return
            
        if str(self.Word.text()) !='':
            outlaw = str(self.Word.text())
        else:
            return


        cur.execute(f"""INSERT INTO data VALUES('{lewd}-{outlaw}','{lang}');""")
        conn.commit()
        Data_Now = f'{lewd}-{outlaw}'
        item = QListWidgetItem(Data_Now)
        item.setTextAlignment(Qt.AlignHCenter)
        self.List_Widget.addItem(item)
        self.Key.clear()
        self.Word.clear()
    #Button and shortcut function to delete item on button DEL
    def Delete(self):
        listItems=self.List_Widget.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.List_Widget.takeItem(self.List_Widget.row(item))
            deleteble = item.text()
            cur.execute("""SELECT keyword FROM data""")
            cur.execute(f"DELETE FROM data WHERE keyword = '{deleteble}';")
            conn.commit()
    #Click to hide window
    def onoff(self,reason):
        if reason == QSystemTrayIcon.Trigger:
            global flag
            if flag:
                self.hide() 
                flag = 0
            else:
                self.show()
                flag = 1
    #Change main language window
    def newwidnow(self):
        global lang_destinition
        config = configparser.ConfigParser()
        dialog = QInputDialog(self)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle('Primary language')
        dialog.setLabelText("""Set your primary language like 
        'EN' to English or 'ES' for Spanish:""")
        dialog.setStyleSheet('background:black;color:#2a7827')
        dialog.setFont(QFont('asi',20))
        dialog.setGeometry(900,400,40,40)
        lineEdit = dialog.findChild(QLineEdit)
        lineEdit.setPlaceholderText(f'Defalut {lang_destinition}')
        lineEdit.setStyleSheet('color:#2a7827')
        
        if dialog.exec_():
            try:
                lang_destinition = dialog.textValue()
                if dialog.textValue() == '':
                    lang_destinition = 'EN'
                    config['Language'] = {'PrimaryLanguage': f'{lang_destinition}'}
                    with open('config.ini', 'w') as configfile:
                        config.write(configfile)
                else:
                    config['Language'] = {'PrimaryLanguage': f'{lang_destinition}'}
                    with open('config.ini', 'w') as configfile:
                        config.write(configfile)
            except:
                return
    #Function to another class
    def LanguageList(self):
        self.w = LL()
#       } 
#Second Window for change languages in combobox
class LL(QWidget):
    def __init__(self):
        super().__init__()
        label_Logo = QLabel(self)
        pixmap = QPixmap('Resources/Logo.png')
        label_Logo.setPixmap(pixmap)
        label_Logo.setGeometry(100,130,100,60)
        self.setWindowIcon(QIcon('Resources/dict.png'))
        self.setGeometry(600,300,200,200)
        self.show()
        self.setWindowTitle("Select lang")
        self.setMaximumSize(200,200)
        self.setMinimumSize(200,200)
        self.setStyleSheet("background: rgb(10, 10, 10)")
        self.List_Lang = QListWidget(self)
        self.List_Lang.setVisible(True)
        self.List_Lang.setGeometry(0,0,100,200)
        self.List_Lang.setFont(QFont('Times bold',15))
        self.List_Lang.setFocusPolicy(Qt.NoFocus)
        self.List_Lang.setStyleSheet('''QListWidget{
            font-family:asi;
            color:green;background: 
            rgb(10, 10, 10);border:4px solid purple;
            }
            QListWidget:pressed{
            
            background-color: black;
            border:2px solid #2a7827;
            }
            QListView::item:selected{
            color:black;
            border-radius:10px;
            border : 0px solid black;
            background : green;
            }
            QScrollBar{
                background:green;border-color:balck solid;
            }''')
        self.List_Lang.clear()    
        try:
            row_data=json_langs['languages']
            for item_text in row_data:
                item = QListWidgetItem(item_text)
                item.setTextAlignment(Qt.AlignHCenter)
                self.List_Lang.addItem(item)
        except:
            pass
        self.Add_Place = QLineEdit(self)

        self.Add_Place.setGeometry(100,0,100,30)
        self.Add_Place.setVisible(True)
        self.Add_Place.setStyleSheet("font-family:Times bold;color: green;border-radius:10px;border:2px solid purple;background:black")
        self.Add_Place.setFont(QFont('Times bold',13))
        self.Add_Place.setAlignment(Qt.AlignCenter)
        self.shortcut_add_place= QShortcut(QKeySequence(Qt.Key_Return),self)
        self.shortcut_add_place.activated.connect(self.lang_adds)
        self.Add_Place.setPlaceholderText(f'Like EN')
        self.validator = Validator(self)
        self.Add_Place.setValidator(self.validator)
        self.Add_Place.setMaxLength(2)
        self.Add_Value= QPushButton('ADD',self)
        self.Add_Value.setGeometry(100,30,100,40)
        self.Add_Value.setVisible(True)
        self.Add_Value.setFont(QFont('Times bold', 13))
        self.Add_Value.setStyleSheet('''
        QPushButton{
            color:whire;
            border-radius:10px;
            border:2px solid #2a7827;
            background:#2a7827
            }
        QPushButton:pressed{
            background-color: black;
            border:2px solid #2a7827;
            }
            ''')
        self.Add_Value.clicked.connect(self.lang_adds)
        self.Delete_Value = QPushButton('DEL',self)
        self.Delete_Value.setFont(QFont('Times bold', 13))
        self.Delete_Value.setVisible(True)
        self.Delete_Value.setGeometry(100,80,100,40)
        self.Delete_Value.setStyleSheet('''
        QPushButton{
            color:whire;
            border-radius:10px;
        border:2px solid #2a7827;
            background:#2a7827
            }
        QPushButton:pressed{
            background-color: black;
            border:2px solid #2a7827;
            }
            ''')
        self.Delete_Value.clicked.connect(self.lang_dels)

    def lang_adds(self):
        #Languages need to write in ISO 639-1 code format
        try:
            text = self.Add_Place.text()
            if text != '':
                item = QListWidgetItem(text)
                item.setTextAlignment(Qt.AlignHCenter)
                self.List_Lang.addItem(item)
                LC.addItem(text)
                json_langs['languages'].append(text)
                with open('Langs_array.json', 'w') as jsoner:
                    json.dump(json_langs, jsoner)
                self.Add_Place.clear()
            else:
                return
        except:
            return
    def lang_dels(self):
        Text_list=self.List_Lang.currentItem().text()
        Index_json=json_langs['languages'].index(Text_list)
        json_langs['languages'].pop(Index_json)
        with open('Langs_array.json', 'w') as jsoner:
            json.dump(json_langs, jsoner)
        LC.clear()
        LC.addItems(json_langs['languages'])
        self.List_Lang.clear()
        row_data=json_langs['languages']
        for item_text in row_data:
            item = QListWidgetItem(item_text)
            item.setTextAlignment(Qt.AlignHCenter)
            self.List_Lang.addItem(item)

if __name__ == "__main__": 
    global conn
    global cur
    global Data
    global state
    global lang_destinition
    global json_langs
    flag =  1
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    config = configparser.ConfigParser()
    config.read('config.ini')
    lang_destinition = config['Language']['primarylanguage']
    try:
        with open("Langs_array.json", "r") as read_file:
            json_langs = json.load(read_file)
    except:
        data_set = {"languages": ["EN"]}
        with open('Langs_array.json', 'w') as jsoner:
                json.dump(data_set, jsoner)
        with open("Langs_array.json", "r") as read_file:
            json_langs = json.load(read_file)
    LC.addItems(json_langs['languages'])
    cur.execute(f"""SELECT keyword FROM data WHERE lang = '{lang}'""")
    sys.exit(app.exec())
   
