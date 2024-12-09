# show_data_windows/dashboard_window.py
from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
                               QHeaderView, QFrame, QDateEdit, QPushButton)
from db_config.db_operations import (get_all_products, get_all_invoices, get_all_customers, get_all_suppliers,
                                     get_daily_sales, get_daily_profit, get_weekly_sales, get_weekly_profit,
                                     get_today_invoices, get_sales_and_profit_in_range, get_invoices_in_range)


class DashboardWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Date Range Section (Moved to Top)
        self.date_range_layout = QHBoxLayout()
        self.date_range_layout.addStretch()

        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(datetime.now())
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd")

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(datetime.now())
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd")

        self.filter_button = QPushButton("Filter")
        self.filter_button.clicked.connect(self.update_date_range_analysis)

        # Clear Button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_date_filter)

        self.date_range_layout.addWidget(QLabel("Start Date:"))
        self.date_range_layout.addWidget(self.start_date_edit)
        self.date_range_layout.addWidget(QLabel("End Date:"))
        self.date_range_layout.addWidget(self.end_date_edit)
        self.date_range_layout.addWidget(self.filter_button)
        self.date_range_layout.addWidget(self.clear_button)

        self.main_layout.addLayout(self.date_range_layout)

        # Statistics Section
        self.stats_layout = QHBoxLayout()
        self.stats_layout.addStretch()
        self.main_layout.addLayout(self.stats_layout)

        # Sales and Profit Section
        self.finance_layout = QHBoxLayout()
        self.main_layout.addLayout(self.finance_layout)

        # Recent Activity Section
        recent_activity_label = QLabel("Today's Invoices")
        recent_activity_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.main_layout.addWidget(recent_activity_label)

        self.recent_invoices_table = self.create_recent_invoices_table()
        self.main_layout.addWidget(self.recent_invoices_table)

        # Set Layout
        self.setLayout(self.main_layout)

    def clear_date_filter(self):
        self.load_data()

    def create_stat_card(self, title, count):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("background-color: #b5b4b3; padding: 15px; border-radius: 8px;")

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
        return table

    def load_data(self):
        self.clear_layout(self.stats_layout)
        self.clear_layout(self.finance_layout)
        self.stats_layout.addWidget(self.create_stat_card("Products", len(get_all_products())))

        total_invoices = len(get_all_invoices())
        today_invoices = len(get_today_invoices())
        self.stats_layout.addWidget(
            self.create_stat_card("Invoices (Today/Total)", f"{today_invoices}/{total_invoices}"))

        self.stats_layout.addWidget(self.create_stat_card("Customers", len(get_all_customers())))
        self.stats_layout.addWidget(self.create_stat_card("Suppliers", len(get_all_suppliers())))

        # Update Sales and Profit Section
        self.finance_layout.addWidget(self.create_stat_card("Today's Sales", f"Rup {round(get_daily_sales(), 2)}"))
        self.finance_layout.addWidget(self.create_stat_card("Today's Profit", f"Rup {round(get_daily_profit(), 2)}"))
        self.finance_layout.addWidget(self.create_stat_card("Weekly Sales", f"Rup {round(get_weekly_sales(), 2)}"))
        self.finance_layout.addWidget(self.create_stat_card("Weekly Profit", f"Rup {round(get_weekly_profit(), 2)}"))
        # self.finance_layout.addWidget(self.create_stat_card("Monthly Sales", f"Rup {round(get_monthly_sales(), 2)}"))
        # self.finance_layout.addWidget(self.create_stat_card("Monthly Profit", f"Rup {round(get_monthly_profit(), 2)}"))

        self.update_recent_invoices_table()

    def update_recent_invoices_table(self):
        today_invoices = get_today_invoices()
        self.recent_invoices_table.setRowCount(len(today_invoices))

        for row, invoice in enumerate(today_invoices):
            self.recent_invoices_table.setItem(row, 0, QTableWidgetItem(invoice.current_date))
            self.recent_invoices_table.setItem(row, 1, QTableWidgetItem(invoice.customer_name))
            self.recent_invoices_table.setItem(row, 2, QTableWidgetItem(f"Rup {round(invoice.receiving_amount, 2)}"))
            self.recent_invoices_table.setItem(row, 3, QTableWidgetItem(f"Rup {round(invoice.remaining_amount, 2)}"))
            self.recent_invoices_table.setItem(row, 4, QTableWidgetItem(f"Rup {round(invoice.discount, 2)}"))
            self.recent_invoices_table.setItem(row, 5, QTableWidgetItem(f"Rup {round(invoice.grand_total, 2)}"))

    def update_date_range_analysis(self):
        start_date = self.start_date_edit.date().toPython()
        end_date = self.end_date_edit.date().toPython()
        sales, profit = get_sales_and_profit_in_range(start_date, end_date)

        self.clear_layout(self.finance_layout)
        self.finance_layout.addWidget(self.create_stat_card("Sales in Range", f"Rup {round(sales, 2)}"))
        self.finance_layout.addWidget(self.create_stat_card("Profit in Range", f"Rup {round(profit, 2)}"))

        invoices_in_range = get_invoices_in_range(start_date, end_date)
        self.update_invoices_table(invoices_in_range)

    def update_invoices_table(self, invoices):
        self.recent_invoices_table.setRowCount(len(invoices))

        for row, invoice in enumerate(invoices):
            self.recent_invoices_table.setItem(row, 0, QTableWidgetItem(invoice.current_date))
            self.recent_invoices_table.setItem(row, 1, QTableWidgetItem(invoice.customer_name))
            self.recent_invoices_table.setItem(row, 2, QTableWidgetItem(f"Rup {round(invoice.receiving_amount, 2)}"))
            self.recent_invoices_table.setItem(row, 3, QTableWidgetItem(f"Rup {round(invoice.remaining_amount, 2)}"))
            self.recent_invoices_table.setItem(row, 4, QTableWidgetItem(f"Rup {round(invoice.discount, 2)}"))
            self.recent_invoices_table.setItem(row, 5, QTableWidgetItem(f"Rup {round(invoice.grand_total, 2)}"))

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
