from PyQt4 import QtCore, QtGui

from discordRPC import DiscordRPC
import lobby, game

class AIOMainWindow(QtGui.QMainWindow):
    ao_app = None
    def __init__(self, _ao_app, _discordRPC):
        super(AIOMainWindow, self).__init__()
        self.ao_app = _ao_app
        self.discordRPC = _discordRPC

        self.stackwidget = QtGui.QStackedWidget(self)
        self.lobbywidget = lobby.lobby(_ao_app)
        self.gamewidget = game.GameWidget(_ao_app)

        self.setCentralWidget(self.stackwidget)
        self.stackwidget.addWidget(self.lobbywidget)
        self.stackwidget.addWidget(self.gamewidget)
        self.setWindowTitle("Attorney Investigations Online")
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.showServers()

    def startGame(self):
        size = self.gamewidget.size()
        self.gamewidget.startGame()
        self.stackwidget.setCurrentWidget(self.gamewidget)
        self.setFixedSize(size)
        self.center()
        # reset time and set status to 'in game'
        joined_server = self.lobbywidget.server[0]
        self.discordRPC.set_details('In Game')
        self.discordRPC.set_state(joined_server)
        self.discordRPC.reset_time()

    def stopGame(self):
        self.gamewidget.stopGame()
        self.showServers()

    def showServers(self):
        size = self.lobbywidget.size()
        self.lobbywidget.showServers()
        self.stackwidget.setCurrentWidget(self.lobbywidget)
        self.setFixedSize(size)
        self.center()

        # initialize discordRPC and/or change status to in lobby
        # idk why on showServers but this is called when you go to lobby (so when you load
        # up the game or rq) therefore it works maybe
        if self.ao_app.rpc:
            if not self.discordRPC.initialized:
                self.discordRPC.connect()
            self.discordRPC.set_details('In Lobby')
            self.discordRPC.set_state('')
            self.discordRPC.reset_time()
            if not self.discordRPC.running:
                self.discordRPC.run_loop()
        else:
            self.discordRPC.close()

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
