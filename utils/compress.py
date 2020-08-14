from PIL import Image, ImageFile
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import sys
ImageFile.LOAD_TRUNCATED_IMAGES = True

def compress_image(uploaded_image, size):
    temp = Image.open(uploaded_image)
    # temp = uploaded_image
    temp.thumbnail(size, Image.ANTIALIAS)
    outputIOStream = io.BytesIO()
    # temp = temp.resize((300, 400), Image.ANTIALIAS)
    temp = temp.convert('RGB')
    temp.save(outputIOStream, format='JPEG', quality=80)
    outputIOStream.seek(0)
    uploaded_image = InMemoryUploadedFile(outputIOStream, 'ImageField', '%s.jpg', uploaded_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIOStream), None)
    # ncoded_string = base64.b64encode(uploaded_image.read())
    # print("len end ",len(ncoded_string))

    return uploaded_image
    # return {
    #     'img': uploaded_image,
    #     'base64': ncoded_string
    # }