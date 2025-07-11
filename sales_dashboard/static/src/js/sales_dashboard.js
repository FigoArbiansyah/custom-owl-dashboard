/** @odoo-module **/

import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
import { Component, useState, onWillStart, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class SalesDashboard extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        this.state = useState({
            data: {},
            topProducts: [],
            period: 'month',
            loading: true,
            chartsLoaded: false,
            chartErrors: {
                revenue: false,
                status: false
            }
        });

        onWillStart(async () => {
            try {
                await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js");
                await this.loadData();
            } catch (error) {
                console.error("Error during initialization:", error);
                this.notification.add("Error initializing dashboard", {
                    type: "danger",
                    title: "Initialization Error",
                });
            }
        });

        onMounted(() => {
            // Add delay to ensure DOM is ready
            setTimeout(() => {
                this.renderCharts();
            }, 1000);
        });
    }

    async loadData() {
        try {
            this.state.loading = true;
            const [salesData, topProducts] = await Promise.all([
                this.rpc("/web/dataset/call_kw/sales.dashboard/get_sales_data", {
                    model: "sales.dashboard",
                    method: "get_sales_data",
                    args: [],
                    kwargs: { period: this.state.period },
                }),
                this.rpc("/web/dataset/call_kw/sales.dashboard/get_top_products", {
                    model: "sales.dashboard",
                    method: "get_top_products",
                    args: [],
                    kwargs: { period: this.state.period, limit: 5 },
                })
            ]);

            this.state.data = salesData;
            this.state.topProducts = topProducts;
        } catch (error) {
            console.error("Error loading sales data:", error);
            this.notification.add("Error loading sales data", {
                type: "danger",
                title: "Error",
            });
        } finally {
            this.state.loading = false;
        }
    }

    async exportData(format) {
        try {
            const url = `/sales_dashboard/export_data?period=${this.state.period}&format=${format}`;
            window.open(url, '_blank');
        } catch (error) {
            console.error("Error exporting data:", error);
            this.notification.add("Error exporting data", {
                type: "danger",
                title: "Export Error",
            });
        }
    }

    async refreshData() {
        try {
            await this.loadData();
            setTimeout(() => {
                this.renderCharts();
            }, 1000);
            this.notification.add("Data refreshed successfully", {
                type: "success",
                title: "Success",
            });
        } catch (error) {
            console.error("Error refreshing data:", error);
            this.notification.add("Error refreshing data", {
                type: "danger",
                title: "Refresh Error",
            });
        }
    }

    async onPeriodChange(period) {
        try {
            this.state.period = period;
            await this.loadData();
            setTimeout(() => {
                this.renderCharts();
            }, 1000);
        } catch (error) {
            console.error("Error changing period:", error);
            this.notification.add("Error changing period", {
                type: "danger",
                title: "Period Change Error",
            });
        }
    }

    renderCharts() {
        try {
            // Check if Chart.js is loaded
            if (typeof Chart === 'undefined') {
                console.error("Chart.js is not loaded");
                this.notification.add("Chart library not loaded", {
                    type: "danger",
                    title: "Chart Error",
                });
                return;
            }

            // Check if data is available
            if (!this.state.data || Object.keys(this.state.data).length === 0) {
                console.warn("No data available for charts");
                return;
            }

            // Reset chart error states
            this.state.chartErrors.revenue = false;
            this.state.chartErrors.status = false;

            // Render Revenue Chart
            this.renderRevenueChart();

            // Render Status Distribution Chart
            this.renderStatusChart();

            this.state.chartsLoaded = true;
        } catch (error) {
            console.error("Error rendering charts:", error);
            this.notification.add("Error rendering charts", {
                type: "danger",
                title: "Chart Rendering Error",
            });
        }
    }

    renderRevenueChart() {
        try {
            const ctx = document.getElementById('revenueChart');
            if (!ctx) {
                console.warn("Revenue chart canvas not found");
                this.state.chartErrors.revenue = true;
                return;
            }

            // Validate data structure
            if (!this.state.data.daily_sales || !Array.isArray(this.state.data.daily_sales)) {
                console.warn("Invalid daily sales data structure");
                this.state.chartErrors.revenue = true;
                return;
            }

            const dailyData = this.state.data.daily_sales;

            // Check if data is not empty
            if (dailyData.length === 0) {
                console.warn("No daily sales data available");
                this.state.chartErrors.revenue = true;
                return;
            }

            // Validate data fields
            const hasRequiredFields = dailyData.every(d =>
                d.hasOwnProperty('date') &&
                d.hasOwnProperty('revenue') &&
                d.hasOwnProperty('orders')
            );

            if (!hasRequiredFields) {
                console.warn("Daily sales data missing required fields");
                this.state.chartErrors.revenue = true;
                return;
            }

            // Destroy existing chart if exists
            if (this.revenueChart) {
                try {
                    this.revenueChart.destroy();
                } catch (destroyError) {
                    console.warn("Error destroying existing revenue chart:", destroyError);
                }
            }

            // Create new chart
            this.revenueChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dailyData.map(d => d.date),
                    datasets: [{
                        label: 'Revenue',
                        data: dailyData.map(d => parseFloat(d.revenue) || 0),
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        tension: 0.1
                    }, {
                        label: 'Orders',
                        data: dailyData.map(d => parseInt(d.orders) || 0),
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        yAxisID: 'y1',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    scales: {
                        y: {
                            type: 'linear',
                            display: true,
                            position: 'left',
                            title: {
                                display: true,
                                text: 'Revenue'
                            }
                        },
                        y1: {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            title: {
                                display: true,
                                text: 'Orders'
                            },
                            grid: {
                                drawOnChartArea: false,
                            },
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    if (context.datasetIndex === 0) {
                                        return `Revenue: ${context.parsed.y.toLocaleString('id-ID', {
                                            style: 'currency',
                                            currency: 'IDR'
                                        })}`;
                                    } else {
                                        return `Orders: ${context.parsed.y}`;
                                    }
                                }
                            }
                        }
                    }
                }
            });

            console.log("Revenue chart rendered successfully");
        } catch (error) {
            console.error("Error rendering revenue chart:", error);
            this.state.chartErrors.revenue = true;
            this.notification.add("Error rendering revenue chart", {
                type: "warning",
                title: "Chart Error",
            });
        }
    }

    renderStatusChart() {
        try {
            const ctx = document.getElementById('statusChart');
            if (!ctx) {
                console.warn("Status chart canvas not found");
                this.state.chartErrors.status = true;
                return;
            }

            // Validate data structure
            if (!this.state.data.status_distribution || !Array.isArray(this.state.data.status_distribution)) {
                console.warn("Invalid status distribution data structure");
                this.state.chartErrors.status = true;
                return;
            }

            const statusData = this.state.data.status_distribution;

            // Check if data is not empty
            if (statusData.length === 0) {
                console.warn("No status distribution data available");
                this.state.chartErrors.status = true;
                return;
            }

            // Validate data fields
            const hasRequiredFields = statusData.every(d =>
                d.hasOwnProperty('label') &&
                d.hasOwnProperty('value') &&
                d.hasOwnProperty('color')
            );

            if (!hasRequiredFields) {
                console.warn("Status distribution data missing required fields");
                this.state.chartErrors.status = true;
                return;
            }

            // Destroy existing chart if exists
            if (this.statusChart) {
                try {
                    this.statusChart.destroy();
                } catch (destroyError) {
                    console.warn("Error destroying existing status chart:", destroyError);
                }
            }

            // Create new chart
            this.statusChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: statusData.map(d => d.label),
                    datasets: [{
                        data: statusData.map(d => parseFloat(d.value) || 0),
                        backgroundColor: statusData.map(d => d.color),
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((context.parsed / total) * 100).toFixed(1);
                                    return `${context.label}: ${context.parsed} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });

            console.log("Status chart rendered successfully");
        } catch (error) {
            console.error("Error rendering status chart:", error);
            this.state.chartErrors.status = true;
            this.notification.add("Error rendering status chart", {
                type: "warning",
                title: "Chart Error",
            });
        }
    }

    // Method to retry chart rendering
    retryChartRendering() {
        try {
            setTimeout(() => {
                this.renderCharts();
            }, 1000);
            this.notification.add("Charts refreshed successfully", {
                type: "success",
                title: "Success",
            });
        } catch (error) {
            console.error("Error retrying chart rendering:", error);
            this.notification.add("Error retrying chart rendering", {
                type: "danger",
                title: "Retry Error",
            });
        }
    }

    // Method to check if charts have errors
    hasChartErrors() {
        return this.state.chartErrors.revenue || this.state.chartErrors.status;
    }

    formatCurrency(amount) {
        try {
            return new Intl.NumberFormat('id-ID', {
                style: 'currency',
                currency: 'IDR'
            }).format(amount);
        } catch (error) {
            console.error("Error formatting currency:", error);
            return `IDR ${amount}`;
        }
    }

    get periodLabel() {
        const labels = {
            'day': 'Hari Ini',
            'week': 'Minggu Ini',
            'month': 'Bulan Ini',
            'year': 'Tahun Ini'
        };
        return labels[this.state.period] || 'Bulan Ini';
    }

    // Cleanup method
    willDestroy() {
        try {
            if (this.revenueChart) {
                this.revenueChart.destroy();
            }
            if (this.statusChart) {
                this.statusChart.destroy();
            }
        } catch (error) {
            console.error("Error destroying charts:", error);
        }
    }
}

SalesDashboard.template = "sales_dashboard.Dashboard";

registry.category("actions").add("sales_dashboard", SalesDashboard);