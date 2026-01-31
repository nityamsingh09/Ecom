from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from django.http import HttpResponse
from datetime import datetime
def safe(val):
    return str(val) if val is not None else ""

def generate_invoice_pdf(order):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="invoice_{order.invoice_no}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    def rupee(val):
        return f"₹{float(val):.2f}"

    # ================= HEADER =================
    p.setFont("Helvetica-Bold", 18)
    p.drawString(40, height - 40, "NYMPH STORE")

    p.setFont("Helvetica", 9)
    p.drawString(40, height - 60, "Premium Clothing Brand")
    p.drawString(40, height - 72, "Website: nymphn.shop")

    p.line(40, height - 80, width - 40, height - 80)

    # ================= INVOICE INFO =================
    p.setFont("Helvetica", 10)
    p.drawString(40, height - 105, f"Invoice No: {safe(order.invoice_no)}")
    p.drawString(50, height - 95, f"Date: {order.order_date.strftime('%d-%m-%Y')}")

    p.drawString(
        40,
        height - 135,
        f"Payment Mode: {safe(order.payment_method).upper()}",
    )

    # ================= CUSTOMER INFO =================
    p.setFont("Helvetica-Bold", 11)
    p.drawString(40, height - 165, "Billing / Shipping Address")

    p.setFont("Helvetica", 10)
    p.drawString(40, height - 185, safe(order.full_name))
    p.drawString(40, height - 200, safe(order.address))

    p.drawString(
        40,
        height - 215,
        f"{safe(order.city)}, {safe(order.state)} - {safe(order.zip_code)}",
    )

    p.drawString(40, height - 230, f"Mobile: {safe(order.mobile)}")
    p.drawString(40, height - 245, f"Email: {safe(order.user.email)}")


    # ================= TABLE HEADER =================
    y = height - 280

    p.setFont("Helvetica-Bold", 10)
    p.drawString(40, y, "Item")
    p.drawString(240, y, "Color")
    p.drawString(300, y, "Size")
    p.drawString(350, y, "Qty")
    p.drawString(400, y, "Price")
    p.drawString(460, y, "Total")

    p.line(40, y - 5, width - 40, y - 5)

    # ================= ITEMS =================
    p.setFont("Helvetica", 10)
    y -= 25
    grand_total = 0

    for item in order.items.all():

        if y < 80:  # page break
            p.showPage()
            p.setFont("Helvetica", 10)
            y = height - 50

        p.drawString(40, y, item.item[:30])
        p.drawString(240, y, item.color or "-")
        p.drawString(300, y, item.size or "-")
        p.drawString(350, y, str(item.qty))
        p.drawString(400, y, rupee(item.price))
        p.drawString(460, y, rupee(item.total))

        grand_total += float(item.total)
        y -= 20

    # ================= TOTAL =================
    p.line(300, y - 10, width - 40, y - 10)

    p.setFont("Helvetica-Bold", 11)
    p.drawString(350, y - 30, "Grand Total")
    p.drawString(460, y - 30, rupee(grand_total))

    p.setFont("Helvetica", 9)
    p.drawString(350, y - 50, "Taxes Included")

    # ================= FOOTER =================
    p.setFont("Helvetica", 8)
    p.drawString(
        40,
        40,
        "This is a computer generated invoice. No signature required.",
    )

    p.showPage()
    p.save()

    return response





