# Contributing

Thanks for helping map computer vision for the wet lab.

## The one hard rule

**Every link must resolve to the real, canonical source.** No guessed URLs, no dead links, no "I think it's called that." Verify before you open a PR:

```bash
# GitHub repos: authoritative existence check
gh api repos/OWNER/REPO --jq .full_name

# Anything else
curl -sIL -o /dev/null -w "%{http_code}\n" "https://example.com/thing"
```

Any performance metric (mAP, F1, etc.) needs a source link and a date. If you can't source it, leave it out.

## What belongs here

- Prefer **official/canonical** repos over mirrors and forks.
- One line per entry: what it is and why it matters for lab execution or eval, not a copied abstract.
- Note the license when it's decision-relevant (e.g. AGPL vs Apache).
- Short and real beats long and shaky. A padded section helps no one.

## How to add an entry

1. Fork and branch.
2. Add your entry in the right section, alphabetical-ish or by relevance, matching the existing format.
3. Verify the link(s) as above.
4. Open a PR describing what you added and how you verified it.

⭐ picks are the maintainer's opinion. Propose one in your PR and make the case, but the star is editorial.
