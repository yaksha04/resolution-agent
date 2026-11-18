# Decision-Making Resolution Agent

Autonomous agent that:
1. Looks up orders (mock DB)
2. Checks inventory
3. Decides exchange vs refund
4. Sends confirmation
5. Handles errors gracefully

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Sample Orders

| Order ID   | Item                  | Stock | Eligible | Expected Outcome |
|------------|-----------------------|-------|----------|------------------|
| ORD-1001   | Wireless Headphones   | 5     | Yes      | Exchange         |
| ORD-1002   | Smart Watch           | 0     | Yes      | Refund           |
| ORD-1003   | Bluetooth Speaker     | 12    | No       | Refund           |
| ORD-9999   | —                     | —     | —        | Error (not found)|

No cloud services or paid APIs are required.
