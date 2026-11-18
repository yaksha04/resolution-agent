import streamlit as st
from agent import run_resolution_agent

st.set_page_config(page_title="Resolution Agent", layout="centered")

st.title("Decision-Making Resolution Agent")
st.write("Autonomous agent that checks orders, inventory, and issues exchanges or refunds.")

st.markdown("""
**Try these sample orders:**
- `ORD-1001` → Headphones (in stock → Exchange)
- `ORD-1002` → Smart Watch (out of stock → Refund)
- `ORD-1003` → Speaker (not eligible → Refund)
- `ORD-9999` → Invalid order (error handling)
""")

user_input = st.text_area(
    "Customer request (include the order ID)",
    value="My Wireless Headphones from order ORD-1001 arrived damaged. Can I get a replacement?",
    height=100,
)

order_id = st.text_input("Order ID (optional, extracted from request if blank)", value="ORD-1001")

if st.button("Resolve Issue", type="primary"):
    if not user_input.strip():
        st.warning("Please enter a customer request.")
    else:
        with st.spinner("Agent is investigating..."):
            result = run_resolution_agent(user_input, order_id=order_id.strip() or None)

        if result["success"]:
            st.success("Resolution complete")
            st.markdown(f"**Summary:**\n\n{result['summary']}")
            st.info(f"Resolution type: **{result.get('resolution', 'unknown').upper()}**")
        else:
            st.error(result["summary"])

        # Show tool trace
        if result.get("trace"):
            with st.expander("View tool call trace"):
                for i, step in enumerate(result["trace"], 1):
                    st.markdown(f"**Step {i}: {step['tool']}**")
                    st.json(step)

st.markdown("---")
st.caption("Mock database · Local only · No external APIs or subscriptions")
