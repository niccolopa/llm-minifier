import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from llm_minifier import compress_payload, decompress_payload

#1) inizialization
load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def main():
    original_data = {
        "server_configuration": {
            "server_hostname": "apollo-database-01",
            "operating_system": "ubuntu-22.04",
            "allocated_ram_gb": 16,
            "cpu_core_count": 8
        }
    }
    print('\n-- PHASE 1: COMPRESSION')
    compressed_dict, mapping = compress_payload(original_data)
    compressed_string = json.dumps(compressed_dict, separators=(',',':'))

    print(f'Payload to send: {compressed_string}')
    print(f'Map saved in RAM: {mapping}')

    #2) Call to LLM
    print('n\-- Phase 2: LLM elaboration --')
    print('Contacted OpenRouter...')

    system_prompt = """
    You are a data processing API. You receive minified JSON.
    CRITICAL INSTRUCTIONS:
    1. Respond ONLY with valid JSON.
    2. Maintain the EXACT same minified keys you received. Do not expand them.
    3. If you add NEW keys, write them normally in full text (do not minify them).
    """

    user_prompt = f"Parse this server. Add a Boolean field 'is_high_performance' that is true if it has at least 8 cores and 16 GB of RAM: {compressed_string}"

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}    
        ],
    )

    llm_response_string = response.choices[0].message.content
    print(f"Alien response received from AI: {llm_response_string}")

    #3) Decompression
    print(f"\n -- Phase 3: Decompression --")
    try:
        json_start=llm_response_string.find('{')
        json_end= llm_response_string.rfind('}')+1

        if json_start != -1 and json_end != -1:
            clean_json_string= llm_response_string[json_start:json_end]
        else:
            clean_json_string = llm_response_string
        
        llm_response_dict = json.loads(clean_json_string)

        final_json = decompress_payload(llm_response_dict, mapping)
        print(json.dumps(final_json, indent=2))

        print('\n--- API statistics ---')
        if response.usage:
            print(f"Tokens used for the prompt:: {response.usage.prompt_tokens}")
            print(f"Token used for response: {response.usage.completion_tokens}")
        else:
            print(f"The OpenRouter provider did not return token data for this call.")

    except json.JSONDecodeError:
        print("ERROR: The AI blocked the request or did not generate valid JSON.")

if __name__=="__main__":
    main()