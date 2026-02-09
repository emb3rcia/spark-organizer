#reused from my spark-builder project

from PyQt6.QtWidgets import QPushButton, QLabel, QWidget, QStackedWidget, QLineEdit, QTableWidget, QMainWindow, QComboBox, QDateTimeEdit

class Button(QPushButton):
    def __init__(self, text, theme_colors, disabled_color):
        super().__init__(text)
        self.disabled_color = disabled_color
        self.theme_colors = theme_colors
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.theme_colors['button_background']};
                color: {self.theme_colors['button_text']};
                border: 1px solid {self.theme_colors['button_border']};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {self.theme_colors['button_hover']};
            }}
            QPushButton:pressed {{
                background-color: {self.theme_colors['button_pressed']};
            }}
            QPushButton:disabled {{
                background-color: {self.theme_colors['button_disabled']};
                color: {self.disabled_color};
            }}
            """
        )
    def update_theme(self, new_theme_colors, new_disabled_color):
        self.theme_colors = new_theme_colors
        self.disabled_color = new_disabled_color
        self.apply_theme()

class Label(QLabel):
    def __init__(self, text, theme_colors, label_type: int):
        super().__init__(text)
        self.theme_colors = theme_colors
        self.label_type = label_type
        self.apply_theme()

    def apply_theme(self):
        PRIMARY = 1
        SECONDARY = 2
        INVERTED = 3
        if self.label_type == PRIMARY:
            self.setStyleSheet(
                f"""
                QLabel {{
                    color: {self.theme_colors['text_primary']};
                }}
                QLabel:disabled {{
                    color: {self.theme_colors['text_disabled']};
                }}
                """
            )
        elif self.label_type == SECONDARY:
            self.setStyleSheet(
                f"""
                QLabel {{
                    color: {self.theme_colors['text_secondary']};
                }}
                QLabel:disabled {{
                    color: {self.theme_colors['text_disabled']};
                }}
                """
            )
        elif self.label_type == INVERTED:
            self.setStyleSheet(
                f"""
                QLabel {{
                    color: {self.theme_colors['text_inverted']};
                }}
                QLabel:disabled {{
                    color: {self.theme_colors['text_disabled']};
                }}
                """
            )
        else:
            raise TypeError("Incorrect label type")
    def update_theme(self, new_theme_colors):
        self.theme_colors = new_theme_colors
        self.apply_theme()

class LineEdit(QLineEdit):
    def __init__(self, theme_colors, highlight_colors, disabled_color):
        super().__init__()
        self.theme_colors = theme_colors
        self.highlight_colors = highlight_colors
        self.disabled_color = disabled_color
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {self.theme_colors['input_background']};
                color: {self.theme_colors['input_text']};
                border: 1px solid {self.theme_colors['input_border']};
                border-radius: 6px;
            }}
            QLineEdit:focus {{
                background-color: {self.highlight_colors['highlight']};
                color: {self.highlight_colors['highlight_text']};
            }}
            QLineEdit:disabled {{
                background-color: {self.theme_colors['input_disabled']};
                color: {self.disabled_color};
            }}
            QLineEdit::placeholder {{
                color: {self.theme_colors['input_placeholder']};
            }}
            """
        )
    def update_theme(self, new_theme_colors, new_highlight_colors, new_disabled_color):
        self.theme_colors = new_theme_colors
        self.highlight_colors = new_highlight_colors
        self.disabled_color = new_disabled_color
        self.apply_theme()

class MainWindow(QMainWindow):
    def __init__(self, theme_colors):
        super().__init__()
        self.theme_colors = theme_colors
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(
            f"""
            QMainWindow {{
                background-color: {self.theme_colors['window_background']};
            }}
            """
        )
    def update_theme(self, new_theme_colors):
        self.theme_colors = new_theme_colors
        self.apply_theme()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

class TableWidget(QTableWidget):
    def __init__(self, theme_colors, disabled_color, extra_colors):
        super().__init__()
        self.theme_colors = theme_colors
        self.disabled_color = disabled_color
        self.extra_colors = extra_colors
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(
            f"""
            QTableWidget {{
                background-color: {self.theme_colors['table_background']};
                color: {self.theme_colors['table_text']};
                gridline-color: {self.theme_colors['table_grid']};
                alternate-background-color: {self.theme_colors['table_alternate_row']};
            }}
            QHeaderView::section {{
                background-color: {self.theme_colors['table_header_background']};
                color: {self.theme_colors['table_header_text']};
            }}
            QScrollBar {{
                background-color: {self.extra_colors['scrollbar_background']};
            }}
            QScrollBar::handle {{
                background-color: {self.extra_colors['scrollbar_handle']};
            }}
            """
        )
    def update_theme(self, new_theme_colors, new_extra_colors, new_disabled_color):
        self.theme_colors = new_theme_colors
        self.extra_colors = new_extra_colors
        self.disabled_color = new_disabled_color
        self.apply_theme()

class Widget(QWidget):
    def __init__(self, theme_colors):
        super().__init__()
        self.theme_colors = theme_colors
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {self.theme_colors["panel_background"]};
            }}
            """
        )
    def update_theme(self, new_theme_colors):
        self.theme_colors = new_theme_colors
        self.apply_theme()

class StackedWidget(QStackedWidget):
    def __init__(self, theme_colors):
        super().__init__()
        self.theme_colors = theme_colors
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(
            f"""
            QStackedWidget {{
                background-color: {self.theme_colors["panel_background"]};
            }}
            """
        )
    def update_theme(self, new_theme_colors):
        self.theme_colors = new_theme_colors
        self.apply_theme()

class ComboBox(QComboBox):
    def __init__(self, theme_colors, disabled_color):
        super().__init__()
        self.theme_colors = theme_colors
        self.disabled_color = disabled_color
        self.apply_theme()
    
    def apply_theme(self):
        self.setStyleSheet(
            f"""
            QComboBox {{
                background-color: {self.theme_colors['combo-box_background']};
                color: {self.theme_colors['combo-box_text']};
                border: 1px solid {self.theme_colors['combo-box_border']};
                border-radius: 6px;
            }}        
            QComboBox:hover {{
                background-color: {self.theme_colors['combo-box_hover']};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid {self.theme_colors['combo-box_border']};
            }}
            QComboBox:disabled {{
                background-color: {self.theme_colors['combo-box_disabled']};
                color: {self.disabled_color};
            }}
            """
        )
    def update_theme(self, new_theme_colors, new_disabled_color):
        self.theme_colors = new_theme_colors
        self.disabled_color = new_disabled_color
        self.apply_theme()

class DateTimeEdit(QDateTimeEdit):
    def __init__(self, theme_colors):
        super().__init__()
        self.theme_colors = theme_colors

    def apply_theme(self):
        self.setStyleSheet(f"""
            QDateTimeEdit {{
                background-color: {self.theme_colors['input']['input_background']};
                color: {self.theme_colors['input']['input_text']};
                border: 2px solid {self.theme_colors['input']['input_border']};
                border-radius: 6px;
            }}
        """
        )
    
    def update_theme(self, theme_colors):
        self.theme_colors = theme_colors
        self.apply_theme()