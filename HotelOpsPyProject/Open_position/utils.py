# import os
# import random
# from django.conf import settings
# from PIL import Image, ImageDraw, ImageFont
# import qrcode
# from io import BytesIO
# from .azure import upload_file_to_blob  

# def generate_position_image(position_name, qr_url, location_name, output_path):
#     base_image_filename = f"{location_name}.jpeg"
#     base_image_path = os.path.join(settings.MEDIA_ROOT, 'images', base_image_filename)

#     try:
#         img = Image.open(base_image_path)
#     except FileNotFoundError:
#         raise FileNotFoundError(f"The base image file was not found: {base_image_path}")

#     draw = ImageDraw.Draw(img)

#     try:
#         font_large = ImageFont.truetype("arial.ttf", 45)
#         font_small = ImageFont.truetype("arial.ttf", 20)
#     except IOError:
#         font_large = ImageFont.load_default()
#         font_small = ImageFont.load_default()

#     draw.text((75, 415), position_name, font=font_large, fill=(50, 50, 50))

#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=20,
#         border=4,
#     )
#     qr.add_data(qr_url)
#     qr.make(fit=True)

#     qr_img = qr.make_image(fill='black', back_color='white')
#     qr_img = qr_img.resize((220, 220))

#     img.paste(qr_img, (700, 1050))

#     draw.text((725, 1050), "Scan here to Apply", font=font_small, fill=(50, 50, 50))

#     unique_folder = os.path.join(settings.MEDIA_ROOT, 'generated_images')
#     os.makedirs(unique_folder, exist_ok=True)

#     unique_id = f"{random.randint(10000, 99999)}"
#     sanitized_position_name = position_name.replace(' ', '_')
#     unique_filename = f"{location_name}_{unique_id}_{sanitized_position_name}.jpeg"
#     unique_file_path = os.path.join(unique_folder, unique_filename)

#     img.save(unique_file_path)

#     try:
        
#         image_url = upload_file_to_blob(unique_file_path)
#     except Exception as e:
#         raise RuntimeError(f"Failed to upload image to Azure Blob Storage: {str(e)}")

#     return image_url
import os
import random
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import qrcode
from io import BytesIO
from .azure import upload_file_to_blob  

import os
import random
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import qrcode
from io import BytesIO
from .azurebanner import Bannerupload_file_to_blob  

# def generate_position_image(position_name, qr_url, location_name):
#     base_image_path_without_ext = os.path.join(settings.MEDIA_ROOT, 'Hotel_Logos', location_name)
 
#     # Check for both .jpeg and .jpg extensions
#     if os.path.exists(f"{base_image_path_without_ext}.jpeg"):
#         base_image_path = f"{base_image_path_without_ext}.jpeg"
#     elif os.path.exists(f"{base_image_path_without_ext}.jpg"):
#         base_image_path = f"{base_image_path_without_ext}.jpg"
#     else:
#         base_image_path = None  # Handle the case where neither file exists
 
#     # Use base_image_path in your logic
#     if base_image_path:
#         print(f"Image found: {base_image_path}")
#     else:
#         print("Image not found.")

    

#     try:
#         img = Image.open(base_image_path)
#     except FileNotFoundError:
#         raise FileNotFoundError(f"The base image file was not found: {base_image_path}")

#     draw = ImageDraw.Draw(img)

#     try:
#         font_large = ImageFont.truetype("arial.ttf", 45)
#         font_small = ImageFont.truetype("arial.ttf", 20)
#     except IOError:
#         font_large = ImageFont.load_default()
#         font_small = ImageFont.load_default()

#     draw.text((75, 415), position_name, font=font_large, fill=(50, 50, 50))

#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=20,
#         border=4,
#     )
#     qr.add_data(qr_url)
#     qr.make(fit=True)

#     qr_img = qr.make_image(fill='black', back_color='white')
#     qr_img = qr_img.resize((220, 220))

#     img.paste(qr_img, (700, 1050))

#     draw.text((725, 1050), "Scan here to Apply", font=font_small, fill=(50, 50, 50))

    
#     image_io = BytesIO()
#     img.save(image_io, format='JPEG')
#     image_io.seek(0)

#     # Read the bytes from the BytesIO object
#     image_bytes = image_io.getvalue()

#     unique_id = f"{random.randint(10000, 99999)}"
#     sanitized_position_name = position_name.replace(' ', '_')
#     unique_filename = f"{location_name}_{unique_id}_{sanitized_position_name}.jpeg"

#     try:
#         # Pass the bytes to the upload function
#         image_url = upload_file_to_blob(image_bytes, unique_filename)
#     except Exception as e:
#         raise RuntimeError(f"Failed to upload image to Azure Blob Storage: {str(e)}")

#     return image_url

from app.models import OrganizationMaster

