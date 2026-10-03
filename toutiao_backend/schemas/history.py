from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class HistoryAddRequest(BaseModel):
    news_id : int = Field(..., alias="newsId")

class HistoryItem(NewsItemBase):
    view_time: datetime = Field(..., alias="viewTime")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class HistoryListResponse(BaseModel):
    list : list[HistoryItem]
    total : int
    hasMore : bool = Field(..., alias="hasMore")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )