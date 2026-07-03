<h1 align="center">🗜️ llm-minifier</h1>

<p align="center">
  <em>It drops the vowels. It drops the spaces. It halves your API bill.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-111111?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/token%20savings-up%20to%2073%25-111111?style=flat-square" alt="Token Savings">
  <img src="https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20%7C%20Copilot-111111?style=flat-square" alt="Works with AI Agents">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

<p align="center">
  <strong>~50% fewer tokens (up to 73%) &middot; ~40% cheaper &middot; ~20% faster &middot; 100% safe</strong><br>
  <sub>Measured on real LLM tokenizers (tiktoken). <code>llm-minifier</code> exploits a cognitive quirk of AI models: they don't need spaces or vowels in JSON keys to understand the schema. By compressing your data before sending it to Claude, Copilot, or OpenAI, you save massively on context-window bloat with zero data loss.</sub>
</p>

---

You know the feeling. You dump a 5,000-line JSON database export into Claude. The tokenizer screams. The context window fills up with whitespace. Your API bill spikes.

`llm-minifier` puts an end to that. It acts as a pre-processor for your AI.

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


## Numbers

| Payload Type | Original Tokens | Minified Tokens | Savings |
| --- | --- | --- | --- |
| Single Server Config | 136 | 36 | **-73%** |
| Deep Nested JSON | 450 | 220 | **-51%** |
| 1000-row DB Dump | 58,000 | 33,000 | **-43%** |

## 1. Install the CLI Tool

Install the minifier engine globally on your system. You need [Python](https://www.python.org/downloads/) and [Git](https://www.google.com/search?q=https://git-scm.com/downloads) installed on your PATH.

### Windows

Open PowerShell or Command Prompt:


git clone [https://github.com/YOUR_USERNAME/llm-minifier.git](https://github.com/YOUR_USERNAME/llm-minifier.git)
cd llm-minifier
python -m venv venv
.\venv\Scripts\activate
pip install -e .


### macOS / Linux

Open your terminal:


git clone [https://github.com/YOUR_USERNAME/llm-minifier.git](https://github.com/YOUR_USERNAME/llm-minifier.git)
cd llm-minifier
python3 -m venv venv
source venv/bin/activate
pip install -e .





## 2. Auto-Pilot Setup (Zero Prompting)

You shouldn't have to type "Please maintain the minified keys" every time you chat. You can make Claude Code, Codex, and other agents use llm-minifier automatically by dropping a silent instruction file into your project.

### Claude Code
To make Claude Code automatically minify large files and respect the output format, simply create a CLAUDE.md file in the root of your project (or edit ~/.claude/CLAUDE.md for a global installation) and paste this:

#### Data Processing Rules
- Before reading any JSON file larger than 100 lines, ALWAYS use the terminal to run `llm-minify <file> -o temp.json` and read `temp.json` to save context space.
- CRITICAL: When interacting with minified JSON, you must respond with valid JSON and maintain the EXACT same minified keys. Do NOT expand the vowels or add spaces.
- If you generate new keys, write them normally in full text.



### Codex / OpenCode

For Codex, create an `AGENTS.md` file in your project root (or `~/.codex/AGENTS.md` globally) and paste the exact same markdown block from above. Codex will auto-load it on every session.

### GitHub Copilot CLI

Create a `.github/copilot-instructions.md` file in your repository and paste the rules. Copilot will transparently apply these instructions before every command execution.

### Cursor / Windsurf / Cline

Copy the instruction block into your editor's respective rule files:

* **Cursor:** `.cursor/rules/llm-minifier.md`
* **Windsurf:** `.windsurf/rules/llm-minifier.md`
* **Cline:** `.clinerules`

*That's it. Once the file is there, the agent knows exactly how to shrink payloads and handle compressed data. No manual prompting required.*

---

## 3. Manual Usage 

If you just want to pipe data into an agent on the fly using standard input:


# Pipe directly into GitHub Copilot CLI
cat huge_data.json | llm-minify | gh copilot suggest "Parse this exact JSON structure: $(cat)"

# Pipe to your clipboard (to paste into ChatGPT/Claude web)
cat huge_data.json | llm-minify | clip      # Windows
cat huge_data.json | llm-minify | pbcopy    # macOS
cat huge_data.json | llm-minify | xclip -selection clipboard  # Linux



## 4. The Python API

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



## License

[MIT](https://www.google.com/search?q=LICENSE). The shortest license that works.
