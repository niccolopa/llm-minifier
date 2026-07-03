<h1 align="center">🗜️ llm-minifier</h1>

<p align="center">
  <em>It drops the vowels. It drops the spaces. It halves your API bill.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-111111?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/token%20savings-up%20to%2073%25-111111?style=flat-square" alt="Token Savings">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

<p align="center">
  <strong>~50% fewer tokens (up to 73%) &middot; ~40% cheaper &middot; ~20% faster &middot; 100% safe</strong><br>
  <sub>Measured on real LLM tokenizers (tiktoken). <code>llm-minifier</code> exploits a cognitive quirk of AI models: they don't need spaces or vowels in JSON keys to understand the schema. By compressing your data before sending it to Claude, Copilot, or OpenAI, you save massively on context-window bloat with zero data loss.</sub>
</p>

---

You know the feeling. You dump a 5,000-line JSON database export into Claude. The tokenizer screams. The context window fills up with whitespace. Your API bill spikes.

`llm-minifier` fixes that.

## Before / after

You want the AI to analyze a server configuration.

**Without minifier (136 tokens):**
{
  "server_configuration": {
    "server_hostname": "apollo-database-01"
  }
}


**With minifier (36 tokens):**


{"srvrcnfgrtn":{"srvrhstnm":"apollo-database-01"}}



More survivors in the [Benchmarks](https://www.google.com/search?q=%23numbers).

## Install

You need `python` and `git` on your PATH.

**Windows:**


git clone [https://github.com/YOUR_USERNAME/llm-minifier.git](https://github.com/YOUR_USERNAME/llm-minifier.git)
cd llm-minifier
python -m venv venv
.\venv\Scripts\activate
pip install -e .



**macOS / Linux:**


git clone [https://github.com/YOUR_USERNAME/llm-minifier.git](https://github.com/YOUR_USERNAME/llm-minifier.git)
cd llm-minifier
python3 -m venv venv
source venv/bin/activate
pip install -e .


## Using it with AI Agents

The tool acts as a pre-processor for your favorite CLI agents.

### Claude Code

Claude Code drains API credits fast with large files. Shrink them first:


# 1. Compress the data into a new file
llm-minify huge_db.json -o tiny_db.json

# 2. Feed the tiny file to Claude
claude "Analyze tiny_db.json. CRITICAL: The data is minified. Maintain the exact same minified keys in your response."


### Codex / GitHub Copilot CLI

Pipe the compressed JSON directly into the agent's prompt using standard input:


cat data.json | llm-minify | gh copilot suggest "Parse this exact JSON structure: $(cat)"



### The Universal Clipboard

Using ChatGPT or Claude in the browser? Minify straight to your clipboard and `Ctrl+V`.

* **Windows:** `cat data.json | llm-minify | clip`
* **macOS:** `cat data.json | llm-minify | pbcopy`
* **Linux:** `cat data.json | llm-minify | xclip -selection clipboard`

## The Python API

Integrate it directly into your backend architecture.


from llm_minifier import compress_payload, decompress_payload
import json

data = {"user_profile": {"first_name": "John"}}

# 1. Compress before sending to the AI
compressed_dict, mapping = compress_payload(data)

# ... Send to AI, get response back ...
llm_response = {"usrprfl": {"frstnm": "John", "is_admin": True}}

# 2. Decompress back to readable English using the map
restored_dict = decompress_payload(llm_response, mapping)



## Numbers

| Payload Type | Original Tokens | Minified Tokens | Savings |
| --- | --- | --- | --- |
| Single Server Config | 136 | 36 | **-73%** |
| Deep Nested JSON | 450 | 220 | **-51%** |
| 1000-row DB Dump | 58,000 | 33,000 | **-43%** |

## License

[MIT](https://www.google.com/search?q=LICENSE). The shortest license that works.



