"""Generates the PDF certificate for users who pass the assessment."""
import uuid
from datetime import date

from fpdf import FPDF

INK = (31, 77, 63)
INDIGO = (31, 77, 63)
TEAL = (201, 134, 28)
GREY = (100, 116, 139)


def _latin1(text: str) -> str:
    # The built-in PDF fonts only support Latin-1 characters
    return text.encode("latin-1", "replace").decode("latin-1")


def make_certificate(name: str, score: int, total: int,
                     cert_id: str | None = None, issued: date | None = None) -> bytes:
    cert_id = cert_id or uuid.uuid4().hex[:10].upper()
    issued = issued or date.today()

    pdf = FPDF(orientation="L", format="A4")  # 297 x 210 mm
    pdf.set_auto_page_break(False)
    pdf.add_page()

    # Frame: thick ink border with a thin teal inner line
    pdf.set_draw_color(*INK)
    pdf.set_line_width(2.2)
    pdf.rect(10, 10, 277, 190)
    pdf.set_draw_color(*TEAL)
    pdf.set_line_width(0.6)
    pdf.rect(15, 15, 267, 180)

    def line(text, size, style="", color=GREY, height=10, gap=0):
        pdf.set_font("Helvetica", style, size)
        pdf.set_text_color(*color)
        pdf.cell(0, height, _latin1(text), align="C", new_x="LMARGIN", new_y="NEXT")
        if gap:
            pdf.ln(gap)

    pdf.set_y(28)
    line("PolicyCompass", 13, "B", TEAL, 8, gap=4)
    line("Certificate of Completion", 34, "B", INK, 16, gap=6)
    line("This certifies that", 14, gap=2)
    line(name, 30, "B", (20, 20, 20), 16, gap=4)
    line("has successfully completed the Compliance Policy Training assessment", 14)
    line("covering the Code of Conduct, Anti-Bribery, POSH and Data Privacy policies.", 14, gap=8)

    percent = round(100 * score / total)
    line(f"Score: {score} / {total}  ({percent}%)", 18, "B", INDIGO, 12, gap=10)
    line(f"Date: {issued.strftime('%d %B %Y')}     Certificate ID: {cert_id}", 11)

    pdf.set_y(178)
    line("Issued by PolicyCompass, a student demo project.", 9, height=5)
    line("This is not an official Infosys certification.", 9, height=5)

    return bytes(pdf.output())


if __name__ == "__main__":
    with open("sample_certificate.pdf", "wb") as f:
        f.write(make_certificate("Test Student", 4, 5))
    print("Saved sample_certificate.pdf")
