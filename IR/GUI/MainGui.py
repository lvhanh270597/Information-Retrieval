import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from processor.ontology.Ontology import Ontology

from processor.searchEngine.searching import Searcher


class MainWindows(QMainWindow):

    def __init__(self):
        super().__init__()
        # app variable
        BASE_DIR = 'data/ontologies'
        self.onto_path = BASE_DIR + '/onto1.csv'
        self.ontology = Ontology.load_from_csv(self.onto_path)
        self.onto_variable = {}
        # init UI
        self.initMenuBar()
        widget = QWidget(self)
        # init 3 stack UI: search, web page, ontology
        self.stackedlayout = QStackedLayout(widget)
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.initStack1()
        self.initStack2()
        self.initstack3()
        self.stackedlayout.addWidget(self.stack1)
        self.stackedlayout.addWidget(self.stack2)
        self.stackedlayout.addWidget(self.stack3)
        self.stackedlayout.setCurrentIndex(0)
        #
        widget.setLayout(self.stackedlayout)
        self.setCentralWidget(widget)

        # edited by Hanh

        self.searcher = Searcher()
        ############################
    # init UI
    def initMenuBar(self):
        menu = self.menuBar()
        file = menu.addMenu('File')
        view = menu.addMenu('View')
        file.addAction("Open")
        file.addAction("Exit")
        view.addAction('Search')
        view.addAction('Web Page')
        view.addAction('Ontology')
        file.triggered[QAction].connect(self.processMenuBar)
        menu.triggered[QAction].connect(self.processMenuBar)
        status = self.statusBar()
        status.showMessage('Ready')
        # toolBar = self.addToolBar('File')
        pass

    def initStack1(self):
        stacklayout = QVBoxLayout()
        searchlayout = QHBoxLayout()
        viewlayout = QHBoxLayout()
        # search box and search button
        self.searchbox = QLineEdit()
        self.searchbox.setText('Trang Uyên')
        self.searchbutton = QPushButton('Search')
        self.searchbutton.clicked.connect(self.search)
        # right info label in search page
        self.infoLabel = QLabel()
        self.infoLabel.setText('Trang Uyên')
        self.infoLabel.setFixedWidth(300)
        self.infoLabel.setMaximumWidth(400)
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setAlignment(Qt.AlignTop)
        self.infoLabel.setStyleSheet("border: 1px inset grey;")
        # left result widget in search page
        self.resultlayout = QVBoxLayout()
        resultwidget = QWidget(self.stack1)
        resultwidget.setLayout(self.resultlayout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(resultwidget)
        # self.showResult()
        # add layout and widget
        searchlayout.addWidget(self.searchbox)
        searchlayout.addWidget(self.searchbutton)
        viewlayout.addWidget(scroll)
        viewlayout.addWidget(self.infoLabel)
        stacklayout.addLayout(searchlayout)
        stacklayout.addLayout(viewlayout)
        self.stack1.setLayout(stacklayout)
        pass

    def initStack2(self):
        stacklayout = QVBoxLayout()
        toolbarlayout = QHBoxLayout()
        self.webView = QWebEngineView()
        # toolbar
        self.urlbox = QLineEdit()
        backbutton = QPushButton()
        nextbutton = QPushButton()
        stopbutton = QPushButton()
        reloadbutton = QPushButton()
        homebutton = QPushButton()


        BASE_DIR = 'data/images'
        backbutton.setIcon(QIcon(BASE_DIR + '/back.png'))
        nextbutton.setIcon(QIcon(BASE_DIR + '/next.png'))
        stopbutton.setIcon(QIcon(BASE_DIR + '/stop.png'))
        reloadbutton.setIcon(QIcon(BASE_DIR + '/reload.png'))
        homebutton.setIcon(QIcon(BASE_DIR + '/home.png'))
        # connect signal to slot
        backbutton.clicked.connect(self.webView.back)
        nextbutton.clicked.connect(self.webView.forward)
        stopbutton.clicked.connect(self.webView.stop)
        reloadbutton.clicked.connect(self.webView.reload)
        homebutton.clicked.connect(self.gohome)

        self.urlbox.returnPressed.connect(self.loadurl)
        self.webView.urlChanged.connect(self.urlchanged)
        self.webView.loadProgress.connect(self.loadprocess)
        # add widget to layout
        toolbarlayout.addWidget(backbutton)
        toolbarlayout.addWidget(nextbutton)
        toolbarlayout.addWidget(stopbutton)
        toolbarlayout.addWidget(reloadbutton)
        toolbarlayout.addWidget(self.urlbox)
        toolbarlayout.addWidget(homebutton)
        toolbarlayout.addSpacing(50)
        # add layout and widget to main layout
        stacklayout.addLayout(toolbarlayout)
        stacklayout.addWidget(self.webView)
        self.stack2.setLayout(stacklayout)
        pass

    def initstack3(self):
        stacklayout = QVBoxLayout()
        centerlayout = QHBoxLayout()
        # left list word in ontology UI
        self.wordlistwidget = QListWidget()
        self.wordlistwidget.setSortingEnabled(True)
        self.wordlistwidget.setMaximumWidth(300)
        for w in self.ontology.onto:
            self.wordlistwidget.addItem(w)
        self.wordlistwidget.itemActivated.connect(self.showword)
        # right widget in ontology UI
        self.rightlayout = QVBoxLayout()
        rightwidget = QWidget()
        rightwidget.setLayout(self.rightlayout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(rightwidget)

        wordbox = QLineEdit()
        classbox = QComboBox()
        classbox.addItems(Ontology.Class)
        wordgroup = QGroupBox()
        form = QFormLayout()
        wordgroup.setLayout(form)
        form.setHorizontalSpacing(40)

        label = QLabel('Word')
        label1 = QLabel('Class')
        label.setFixedWidth(100)
        label1.setFixedWidth(100)
        self.onto_variable['Word'] = wordbox
        self.onto_variable['Class'] = classbox
        form.addRow(label, wordbox)
        form.addRow(label1, classbox)
        self.rightlayout.addWidget(wordgroup)
        # init ontology properties UI
        self.initOntoUI(self.rightlayout, 'Relation', Ontology.Relation)
        self.initOntoUI(self.rightlayout, 'Data Properties', Ontology.DataProperty)
        self.initOntoUI(self.rightlayout, 'PersonData', Ontology.PersonData)
        self.initOntoUI(self.rightlayout, 'BookData', Ontology.BookData)
        # init button in bottom ontology UI
        buttonlayout = QHBoxLayout()
        addbutton = QPushButton('ADD')
        deletebutton = QPushButton('DELETE')
        reasonerbutton = QPushButton('REASONER')
        savebutton = QPushButton('SAVE')
        clearbutton = QPushButton('CLEAR')

        addbutton.clicked.connect(self.addword)
        deletebutton.clicked.connect(self.deleteword)
        clearbutton.clicked.connect(self.clear)
        reasonerbutton.clicked.connect(self.reasoner)
        savebutton.clicked.connect(self.save)
        buttonlayout.addWidget(addbutton)
        buttonlayout.addWidget(deletebutton)
        buttonlayout.addWidget(reasonerbutton)
        buttonlayout.addWidget(savebutton)
        buttonlayout.addWidget(clearbutton)
        # add layout and widget to main layout
        centerlayout.addWidget(self.wordlistwidget)
        centerlayout.addWidget(scroll)
        stacklayout.addLayout(centerlayout)
        stacklayout.addLayout(buttonlayout)
        self.stack3.setLayout(stacklayout)
        pass

    def save():
        self.ontology.save2csv(self.onto_path)
        pass

    def initOntoUI(self, layout, name, list):
        form = QFormLayout()
        groupbox = QGroupBox(name)
        form.setHorizontalSpacing(40)
        maxlen = 0
        for i in list:
            if len(i) > maxlen:
                maxlen = len(i)
            textbox = QLineEdit()
            label = QLabel(i)
            label.setFixedWidth(100)
            form.addRow(label, textbox)
            self.onto_variable[i] = textbox

        groupbox.setLayout(form)
        layout.addWidget(groupbox)
        pass

    # end init UI
# =============== event function ==============
# stack1: event function in stack 1

    # action when click hyperlink in result label
    def clickLink(self, url):
        self.stackedlayout.setCurrentIndex(1)
        self.webView.setUrl(QUrl(checkurl(url)))
        self.urlbox.setText(url)
        #print(self.webView.url())
        # QDesktopServices.openUrl(QUrl(url))
        pass

    # action when mouse hover hyperlink in result label
    def hoveredLink(self, url):
        self.statusBar().showMessage(url)
        pass

    # action when click search button
    def search(self):
        clearLayout(self.resultlayout)

        # edited by Hanh

        query = self.searchbox.text()
        self.searcher.searching(query)
        results = self.searcher.getResults()

        self.showResult(results)
        self.showInfo(self.searcher.query)
        pass

    # show array of doc to result widget in search page
    def showResult(self, array=None):
        # array = [[doc1 title, doc1 url, doc1 preview],[doc2 title, doc2 url, doc2 preview],....]
        for doc in array:

            # groupbox = QGroupBox('%d' % (i+1))
            # grouplayout = QHBoxLayout()
            label = QLabel()
            label.setWordWrap(True)
            preview = doc[2].replace('\n', '<br>')
            label.setText("<a href='" + doc[1] + "'style='text-decoration:none'>"
                                                 "<font size='5'>" + doc[0] + "</font>"
                                                                              "</a>"
                                                                              "<p style='font-size:10pt'>" + preview + "</p>")
            # label.setToolTip('www.google.com')
            label.linkActivated.connect(self.clickLink)
            label.linkHovered.connect(self.hoveredLink)
            # grouplayout.addWidget(label)
            # groupbox.setLayout(grouplayout)
            # resultlayout.addWidget(groupbox)
            self.resultlayout.addWidget(label)
            self.resultlayout.addSpacing(20)
        pass

    # show infomation of word
    def showInfo(self, word):
        result = ''
        if word in self.ontology.onto:
            if self.ontology.onto[word]['Data']:
                result += "<font size='5'>" + word + "</font><p style='font-size:10pt'>"
                for i in range(len(Ontology.AllDataProperty)):
                    data = Ontology.AllDataProperty[i]
                    if data in self.ontology.onto[word]['Data']:
                        result += Ontology.AllDataName[i] + ': ' + self.ontology.onto[word]['Data'][data] + '<br>'
                result += '</p>'
        self.infoLabel.setText(result)
        pass

# stack 2: event function in stack 2
    # action when press enter in url text box
    def loadurl(self):
        #if url is None:
         #   url = self.urlbox.text()
        url = checkurl(self.urlbox.text())
        self.webView.setUrl(QUrl(url))
        pass

    # action when url of web page change (click link)
    def urlchanged(self, url):
        #print(url)
        self.urlbox.setText(url.toString())
        pass

    # action update status bar when web page is loading
    def loadprocess(self, load):
        self.statusBar().showMessage('Loading '+str(load)+'%')
        pass

    # action go to stack 1 (search page) when click home button
    def gohome(self):
        self.stackedlayout.setCurrentIndex(0)
        pass

    # action when choose in menu bar
    def processMenuBar(self, q):
        if q.text() == 'Exit':
            sys.exit()
        elif q.text() == 'Search':
            self.stackedlayout.setCurrentIndex(0)
        elif q.text() == 'Web Page':
            self.stackedlayout.setCurrentIndex(1)
        elif q.text() == 'Ontology':
            self.stackedlayout.setCurrentIndex(2)
        pass

# stack 3: event function in stack 3
    def addword(self):
        word = self.onto_variable['Word'].text()
        if word in self.ontology.onto:
            self.ontology.deleteWord(word)
        if word:
            self.ontology.initword(word, wclass=self.onto_variable['Class'].currentText())
            for rela in Ontology.Relation:
                list = self.onto_variable[rela].text()
                if list:
                    list = list.split(',')
                    for w in list:
                        self.ontology.addRelation(word, rela, w)
            for data in Ontology.AllDataProperty:
                value = self.onto_variable[data].text()
                if value:
                    self.ontology.addData(word, data, value)
            self.reloadlistword()
            #self.wordlistwidget.setCurrentItem(word)
        pass

    def showword(self, item):
        word = item.text()
        onto = self.ontology.onto[word]
        self.onto_variable['Word'].setText(word)
        if onto['Class'] in Ontology.Class:
            self.onto_variable['Class'].setCurrentText(onto['Class'])
        for rela in Ontology.Relation:
            if rela in onto['Relation']:
                self.onto_variable[rela].setText(','.join(onto['Relation'][rela]))
            else:
                self.onto_variable[rela].setText('')
        pass
        for data in Ontology.AllDataProperty:
            if data in onto['Data']:
                self.onto_variable[data].setText(onto['Data'][data])
            else:
                self.onto_variable[data].setText('')
        pass

    def deleteword(self):
        def msgbtn(i):
            if i.text()=='OK':
                self.ontology.deleteWord(word)
                self.reloadlistword()
                print(word)
            pass
        word = self.wordlistwidget.currentItem().text()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Bạn có muốn xóa từ " + word + " khỏi Ontology?")
        #msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Xóa từ")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(msgbtn)
        msg.exec_()
        pass

    def clear(self):
        for i in Ontology.AllDataProperty:
            self.onto_variable[i].setText('')
        for i in Ontology.Relation:
            self.onto_variable[i].setText('')
        self.onto_variable['Word'].setText('')
        pass

    def reasoner(self):
        self.ontology.reasoner()
        self.reloadlistword()
        self.clear()
        pass

    def reloadlistword(self):
        self.wordlistwidget.clear()
        self.wordlistwidget.addItems([i for i in self.ontology.onto])
        pass
# End Class


def clearLayout(layout):
    while layout.count() > 0:
        item = layout.takeAt(0)
        if not item:
            continue
        w = item.widget()
        if w:
            w.deleteLater()
    pass


def checkurl(url):
    if not str(url).startswith('http://'):
        return r'http://' + url
    return url
    pass

def run():
    root = QApplication(sys.argv)
    windows = MainWindows()
    windows.setWindowTitle('Algorithm IR System')
    windows.setGeometry(50, 50, 800, 500)
    windows.show()
    sys.exit(root.exec_())

