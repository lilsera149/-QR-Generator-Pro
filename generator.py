import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

def create_designer_qr(text_data, rgb_color):
    """Генерирует дизайнерский цветной QR-код со скруглениями"""
    # Настройка QR-кода с высокой коррекцией ошибок
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        box_size=10, 
        border=4
    )
    qr.add_data(text_data)
    qr.make(fit=True)
    
    # Рендеринг закругленного цветного кода
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=rgb_color)
    )
    
    # Автоматическое создание папки для выгрузки в корне проекта
    output_dir = "QR_Outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Формирование безопасного имени файла
    safe_name = "".join([c for c in text_data if c.isalnum() or c in ("-", "_")])[:20]
    if not safe_name:
        safe_name = "designer_qr"
        
    file_path = os.path.join(output_dir, f"{safe_name}.png")
    img.save(file_path)
    
    return img, safe_name
