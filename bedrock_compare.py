import os
import base64
import tempfile
from pdf2image import convert_from_path
from PIL import Image
import boto3
import json

def download_file_from_s3(s3_uri, local_path):
    s3 = boto3.client('s3')
    bucket, key = s3_uri.replace("s3://", "").split("/", 1)
    s3.download_file(bucket, key, local_path)

def convert_pdf_to_image(pdf_path, output_path):
    pages = convert_from_path(pdf_path)
    if pages:
        pages[0].save(output_path, 'JPEG')
        return output_path
    return None

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def compare_images(image1_s3_uri, image2_s3_uri):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download files from S3
        image1_path = os.path.join(temp_dir, 'image1.pdf')
        image2_path = os.path.join(temp_dir, 'image2.pdf')
        download_file_from_s3(image1_s3_uri, image1_path)
        download_file_from_s3(image2_s3_uri, image2_path)

        # Convert PDFs to images
        image1_converted = convert_pdf_to_image(image1_path, os.path.join(temp_dir, 'temp_image1.jpg'))
        image2_converted = convert_pdf_to_image(image2_path, os.path.join(temp_dir, 'temp_image2.jpg'))
        
        if not image1_converted or not image2_converted:
            return 'Error: Failed to convert PDF to image'

        # Encode images
        base64_image1 = encode_image(image1_converted)
        base64_image2 = encode_image(image2_converted)

    # Prepare the payload for Bedrock
    payload = {
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': 1000,
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'image',
                        'source': {
                            'type': 'base64',
                            'media_type': 'image/jpeg',
                            'data': base64_image1
                        }
                    },
                    {
                        'type': 'image',
                        'source': {
                            'type': 'base64',
                            'media_type': 'image/jpeg',
                            'data': base64_image2
                        }
                    },
                    {
                        'type': 'text',
                        'text': 'Compare these two images and describe the differences.'
                    }
                ]
            }
        ]
    }

    # Initialize Bedrock client
    bedrock = boto3.client(service_name='bedrock-runtime')

    # Invoke Bedrock
    response = bedrock.invoke_model(
        body=json.dumps(payload),
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        accept='application/json',
        contentType='application/json'
    )

    # Parse and return the response
    response_body = json.loads(response.get('body').read())
    return response_body['content'][0]['text']

# Main function and cleanup code removed
