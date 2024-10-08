import sys
import json
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QDialog, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog
from PyQt6.QtGui import QIcon, QAction
from AboutDialog import AboutDialog

VERSION = "1.0.1"

class AppFire(QWidget):
    def __init__(self):
        super().__init__()
        self.app_data = self.load_app_definitions()
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("./icons/launcher.png"))
        self.tray_icon.setToolTip("AppFire " + VERSION)
        self.tray_icon.setVisible(True)
        self.create_tray_menu()
        self.about_dialog = None

    def create_tray_menu(self):
        menu = QMenu()
        self.tray_icon.setContextMenu(menu)
    
        self.app_menu = menu.addMenu("Apps")
        self.create_app_menu_items()
    
        menu.addSeparator()
    
        about_action = menu.addAction("About")
        about_action.triggered.connect(self.show_about_dialog)
    
        menu.addSeparator()
    
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.quit)
    
    
    def create_app_menu_items(self):
        self.app_menu.clear()
        add_new_app_action = self.app_menu.addAction("Add New App")
        add_new_app_action.triggered.connect(self.add_new_app)
    
        self.app_menu.addSeparator()

        app_names = sorted(self.app_data.keys())
        for app_name in app_names:
            app_submenu = self.app_menu.addMenu(app_name)
            launch_action = QAction("Launch", self)
            launch_action.triggered.connect(lambda checked, name=app_name: self.launch_app(name))
            app_submenu.addAction(launch_action)
            edit_action = QAction("Edit", self)
            edit_action.triggered.connect(lambda checked, name=app_name: self.edit_app(name))
            app_submenu.addAction(edit_action)
            remove_action = QAction("Remove", self)
            remove_action.triggered.connect(lambda checked, name=app_name: self.remove_app(name))
            app_submenu.addAction(remove_action)

    def launch_app(self, app_name):
        subprocess.Popen(self.app_data[app_name], shell=True, start_new_session=True)

    def add_new_app(self):
        self.add_dialog = QDialog(self)
        self.add_dialog.setWindowTitle("Add New App")
        self.add_dialog.resize(435, 200)
        self.center_dialog_on_screen(self.add_dialog)
        
        layout = QVBoxLayout()

        name_label = QLabel("Name:")
        layout.addWidget(name_label)
        name_input = QLineEdit()
        layout.addWidget(name_input)
        
        path_label = QLabel("Path:")
        layout.addWidget(path_label)
        path_input = QLineEdit()
        layout.addWidget(path_input)
        
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.browse_for_path(path_input))
        layout.addWidget(browse_button)
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.add_app(name_input.text(), path_input.text()))
        add_button.clicked.connect(self.add_dialog.accept)
        layout.addWidget(add_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.add_dialog.reject)
        layout.addWidget(cancel_button)
        
        self.add_dialog.setLayout(layout)
        self.add_dialog.exec()
        
    def edit_app(self, app_name):
        self.edit_dialog = QDialog(self)
        self.edit_dialog.setWindowTitle("Edit App")
        
        layout = QVBoxLayout()
    
        name_label = QLabel("Name:")
        layout.addWidget(name_label)
        name_input = QLineEdit(app_name)
        layout.addWidget(name_input)
    
        path_label = QLabel("Path:")
        layout.addWidget(path_label)
        path_input = QLineEdit(self.app_data[app_name])
        layout.addWidget(path_input)
    
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.browse_for_path(path_input))
        layout.addWidget(browse_button)
    
        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_app(name_input.text(), path_input.text(), app_name))
        save_button.clicked.connect(self.edit_dialog.hide)
        layout.addWidget(save_button)
    
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.edit_dialog.reject)
        layout.addWidget(cancel_button)
    
        self.edit_dialog.setLayout(layout)

        # size and center
        self.edit_dialog.resize(435, 200)
        self.center_dialog_on_screen(self.edit_dialog)
        
        self.edit_dialog.exec()
    
    def remove_app(self, app_name):
        del self.app_data[app_name]
        self.sort_and_save_app_definitions()
        self.create_app_menu_items()

    def add_app(self, name, path):  # not the same as add_new_app above
        self.app_data[name] = path
        self.sort_and_save_app_definitions()
        self.create_app_menu_items()

    def save_app(self, name, path, old_name):
        if name != old_name:
            del self.app_data[old_name]
        self.app_data[name] = path
        self.sort_and_save_app_definitions()
        self.create_app_menu_items()

    def browse_for_path(self, path_input):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_name:
            path_input.setText(file_name)

    def load_app_definitions(self):
        try:
            with open('app_setup.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def sort_and_save_app_definitions(self):
        sorted_app_data = dict(sorted(self.app_data.items()))
        with open('app_setup.json', 'w') as f:
            json.dump(sorted_app_data, f, indent=4)
        self.app_data = sorted_app_data

    def center_dialog_on_screen(self, dialog):
        screen = QApplication.primaryScreen().availableGeometry()
        dialog.move(screen.center() - dialog.rect().center())

    def show_about_dialog(self):
        if not self.about_dialog:
            self.about_dialog = AboutDialog(
                title="About AppFire",
                app_name="AppFire",
                version="1.0.0",
                description="Launches and manages your tools.",
                author="Ryon Shane Hall",
                email="endorpheus@gmail.com",
                website="https://github.com/endorpheus/AppFire",
                opacity=0.8
            )
        self.about_dialog.show()
        self.about_dialog.raise_()  # Bring the dialog to the front
        self.about_dialog.activateWindow()  # Activate the dialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppFire()
    sys.exit(app.exec())