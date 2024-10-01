from fastapi import FastAPI, UploadFile, HTTPException, File, Query
from app.parser_csv import parse_csv
from app.normalization import (normalize_phone, normalize_name,
                               normalize_amount, normalize_data)
from typing import Annotated

app = FastAPI()

normalizers = {
    'phone': normalize_phone,
    'fullname': normalize_name,
    'some_amount': normalize_amount
}


def sorter(data, field: str, order: str):
    try:
        reverse = True if order == "descending" else False
        sorted_data = sorted(data, key=lambda x: x.get(field, ''),
                             reverse=reverse)
        return sorted_data
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f'Invalid sorting feild {e}')


@app.get("/")
async def root():
    return {"message": "Парсер csv, тестовое задание"}


@app.post("/csv-processor/")
async def prosess_csv(file: UploadFile = File(...),
                      sorting_field: Annotated[str | None,
                      Query(description='sorting field')] = None,
                      sort_order: Annotated[str | None,
                      Query(description='sorting order',
                            pattern='^ascending|descending')] = None
                      ):
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


@app.post("/csv-processor/sort")
async def prosess_csv_and_sort(file: UploadFile = File(...),
                               sorting_field: Annotated[str | None,
                               Query(description='sorting field')] = None,
                               sort_order: Annotated[str | None,
                               Query(description='sorting order',
                                     pattern='^ascending|descending')] = None
                               ):
    if (file.content_type != 'text/csv'):
        raise HTTPException(status_code=400,
                            detail="Invalid file type. Supported types: csv")
    try:
        file = await file.read()
        data = file.decode("utf-8")
        parsed = parse_csv(data)
        normalized = normalize_data(parsed, normalizers)
        if (sorting_field):
            sorted_data = sorter(normalized, sorting_field, sort_order)
        else:
            sorted_data = normalized
        return {"sorted data": sorted_data}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail="Error processing file" + str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
