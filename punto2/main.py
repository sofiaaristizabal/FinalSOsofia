from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import boto3
import io
import csv
from botocore.exceptions import ClientError

class Persona(BaseModel):
    nombre: str
    edad: int
    altura: float

def uploadPersona(person: Persona):

    s3 = boto3.client('s3')
    bucket_name = 'sam-bucket-final'
    file_name = 'personas.csv'
    item_data = person.model_dump()
    csv_buffer = io.StringIO()

    try:
        existing_obj = s3.get_object(Bucket=bucket_name, Key=file_name)
        existing_data = existing_obj['Body'].read().decode('utf-8')

        csv_reader = list(csv.DictReader(io.StringIO(existing_data)))
        csv_reader.append(item_data)

        writer = csv.DictWriter(csv_buffer, fieldnames=item_data.keys())
        writer.writeheader()
        writer.writerows(csv_reader)
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            writer = csv.DictWriter(csv_buffer, fieldnames=item_data.keys())
            writer.writeheader()
            writer.writerow(item_data)
        else:
            raise

    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=csv_buffer.getvalue(),
        ContentType='text/csv'
    )

    return {"mensaje": "persona guardada exitosamente"}

def getNumberRows():
    s3 = boto3.client('s3')
    bucket_name = 'sam-bucket-final'
    file_name = 'personas.csv'

    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file_name)
        content = obj['Body'].read().decode('utf-8')
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        
        num_rows = len(rows) - 1 if len(rows) > 1 else 0
        return {"rows": num_rows}
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return {"rows": 0}
        else:
            raise

app = FastAPI()


@app.post("/personas/", status_code=status.HTTP_201_CREATED)
def upload_persona(persona: Persona):
    return uploadPersona(persona)
    
@app.get("/personas/")
def read_root():
    return getNumberRows()

@app.get("/")
def read_item():
    return {"message":"Final Sofia"}
