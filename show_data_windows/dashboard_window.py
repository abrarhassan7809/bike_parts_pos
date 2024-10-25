# dashboard_window.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
                               QTableWidgetItem, QHeaderView, QFrame)
from db_config.db_operations import (get_all_products, get_all_invoices, get_all_customers, get_all_suppliers,
                                     get_daily_sales, get_daily_profit, get_monthly_sales, get_monthly_profit)


class DashboardWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Statistics Section
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(self.create_stat_card("Products", len(get_all_products())))
        stats_layout.addWidget(self.create_stat_card("Invoices", len(get_all_invoices())))
        stats_layout.addWidget(self.create_stat_card("Customers", len(get_all_customers())))
        stats_layout.addWidget(self.create_stat_card("Suppliers", len(get_all_suppliers())))
        main_layout.addLayout(stats_layout)

        # Sales and Profit Section
        finance_layout = QHBoxLayout()
        finance_layout.addWidget(self.create_stat_card("Today's Sales", f"Rup {get_daily_sales()}"))
        finance_layout.addWidget(self.create_stat_card("Today's Profit", f"Rup {get_daily_profit()}"))
        finance_layout.addWidget(self.create_stat_card("Monthly Sales", f"Rup {get_monthly_sales()}"))
        finance_layout.addWidget(self.create_stat_card("Monthly Profit", f"Rup {get_monthly_profit()}"))
        main_layout.addLayout(finance_layout)

        # Recent Activity Section
        recent_activity_label = QLabel("Recent Invoices")
        recent_activity_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(recent_activity_label)

        self.recent_invoices_table = self.create_recent_invoices_table()
        main_layout.addWidget(self.recent_invoices_table)

        # Set Layout
        self.setLayout(main_layout)

    def create_stat_card(self, title, count):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("background-color: #f7f7f7; padding: 15px; border-radius: 8px;")

        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: #555;")

        count_label = QLabel(str(count))
        count_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")

        layout.addWidget(title_label)
        layout.addWidget(count_label)

        card.setLayout(layout)
        return card

    def create_recent_invoices_table(self):
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Date", "Customer", "Receiving", "Remaining", "Discount", "Total Amount"])
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        invoices = get_all_invoices()
        table.setRowCount(min(len(invoices), 6))

        for row, invoice in enumerate(invoices[:6]):
            table.setItem(row, 0, QTableWidgetItem(invoice.current_date))
            table.setItem(row, 1, QTableWidgetItem(invoice.customer_name))
            table.setItem(row, 2, QTableWidgetItem(f"Rup {invoice.receiving_amount}"))
            table.setItem(row, 3, QTableWidgetItem(f"Rup {invoice.remaining_amount}"))
            table.setItem(row, 4, QTableWidgetItem(f"Rup {invoice.discount}"))
            table.setItem(row, 5, QTableWidgetItem(f"Rup {invoice.grand_total}"))

        return table
