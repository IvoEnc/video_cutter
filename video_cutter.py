import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QProgressDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QTimer

class VideoCutterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Cutter")
        self.setGeometry(100, 100, 800, 600)
        self.setFocusPolicy(Qt.StrongFocus)  # Задаваме силен фокус на основния прозорец

        self.video_file = None
        self.start_time = None
        self.end_time = None
        self.layout = QVBoxLayout()

        self.label = QLabel("Choose a video file")
        self.layout.addWidget(self.label)

        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        # Създаваме хоризонтален лайаут за бутоните
        self.button_layout = QHBoxLayout()

        self.open_button = QPushButton("Open File")
        self.open_button.setFixedSize(100, 30)  # Намаляване на размера на бутона
        self.open_button.setFocusPolicy(Qt.NoFocus)  # Предотвратява прихващането на фокуса
        self.open_button.clicked.connect(self.open_file)
        self.button_layout.addWidget(self.open_button)

        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(100, 30)  # Намаляване на размера на бутона
        self.save_button.setFocusPolicy(Qt.NoFocus)  # Предотвратява прихващането на фокуса
        self.save_button.clicked.connect(self.save_cut)
        self.save_button.setEnabled(False)
        self.button_layout.addWidget(self.save_button)

        # Добавяме хоризонталния лайаут с бутоните в основния лайаут
        self.layout.addLayout(self.button_layout)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)

        self.setLayout(self.layout)

    def open_file(self):
        self.video_file, _ = QFileDialog.getOpenFileName(
            self, "Open Video", "", 
            "Video files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.webm *.MP4 *.m4v)"
        )
        if self.video_file:
            self.label.setText(f"Selected file: {self.video_file}")
            self.play_video()  # Автоматично стартиране на видеото

    def play_video(self):
        if self.video_file:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_file)))
            self.media_player.play()
            self.video_widget.setFocus()  # Задаваме фокус на видео виджета

    def keyPressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        print(f"Focused widget: {focused_widget}")  # Отладъчно съобщение за текущия фокусиран виджет

        key = event.key()
        print(f"Key pressed: {key}")  # Отладъчно съобщение за натискането на клавиш

        if key == Qt.Key_1:
            self.start_time = self.media_player.position() / 1000  # В секунда
            self.show_status_message(f"Start time marked at: {self.start_time} seconds")
            self.check_if_ready_to_save()

        elif key == Qt.Key_2:
            self.end_time = self.media_player.position() / 1000  # В секунда
            self.show_status_message(f"End time marked at: {self.end_time} seconds")
            self.check_if_ready_to_save()

        elif key == Qt.Key_Left:
            print("Left arrow key pressed")  # Отладъчно съобщение за стрелка наляво
            # Превъртане назад с 5 секунди
            new_position = self.media_player.position() - 5000
            if new_position < 0:
                new_position = 0
            self.media_player.setPosition(new_position)

        elif key == Qt.Key_Right:
            print("Right arrow key pressed")  # Отладъчно съобщение за стрелка надясно
            # Превъртане напред с 5 секунди
            new_position = self.media_player.position() + 5000
            if new_position > self.media_player.duration():
                new_position = self.media_player.duration()
            self.media_player.setPosition(new_position)

        elif key == Qt.Key_Escape:
            self.media_player.stop()

    def show_status_message(self, message):
        self.status_label.setText(message)
        QTimer.singleShot(1500, lambda: self.status_label.clear())  # Изчиства съобщението след 1.5 секунди

    def check_if_ready_to_save(self):
        if self.start_time is not None and self.end_time is not None:
            self.save_button.setEnabled(True)

    def save_cut(self):
        if self.start_time is not None and self.end_time is not None:
            output_file = self.video_file.rsplit('.', 1)[0] + "_CUT." + self.video_file.rsplit('.', 1)[1]
            self.media_player.pause()  # Спираме плейъра по време на обработката

            progress_dialog = QProgressDialog("Processing...", None, 0, 100, self)
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setMinimumDuration(0)
            progress_dialog.setValue(0)
            progress_dialog.show()

            QTimer.singleShot(500, lambda: self.run_ffmpeg_command(output_file, progress_dialog))

    def run_ffmpeg_command(self, output_file, progress_dialog):
        command = [
            "ffmpeg",
            "-i", self.video_file,
            "-ss", str(self.start_time),
            "-to", str(self.end_time),
            "-c", "copy",  # Запазва ориентацията и кодека без промени
            output_file
        ]
        subprocess.run(command)

        progress_dialog.setValue(100)
        QTimer.singleShot(500, self.close)  # Затваря приложението след 0.5 секунди

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoCutterApp()
    window.show()
    sys.exit(app.exec_())
