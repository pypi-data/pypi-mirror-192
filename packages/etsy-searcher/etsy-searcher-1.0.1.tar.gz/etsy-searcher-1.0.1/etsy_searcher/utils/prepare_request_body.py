from typing import List

def prepare_listing_search_body(keyword: str, page: int, order: str, only_star_seller: bool):
        
    ref = "search_bar"
    if page != 1:
        ref = "pagination"
    
    data = {
        "log_performance_metrics": True,
        "specs[async_search_results][]": "Search2_ApiSpecs_WebSearch",
        "specs[async_search_results][1][search_request_params][detected_locale][language]": "en-US",
        "specs[async_search_results][1][search_request_params][detected_locale][currency_code]": "USD",
        "specs[async_search_results][1][search_request_params][detected_locale][region]": "US",
        "specs[async_search_results][1][search_request_params][locale][language]": "en-US",
        "specs[async_search_results][1][search_request_params][locale][currency_code]": "USD",
        "specs[async_search_results][1][search_request_params][locale][region]": "US",
        "specs[async_search_results][1][search_request_params][name_map][query]": "q",
        "specs[async_search_results][1][search_request_params][name_map][query_type]": "qt",
        "specs[async_search_results][1][search_request_params][name_map][results_per_page]": "result_count",
        "specs[async_search_results][1][search_request_params][name_map][min_price]": "min",
        "specs[async_search_results][1][search_request_params][name_map][max_price]": "max",
        "specs[async_search_results][1][search_request_params][parameters][q]": keyword,
        "specs[async_search_results][1][search_request_params][parameters][order]": order,
        "specs[async_search_results][1][search_request_params][parameters][page]": page,
        "specs[async_search_results][1][search_request_params][parameters][ref]": ref,
        "specs[async_search_results][1][search_request_params][parameters][referrer]": "https://www.etsy.com/",
        "specs[async_search_results][1][search_request_params][parameters][is_prefetch]": False,
        "specs[async_search_results][1][search_request_params][parameters][placement]": "wsg",
        "specs[async_search_results][1][search_request_params][user_id]":None,
        "specs[async_search_results][1][request_type]": "pagination_preact",
        "view_data_event_name": "search_async_pagination_specview_rendered",
    }
    
    if only_star_seller:
        data.update({
            "specs[async_search_results][1][search_request_params][parameters][is_star_seller]": True
        })
    
    return data


def prepare_listing_cards_body(keyword: str, organic_listing_ids: List[int], ad_listing_ids: List[int]) -> dict:
    data = {
        "log_performance_metrics": "true",
        "specs[listingCards][]": "Search2_ApiSpecs_LazyListingCards",
        "specs[listingCards][1][listing_ids][]": organic_listing_ids,
        "specs[listingCards][1][ad_ids][]": ad_listing_ids,
        "specs[listingCards][1][search_request_params][detected_locale][language]": "en-US",
        "specs[listingCards][1][search_request_params][detected_locale][currency_code]": "TRY",
        "specs[listingCards][1][search_request_params][detected_locale][region]": "TR",
        "specs[listingCards][1][search_request_params][locale][language]": "en-US",
        "specs[listingCards][1][search_request_params][locale][currency_code]": "USD",
        "specs[listingCards][1][search_request_params][locale][region]": "US",
        "specs[listingCards][1][search_request_params][name_map][query]": "q",
        "specs[listingCards][1][search_request_params][name_map][query_type]": "qt",
        "specs[listingCards][1][search_request_params][name_map][results_per_page]": "result_count",
        "specs[listingCards][1][search_request_params][name_map][min_price]": "min",
        "specs[listingCards][1][search_request_params][name_map][max_price]": "max",
        "specs[listingCards][1][search_request_params][parameters][q]": keyword,
        "specs[listingCards][1][search_request_params][parameters][explicit]": "1",
        "specs[listingCards][1][search_request_params][parameters][ref]": "search_bar",
        "specs[listingCards][1][search_request_params][parameters][is_personalizable]": True,
        "specs[listingCards][1][search_request_params][parameters][utm_medium]": None, 
        "specs[listingCards][1][search_request_params][parameters][utm_source]": None, 
        "specs[listingCards][1][search_request_params][parameters][placement]": "wsg",
        "specs[listingCards][1][search_request_params][parameters][page_type]": "search",
        "specs[listingCards][1][search_request_params][parameters][referrer]": None, 
        "specs[listingCards][1][search_request_params][parameters][user_id]": None, 
        "specs[listingCards][1][search_request_params][parameters][filter_distracting_content]": True,
        "specs[listingCards][1][search_request_params][parameters][spell_correction_via_mmx]": True,
        "specs[listingCards][1][search_request_params][parameters][interleaving_option]": None, 
        "specs[listingCards][1][search_request_params][parameters][result_count]": 48,
        "specs[listingCards][1][search_request_params][user_id]": None,
        "specs[listingCards][1][is_mobile]": False,
        "specs[listingCards][1][organic_listings_count]": 0,
        "view_data_event_name": "search_lazy_loaded_cards_specview_rendered"
    }
    return data