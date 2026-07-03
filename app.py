import streamlit as st
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from llm_minifier import compress_payload, decompress_payload

# initialization
load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# page setup
st.set_page_config(page_title="LLM JSON Minifier", page_icon="🗜️", layout="wide")

st.title("🗜️ LLM Semantic Minifier")
st.markdown("Cut API Token costs in half by compressing JSON before sending it to the LLM.")

# Two-column layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Input (JSON Originale)")
    default_json = """{
  "server_configuration": {
    "server_hostname": "apollo-database-01",
    "operating_system": "ubuntu-22.04",
    "allocated_ram_gb": 16,
    "cpu_core_count": 8
  }
}"""
    user_json_input = st.text_area("Paste your verbose JSON here:", value=default_json, height=250)
    user_prompt = st.text_input("What do you want to ask the AI?", value="Add the field 'is_high_performance' (true se RAM >= 16 e CPU >= 8)")

with col2:
    st.subheader("2. Compressed Data (Payload)")
    try:
        original_data = json.loads(user_json_input)
        compressed_dict, mapping = compress_payload(original_data)
        compressed_string = json.dumps(compressed_dict, separators=(',', ':'))
        
# Savings calculation (using characters as a proportional estimate of tokens)        original_len = len(json.dumps(original_data))
        original_len = len(json.dumps(original_data))
        compressed_len = len(compressed_string)
        savings = 100 - ((compressed_len / original_len) * 100)
        
        st.code(compressed_string, language="json")
        st.metric(label="Estimated Savings (Space/Tokens)", value=f"{savings:.1f}%", delta="Lower API costs")
        
    except json.JSONDecodeError:
        st.error("Please enter valid JSON!")

st.divider()

# Run button
if st.button("Send to LLMs (Use OpenRouter Llama 3)", use_container_width=True):
    with st.spinner("Compressing, sending to AI, and decompressing..."):
        try:
            # System Prompt
            system_prompt = """
            You are a data processing API. You receive minified JSON.
            CRITICAL INSTRUCTIONS:
            1. Respond ONLY with valid JSON.
            2. Maintain the EXACT same minified keys you received. Do not expand them.
            3. If you add NEW keys, write them normally in full text.
            """
            
            full_prompt = f"{user_prompt}\nData: {compressed_string}"
            
            # Chiamata API
            response = client.chat.completions.create(
                model="meta-llama/llama-3.1-8b-instruct",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt}
                ]
            )
            
            llm_response_string = response.choices[0].message.content
            
            # Secure JSON extraction
            json_start = llm_response_string.find('{')
            json_end = llm_response_string.rfind('}') + 1
            clean_json_string = llm_response_string[json_start:json_end] if json_start != -1 else llm_response_string
            
            # Decompression
            llm_response_dict = json.loads(clean_json_string)
            final_json = decompress_payload(llm_response_dict, mapping)
            
            st.subheader("3. Final result")
            st.json(final_json)
            
            if response.usage:
                st.success(f"Token Prompt: {response.usage.prompt_tokens} | Answer token: {response.usage.completion_tokens}")
            
        except Exception as e:
            st.error(f"Something went wrong with the AI: {e}")