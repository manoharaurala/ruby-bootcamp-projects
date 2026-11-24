import yfinance as yf
from agents import Agent, Runner, function_tool
from ai_agents_finance.config import load_config
from openai import OpenAI

client = OpenAI(
    api_key=load_config()["openai_api_key"]
)

print("\n================ FIRST ISSUE: MODEL WITHOUT A TOOL ================")
response = client.responses.create(model="gpt-4.1", input="What is the last price of Titan India?")
print(response.output_text)


@function_tool  # turns this function into a tool the LLM can call
def get_latest_stock_price(symbol: str) -> dict:
    """Fetch the current stock price for the given symbol."""  # the LLM reads this to decide when to use it
    ticker = yf.Ticker(symbol)  # a handle for one stock, e.g. "NVDA"
    hist = ticker.history(period="1d")  # a table of the last trading day
    latest_close = hist["Close"].iloc[-1]  # column "Close", last row  → latest price
    latest_date = hist.index[-1]  # label of that last row    → its date
    return {"price": float(latest_close), "date": str(latest_date.date())}

stock_price_agent = Agent(
    name="Stock Price Agent",                                          # a label, shows up in logs
    instructions="Fetch Historical prices for a given stock symbol",   # its job description
    model="gpt-4.1",                                                   # the brain
    tools=[get_latest_stock_price],                                    # what it may call
)

print("\n================ SOLUTION: AGENT WITH A LIVE PRICE TOOL ================")
output = Runner.run_sync(                                              # run_sync: no 'await' needed
    starting_agent=stock_price_agent,
    input="What is today's date, and what is the current stock price of Titan India?",
)
print(output.final_output)
