from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QApplication
from PySide6.QtGui import QColor, QPainter, QBrush, QPen
import math
import time

class AboutDialog(QDialog):
    def __init__(self, parent=None, title="About", app_name="My Application", version="1.0.0", 
                 description="A brief description of your application.", 
                 author="Your Name", email="your_email@example.com", website="your.website.com", fixed_width=None, opacity=0.9):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowTitle(title)
        self.app_name = app_name
        self.version = version
        self.description = description
        self.author = author
        self.email = email
        self.website = website
        self.fixed_width = fixed_width
        self.opacity = opacity
        
        self.color_ball_size = 15
        self.color_ball_color = QColor(255, 0, 0, 150)

        self._init_ui()
        self.centerOnScreen()

        # Set up timer for color animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_color)
        self.timer.start(20)  # Update every 20 milliseconds

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Content layout
        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)

        title_label = QLabel(f"<center><b>{self.app_name}</b></center>")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: black;")
        content_layout.addWidget(title_label)

        content_layout.addWidget(QLabel(f"Version {self.version}", styleSheet="font-size: 14pt; color: black;"), alignment=Qt.AlignCenter)
        content_layout.addWidget(QLabel(self.description, styleSheet="font-size: 12pt; color: black;"), alignment=Qt.AlignCenter)
        content_layout.addWidget(QLabel(f"Author: {self.author}", styleSheet="font-size: 12pt; color: black;"), alignment=Qt.AlignCenter)
        content_layout.addWidget(QLabel(f"Email: {self.email}", styleSheet="font-size: 12pt; color: black;"), alignment=Qt.AlignCenter)
        website_label = QLabel(f"Website: <a href=\"{self.website}\">{self.website}</a>", styleSheet="font-size: 12pt; color: black; text-decoration: none;")
        website_label.setOpenExternalLinks(True)
        content_layout.addWidget(website_label, alignment=Qt.AlignCenter)
        if self.fixed_width:
            self.setFixedWidth(self.fixed_width)
        else:
            self.adjustSize()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw dialog background
        painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
        background_color = QColor(127, 224, 255, int(255 * self.opacity))
        painter.setBrush(QBrush(background_color))
        painter.drawRoundedRect(self.rect(), 10, 10)

        # Draw color ball in upper right corner
        painter.setBrush(QBrush(self.color_ball_color))
        painter.setPen(Qt.NoPen)
        ball_rect = QRectF(self.width() - self.color_ball_size - 10, 10, self.color_ball_size, self.color_ball_size)
        painter.drawEllipse(ball_rect)

    def update_color(self):
        current_time = time.time()          # why not use pi?
        r = int(127.5 * (1 + math.sin(2 * math.pi * current_time)))
        g = int(127.5 * (1 + math.sin(2 * math.pi * current_time + (2/3) * math.pi)))
        b = int(127.5 * (1 + math.sin(2 * math.pi * current_time + (4/3) * math.pi)))
        self.color_ball_color = QColor(r, g, b, 150)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Check if the click is within the color ball
            ball_rect = QRectF(self.width() - self.color_ball_size - 10, 10, self.color_ball_size, self.color_ball_size)
            if ball_rect.contains(event.pos()):
                self.hide()
            else:
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def centerOnScreen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.center() - self.rect().center())

    def sizeHint(self):
        return self.minimumSizeHint()
