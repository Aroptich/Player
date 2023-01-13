import sys
import os
import time
from playsound import playsound
from media import Ui_MainWindow
from PyQt5.QtCore import QUrl, QUrlQuery, QMimeData
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.func_btns() # Инициализация метода с функцианалом кнопок
        self.player = QMediaPlayer() # Инициализация класса QMediaPlayer
        self.state = "Play" # Просто переменная
        self.playlist = [] #Список с url-адресами треков
        self.position = 0 # Позиция

        self.player.durationChanged.connect(self.duration)# Получение сигнала от воспроизводимого трека(продолжительность)
        self.player.durationChanged.connect(self.volume)# Получение сигнала от воспроизводимого трека(громкость)
        self.player.durationChanged.connect(self.duration)

    def func_btns(self):
        self.ui.add_btn.clicked.connect(self.file_open)
        self.ui.play_btn.pressed.connect(self.play)
        self.ui.pause_btn.pressed.connect(self.pause)
        self.ui.stop_btn.clicked.connect(self.stop)
        self.ui.slider_volume.valueChanged.connect(self.volume)
        self.ui.slider_volume.setMinimum(0)
        self.ui.slider_volume.setMaximum(100)


        self.ui.duration_slider.valueChanged.connect(self.duration)


    #
    def file_open(self):
        '''Функция возвращает список с полными путями файлов разрешения .mp3 '''
        import os.path

        filename = QFileDialog.getOpenFileNames(self,
                                                "Выбрать файл",
                                                'D://',
                                                "All Files (*.*);; Mp3 Files (*.mp3)")

        list_of_paths = filename[0]
        # self.playlist = [ i for i in list_of_paths if i not in self.playlist]
        self.playlist += list_of_paths
        list_of_track_name = [os.path.split(i)[1] for i in self.playlist]
        # dict_of_track_names_paths = dict(zip(list_of_track_name, list_of_paths))
        self.ui.listWidget.addItems(list_of_track_name)


    def playlist(self):
        pass

    #
    # def load_file_list_widget(self, track_name):
    #     print(f'load_file_list_widget: {track_name}')
    #     self.ui.listWidget.addItems(track_name)


    #
    def info(self):
        current_index = self.ui.listWidget.currentRow() # При нажатии на трек в listview получаем текущиюю позицию трека
        return current_index # возвращает позицию трека выбранного из списка в listview

    def volume(self):
        value = self.ui.slider_volume.value()
        self.player.setVolume(value) # Регулирование громкости воспроизводимого трека
        self.ui.label_volume_2.setText(str(value)) # Задаем значение громкости текущего положения ползунка громкости

    def play(self):
        # if self.state == "Play":
        #     self.ui.play_btn.setText("Pause")
        #     self.state = "Pause"
        position = self.info()
        print(f'Текущая позиция трека: {position}')
        url = QUrl.fromLocalFile(self.playlist[position])
        content = QMediaContent(url)
        self.player.setMedia(content)

        self.player.play()
        # else:
        #     self.ui.play_btn.setText("Play")
        #     self.state = "Play"
        #     self.player.pause()
        #     paused = self.player.position()
        #     self.position = paused

        self.duration()
    def duration(self):
        duration = self.player.duration()
        print('!', duration)
        print("?", self.player.duration())

        m = duration /1000 // 60
        s = duration /1000 % 60
        self.ui.label_duration.setText(f'{str(int(m))}:{str(int(s))}')
        self.ui.duration_slider.setMinimum(0)
        self.ui.duration_slider.setMaximum(duration)
        value = self.ui.duration_slider.value()
        self.ui.label_2.setText(str(value))
        # print(a := self.ui.duration_slider.blockSignals(True))

    # def pause(self):
    #     self.player.pause()


    def stop(self):
        if self.state == "Pause": # Сбрасывает название кнопочки с Pause на Play
            self.ui.play_btn.setText("Play")
            self.state = "Play"
        self.player.stop() # Останавливает трек и сбрасывает на начало

    def pause(self):
        self.player.pause() # Ставит трек на паузу

    #









    def play_track(self):
        # full_file_path = os.path.join(os.getcwd(), 'harrison_-_touch_me_muzati.net.mp3') # Получаем полный путь к треку
        # url = QUrl.fromLocalFile(full_file_path) # Конвертируем полученный путь в URL
        # content = QMediaContent(url) # передаем URL в медиаконтент
        # self.ui.player.setMedia(content) # Передаем полученный URL в класс QMediaplayer
        # self.ui.player.play() # Запускаем на проигрывание трек
        if self.state == "Play":
            self.ui.play_btn.setText("Pause")
            self.state = "Pause"
            path = self.ui.listWidget.currentItem().text()
            url = QUrl.fromLocalFile(path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.setPosition(self.position)
            self.playlist.append(path)
            if len(self.ui.listWidget) > 2:
                self.playlist.pop(0)
            if self.ui.listWidget.currentItem().text() != self.playlist[0]:
                self.position = 0
                self.player.setPosition(self.position)
            self.player.setVolume(15)
            self.player.play()
            self.ui.label_duration.setText(str(self.player.duration()))
        else:
            self.ui.play_btn.setText("Play")
            self.state = "Play"
            self.player.pause()
            paused = self.player.position()
            self.position = paused





if __name__ == '__main__':
    app = QApplication(sys.argv)  # Создание приложения
    App = App()  # Создаем объект класса
    App.show()  # Отображение GUI
    sys.exit(app.exec_())  # Запуск приложения
