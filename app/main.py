from fastapi import FastAPI, UploadFile, File, Query
from app.submodules.csv_processor import process_csv_file, process_and_sort
from app.normalization import normalizers
from typing import Annotated

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Парсер csv, тестовое задание"}


@app.post("/csv-processor/")
async def prosess_csv(file: UploadFile = File(...)):
    res = await process_csv_file(file, normalizers)
    return res


@app.post("/csv-processor/sort")
async def prosess_csv_and_sort(file: UploadFile = File(...),
                               sorting_field: Annotated[str | None,
                               Query(description='sorting field')] = None,
                               sort_order: Annotated[str | None,
                               Query(description='sorting order',
                                     pattern='^ascending|descending')] = None
                               ):
    res = await process_and_sort(file, normalizers, sorting_field, sort_order)
    return res


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
