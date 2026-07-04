[![GitHub license](https://img.shields.io/github/license/CoderShivamGusain/binance-trading-bot)](https://github.com/CoderShivamGusain/binance-trading-bot/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/CoderShivamGusain/binance-trading-bot)](https://github.com/CoderShivamGusain/binance-trading-bot/stargazers)

# Binance Futures Testnet Trading Bot

A lightweight, modular Python CLI tool that places **Market** and **Limit** orders on the Binance Futures USDT‑M testnet. The project emphasizes clean architecture, defensive validation, and institutional‑grade logging.

---

## Project Architecture

```
trading_bot/
│   cli.py               # Click‑based entry point
│   requirements.txt     # Production dependencies
│   README.md            # Documentation (this file)
│
└───bot/
    │   __init__.py      # Package init – imports logger
    │   logging_config.py# Dual‑destination logger (file + console)
    │   client.py        # Loads .env and configures Binance testnet client
    │   validators.py    # Strict input validation with ValidationError
    │   orders.py        # Order payload building and API call with error handling
```

* **CLI Wrapper (`cli.py`)** – Handles user interaction via Click, displays clear messages, and orchestrates the workflow.
* **Validation Engine (`validators.py`)** – Guarantees only well‑formed, sanitized data reaches the network layer.
* **Network Client (`client.py`)** – Loads credentials securely from a `.env` file and creates a testnet‑ready Binance client.
* **Dual‑Destination Logger (`logging_config.py`)** – Streams detailed logs to `bot.log` **and** to the console, with timestamps, log levels, and module names.

---

## Prerequisites & Setup

1. **Clone / open the project** and navigate to its root directory.
2. **Create a virtual environment** (highly recommended):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # Windows PowerShell
   # Or: source .venv/bin/activate on Unix
   ```
3. **Install production dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Create a `.env` file** (do **not** commit this file):
   ```text
   BINANCE_API_KEY=your_testnet_api_key
   BINANCE_SECRET_KEY=your_testnet_secret_key
   ```
   *Obtain the keys from your Binance Futures Testnet account.*
5. Verify the logger works by running a quick sanity check:
   ```bash
   python -m bot.client   # Should print your USDT balance and create bot.log
   ```

---

## How to Run Examples

The CLI command is `trade`. Below are ready‑to‑copy examples.

### Market Order (BUY 0.001 BTCUSDT)
```bash
python cli.py \
    --symbol BTCUSDT \
    --side BUY \
    --type MARKET \
    --quantity 0.001
```

### Limit Order (SELL 0.001 BTCUSDT at $30,000)
```bash
python cli.py \
    --symbol BTCUSDT \
    --side SELL \
    --type LIMIT \
    --quantity 0.001 \
    --price 30000
```

Both commands will:
1. Initialise the Binance testnet client.
2. Validate the supplied arguments.
3. Place the order.
4. Print a concise summary and log the full request/response to `bot.log`.

---

## Assumptions & Safety Design

- **Testnet Only** – The client is hard‑coded to use `https://testnet.binancefuture.com`. No real funds are affected.
- **USDT‑M Futures** – The bot targets the USDT‑margin futures market.
- **Limit Orders** use `timeInForce='GTC'` (Good‑Till‑Cancelled).
- **Credential Isolation** – API keys are loaded from a non‑tracked `.env` file; they never appear in source control.
- **Logging** – All request payloads and Binance responses are written to `bot.log` (rotated manually if needed) and also displayed on the console for transparency.
- **Graceful Failure** – Validation errors, Binance API errors, and network problems are caught and presented without a Python traceback, ensuring a clean user experience.

---

## Verification Guide (Populate `bot.log`)

1. **Run a Market Order** (replace the quantity with a tiny test amount you prefer):
   ```bash
   python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
   ```
   - Verify that the console shows a success message and that `bot.log` now contains an INFO entry for the outbound payload and the Binance response.
2. **Run a Limit Order** (choose any price you like for the testnet):
   ```bash
   python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 30000
   ```
   - Again, check the console output and confirm a new entry in `bot.log` documenting the limit order request and response.

After completing these two commands, you will have fulfilled the assignment requirement of providing log files for at least one MARKET and one LIMIT order.

---

*Happy trading on the testnet!*
