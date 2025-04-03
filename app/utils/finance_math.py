
def calculate_common_dividend_yield(last_dividend: float, price: float) -> float:
    return last_dividend / price

def calculate_preferred_dividend_yield(fixed_dividend: float, par_value: float, price: float) -> float:
    return (fixed_dividend * par_value) / price

def calculate_pe_ratio(price: float, dividend: float) -> float:
    return price / dividend if dividend > 0 else float('inf')
