# 🚀 ProfitPilot - AI-Powered Equity Research Platform

**ProfitPilot** is a full-stack financial intelligence dashboard that provides real-time **Sentiment Analysis** and **Fundamental Data** for Indian Stocks (NSE). 

It solves the problem of "Information Overload" for investors by aggregating news from multiple sources and using AI to determine if the market sentiment is **Bullish** or **Bearish**.

![ProfitPilot Demo](https://via.placeholder.com/800x400.png?text=Add+Your+Screenshot+Here)
*(Add a screenshot of your dashboard here)*

## ⚡ Key Features
- **Hybrid AI Engine:** Uses `TextBlob` for NLP sentiment scoring, with a fallback dual-engine architecture (Yahoo Finance + Google News) to ensure 100% data availability.
- **Smart Ticker Resolution:** Automatically resolves fuzzy user queries (e.g., "Tata Motors" → `TATAMOTORS.NS`) using a custom lookup algorithm.
- **Real-Time Fundamentals:** Fetches live Price, P/E Ratio, and Market Cap (formatted in Crores).
- **Daily Market Feed:** A sidebar aggregating broader market news using the Google News API.

## 🛠️ Tech Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | Next.js 14, Tailwind CSS, Framer Motion | Modern, responsive UI with glassmorphism effects. |
| **Backend** | Node.js, Express.js | API Gateway and request orchestration. |
| **AI Service** | Python, FastAPI, yfinance, TextBlob | The "Brain" handling data scraping and NLP. |
| **Architecture** | Microservices | Decoupled services for scalability. |

## 🚀 How to Run Locally

### 1. Clone the Repo
```bash
git clone [https://github.com/your-username/profit-pilot-ai.git](https://github.com/your-username/profit-pilot-ai.git)
cd profit-pilot-ai
