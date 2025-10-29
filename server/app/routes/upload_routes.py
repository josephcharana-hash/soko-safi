from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

upload_bp = Blueprint('upload_bp', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/image', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Upload to Cloudinary
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
        upload_preset = os.getenv('CLOUDINARY_UPLOAD_PRESET')
        
        if not cloud_name or not upload_preset:
            return jsonify({'error': 'Cloudinary configuration missing'}), 500
        
        # Prepare the upload
        upload_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"
        
        files = {'file': file}
        data = {
            'upload_preset': upload_preset,
            'folder': 'soko-safi'
        }
        
        # Upload to Cloudinary
        response = requests.post(upload_url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'message': 'File uploaded successfully',
                'url': result['secure_url'],
                'public_id': result['public_id']
            }), 200
        else:
            return jsonify({'error': 'Upload failed'}), 500
            
    except Exception as e:
        return jsonify({'error': 'Upload failed'}), 500
