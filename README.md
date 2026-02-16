# Binance Futures Order Bot

A CLI-based trading bot for Binance USDT-M Futures Testnet. Supports Market, Limit, Stop-Limit, and TWAP orders with robust logging and validation.

## Features
- **Core Orders**: Market and Limit (BUY/SELL).
- **Advanced Orders**: Stop-Limit (Trigger + Limit) and TWAP (Time-Weighted Average Price).
- **Validation**: Strict input validation for symbols, quantities, and prices.
- **Logging**: Detailed logs of every API request and response in `bot.log`.
- **Error Handling**: Graceful handling of API errors and network issues.

## Setup

1. **Clone the project**:
   ```bash
   git clone <repo-url>
   cd binance-futures-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Binance Testnet API Key and Secret:
   ```env
   BINANCE_API_KEY=your_actual_testnet_key
   BINANCE_API_SECRET=your_actual_testnet_secret
   BINANCE_BASE_URL=https://testnet.binancefuture.com
   ```

## Usage

### Using the Unified CLI
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Specific Scripts (As per requirements)
- **Market Order**: `python src/market_orders.py BTCUSDT BUY 0.001`
- **Limit Order**: `python src/limit_orders.py BTCUSDT SELL 0.001 45000`
- **Stop-Limit**: `python src/advanced/stop_limit.py BTCUSDT BUY 0.001 42000 42500`

### Advanced Strategies
- **TWAP Strategy**:
  ```bash
  python cli.py --symbol BTCUSDT --side BUY --type TWAP --quantity 0.01 --duration 10 --chunks 5
  ```
- **OCO Strategy**:
  ```bash
  python cli.py --symbol BTCUSDT --side BUY --type OCO --quantity 0.001 --price 46000 --stop_price 42500 --limit_price 42000
  ```

## Project Structure
- `src/`: Main entry points for mandatory and advanced orders.
- `bot/`: Core reusable logic (Client, Orders, Validators).
- `tests/`: Unit tests for validation logic.
- `cli.py`: Unified CLI for all features.
- `bot.log`: Execution logs.

## Testing & Validation
All actions are logged to `bot.log`. You can verify order execution statuses and IDs in this file or on the Binance Futures Testnet dashboard.
