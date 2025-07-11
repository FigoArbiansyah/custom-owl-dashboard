from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class SalesDashboard(models.Model):
    _name = 'sales.dashboard'
    _description = 'Sales Dashboard'

    @api.model
    def get_sales_data(self, period='month'):
        """
        Mengambil data penjualan berdasarkan periode yang dipilih
        """
        domain = []

        # Tentukan range tanggal berdasarkan periode
        today = datetime.now()
        if period == 'day':
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
        elif period == 'week':
            start_date = today - timedelta(days=today.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=7)
        elif period == 'month':
            start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + relativedelta(months=1)
        else:
            start_date = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + relativedelta(years=1)

        domain = [('date_order', '>=', start_date), ('date_order', '<', end_date)]

        # Query semua sales order dalam periode
        sales_orders = self.env['sale.order'].search(domain)

        # Hitung total sales order
        total_orders = len(sales_orders)

        # Hitung total omzet
        total_revenue = sum(order.amount_total for order in sales_orders)

        # Hitung berdasarkan status
        draft_orders = sales_orders.filtered(lambda x: x.state == 'draft')
        confirmed_orders = sales_orders.filtered(lambda x: x.state == 'sale')
        cancelled_orders = sales_orders.filtered(lambda x: x.state == 'cancel')

        # Data untuk chart
        daily_sales = self._get_daily_sales_data(sales_orders, start_date, end_date)
        status_distribution = self._get_status_distribution(sales_orders)

        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'draft_orders': len(draft_orders),
            'confirmed_orders': len(confirmed_orders),
            'cancelled_orders': len(cancelled_orders),
            'daily_sales': daily_sales,
            'status_distribution': status_distribution,
            'period': period,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
        }

    def _get_daily_sales_data(self, orders, start_date, end_date):
        """
        Mengambil data penjualan harian untuk chart
        """
        daily_data = []
        current_date = start_date

        while current_date < end_date:
            next_date = current_date + timedelta(days=1)
            daily_orders = orders.filtered(
                lambda x: x.date_order >= current_date and x.date_order < next_date
            )

            daily_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'orders': len(daily_orders),
                'revenue': sum(order.amount_total for order in daily_orders)
            })
            current_date = next_date

        return daily_data

    def _get_status_distribution(self, orders):
        """
        Mengambil distribusi status untuk pie chart
        """
        status_counts = {
            'draft': len(orders.filtered(lambda x: x.state == 'draft')),
            'sent': len(orders.filtered(lambda x: x.state == 'sent')),
            'sale': len(orders.filtered(lambda x: x.state == 'sale')),
            'done': len(orders.filtered(lambda x: x.state == 'done')),
            'cancel': len(orders.filtered(lambda x: x.state == 'cancel')),
        }

        return [
            {'label': 'Draft', 'value': status_counts['draft'], 'color': '#17a2b8'},
            {'label': 'Quotation Sent', 'value': status_counts['sent'], 'color': '#ffc107'},
            {'label': 'Sales Order', 'value': status_counts['sale'], 'color': '#28a745'},
            {'label': 'Done', 'value': status_counts['done'], 'color': '#6c757d'},
            {'label': 'Cancelled', 'value': status_counts['cancel'], 'color': '#dc3545'},
        ]

    @api.model
    def get_top_products(self, period='month', limit=10):
        """
        Mengambil produk terlaris
        """
        domain = []

        # Tentukan range tanggal
        today = datetime.now()
        if period == 'day':
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'week':
            start_date = today - timedelta(days=today.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'month':
            start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start_date = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        domain = [('order_id.date_order', '>=', start_date), ('order_id.state', '!=', 'cancel')]

        # Query order lines
        order_lines = self.env['sale.order.line'].search(domain)

        # Group by product
        product_data = {}
        for line in order_lines:
            product_id = line.product_id.id
            if product_id not in product_data:
                product_data[product_id] = {
                    'name': line.product_id.name,
                    'qty': 0,
                    'revenue': 0,
                }
            product_data[product_id]['qty'] += line.product_uom_qty
            product_data[product_id]['revenue'] += line.price_subtotal

        # Sort by revenue and limit
        sorted_products = sorted(product_data.values(), key=lambda x: x['revenue'], reverse=True)

        return sorted_products[:limit]