def generate_position_image(position_name, qr_url, location_name):
    base_image_path_without_ext = os.path.join(settings.MEDIA_ROOT, 'Hotel_Logos', location_name)
    
    print("base_image_path_without_ext:", base_image_path_without_ext)
 
    # Check for both .jpeg and .jpg extensions
    if os.path.exists(f"{base_image_path_without_ext}.jpeg"):
        base_image_path = f"{base_image_path_without_ext}.jpeg"
    elif os.path.exists(f"{base_image_path_without_ext}.jpg"):
        base_image_path = f"{base_image_path_without_ext}.jpg"
    else:
        raise FileNotFoundError("Base image file not found.")
    
    print("base_image_path::",base_image_path)

    try:
        img = Image.open(base_image_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The base image file was not found: {base_image_path}")

    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype("arial.ttf", 22)
        font_small = ImageFont.truetype("arial.ttf", 15)
        font_Extra_large = ImageFont.truetype("arial.ttf", 100)
    except IOError:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    selected_orgs = ['2150', '2140', '2130', '2120']
    # selected_orgs = ['1501', '2010', '2130', '2120']
    current_location = location_name
    color = (0, 0, 0) if current_location in selected_orgs else (255, 255, 255)


    # Calculate text position for right alignment
    # text_bbox = draw.textbbox((0, 0), position_name, font=font_large)  # Get bounding box
    # text_width = text_bbox[2] - text_bbox[0]  # Calculate width
    # text_x =688  #img.width - text_width - 375 # 325px padding from the right
    # text_y = 280  # Adjusted vertical position

    # Mimic bold by drawing with slight offsets
    #for offset in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        #draw.text((text_x + offset[0], text_y + offset[1]), position_name, font=font_large, fill=(255, 255, 255))
    # draw.text((text_x , text_y), position_name, font=font_large, fill=(255, 255, 255))


    if current_location in selected_orgs:
        text_bbox = draw.textbbox((0, 0), position_name, font=font_Extra_large)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # hiring_center_x = 2780   
        hiring_center_x = 2900   
        hiring_bottom_y = 1000 

        text_x = hiring_center_x - (text_width // 2)
        text_y = hiring_bottom_y + 15  

        draw.text((text_x, text_y), position_name, font=font_Extra_large, fill=color)
    else:
        # Calculate text position for right alignment
        text_bbox = draw.textbbox((0, 0), position_name, font=font_large)  
        text_width = text_bbox[2] - text_bbox[0]  
        text_x =688 
        text_y = 280  
        draw.text((text_x , text_y), position_name, font=font_large, fill=(255, 255, 255))

        # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=17,
        border=1,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill='black', back_color='white')
    qr_img = qr_img.resize((150, 150))

    
    qr_x = img.width - qr_img.width - 50  # 50px padding from the right
    qr_y = img.height - qr_img.height - 50  # 50px padding from the bottom
    img.paste(qr_img, (qr_x, qr_y))

    
    scan_text = "Scan here to Apply"
    scan_text_bbox = draw.textbbox((0, 0), scan_text, font=font_small)  # Get bounding box
    scan_text_width = scan_text_bbox[2] - scan_text_bbox[0]  # Calculate width
    scan_text_x = qr_x + (qr_img.width - scan_text_width) // 2  # Center align below QR code
    scan_text_y = qr_y + qr_img.height + 5  # Position below QR code

    
    draw.text((scan_text_x, scan_text_y), scan_text, font=font_small, fill=(255, 255, 255))  # White text
    
    image_io = BytesIO()
    img.save(image_io, format='JPEG')
    image_io.seek(0)

   
    unique_id = f"{random.randint(10000, 99999)}"
    sanitized_position_name = position_name.replace(' ', '_')
    unique_filename = f"{location_name}_{unique_id}_{sanitized_position_name}.jpeg"

    try:
        image_url = Bannerupload_file_to_blob(image_io.getvalue(), unique_filename)
    except Exception as e:
        raise RuntimeError(f"Failed to upload image to Azure Blob Storage: {str(e)}")

    return image_url




# get_organization_Shortname_name_from_location
def get_organization_Shortname_name_from_location(location_value):
    """
    Returns ShortDisplayLabel based on OrganizationID or OrganizationName
    """
    if not location_value:
        return "Unknown Organization"

    try:
        if str(location_value).isdigit():
            organization = OrganizationMaster.objects.filter(
                OrganizationID=int(location_value)
            ).values_list("ShortDisplayLabel", flat=True).first()
        else:
            organization = OrganizationMaster.objects.filter(
                OrganizationName=location_value
            ).values_list("ShortDisplayLabel", flat=True).first()

        return organization or "Unknown Organization"

    except OrganizationMaster.DoesNotExist:
        return "Unknown Organization"
    except Exception:
        return "Unknown Organization"
