import magic
from uuid import uuid4
from fastapi import FastAPI, HTTPException, UploadFile, status
from loguru import logger
import uvicorn
import boto3
from botocore.exceptions import ClientError
from fastapi import Response

kb= 1024
mb= 1024*kb

SUPPORTED_FILE_TYPES ={
    'images/png': 'png',
    'image/jpeg': 'jpg',
    'application/pdf': 'pdf'
}

AWS_BUCKET = 'raqim-module5-day5'

s3 = boto3.resource('s3')
bucket = s3.Bucket(AWS_BUCKET)

async def s3_upload(contents: bytes, key: str):
    logger.info(f'Uploading {key} to s3')
    bucket.put_object(key=key, Body=contents)

async def s3_download(key: str):
    try:
        return s3.Object(bucket_name=AWS_BUCKET, key=key).get()['Body'].read()
    except ClientError as err:
        logger.error(str(err))

async def upload_folder(folder_path: str):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as file:
                contents = file.read()
                key = f'{uuid4()}-{file_name}'
                await s3_upload(contents, key)


app = FastAPI()


@app.get('/')
async def home():
    return{'message': 'Hello from file-upload'}

@app.post('/upload')
async def upload(file: UploadFile | None = None):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No File found!!'
        )
    contents= await file.read()
    size = len(contents)

    if not 0 < size <= 1 * mb:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= 'Supported file size is 0 - 1 MB'
        )

    file_type = magic.from_buffer(buffer=contents, mime=True)
    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Unsupported file type: {file_type}. Supoorted types are {SUPPORTED_FILE_TYPES}'
        )
    file_name = f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}'
    await s3_upload(contents, key= file_name)
    return {'file_name': file_name}



@app.get('/download')
async def download(file_name: str | None = None):
    if not file_name:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= 'No file name provided'
        )

    contents= await s3_download(key=file_name)
    return Response(
        content = contents,
        headers = {
            'Content-Disposition': f'attachment; filename={file_name}',
            'Content-Type': 'application/octet-stream',
            
        } 
    )



if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)