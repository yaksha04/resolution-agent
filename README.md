# Decision-Making Resolution Agent

An autonomous agent that resolves customer order issues by reading order records, checking inventory, and either initiating an exchange or issuing a refund. Built with a simple Streamlit frontend and a fully local mock database.

---

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Component Breakdown](#component-breakdown)
4. [Agent Workflow (Flowchart)](#agent-workflow-flowchart)
5. [Tool Definitions](#tool-definitions)
6. [Decision Logic](#decision-logic)
7. [Guardrails & Error Handling](#guardrails--error-handling)
8. [Project Structure](#project-structure)
9. [How to Run](#how-to-run)
10. [Sample Test Cases](#sample-test-cases)

---

## Overview

This project implements an **agentic tool-using system** that acts as an automated resolution specialist.  
When a customer reports a problem with an order, the agent:

1. Looks up the order in the database  
2. Checks real-time inventory for a replacement  
3. Decides whether to process an **exchange** or a **refund**  
4. Sends a confirmation notification  
5. Returns a clear summary to the user  

Everything runs locally with a mock database — no external APIs or paid services are required.

---

## System Architecture
┌─────────────────────┐
│ Streamlit UI │ ← User enters request + Order ID
│ (app.py) │
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│ Resolution Agent │ ← Controls the decision loop
│ (agent.py) │
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│ Safe Dispatcher │ ← Whitelist + argument validation
│ (dispatcher.py) │
└──────────┬──────────┘
│
┌─────┴─────┬─────────────┬──────────────┐
▼ ▼ ▼ ▼
┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│ lookup_ │ │ check_ │ │ process_ │ │ send_ │
│ order │ │ inventory│ │ refund │ │ notification │
└────┬────┘ └────┬─────┘ └────┬─────┘ └──────┬───────┘
│ │ │ │
└───────────┴────────────┴───────────────┘
│
▼
┌─────────────────┐
│ Mock Database │
│ (mock_db.py) │
└─────────────────┘



## Component Breakdown

| File              | Responsibility |
|-------------------|----------------|
| `app.py`          | Streamlit frontend. Collects user input and displays the agent's result + tool trace. |
| `agent.py`        | Core agent logic. Runs the resolution workflow, calls tools in the correct order, and handles both exchange and refund paths. |
| `dispatcher.py`   | Safe tool registry. Only allows whitelisted tools to execute and catches invalid arguments. |
| `tools.py`        | Actual tool implementations (`lookup_order`, `check_inventory`, `process_refund`, `send_notification`). |
| `schemas.py`      | Declarative tool contracts (name, description, parameters) that an LLM would see. |
| `mock_db.py`      | In-memory database containing sample orders and inventory stock levels. |
| `requirements.txt`| Python dependencies (Streamlit). |
| `README.md`       | This file. |


## Agent Workflow (Flowchart)
Start
│
▼
User provides Order ID + issue description
│
▼
┌─────────────────────────┐
│ 1. lookup_order(order_id) │
└──────────┬──────────────┘
│
Order found?
/
No Yes
│ │
▼ ▼
Return error Eligible for exchange?
message /
No Yes
│ │
▼ ▼
Process refund ┌──────────────────────┐
│ 2. check_inventory() │
└──────────┬───────────┘
│
Stock > 0?
/
Yes No
│ │
▼ ▼
Confirm exchange Process refund
│ │
└─────┬─────┘
▼
┌──────────────────────┐
│ 3. send_notification │
└──────────┬───────────┘
▼
Return final summary
│
▼
End

Text

---

## Tool Definitions

### 1. `lookup_order`
- **Purpose**: Retrieve order details  
- **Input**: `order_id`  
- **Returns**: Customer name, email, item, eligibility, amount, or error if not found

### 2. `check_inventory`
- **Purpose**: Check if a replacement unit is in stock  
- **Input**: `item_id`  
- **Returns**: Current stock count and availability status

### 3. `process_refund`
- **Purpose**: Issue a refund when exchange is not possible  
- **Input**: `order_id`, `reason`  
- **Returns**: Refund reference ID and amount

### 4. `send_notification`
- **Purpose**: Send confirmation email to the customer  
- **Input**: `email`, `message`  
- **Returns**: Delivery status

---

## Decision Logic

| Condition                          | Action Taken     |
|------------------------------------|------------------|
| Order not found                    | Return error     |
| Eligible + Stock > 0               | Exchange         |
| Eligible + Stock = 0               | Refund           |
| Not eligible for exchange          | Refund           |

---

## Guardrails & Error Handling

- **Whitelist registry**: Only predefined tools can be executed  
- **Argument validation**: Invalid inputs return structured errors instead of crashing  
- **Graceful failure**: Missing orders or invalid data produce clear messages  
- **Bounded execution**: The agent follows a fixed, safe sequence (no unbounded loops)  
- **Structured outputs**: Every tool returns `success`, `error`, and `data` fields

---

## Project Structure
resolution-agent/
├── app.py
├── agent.py
├── dispatcher.py
├── tools.py
├── schemas.py
├── mock_db.py
├── requirements.txt
└── README.md



## How to Run

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the app
streamlit run app.py
Open [localhost](http://localhost:8501/) in your browser.

Sample Test Cases
Order ID	Item	Stock	Eligible	Expected Result
ORD-1001	Wireless Headphones	5	Yes	Exchange
ORD-1002	Smart Watch	0	Yes	Refund
ORD-1003	Bluetooth Speaker	12	No	Refund
ORD-9999	—	—	—	Error (not found)
Notes
This implementation uses a deterministic decision flow so it can run completely offline.
The architecture (schemas + safe dispatcher + tool loop) is designed so a real LLM can be plugged in later if desired.
All data is mock data for demonstration and assignment purposes.
