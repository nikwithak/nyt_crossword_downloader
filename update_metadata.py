from pypdf import PdfReader, PdfWriter

def update_pdf(filename: str):
    reader = PdfReader(filename)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    if reader.metadata is not None:
        writer.add_metadata(reader.metadata)

    new_title = f"NYT Crossword - {filename[:-4]}"

    writer.add_metadata(
        {
            "/Title": new_title,
        }
    )

    with open(f"updated_{filename}", "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    for filename in args:
        update_pdf(filename)

