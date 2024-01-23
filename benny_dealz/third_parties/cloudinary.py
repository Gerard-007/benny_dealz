import cloudinary
from decouple import config
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name=config('CLOUD_NAME'),
    api_key=config('API_KEY'),
    api_secret=config('API_SECRET'),
    secure=True,
)
