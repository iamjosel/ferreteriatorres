from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
import openpyxl

'''def export_to_pdf(request, sales, start_date, end_date, total_sales_quantity, total_sales_value):
    template = get_template('products/sales_report_by_date_range_pdf.html')
    context = {
        'sales': sales,
        'start_date': start_date,
        'end_date': end_date,
        'total_sales_quantity': total_sales_quantity,
        'total_sales_value': total_sales_value,
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
    pisa_status = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    
    # Generar el PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    
    return None

def export_to_excel(sales, start_date, end_date):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sales Report"

    # Escribir encabezados
    ws.append(['Producto', 'Precio Venta', 'Cantidad Vendida'])

    # Escribir datos de ventas
    for sale in sales:
        ws.append([sale.product.product_name, sale.product.selling_price, sale.quantity_sold])

    # Crear respuesta para enviar el archivo
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="sales_report_{start_date}_to_{end_date}.xlsx"'
    wb.save(response)
    return response
'''