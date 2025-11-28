# fluxia_gui.py
"""
Module GUI pour Fluxia, basé sur PySide6 (Qt).

Usage côté Fluxia :

use gui;

fn build_ui(win) {
    gui_label(win, "Hello from Fluxia GUI!");
    gui_button(win, "Click me", "on_click");
}

fn on_click() {
    print("Button clicked!");
}

fn main() {
    gui_app("Fluxia GUI Demo", "build_ui");
}
"""

from typing import Any

try:
    from PySide6 import QtWidgets, QtCore
except ImportError as e:
    raise ImportError(
        "PySide6 n'est pas installé. Installe-le avec :\n"
        "    pip install PySide6\n"
    ) from e


def setup_gui_builtins(vm: "FluxiaVM"):
    vm.builtins["gui_app"] = lambda title, builder_name: gui_app(vm, title, builder_name)
    vm.builtins["gui_label"] = lambda win, text: gui_label(win, text)
    vm.builtins["gui_button"] = lambda win, text, callback_name: gui_button(vm, win, text, callback_name)


class FluxiaWindow:
    """Wrapper simple autour d'un QWidget Qt + QVBoxLayout."""
    def __init__(self, widget: QtWidgets.QWidget):
        self.widget = widget
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(8)
        self.widget.setLayout(self.layout)


def gui_app(vm: "FluxiaVM", title: str, builder_name: str) -> None:
    """Crée l'app Qt, une fenêtre, appelle la fonction Fluxia builder_name(win) puis lance la boucle."""
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    main = QtWidgets.QWidget()
    main.setWindowTitle(str(title))
    main.resize(480, 320)

    win = FluxiaWindow(main)

    try:
        vm.call_function(builder_name, [win])
    except Exception as e:
        print("Erreur dans la fonction de construction d'UI :", e)

    main.show()
    app.exec()
    return None


def gui_label(win: FluxiaWindow, text: Any):
    """Ajoute un QLabel dans la fenêtre."""
    lbl = QtWidgets.QLabel(str(text), win.widget)
    lbl.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    win.layout.addWidget(lbl)
    return lbl


def gui_button(vm: "FluxiaVM", win: FluxiaWindow, text: Any, callback_name: str):
    """Ajoute un QPushButton et connecte le clic à une fonction Fluxia."""
    btn = QtWidgets.QPushButton(str(text), win.widget)

    def on_click():
        try:
            vm.call_function(callback_name, [])
        except Exception as e:
            print("Erreur dans le callback bouton :", e)

    btn.clicked.connect(on_click)
    win.layout.addWidget(btn)
    return btn
