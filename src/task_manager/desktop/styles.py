"""Centralized dark theme for a consistent modern interface."""

APP_STYLESHEET = """
QWidget { background: #0f172a; color: #e2e8f0; font-family: 'Segoe UI'; font-size: 13px; }
QMainWindow { background: #0b1120; }
#sidebar { background: #111827; border-right: 1px solid #253047; }
#brand { font-size: 22px; font-weight: 700; color: #f8fafc; padding: 8px; }
#subtitle { color: #64748b; padding-left: 8px; }
#pageTitle { font-size: 26px; font-weight: 700; color: #f8fafc; }
#muted { color: #94a3b8; }
QPushButton { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 9px 14px; }
QPushButton:hover { background: #273449; border-color: #475569; }
QPushButton:pressed { background: #172033; }
QPushButton#primary { background: #2563eb; border: none; font-weight: 600; }
QPushButton#primary:hover { background: #3b82f6; }
QPushButton#danger { color: #fda4af; }
QPushButton#nav { text-align: left; border: none; padding: 11px 14px; }
QPushButton#nav:checked { background: #1d4ed8; color: white; }
QLineEdit, QTextEdit, QComboBox, QDateEdit { background: #111827; border: 1px solid #334155; border-radius: 8px; padding: 9px; selection-background-color: #2563eb; }
QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus { border-color: #3b82f6; }
QTableView { background: #111827; alternate-background-color: #151f31; border: 1px solid #253047; border-radius: 10px; gridline-color: #253047; selection-background-color: #1e40af; }
QHeaderView::section { background: #162033; color: #94a3b8; border: none; border-bottom: 1px solid #334155; padding: 10px; font-weight: 600; }
QFrame#card { background: #111827; border: 1px solid #253047; border-radius: 12px; }
QLabel#cardValue { font-size: 24px; font-weight: 700; color: #f8fafc; }
QLabel#cardLabel { color: #94a3b8; }
QStatusBar { background: #111827; color: #94a3b8; }
QScrollBar:vertical { background: #0f172a; width: 10px; }
QScrollBar::handle:vertical { background: #334155; border-radius: 5px; min-height: 24px; }
"""
