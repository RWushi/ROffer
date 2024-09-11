from docx.shared import Pt


async def company_information(doc, company_data):
    section = doc.sections[0]
    header = section.header

    phone, address, email, name = company_data

    for paragraph in header.paragraphs:
        for run in paragraph.runs:
            if "Номер телефона:" in run.text:
                run.text = f"Номер телефона: {phone}"
                run.font.size = Pt(12)
            if "Адрес:" in run.text:
                run.text = f"Адрес: {address}"
                run.font.size = Pt(12)
            if "Email:" in run.text:
                run.text = f"Email: {email}"
                run.font.size = Pt(12)

    for paragraph in doc.paragraphs:
        if "КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ от" in paragraph.text:
            paragraph.text = f"КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ от {name}"
            for run in paragraph.runs:
                run.font.size = Pt(14)
