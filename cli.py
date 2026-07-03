import argparse
import json
import sys
from llm_minifier import compress_payload

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="LLM Semantic Minifier: Compress JSON to save API tokens.")
    
    # Accept input from a file or directly from standard input (piping)
    parser.add_argument(
        "input_file", 
        nargs="?", 
        type=argparse.FileType("r"), 
        default=sys.stdin, 
        help="Path to the input JSON file (leave empty to use piped data)"
    )
    
    # Output to a file or standard output (terminal)
    parser.add_argument(
        "-o", "--output", 
        type=argparse.FileType("w"), 
        default=sys.stdout, 
        help="Path to the output JSON file (default is terminal stdout)"
    )

    args = parser.parse_args()

    # Prevent the script from freezing if the user runs it without arguments or piped data
    if args.input_file.name == "<stdin>" and sys.stdin.isatty():
        parser.print_help()
        sys.exit(1)

    try:
        # 1. Read the JSON data
        data = json.load(args.input_file)
        
        # 2. Compress the payload
        compressed_dict, mapping = compress_payload(data)
        
        # 3. Output the minified JSON with zero spaces
        json.dump(compressed_dict, args.output, separators=(',', ':'))
        
        # Add a clean newline if outputting directly to the terminal
        if args.output.name == "<stdout>":
            args.output.write("\n")
            
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON input. Ensure your data is properly formatted.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()