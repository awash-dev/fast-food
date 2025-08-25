import cloudinary
import cloudinary.uploader
import cloudinary.api
from config import Config
from werkzeug.utils import secure_filename
import os

def configure_cloudinary():
    """Configure Cloudinary with credentials from config"""
    cloudinary.config(
        cloud_name=Config.CLOUDINARY_CLOUD_NAME,
        api_key=Config.CLOUDINARY_API_KEY,
        api_secret=Config.CLOUDINARY_API_SECRET
    )

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def upload_image(file, folder="fastfood-app", transformation=None):
    """
    Upload an image to Cloudinary
    
    Args:
        file: File object from request
        folder: Cloudinary folder to store the image
        transformation: Optional transformation parameters
    
    Returns:
        dict: Upload result with URL and public_id
    """
    configure_cloudinary()
    
    try:
        # Check if the file is allowed
        if not allowed_file(file.filename):
            return {"error": "File type not allowed"}
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Read file data
        file_data = file.read()
        
        # Set default transformation if none provided
        if transformation is None:
            transformation = {
                "width": 800,
                "height": 600,
                "crop": "limit",
                "quality": "auto"
            }
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file_data,
            folder=folder,
            transformation=[transformation]
        )
        
        return {
            "url": upload_result.get("secure_url"),
            "public_id": upload_result.get("public_id"),
            "filename": filename
        }
        
    except Exception as e:
        return {"error": str(e)}

def delete_image(public_id):
    """
    Delete an image from Cloudinary
    
    Args:
        public_id: The public ID of the image to delete
    
    Returns:
        dict: Result of the deletion operation
    """
    configure_cloudinary()
    
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result
    except Exception as e:
        return {"error": str(e)}

def generate_image_url(public_id, transformation=None):
    """
    Generate a URL for an image with optional transformations
    
    Args:
        public_id: The public ID of the image
        transformation: Transformation parameters
    
    Returns:
        str: The generated URL
    """
    configure_cloudinary()
    
    if transformation is None:
        transformation = {
            "width": 400,
            "height": 300,
            "crop": "fill",
            "quality": "auto"
        }
    
    return cloudinary.CloudinaryImage(public_id).build_url(transformation=transformation)