---
title: Customer Support Chatbot
emoji: 🛍️
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.52.2
app_file: app.py
pinned: false
---

# Customer Support Chatbot

An AI-powered customer support chatbot for a computer products company, built with:
- **GPT-4o-mini** for natural language understanding
- **MCP (Model Context Protocol)** for accessing company data
- **Streamlit** for the user interface

## Features

- 🔍 **Product Search** - Search and browse monitors, printers, and computers
- 📦 **Order Management** - Check order status and create new orders
- 👤 **Customer Lookup** - Verify customer information
- 💬 **Natural Conversation** - Chat naturally about products and orders

## How It Works

The chatbot connects to an MCP server that provides 8 tools for customer support:

**Product Tools:**
- `list_products` - Browse products by category
- `get_product` - Get detailed product info by SKU
- `search_products` - Search products by keyword

**Customer Tools:**
- `get_customer` - Look up customer details
- `verify_customer_pin` - Verify customer identity

**Order Tools:**
- `list_orders` - View order history
- `get_order` - Get order details
- `create_order` - Place new orders

## Try It Out

Ask questions like:
- "Show me all monitors"
- "Search for printers under $300"
- "What's the status of order [order-id]?"
- "Tell me about product SKU MON-0051"

## Environment Variables

To run this app, you need to set:

```
MCP_SERVER_URL=https://vipfapwm3x.us-east-1.awsapprunner.com/mcp
OPENAI_API_KEY=your_openai_api_key_here
```

In HuggingFace Spaces: Settings → Variables and secrets → Add secret

## Technical Details

- **LLM**: GPT-4o-mini with function calling
- **Transport**: HTTP JSON-RPC for MCP communication
- **Framework**: Streamlit (Python)

Built for the Andela Bootcamp MCP Assessment.
