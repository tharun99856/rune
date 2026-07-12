"""The 'AI proposes' front-end: English -> (LLM) -> Rune -> (verify) -> verdict.

The LLM is a Groq chat model (OpenAI-compatible API). It only *proposes*;
rune.verify is the source of truth that certifies or rejects the proposal.
The API key is read from the GROQ_API_KEY environment variable and is never
stored in code or the repo.

Note: the live call needs network access to Groq. If run from an IP Groq's
bot-protection blocks (e.g. some datacenter/CI IPs -> Cloudflare 1010), the
call fails there; it works from a normal machine. The propose function is
injectable so everything except the literal HTTP call is testable offline.
"""

import json
import os
import urllib.request
from pathlib import Path

from rune.verify import verify_program


def _load_dotenv():
    # Populate os.environ from a local .env (gitignored) if present, without
    # a third-party dependency. Existing env vars win over the file.
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

_GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
_DEFAULT_MODEL = "llama-3.1-8b-instant"

_SYSTEM_PROMPT = """You translate a plain-English task into a Rune program.

Rune is a tiny, CLOSED language. Output ONLY a Rune program -- no prose, no
markdown fences. Use ONLY these statements, one per line; each line transforms
the previous line's result:

  GROUP <source> BY <key>            -- partition a collection by a key
  COUNT EACH <noun>                  -- count items in each group
  ORDER BY <key> [ASC|DESC]          -- sort by a key
  TAKE <n>                           -- keep the first n
  EXPLORE <graph> FROM <a> [TO <b>]  -- shortest paths / reachability
  MAXIMIZE SUM OVER CONTIGUOUS <x>   -- best contiguous-subarray sum (or MINIMIZE)

Examples:
Task: the 10 most frequent values in nums
GROUP nums BY value
COUNT EACH group
ORDER BY count DESC
TAKE 10

Task: largest sum of a contiguous chunk of nums
MAXIMIZE SUM OVER CONTIGUOUS nums

If the task cannot be expressed with these statements, output exactly:
CANNOT_EXPRESS
"""


def _strip_fences(text: str) -> str:
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("```")]
    return "\n".join(lines).strip()


def propose_rune(english: str, model: str = _DEFAULT_MODEL) -> str:
    """Ask the LLM to translate English -> a Rune program. Live network call."""
    _load_dotenv()
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY is not set (env var or .env file)")
    body = json.dumps({
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": f"Task: {english}"},
        ],
    }).encode()
    req = urllib.request.Request(
        _GROQ_URL, data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    return _strip_fences(data["choices"][0]["message"]["content"].strip())


def english_to_verified_rune(english, test_input=None, expected=None, propose=propose_rune):
    """The full loop: LLM proposes a Rune program, Rune verifies it.

    `propose` is injectable so this is testable without any network/API.
    Returns (proposed_source, VerificationResult).
    """
    source = propose(english)
    return source, verify_program(source, test_input=test_input, expected=expected)
