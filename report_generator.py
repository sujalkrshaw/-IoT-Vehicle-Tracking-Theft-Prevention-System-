from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

import pandas as pd


def create_pdf(csv_file, pdf_file):

    df = pd.read_csv(csv_file)

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Vehicle Tracking Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    for _, row in df.iterrows():

        text = (
            f"{row['Timestamp']} | "
            f"{row['Latitude']} | "
            f"{row['Longitude']} | "
            f"{row['Status']}"
        )

        content.append(
            Paragraph(
                text,
                styles["BodyText"]
            )
        )

    doc.build(content)