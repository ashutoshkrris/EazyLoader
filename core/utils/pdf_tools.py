from PyPDF2 import PdfFileReader, PdfFileWriter, utils


def is_encrypted(filepath: str) -> bool:
    with open(filepath, 'rb') as f:
        pdf_reader = PdfFileReader(f, strict=False)
        return pdf_reader.isEncrypted


# Responses:
# 1 -> Encryption Success
# 2 -> Already encrypted/decrypted
# 3 -> Error while reading file


def encrypt_file(filepath: str, password: str, output_path: str) -> int:
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(open(filepath, 'rb'), strict=False)
    if is_encrypted(filepath):
        return 2

    try:
        for page_number in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page_number))
        if not password:
            password = 'EazyLoader'
        pdf_writer.encrypt(user_pwd=password, use_128bit=True)

        with open(output_path, "wb") as f:
            pdf_writer.write(f)
        return 1
    except utils.PdfReadError:
        return 3


def decrypt_file(filepath: str, password: str, output_path: str) -> int:
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(open(filepath, 'rb'), strict=False)
    if not is_encrypted(filepath):
        return 2

    pdf_reader.decrypt(password=password)
    try:
        for page_number in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page_number))
        with open(output_path, "wb") as f:
            pdf_writer.write(f)

        return 1
    except utils.PdfReadError:
        return 3
