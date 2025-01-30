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
st.title("🔍 Pelindo AI Search Engine with Thought Process + Answer")

# User input
query = st.text_input("Ask me anything:", "")

if query:
    with st.spinner("🤔 Thinking..."):
        # Step 1: Generate thought process
        thought_prompt = f"Analyze the following question and describe how an AI should approach answering it: {query}"
        thought_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Anda adalah AI yang memberikan pemikiran terstruktur dan framework of thinking sebagai acuan dalam menjawab pertanyaan. Silakan gunakan Bahasa yang casual dan berikan juga urutan berpikir sesuai kaidah critical thinking yang digunakan dalam menjawab pertanyaan yang diajukan! Sajikan dalam beberapa paragraph dan jangan dalam bentuk poin-poin. Tidak perlu langsung menjawab pertanyaan tapi berikan sistematika berpikirnya!"},
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
            messages=[{"role": "system", "content": "Kamu adalah AI Assistant yang dapat memberi jawaban detail dan mampu mengelaborasi jawaban dengan detail! Dan berikan jawaban dalam bentuk paragraph dan sebisa mungkin beri case study yang kamu ketahui. Apabila ditanya dan diperlukan tabel, mohon berikan. Mohon juga bentuk kata dan narasi jangan sama dengan yang process thought (Step 1), kalau bisa dielaborasi lagi dari yang Step 1!"},
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
    st.markdown(f"### **📝 Kesimpulan:**\n\n{full_response}")

    # Optional: Add feedback section
    st.markdown("Apakah menjawab pertanyaan Anda? [👍 Yes] [👎 No]")

