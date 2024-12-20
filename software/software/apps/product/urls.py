from django.urls import path, include
from django.contrib.auth.decorators import login_required

from apps.product.views import index, product_view, product_list, product_edit, product_delete, \
    ProductList, ProductCreate, ProductUpdate, ProductDelete, product_detail, product_api_detail, product_api_list, import_products, product_entry_report_by_date_range, export_product_entry_report_range_pdf, export_product_entry_report_range_excel, \
    product_entry_report_day, export_product_entry_day_pdf, export_product_entry_day_excel, sales_report_day, sales_report_by_date_range, sales_report_day, sales_report_day_excel, sales_report_day_pdf, \
    sales_report_by_date_range, export_to_pdf, export_to_excel, confirm_sale, add_product_entry, product_entry_create, CustomerCreate, CustomerList
urlpatterns = [
    path('', index, name='index'),
    path('nuevo/', login_required(ProductCreate.as_view()), name='product_create'),
    path('listar/', login_required(ProductList.as_view()), name='product_list'),
    path('editar/<pk>/', login_required(ProductUpdate.as_view()), name='product_edit'),
    path('eliminar/<pk>/', login_required(ProductDelete.as_view()), name='product_delete'),
    path('product/<int:id>/', login_required(product_detail), name='product_detail'),
    path('products/', product_api_list, name='product_api_list'),
    path('products/<int:pk>/', product_api_detail, name='product_api_detail'),
    path('import/', import_products, name='import_products'),
    path('report/product_entries_range/', product_entry_report_by_date_range, name='product_entry_report_by_date_range'),
    path('report/product_entries_range/pdf/<str:start_date>/<str:end_date>/', export_product_entry_report_range_pdf, name='export_product_entry_report_range_pdf'),
    path('report/product_entries_range/excel/<str:start_date>/<str:end_date>/', export_product_entry_report_range_excel, name='export_product_entry_report_range_excel'),
    path('report/product_entry_day/', product_entry_report_day, name='product_entry_report_day'),
    path('report/product_entry_day/pdf/<str:entry_date>/', export_product_entry_day_pdf, name='export_product_entry_day_pdf'),
    path('report/product_entry_day/excel/<entry_date>/', export_product_entry_day_excel, name='export_product_entry_day_excel'),
    #path('report-sale/', report_sale, name='report_sale'),#esta url la creé para reportar una venta, pero es una funcionalidad que se quitó el 15/oct/2024, porque en el momento no se va usar
    #urls de ventas 
    path('sales-report-by-date-range/', sales_report_by_date_range, name='sales_report_by_date_range'),
    path('sales-report-by-date-range/pdf/<str:start_date>/<str:end_date>/', export_to_pdf, name='export_sales_report_range_pdf'),
    path('sales-report-by-date-range/excel/<str:start_date>/<str:end_date>/', export_to_excel, name='export_sales_report_range_excel'),
    path('sales-report-day/', sales_report_day, name='sales_report_day'),
    path('sales-report-day-pdf/', sales_report_day_pdf, name='sales_report_day_pdf'),
    path('sales-report-day-excel/', sales_report_day_excel, name='sales_report_day_excel'),
    path('confirm-sale/', confirm_sale, name='confirm_sale'),
    path('add-product-entry/', add_product_entry, name='add_product_entry'),
    path('products/entry/create/', product_entry_create, name='product_entry_create'),  # URL para registrar entrada de producto
    #urls de clientes
    path('customers/register/', CustomerCreate.as_view(), name='customer_create'),
    path('customers/list/', CustomerList.as_view(), name='customer_list'),
]