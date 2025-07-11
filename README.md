# Sales Dashboard Module untuk Odoo 17

## Deskripsi

Custom Dashboard Sales Order untuk Odoo 17 yang dibangun menggunakan OWL JS Framework. Dashboard ini menyediakan visualisasi data penjualan yang komprehensif dengan fitur-fitur berikut:

### Fitur Utama

**📊 Ringkasan Penjualan**
- Total sales order dalam periode tertentu (hari, minggu, bulan, tahun)
- Total omzet dari sales order
- Jumlah order berdasarkan status (draft, confirmed, cancelled)

**📈 Visualisasi Data**
- Chart tren penjualan harian dengan dual-axis (revenue & orders)
- Pie chart distribusi status order
- Tabel produk terlaris

**🔄 Fitur Interaktif**
- Filter periode waktu (hari, minggu, bulan, tahun)
- Refresh data real-time
- Export data ke Excel/CSV
- Responsive design

## Struktur File

```
sales_dashboard/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── sales_dashboard.py
├── controllers/
│   ├── __init__.py
│   └── main.py
├── views/
│   ├── sales_dashboard_views.xml
│   └── menu.xml
├── security/
│   └── ir.model.access.csv
└── static/
    └── src/
        ├── js/
        │   └── sales_dashboard.js
        ├── xml/
        │   └── sales_dashboard.xml
        └── css/
            └── sales_dashboard.css
```

## Instalasi

### 1. Persiapan
- Pastikan Odoo 17 sudah terinstall
- Modul `sale` sudah diaktifkan
- Python dependencies: `xlsxwriter` (untuk export Excel)

### 2. Install Dependencies
```bash
pip install xlsxwriter
```

### 3. Copy Module
Copy folder `sales_dashboard` ke direktori addons Odoo Anda:
```bash
cp -r sales_dashboard /path/to/odoo/addons/
```

### 4. Update Apps List
- Masuk ke Odoo sebagai Administrator
- Pergi ke Apps > Update Apps List
- Cari "Sales Dashboard"
- Klik Install

## Penggunaan

### Mengakses Dashboard
1. Setelah instalasi, menu "Sales Dashboard" akan muncul di menu utama
2. Klik "Dashboard" untuk membuka dashboard

### Fitur Dashboard

#### Filter Periode
- **Hari**: Menampilkan data hari ini
- **Minggu**: Menampilkan data minggu ini
- **Bulan**: Menampilkan data bulan ini  
- **Tahun**: Menampilkan data tahun ini

#### Metrics yang Ditampilkan
- **Total Sales Order**: Jumlah total order dalam periode
- **Total Omzet**: Total nilai penjualan
- **Order Terkonfirmasi**: Jumlah order dengan status 'sale'
- **Order Pending**: Jumlah order dengan status 'draft'

#### Charts
- **Trend Penjualan**: Line chart showing daily revenue and order count
- **Status Distribusi**: Pie chart showing order status distribution

#### Export Data
- **Excel**: Export lengkap dengan format yang rapi
- **CSV**: Export dalam format CSV untuk analisis lebih lanjut

## Kustomisasi

### Menambah Metric Baru
Edit file `models/sales_dashboard.py` dan tambahkan logic di method `get_sales_data()`:

```python
def get_sales_data(self, period='month'):
    # ... existing code ...
    
    # Tambah metric baru
    new_metric = self._calculate_new_metric(sales_orders)
    
    return {
        # ... existing data ...
        'new_metric': new_metric,
    }
```

### Modifikasi Tampilan
Edit file `static/src/xml/sales_dashboard.xml` untuk menambah atau mengubah elemen UI.

### Styling
Edit file `static/src/css/sales_dashboard.css` untuk mengubah tampilan visual.

## Model Data

Dashboard menggunakan model `sale.order` standar Odoo dengan field-field berikut:
- `date_order`: Tanggal order
- `amount_total`: Total nilai order
- `state`: Status order (draft, sent, sale, done, cancel)
- `order_line`: Lines order untuk analisis produk

## Troubleshooting

### Error: Chart.js tidak load
Pastikan koneksi internet aktif karena Chart.js di-load dari CDN.

### Error: xlsxwriter not found
Install xlsxwriter: `pip install xlsxwriter`

### Dashboard tidak muncul
1. Pastikan module sudah diinstall
2. Refresh browser
3. Check console untuk error JavaScript

### Data tidak akurat
1. Pastikan timezone server sudah benar
2. Refresh data dengan tombol refresh

## Pengembangan Lebih Lanjut

### Fitur yang Bisa Ditambahkan
1. **Filter berdasarkan sales person**
2. **Comparison dengan periode sebelumnya**
3. **Target vs actual sales**
4. **Forecast penjualan**
5. **Integration dengan WhatsApp/Email untuk laporan otomatis**

### Performance Optimization
1. Implementasi caching untuk data yang sering diakses
2. Pagination untuk data dalam jumlah besar
3. Background job untuk perhitungan kompleks

## Kontribusi

Jika Anda ingin berkontribusi:
1. Fork repository
2. Buat branch feature
3. Commit perubahan
4. Submit pull request

## Lisensi

Module ini dibuat untuk keperluan demonstrasi dan pembelajaran. Silakan disesuaikan dengan kebutuhan Anda.

## Support

Untuk pertanyaan atau bantuan teknis, silakan buat issue di repository atau hubungi tim development.

---

**Dikembangkan dengan ❤️ untuk komunitas Odoo Indonesia**