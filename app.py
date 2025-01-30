import openai
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Streamlit UI
st.set_page_config(page_title="Pelindo AI Search Engine", layout="wide")
st.title("🔍 AI Search Engine with Thought Process + Answer")

# User input
query = st.text_input("Ask me anything:", "")

if query:
    with st.spinner("🤔 Thinking..."):
        # Step 1: Generate thought process
        thought_prompt = f"Analyze the following question and describe how an AI should approach answering it: {query}"
        thought_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are an AI that provides structured thought before answering. Please provide your thought in paragraphs dan elaborasi jawaban dalam bahasa indonesia. Jangan lupa untuk memberikan font italic dan ukuran font harus lebih kecil dibandingkan hasil output dari Answer!"},
                      {"role": "user", "content": thought_prompt}],
            temperature=1.0,
            max_tokens=2048
        )
        thought_text = thought_response["choices"][0]["message"]["content"]
        st.markdown(f"**🤖 Thought Process:**\n\n{thought_text}")

    with st.spinner("💡 Generating answer..."):
        # Step 2: Generate the final response with streaming
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are an AI assistant that provides detailed, thoughtful answers. Elaborasi jawaban dengan detail! Dan berikan jawaban dalam bentuk paragraph dan sebisa mungkin beri case study yang kamu ketahui. Apabila ditanya dan diperlukan tabel dan atau grafik, mohon berikan."},
                      {"role": "user", "content": query}],
            temperature=1.0,
            max_tokens=2048,
            stream=True  # Enable streaming
        )

        # Stream output dynamically
        response_container = st.empty()
        full_response = ""

        for chunk in response:
            if "choices" in chunk and chunk["choices"]:
                delta = chunk["choices"][0].get("delta", {}).get("content", "")
                full_response += delta
                response_container.write(full_response)

    # Display final answer
    st.markdown(f"### **📝 Final Answer:**\n\n{full_response}")

    # Optional: Add feedback section
    st.markdown("Did this answer your question? [👍 Yes] [👎 No]")

