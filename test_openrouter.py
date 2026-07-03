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
    original_data ={
        "user_profile_information": {
            'first_name':'Giovanni',
            'last_name':'Bianco',
            'favorite_programming_language': 'Python',
            'years_of_experience': 5
        }
    }
    print('\n-- PHASE 1: COMPRESSION')
    compressed_dict, mapping = compress_payload(original_data)
    compressed_string = json.dumps(compressed_dict, separators=(',',','))

    print(f'Payload to send: {compressed_string}')
    print(f'Map saved in RAM: {mapping}')

    #2) Calls to LLM
    print('n\-- Phase 2: LLM elaboration --')
    print('Contacted OpenRouter...')

    system_prompt = """
    You are a data processing API. You receive minified JSON.
    CRITICAL INSTRUCTIONS:
    1. Respond ONLY with valid JSON.
    2. Maintain the EXACT same minified keys you received. Do not expand them.
    3. If you add new keys, minify them by removing all vowels and underscores (keep the first letter).
    """

    user_prompt = f"Read this user and add a 'seniority_level' field evaluating years of experience: {compressed_string}"

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}    
        ],
        response_format={"type": "json_object"}
    )

    llm_response_string = response.choices[0].message.content
    print(f"Alien response received from AI: {llm_response_string}")

    #3) Decompression
    print(f"\n -- Phase 3: Decompression --")
    llm_response_dict= json.loads(llm_response_string)

    final_json = decompress_payload(llm_response_dict, mapping)
    print(json.dumps(final_json, indent=2))

    print('\n--- API statistics ---')
    print(f"Utilizzo del token per il prompt: {response.usage.prompt_tokens}")
    print(f"Token used for response: {response.usage.completion_tokens}")

if __name__=="__main__":
    main()