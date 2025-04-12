"""
Pattern Encoder - Generate encoded combinations from template patterns
Created by Cyto0x | GitHub: github.com/cyto0x
"""

import argparse
import re
import sys
import itertools
import hashlib
import base64
from urllib.parse import quote

class DynamicEncoder:
    def __init__(self, pattern):
        self.pattern = pattern
        self.operations = {
            # Hash functions
            'md5': lambda s: hashlib.md5(s.encode()).hexdigest(),
            'sha1': lambda s: hashlib.sha1(s.encode()).hexdigest(),
            'sha256': lambda s: hashlib.sha256(s.encode()).hexdigest(),
            'sha512': lambda s: hashlib.sha512(s.encode()).hexdigest(),
            
            # Encoding functions
            'base16': lambda s: base64.b16encode(s.encode()).decode(),
            'base32': lambda s: base64.b32encode(s.encode()).decode(),
            'base64': lambda s: base64.b64encode(s.encode()).decode(),
            'urlencode': lambda s: quote(s),
            
            # Text transformations
            'upper': lambda s: s.upper(),
            'lower': lambda s: s.lower(),
        }

    def process(self, values):
        def replace_nested(match):
            func = match.group(1)
            content = match.group(2)
            return self.operations[func](process_content(content))
        
        def process_content(content):
            for ph, val in values.items():
                content = content.replace(f'{{{ph}}}', val)
            return content
        
        current = self.pattern
        while True:
            prev = current
            # Updated regex to handle function names without underscores
            current = re.sub(r'([a-zA-Z0-9]+)\(([^()]*)\)', replace_nested, current)
            if current == prev:
                break
                
        for ph, val in values.items():
            current = current.replace(f'{{{ph}}}', val)
            
        return current

def main():
    examples = """
Examples (Underscores Fixed):

1. With static underscore before hash:
  python PatternEncoder.py '{ORG}_{USER}_sha256({KEY})' ORG orgs.txt USER users.txt KEY keys.txt output.txt

2. Underscore between multiple functions:
  python PatternEncoder.py 'md5({ID})_sha256({SECRET})' ID ids.txt SECRET secrets.txt hashes.txt

3. Complex pattern with mixed text:
  python PatternEncoder.py 'API_{ORG}_{USER}_base64({TOKEN})' ORG orgs.txt USER users.txt TOKEN tokens.txt api_keys.txt

Supported functions: md5, sha1, sha256, sha512, base16, base32, base64, urlencode, upper, lower
"""

    parser = argparse.ArgumentParser(
        description="Generate encoded wordlists from template patterns",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=examples,
        usage="python %(prog)s [PATTERN] [PLACEHOLDER FILE]... OUTPUT_FILE",
        add_help=False
    )
    
    if len(sys.argv) == 1 or '--help' in sys.argv or '-h' in sys.argv:
        print("Pattern Encoder - Generate encoded combinations from template patterns\n")
        print("Usage: python PatternEncoder.py [PATTERN] [PLACEHOLDER FILE]... OUTPUT_FILE")
        print("\nArguments:")
        print("  PATTERN           Template pattern with placeholders and functions")
        print("  PLACEHOLDER FILE  Alternating placeholder names (UPPERCASE) and wordlist files")
        print("  OUTPUT_FILE       File to save generated combinations")
        print(examples)
        print("Note: Function names must NOT contain underscores")
        sys.exit(0)

    # Manual argument parsing
    args = sys.argv[1:]
    pattern = args[0]
    output_file = args[-1]
    placeholders = args[1:-1]

    if len(placeholders) % 2 != 0:
        print("\nError: Invalid number of arguments. Expected even number of placeholder-file pairs")
        print("Correct format: python PatternEncoder.py [PATTERN] [PLACEHOLDER FILE]... OUTPUT_FILE")
        sys.exit(1)

    # Read wordlists
    wordlists = {}
    for i in range(0, len(placeholders), 2):
        name = placeholders[i].upper()
        filename = placeholders[i+1]
        try:
            with open(filename) as f:
                wordlists[name] = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"\nError: File not found for {name} - {filename}")
            sys.exit(1)

    # Validate placeholders
    pattern_placeholders = set(re.findall(r'\{(\w+)\}', pattern))
    defined_placeholders = set(wordlists.keys())
    
    if missing := pattern_placeholders - defined_placeholders:
        print(f"\nError: Missing placeholder files for: {', '.join(missing)}")
        sys.exit(1)

    # Generate entries
    encoder = DynamicEncoder(pattern)
    total = 0
    
    try:
        with open(output_file, 'w') as out:
            for combination in itertools.product(*wordlists.values()):
                values = dict(zip(wordlists.keys(), combination))
                entry = encoder.process(values)
                out.write(f"{entry}\n")
                total += 1
                
        print(f"\nGenerated {total} entries in {output_file}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
