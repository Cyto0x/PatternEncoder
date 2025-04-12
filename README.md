# Pattern Encoder Tool

**Generate encoded wordlists from template patterns**

Create custom combinations of hashed/encoded values for security testing and data generation.

---
## What It Does

Create custom patterns like this:
- `base64(username:md5(password))`
- `sha256(salt+password)`
- Any combination you need

## Quick Start

```bash
git clone https://github.com/Cyto0x/PatternEncoder
cd Pattern-Encoder
```

```bash
python PatternEncoder.py [PATTERN] [PLACEHOLDER FILES]... OUTPUT_FILE
```


### Examples

**Cookie Generator**  
Create `base64(username:md5(password))` cookies:

```sh
python PatternEncoder.py 'base64({USER}:md5({PASS}))' USER users.txt PASS passwords.txt cookies.txt
```

**API Key Generator** with 3 components:

```sh
python PatternEncoder.py '{ORG}_{USER}_sha256({KEY})' ORG orgs.txt USER users.txt KEY keys.txt api_keys.txt
```


 Placeholder names MUST BE UPPERCASE (like `{USER}` not `{user}`)

## When to Use This

- Generate login cookies wordlist after identify the pattern for testing
- Create password variants wordlist (md5, base64, etc)
- Combine multiple wordlists into complex patterns

**Need ideas?** Start with 2 wordlists and simple pattern:  

`base64({PART1}:{PART2})` → converts "admin:password" to "YWRtaW46cGFzc3dvcmQ="

`sha256({WORD})` → Hashes every word in your list
