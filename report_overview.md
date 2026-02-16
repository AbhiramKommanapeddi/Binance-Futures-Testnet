# Binance Futures Order Bot - Report

## Implementation Overview
The bot is designed to interact with the Binance USDT-M Futures Testnet. It uses a custom `BinanceClient` for authenticated REST API calls and an `OrderManager` to abstract different order types.

### Key Components
1. **Client Layer**: Handles HMAC SHA256 signing and HTTP requests using `requests`.
2. **CLI Layer**: Built with `argparse` for a clean terminal interface.
3. **Advanced Strategies**:
   - **TWAP**: Splits orders into smaller chunks over a defined period to minimize market impact.
   - **Stop-Limit**: Uses trigger prices to execute limit orders automatically.

### Validation & Logging
- All inputs are sanitized and validated before API calls.
- Every API interaction (URL, Parameters, Response) is logged with timestamps in `bot.log`.

## Verification Screenshots (Placeholders)
*Note: Due to the nature of this task, actual screenshots would be added here after manual execution with live keys.*

1. **Market Order Placement**
   - Expected Output: Success message with OrderID and ExecutedQty.
2. **Limit Order Placement**
   - Expected Output: Success message showing status 'NEW'.
3. **Log File Snippets**
   - Shows structured JSON responses for traceability.
