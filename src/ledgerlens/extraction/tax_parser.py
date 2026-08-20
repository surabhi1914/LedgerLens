import re
from decimal import Decimal

from ledgerlens.extraction.money_parser import parse_money


def extract_tax(text: str | None) -> Decimal | None:
    if not text:
        return None

    pattern = r"""
        # Initial primary tax label
        \b (?:sales\s*tax|tax(?:\s*amount)?|vat|gst|hst) \b    
        # Ignore structural tax headers
        (?!\s*(?:rate|id|number|no\.?|\#))                     
        
        # Optional secondary tax label (e.g. :VAT, - GST)
        (?:\s*[:\-\#]?\s*(?:vat|gst|hst|sales\s*tax))?         
        
        # Optional percentage rate (e.g. (4.75%) or 4.75%)
        (?:\s*\(?\s*\d+(?:\.\d+)?\s*%\s*\)?)?                  
        
        [\s:\-\#]*                                              
        (    # CAPTURE GROUP: monetary value only                                       
            (?:[A-Z]{3}|[\$\u20AC\u00A3\u00A5\u20B9])?   
             # Optional leading currency      
            \s*
            (?:
                # Comma-separated digits
                \d{1,3}(?:,\d{3})+(?:\.\d{1,2})?               
                |
                # Plain numeric digits
                \d+(?:\.\d{1,2})?                              
            )
        )
        (?:\s*[A-Z]{3})?
        # Ensure full number match
        (?!\d|[\.,]\d)             
        # Ensure captured number is NOT a percentage                            
        (?!\s*\%)                                              
    """

    match = re.search(pattern, text, flags=re.VERBOSE | re.IGNORECASE)
    if not match:
        return None

    candidate_str = match.group(1).strip()

    return parse_money(candidate_str)
