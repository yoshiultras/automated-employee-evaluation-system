from typing import Dict, List, Union

from pydantic import BaseModel


class HTTPException(BaseModel):
    status_code: int
    detail: Union[Dict, List, str] = ""
    errors: Union[Dict, List, str] = ""
