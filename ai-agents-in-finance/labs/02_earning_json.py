import json
from ai_agents_finance.config import load_config
from openai import OpenAI

client = OpenAI(api_key=load_config()["openai_api_key"])  # cheap + fast: fine for summarizing

# WHO the model is + WHAT SHAPE the answer must have
system_prompt = """
You are a finance analyst writing for portfolio managers.
Return strict JSON with exactly these keys and types:
  company: string
  quarter: string, like "FY2025 Q3"
  revenue_usd: number in US dollars, no symbols or words (98700000000, not "$98.7B")
  revenue_growth_yoy_pct: number (6 means +6%)
  eps_usd: number
  guidance: string
  highlights: list of strings
  risks: list of strings
  outlook: one of "positive", "neutral", "negative"
"""

transcript_infosys_earnings_call = """INFOSYS LIMITED
Q2 FY2026-27 EARNINGS CONFERENCE CALL
Quarter ended September 30, 2026

PARTICIPANTS:
Salil Parekh – Chief Executive Officer
Jayesh Sanghrajka – Chief Financial Officer

MODERATOR:
Good morning, ladies and gentlemen. Welcome to the Infosys Q2 FY27 earnings conference call. I will now hand over the call to Mr. Salil Parekh.

CEO – SALIL PAREKH:
Thank you. We delivered a steady performance during the second quarter, supported by large deal wins, continued client engagement and increasing demand for artificial intelligence services.

Our revenue for Q2 FY27 stood at INR 49,244 crore, representing year-on-year growth of 10.7%. In constant currency terms, revenue increased by 1.5% year-on-year and 1.2% sequentially.

We continue to see demand for digital transformation, cloud modernization and enterprise AI adoption. Financial services and manufacturing remained important contributors to our business.

CFO – JAYESH SANGHRAJKA:
Revenue for the quarter was INR 49,244 crore compared with INR 44,490 crore in the corresponding quarter last year.

Operating profit margin stood at 21.0%, compared with 21.1% in the previous quarter.

Free cash flow generation was INR 8,898 crore, representing 113.5% of net profit.

Basic earnings per share stood at INR 19.32, representing year-on-year growth of 8.7%.

During the quarter, we generated large deal total contract value of USD 5.2 billion, of which 62% represented net new business.

BUSINESS HIGHLIGHTS:
We signed multiple large transformation deals across financial services, manufacturing and technology.

Our artificial intelligence business continued to expand. AI-related services contributed approximately 10.5% of total revenue.

We are investing in generative AI platforms, automation capabilities and industry-specific AI solutions.

The company continues to focus on employee reskilling, operational efficiency and improving productivity through automation.

FY27 MANAGEMENT GUIDANCE:
Based on current business conditions, we expect FY27 revenue growth in the range of 1% to 2% in constant currency terms.

We expect operating margins to remain within the range of 20% to 22%.

Our guidance considers macroeconomic uncertainty, client spending patterns and foreign exchange movements.

ANALYST Q&A SESSION:
Analysts asked about revenue growth, discretionary technology spending, margin risks, AI revenue, large deal wins and capital returns. Management cited stable demand for cloud and AI transformation, selective discretionary spending, operational efficiencies, wage and subcontracting cost risks, a healthy USD 5.2 billion deal pipeline, and disciplined capital allocation.

KEY FINANCIAL METRICS:
Revenue: INR 49,244 crore
Revenue growth YoY: 10.7%
Constant currency growth YoY: 1.5%
Constant currency growth QoQ: 1.2%
Operating margin: 21.0%
Basic EPS: INR 19.32
Free cash flow: INR 8,898 crore
FCF conversion: 113.5%
Large deal TCV: USD 5.2 billion
Net new deal contribution: 62%

FY27 GUIDANCE:
Revenue growth: 1%-2%
Operating margin: 20%-22%

MANAGEMENT CONCLUSION:
We remain focused on profitable growth, strengthening our AI capabilities, expanding our large deal pipeline and delivering long-term value to shareholders."""

# The actual job + the data. The f"..." drops the transcript text into the {...} slot.
user_prompt = f"""Summarize the following earnings call transcript:
{transcript_infosys_earnings_call}"""

response = client.responses.create(
    model=load_config()["openai_model"],
    input=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    text={"format": {"type": "json_object"}},  # JSON mode: the reply must be valid JSON
)

raw_text = response.output[0].content[0].text  # dig the text out of the response box
summary = json.loads(raw_text)  # JSON text → Python dictionary
print("\n================ OPENAI SUMMARY ================")
print(json.dumps(summary, indent=2))  # dictionary →  pretty, indented text

from google import genai

gclient = genai.Client(
    api_key=load_config()["gemini_api_key"])  # separate name, so we don't overwrite 'client'
print("\n================ GEMINI SUMMARY ================")
config = load_config()
gemini_models = [config["gemini_model"], config["gemini_fallback_model"]]
for model_name in dict.fromkeys(gemini_models):
    try:
        resp_genai = gclient.models.generate_content(
            model=model_name,
            contents=system_prompt + "\n\n" + user_prompt,  # both prompts in one text
            config={"response_mime_type": "application/json"},  # Gemini JSON mode
        )
        print(f"Model: {model_name}")
        print(resp_genai.text)
        break
    except Exception as exc:
        print(f"{model_name} unavailable: {exc}")
else:
    print("Gemini summary unavailable: all configured models failed.")
