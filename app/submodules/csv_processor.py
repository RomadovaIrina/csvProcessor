from fastapi import UploadFile, HTTPException
from app.parser_csv import parse_csv
from app.normalization import normalize_data
from app.req_sorter import sorter


async def process_csv_file(file: UploadFile, normalizers: dict):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=415, detail="Invalid file type. Supported types: csv")

    try:
        file_content = await file.read()
        data = file_content.decode("utf-8")
        parsed_data = parse_csv(data)
        normalized_data = normalize_data(parsed_data, normalizers)
        return {"parsed": normalized_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")


async def process_and_sort(file: UploadFile, normalizers: dict, sorting_field: str, sort_order: str):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=415, detail="Invalid file type. Supported types: csv")

    try:
        file_content = await file.read()
        data = file_content.decode("utf-8")
        parsed_data = parse_csv(data)
        normalized_data = normalize_data(parsed_data, normalizers)

        if sorting_field:
            sorted_data = sorter(normalized_data, sorting_field, sort_order)
        else:
            sorted_data = normalized_data

        return {"sorted": sorted_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing and sorting file: {str(e)}")
