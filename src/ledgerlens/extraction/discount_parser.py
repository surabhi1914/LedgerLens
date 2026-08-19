import re
from decimal import Decimal

from ledgerlens.extraction.money_parser import parse_money


def extract_discount(text: str | None) -> Decimal | None:
    if not text:
        return None

    pattern = r"""
        # Primary discount label
        \b (?:discount(?:\s*amount)?|rebate|savings) \b    
         # Ignore structural headers/metadata   
        (?!\s*(?:rate|code|type|id|number|no\.?|\#))         
        
        # Optional percentage rate (e.g. (2.91%) or 10%)
        (?:\s*\(?\s*\d+(?:\.\d+)?\s*%\s*\)?)?                  
        
        [\s:\-\#]*                                             # Separator before amount
        
        # Optional negative sign indicator, e.g., (-), -, or ( - )
        (?:\(?\s*-\s*\)?\s*)?                                   
        
        (                                                     
             # CAPTURE GROUP: monetary value only
            (?:[A-Z]{3}|[\$\u20AC\u00A3\u00A5\u20B9])?         
            # Optional leading currency symbol/code
            \s*
            (?: 
            # Standard comma-separated digits
                \d{1,3}(?:,\d{3})+(?:\.\d{1,2})?              
                |
                # Plain numeric digits
                \d+(?:\.\d{1,2})?                             
            )
        )
        # Trailing currency code outside capture group
        (?:\s*[A-Z]{3})?    
        # Ensure full number boundary match                                  
        (?!\d|[\.,]\d)  
        # Ensure captured value is NOT a standalone %                                      
        (?!\s*\%)                                             
    """

    match = re.search(pattern, text, flags=re.VERBOSE | re.IGNORECASE)
    if not match:
        return None

    candidate_str = match.group(1).strip()

    return parse_money(candidate_str)
