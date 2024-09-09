
import sys
import subprocess
import os
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QProgressDialog, QLineEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QTimer

class VideoCutterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Cutter")
        self.setGeometry(100, 100, 800, 600)
        self.setFocusPolicy(Qt.StrongFocus)  # Set strong focus to the main window

        self.video_file = None
        self.start_time = None
        self.end_time = None
        self.cut_video_file = None  # To store the cut video path
        self.layout = QVBoxLayout()

        self.label = QLabel("Choose a video file")
        self.layout.addWidget(self.label)

        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        # Create a horizontal layout for the buttons
        self.button_layout = QHBoxLayout()

        self.open_button = QPushButton("Open Video")
        self.open_button.clicked.connect(self.open_file)
        self.button_layout.addWidget(self.open_button)

        self.start_button = QPushButton("Set Start")
        self.start_button.clicked.connect(self.set_start)
        self.button_layout.addWidget(self.start_button)

        self.end_button = QPushButton("Set End")
        self.end_button.clicked.connect(self.set_end)
        self.button_layout.addWidget(self.end_button)

        self.save_button = QPushButton("Save Cut")
        self.save_button.clicked.connect(self.save_cut)
        self.button_layout.addWidget(self.save_button)

        # Adding Take Photos button and interval input
        self.take_photos_button = QPushButton("Take Photos")
        self.take_photos_button.clicked.connect(self.extract_frames)
        self.button_layout.addWidget(self.take_photos_button)

        self.interval_label = QLabel("Frame Interval (seconds):")
        self.button_layout.addWidget(self.interval_label)

        self.interval_input = QLineEdit("1")  # Default to 1 second interval
        self.button_layout.addWidget(self.interval_input)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.video_widget)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mov)", options=options)
        if file_name:
            self.video_file = file_name
            self.label.setText(f"Selected: {file_name}")
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.player.play()

    def set_start(self):
        self.start_time = self.player.position() / 1000  # Time in seconds
        self.label.setText(f"Start Time: {self.start_time} seconds")

    def set_end(self):
        self.end_time = self.player.position() / 1000  # Time in seconds
        self.label.setText(f"End Time: {self.end_time} seconds")

    def save_cut(self):
        if not self.video_file or self.start_time is None or self.end_time is None:
            self.label.setText("Set start and end times first.")
            return

        # Use ffmpeg to cut the video (assuming ffmpeg is installed and in the system path)
        cut_file_name = os.path.splitext(self.video_file)[0] + "_CUT.mp4"
        start_time_str = str(self.start_time)
        duration_str = str(self.end_time - self.start_time)

        command = [
            'ffmpeg',
            '-i', self.video_file,
            '-ss', start_time_str,
            '-t', duration_str,
            '-c', 'copy',  # Copy codec to avoid re-encoding
            cut_file_name
        ]

        subprocess.run(command)

        self.cut_video_file = cut_file_name  # Store the path of the cut video
        self.label.setText(f"Saved cut video: {cut_file_name}")

    def extract_frames(self):
        if not self.cut_video_file:
            self.label.setText("No cut video file available. Save the cut first.")
            return

        interval = float(self.interval_input.text())
        cap = cv2.VideoCapture(self.cut_video_file)

        if not cap.isOpened():
            self.label.setText("Error opening cut video file.")
            return

        folder_name = os.path.splitext(os.path.basename(self.cut_video_file))[0] + '-photos'
        folder_path = os.path.join(os.path.dirname(self.cut_video_file), folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        interval_frames = int(interval * fps)

        count = 0
        frame_number = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Extract first, interval-based, and last frames
            if frame_number == 0 or frame_number % interval_frames == 0 or frame_number == total_frames - 1:
                frame_name = f"frame_{frame_number}.jpg"
                frame_path = os.path.join(folder_path, frame_name)
                cv2.imwrite(frame_path, frame)
                count += 1

            frame_number += 1

        cap.release()
        self.label.setText(f"Extracted {count} frames to {folder_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoCutterApp()
    window.show()
    sys.exit(app.exec_())
