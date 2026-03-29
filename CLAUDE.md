# X Admin Tool

Personal X (Twitter) account management using `xurl` (github.com/xdevplatform/xurl).

## Account

- Username: @langkilde
- User ID: 18781061

## xurl Setup

Installed via Homebrew. App name: `langkilde` (Pay Per Use project in developer.x.com).

Auth: OAuth 1.0a (OAuth2 has a known bug in xurl — UsernameNotFound, issue #47).

```bash
xurl --app langkilde /2/users/18781061          # GET (default method)
xurl --app langkilde -X POST /2/tweets -d '...' # POST
xurl --app langkilde -X DELETE /2/users/18781061/following/TARGET_ID
```

Common endpoints:
```bash
# User lookups
xurl --app langkilde /2/users/18781061
xurl --app langkilde /2/users/by/username/HANDLE
xurl --app langkilde /2/users/me

# Following / followers
xurl --app langkilde /2/users/18781061/following
xurl --app langkilde /2/users/18781061/followers
xurl --app langkilde -X POST /2/users/18781061/following -d '{"target_user_id":"ID"}'
xurl --app langkilde -X DELETE /2/users/18781061/following/TARGET_ID

# Lists
xurl --app langkilde /2/users/18781061/owned_lists
xurl --app langkilde -X POST /2/lists -d '{"name":"list-name"}'
xurl --app langkilde -X DELETE /2/lists/LIST_ID
xurl --app langkilde -X POST /2/lists/LIST_ID/members -d '{"user_id":"ID"}'
xurl --app langkilde -X DELETE /2/lists/LIST_ID/members/USER_ID

# Tweets / timeline
xurl --app langkilde /2/users/18781061/timelines/reverse_chronological
xurl --app langkilde /2/tweets/TWEET_ID
xurl --app langkilde -X POST /2/tweets -d '{"text":"Hello"}'
xurl --app langkilde -X DELETE /2/tweets/TWEET_ID

# Search
xurl --app langkilde "/2/tweets/search/recent?query=from:langkilde&max_results=10"
```

xurl errors go to **stdout** (not stderr), as JSON with a trailing ANSI "Error: request failed" string. Parse with a JSON extractor that ignores trailing content.

## Pricing (Pay Per Use)

Pay Per Use launched February 6, 2026. Credits are deducted per request; exact per-endpoint rates are shown in the Developer Console.

### Credit costs (approximate)
| Operation | Credits | Est. cost |
|-----------|---------|-----------|
| Single user lookup | 1 | $0.01 |
| Paginated endpoint (~20 items) | 5 | $0.05 |
| Batch lookup (up to 100 items) | 25 | $0.25 |
| Bulk following/followers (200 profiles/page) | 50 | $0.50 |
| Tweet post | 1 | $0.01 |
| Follow / unfollow | 1 | $0.01 |
| List create / delete | 1 | $0.01 |
| List member add / remove | 1 | $0.01 |

**Deduplication:** The same resource requested within a 24-hour UTC window is not charged again.

**xAI credit bonus:** Up to 20% credits back on spend.

### Observed costs
- Fetching all 582 following IDs (50 credits/page × 3 pages): ~$1.50, not ~$5.82 as initially thought
- Bulk account reorganization (332 unfollows + 46 follows + list ops): ~$4–5

Cache user IDs in `following.txt` to avoid repeat lookup charges.

## Rate Limits

Window type is **not officially documented** as rolling vs. fixed. The `x-rate-limit-reset` header gives a Unix timestamp for window expiry.

### Write operations
| Endpoint | Per 15-min window | Per 24 hours |
|----------|-------------------|--------------|
| POST /2/users/:id/following | 50 (documented) | 400 |
| DELETE /2/users/:id/following | 50 (documented) | 500 |
| POST /2/lists | 300 | — |
| POST /2/lists/:id/members | 300 | — |
| DELETE /2/lists/:id/members/:id | 300 | — |
| POST /2/tweets | 100 | 10,000 |

**Observed unfollow limit: 50 per 15-min window** — matches the documented limit exactly. Confirmed empirically: two consecutive windows of exactly 50 unfollows, each completing in ~2 minutes before hitting 429. The 24-hour limit of 500 is a hard cap.

No bulk unfollow endpoint exists. No premium tier removes these limits.

### Rate limit response
```json
{"title":"Too Many Requests","detail":"Too Many Requests","type":"about:blank","status":429}
```

### Tiers (for reference)
| Tier | Cost | Tweet reads/month | Notes |
|------|------|-------------------|-------|
| Free | $0 | 100 | 500 ops/month total |
| Basic | $200/mo | 15,000 | v1.1 + v2 access |
| Pro | $5,000/mo | 1,000,000 | Full-archive search, streaming |
| Pay Per Use | usage | up to 2M | Default for new apps since Feb 2026 |

## Files

- `following.txt` — cached list of followed accounts, format: `@username — Display Name`
- `reorganize.log` — append-only operation log for resume support, format: `operation:key:id`
- `reorganize.py` — bulk reorganization script (unfollow 332, follow 46, delete 5 lists, create 10 lists, add 247 members)
- `run.log` — stdout from background process

## Running in Background

```bash
nohup python3 -u reorganize.py > run.log 2>&1 &
tail -f run.log

# Check progress
grep -c "^unfollowed:" reorganize.log
grep -c "^followed:" reorganize.log
grep -c "^created_list:" reorganize.log
grep -c "^added:" reorganize.log
```

The script is resume-safe: completed operations are logged line-by-line and skipped on restart.
