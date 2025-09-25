from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
import yfiance as yf 

def check_stock(company: str) -> dict: 
    try: 
        stock = yf.ticker(company)
        info = stock.info
        
        return { 
            "company": company,
            "price": info.get("currentPrice", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
        }
    except Exception as e: 
        return {"error": str(e)}

stockChecker = FunctionTool(
    name="stock_checker",
    description="Checks stock information for a given company.",
    function=check_stock
)

stock_agent = LlmAgent(
    name="stock_agent",
    model="gemini-2.5-flash",
    description="Checks stock information for a given company.",
    instruction=
    """
    Check the stock information for the company {company}.
    """,
    tools=[stockChecker],
    output_key="stock_info"
)

root_agent = stock_agent