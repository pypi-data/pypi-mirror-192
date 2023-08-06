from typing import List, Optional
from pydantic import BaseModel

BADGES = {
    "pop": "Popular Now",
    "frs": "Free Shipping",
    "sts": "Star Seller",
    "pro": "Promotion",
    "bes": "Best Seller"
}

class Listing(BaseModel):
    listing_id: int
    badges: Optional[List[str]]

    def __init__(__pydantic_self__, **data) -> None:
        badges = data.get("badges")
        if badges:
            data["badges"] = [BADGES.get(badge) for badge in badges]
        super().__init__(**data)
    
class Result(BaseModel):
    organic_listings: List[Listing]
    ad_listings: List[Listing]