from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel

class BacktestRequest(BaseModel):
    symbols: List[str]
    startDate: datetime
    endDate: datetime
    strategy: str
    strategyParams: Dict[str, Any]
    startingCash: float
