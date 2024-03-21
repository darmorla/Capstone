import validators
import shortuuid
import models
import qrcode
import tempfile

def is_valid_url(url: str) -> bool:
    return validators.url(url)

def generate_short_url(long_url: str, custom_path: str = None) -> models.URL:
    short_path = custom_path if custom_path else shortuuid.uuid()[:8]
    return models.URL(long_url=long_url, short_path=short_path)

def generate_qr_code(url: str) -> str:
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create a temporary file to save the QR code image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as qr_code_file:
        qr.make_image(fill_color="black", back_color="white").save(qr_code_file)
        qr_code_file_path = qr_code_file.name

    return qr_code_file_path
