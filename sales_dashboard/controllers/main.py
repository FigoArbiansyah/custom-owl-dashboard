from odoo import http
from odoo.http import request
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class SalesDashboardController(http.Controller):

    @http.route('/sales_dashboard/data', type='json', auth='user')
    def get_sales_dashboard_data(self, period='month'):
        """
        Endpoint untuk mengambil data dashboard penjualan
        """
        try:
            dashboard_model = request.env['sales.dashboard']
            data = dashboard_model.get_sales_data(period)
            return {
                'success': True,
                'data': data
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/sales_dashboard/top_products', type='json', auth='user')
    def get_top_products(self, period='month', limit=10):
        """
        Endpoint untuk mengambil produk terlaris
        """
        try:
            dashboard_model = request.env['sales.dashboard']
            products = dashboard_model.get_top_products(period, limit)
            return {
                'success': True,
                'data': products
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/sales_dashboard/export_data', type='http', auth='user')
    def export_dashboard_data(self, period='month', format='xlsx'):
        """
        Endpoint untuk export data dashboard
        """
        try:
            dashboard_model = request.env['sales.dashboard']
            data = dashboard_model.get_sales_data(period)

            if format == 'xlsx':
                return self._export_to_excel(data, period)
            elif format == 'csv':
                return self._export_to_csv(data, period)
            else:
                return request.make_response(
                    json.dumps({'error': 'Format not supported'}),
                    headers=[('Content-Type', 'application/json')]
                )

        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers=[('Content-Type', 'application/json')]
            )

    def _export_to_excel(self, data, period):
        """
        Export data ke format Excel
        """
        try:
            import io
            from xlsxwriter import Workbook

            output = io.BytesIO()
            workbook = Workbook(output)

            # Summary worksheet
            summary_sheet = workbook.add_worksheet('Summary')

            # Header format
            header_format = workbook.add_format({
                'bold': True,
                'font_size': 12,
                'bg_color': '#4CAF50',
                'font_color': 'white'
            })

            # Data format
            data_format = workbook.add_format({
                'font_size': 11,
                'num_format': '#,##0'
            })

            currency_format = workbook.add_format({
                'font_size': 11,
                'num_format': '"Rp "#,##0'
            })

            # Write summary data
            summary_sheet.write('A1', 'Metrics', header_format)
            summary_sheet.write('B1', 'Value', header_format)

            summary_sheet.write('A2', 'Period', data_format)
            summary_sheet.write('B2', period.title(), data_format)

            summary_sheet.write('A3', 'Total Orders', data_format)
            summary_sheet.write('B3', data['total_orders'], data_format)

            summary_sheet.write('A4', 'Total Revenue', data_format)
            summary_sheet.write('B4', data['total_revenue'], currency_format)

            summary_sheet.write('A5', 'Draft Orders', data_format)
            summary_sheet.write('B5', data['draft_orders'], data_format)

            summary_sheet.write('A6', 'Confirmed Orders', data_format)
            summary_sheet.write('B6', data['confirmed_orders'], data_format)

            summary_sheet.write('A7', 'Cancelled Orders', data_format)
            summary_sheet.write('B7', data['cancelled_orders'], data_format)

            # Daily sales worksheet
            daily_sheet = workbook.add_worksheet('Daily Sales')
            daily_sheet.write('A1', 'Date', header_format)
            daily_sheet.write('B1', 'Orders', header_format)
            daily_sheet.write('C1', 'Revenue', header_format)

            for i, daily_data in enumerate(data['daily_sales'], 2):
                daily_sheet.write(f'A{i}', daily_data['date'], data_format)
                daily_sheet.write(f'B{i}', daily_data['orders'], data_format)
                daily_sheet.write(f'C{i}', daily_data['revenue'], currency_format)

            workbook.close()
            output.seek(0)

            filename = f'sales_dashboard_{period}_{datetime.now().strftime("%Y%m%d")}.xlsx'

            return request.make_response(
                output.read(),
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    ('Content-Disposition', f'attachment; filename="{filename}"')
                ]
            )

        except ImportError:
            return request.make_response(
                json.dumps({'error': 'xlsxwriter not installed'}),
                headers=[('Content-Type', 'application/json')]
            )

    def _export_to_csv(self, data, period):
        """
        Export data ke format CSV
        """
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)

        # Write summary
        writer.writerow(['Sales Dashboard Summary'])
        writer.writerow(['Period', period.title()])
        writer.writerow(['Total Orders', data['total_orders']])
        writer.writerow(['Total Revenue', data['total_revenue']])
        writer.writerow(['Draft Orders', data['draft_orders']])
        writer.writerow(['Confirmed Orders', data['confirmed_orders']])
        writer.writerow(['Cancelled Orders', data['cancelled_orders']])
        writer.writerow([])

        # Write daily sales
        writer.writerow(['Daily Sales'])
        writer.writerow(['Date', 'Orders', 'Revenue'])
        for daily_data in data['daily_sales']:
            writer.writerow([daily_data['date'], daily_data['orders'], daily_data['revenue']])

        filename = f'sales_dashboard_{period}_{datetime.now().strftime("%Y%m%d")}.csv'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'text/csv'),
                ('Content-Disposition', f'attachment; filename="{filename}"')
            ]
        )