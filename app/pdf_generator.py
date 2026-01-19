from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO

def generate_teaser_pdf(company, data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 1 * inch

    # -------- TITLE --------
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1 * inch, y, company)

    y -= 0.4 * inch
    c.setFont("Helvetica", 10)
    c.drawString(1 * inch, y, "Confidential – For discussion purposes only")

    y -= 0.6 * inch

    # -------- SECTIONS --------
    def draw_section(title, text):
        nonlocal y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1 * inch, y, title)
        y -= 0.25 * inch

        c.setFont("Helvetica", 10)
        for line in text.split("\n"):
            c.drawString(1 * inch, y, line[:110])
            y -= 0.18 * inch

        y -= 0.25 * inch

    draw_section("Market", data["market"])
    draw_section("Company", data["company"])
    draw_section("Product", data["product"])
    draw_section("Investment Opportunity", data["investment_opportunity"])

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
