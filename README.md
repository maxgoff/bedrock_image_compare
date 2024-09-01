# Bedrock Image Comparison API

This project provides an API for comparing two images stored in AWS S3 buckets using AWS Bedrock's image comparison capabilities.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/maxgoff/bedrock-image-compare.git
   cd bedrock-compare
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Ensure you have AWS credentials configured with access to S3 and Bedrock services. You can set these up using the AWS CLI or by setting environment variables:
   ```
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=your_preferred_region
   ```

## Usage

1. Start the API server:
   ```
   uvicorn api_compare:app --host 0.0.0.0 --port 8000
   ```

2. The API will be available at `http://localhost:8000`. You can use the `/compare` endpoint to compare two images.

### API Endpoint

- **POST /compare**
  - Request body:
    ```json
    {
      "image1_uri": "s3://your-bucket/path/to/image1.pdf",
      "image2_uri": "s3://your-bucket/path/to/image2.pdf"
    }
    ```
  - Response:
    ```json
    {
      "comparison_result": "Description of the differences between the two images."
    }
    ```

## Example

Using curl to make a request:

```bash
curl -X POST "http://localhost:8000/compare" \
     -H "Content-Type: application/json" \
     -d '{"image1_uri": "s3://your-bucket/image1.pdf", "image2_uri": "s3://your-bucket/image2.pdf"}'
```

## Notes

- The API accepts PDF files stored in S3 buckets. It will convert the first page of each PDF to an image for comparison.
- Ensure that your AWS credentials have the necessary permissions to access the S3 buckets and use the Bedrock service.
- The comparison is performed using AWS Bedrock's image comparison capabilities, which uses AI to describe the differences between the images.

## Error Handling

If an error occurs during the comparison process, the API will return a 500 Internal Server Error with details about the error in the response body.

## Support

For any issues or questions, please open an issue in the GitHub repository.
