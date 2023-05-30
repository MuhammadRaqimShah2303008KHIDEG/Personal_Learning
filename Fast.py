import magic
from uuid import uuid4
from fastapi import FastAPI, HTTPException, UploadFile, status
from loguru import logger
import uvicorn
import boto3

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
    bucket.put_object(Key=key, Body=contents)


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

    await s3_upload(contents, key=f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}')

if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
   
