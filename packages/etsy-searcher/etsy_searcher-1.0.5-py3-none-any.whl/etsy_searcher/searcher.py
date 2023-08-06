from typing import List
from bs4 import BeautifulSoup
import requests
from etsy_searcher.models.Result import Result
from etsy_searcher.utils.prepare_request_body import prepare_listing_cards_body, prepare_listing_search_body
class EtsySearcher:
    
    def __init__(self) -> None:
        self.session = requests.Session()
        self.listing_search_url = "https://www.etsy.com/api/v3/ajax/bespoke/member/neu/specs/async_search_results"
        self.listing_cards_url = "https://www.etsy.com/api/v3/ajax/bespoke/member/neu/specs/listingCards"
        
    def get_csrf_token(self) -> str:
        req = self.session.get("https://etsy.com/")
        bs = BeautifulSoup(req.content, "html.parser")
        csrf_nonce = bs.find("meta", attrs={"name": "csrf_nonce"})
        return csrf_nonce.get("content")
          
    def get_headers(self) -> dict:
        return {
            "x-csrf-token":self.get_csrf_token(),
            "x-detected-locale": "USD|en-US|US",
            "x-recs-primary-referrer": "https://www.etsy.com/",
            "x-requested-with": "XMLHttpRequest",
            "x-recs-primary-location": "https://www.etsy.com/",
            "sec-fetch-mode": "cors",
            "origin": "https://www.etsy.com",
            "sec-fetch-dest": "empty",
            "dnt": "1",
            "pragma": "no-cache",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-site": "same-origin",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cache-control": "no-cache",
            "accept-encoding": "gzip, deflate, br",
            "accept": "*/*",
            "accept-language": "en-US,en,q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "referer": "https://www.etsy.com/"
        }
    
    def get_listing_cards(self, keyword:str, headers: dict, organic_listing_ids: List[int], ad_listing_ids: List[int]):
        data = prepare_listing_cards_body(
            keyword, organic_listing_ids, ad_listing_ids
        )
        req = self.session.post(self.listing_cards_url, data=data, headers=headers)
        return req.json().get("eventData").get("badge_lc")
    
    def json_to_result(self, organic_listing_ids: List[int], ad_listing_ids: List[int], badges: list):
                
        organic_listings = []
        for organic_listing_id in organic_listing_ids:
            for badge in badges:
                if badge[0] == organic_listing_id:
                    organic_listings.append({"listing_id": organic_listing_id, "badges": badge[1].split(" ")})
                    badges.remove(badge)
        
        ad_listings = [{"listing_id": listing_id} for listing_id in ad_listing_ids]
        return Result(organic_listings=organic_listings, ad_listings=ad_listings)    
    
    def search(self, keyword: str, max_page: int = 10, order: str = "most_relevant", only_star_seller: bool = False) -> List[Result]:
        headers = self.get_headers()
        results = []
        
        for page in range(1, max_page + 1):
            if page != 1:
                keyword_with_plus = "+".join(keyword.split(" "))
                headers.update({
                    "referer": f"https://www.etsy.com/search?q={keyword_with_plus}&ref=pagination&page={page}",
                    "x-recs-primary-location": f"https://www.etsy.com/search?q={keyword_with_plus}&ref=pagination&page={page}"
                })
                
            data = prepare_listing_search_body(keyword, page, order, only_star_seller)
            
            req = self.session.post(self.listing_search_url, data=data, headers=headers)
            
            json_data = req.json()
            organic_listing_ids = json_data.get("jsData").get("lazy_loaded_listing_ids")
            ad_listing_ids = json_data.get("jsData").get("lazy_loaded_ad_ids")
            badges = self.get_listing_cards(keyword, headers, organic_listing_ids, ad_listing_ids)
            
            result = self.json_to_result(organic_listing_ids, ad_listing_ids, badges)
            
            results.append(result)
        return results
    