from fastapi import HTTPException


def sorter(data, field: str, order: str):
    try:
        reverse = True if order == "descending" else False
        sorted_data = sorted(data, key=lambda x: x.get(field, ''),
                             reverse=reverse)
        return sorted_data
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f'Invalid sorting feild {e}')
