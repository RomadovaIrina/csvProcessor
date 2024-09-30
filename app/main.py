from fastapi import FastAPI, UploadFile, HTTPException, File
import csv
from app.parser_csv import parse_csv
from app.normalization import normalize_phone, normalize_name, normalize_amount, normalize_data

app = FastAPI()

# Словарь с функциями нормализации для каждого ключа
normalizers = {
    'phone': normalize_phone,
    'fullname': normalize_name,
    'some_amount': normalize_amount
}

@app.get("/")
async def root():
    return {"message": "Парсер csv, тестовое задание"}


@app.post("/process-csv/")
async def process_csv(file: UploadFile = File(...)):
    try:
        file = await file.read()
        data = file.decode("utf-8")
        parsed_data = parse_csv(data)
        normalized_data = normalize_data(parsed_data, normalizers)
        return {"data": normalized_data}
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(ex)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
