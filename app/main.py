from fastapi import FastAPI, UploadFile, HTTPException, File
from app.parser_csv import parse_csv
from app.normalization import (normalize_phone, normalize_name,
                               normalize_amount, normalize_data)

app = FastAPI()

normalizers = {
    'phone': normalize_phone,
    'fullname': normalize_name,
    'some_amount': normalize_amount
}


@app.get("/")
async def root():
    return {"message": "Парсер csv, тестовое задание"}


@app.post("/csv-processor/")
async def prosess_csv(file: UploadFile = File(...)):
    if (file.content_type != 'text/csv'):
        raise HTTPException(status_code=400,
                            detail="Invalid file type. Supported types: csv")
    try:
        file = await file.read()
        data = file.decode("utf-8")
        parsed = parse_csv(data)
        normalized = normalize_data(parsed, normalizers)
        return {"parsed": normalized}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail="Error processing file" + str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
