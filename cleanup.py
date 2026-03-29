#!/usr/bin/env python3
"""Unfollow 51 accounts and follow 7 new ones via xurl."""

import json
import subprocess
import time
import sys

MY_USER_ID = "18781061"
LOG_FILE = "cleanup.log"

UNFOLLOW = [
    "AarianMarshall", "alliansswe", "arxiv_cs_cl", "atpfm", "BarackObama",
    "bengtzboe", "BillClinton", "carlbildt", "caseyliss", "chenglou",
    "claudioguglieri", "cloudera", "dagensnyheter", "DalaiLama", "databricks",
    "didigital_se", "Dr_PO", "FLI_org", "github", "GoogleCloudTech",
    "HillaryClinton", "ISYudkowsky", "jasonyo", "jhagel", "K_GBergstrom",
    "KinbergBatra", "madeleine", "marcoarment", "matsknutson", "Modular",
    "OlleAronsson", "perschlingmann", "Pontifex", "Pontifex266Arch", "psawers",
    "pwolodarski", "rmetzger", "SenJohnMcCain", "siracusa", "sparud",
    "SvDledare", "timbro", "tnachen", "vanschneider", "vdbergrianne",
    "viktorbk", "viktorsval", "WHOSTP44", "wjzeng", "ykilcher",
    "ZetterbergUlf",
]

FOLLOW = [
    "crmiller1", "JeffDean", "jimkxa", "olivercameron",
    "pmddomingos", "TheEconomist", "ZachFlom",
]


def load_done() -> set[str]:
    try:
        with open(LOG_FILE) as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set()


def log_done(entry: str):
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")


def xurl(args: list[str]) -> dict | None:
    cmd = ["xurl", "--app", "langkilde"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout.strip()
    if not output:
        return None
    # xurl puts JSON then sometimes trailing ANSI error text
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        # Try to extract JSON from the beginning
        for i in range(len(output), 0, -1):
            try:
                return json.loads(output[:i])
            except json.JSONDecodeError:
                continue
    return None


def lookup_user_id(username: str) -> str | None:
    data = xurl([f"/2/users/by/username/{username}"])
    if data and "data" in data:
        return data["data"]["id"]
    print(f"  ERROR looking up @{username}: {data}")
    return None


def unfollow(user_id: str, username: str) -> bool:
    data = xurl(["-X", "DELETE", f"/2/users/{MY_USER_ID}/following/{user_id}"])
    if data and "data" in data:
        return True
    if data and data.get("status") == 429:
        return False  # rate limited
    print(f"  ERROR unfollowing @{username}: {data}")
    return True  # non-rate-limit error, skip


def follow(user_id: str, username: str) -> bool:
    data = xurl(["-X", "POST", f"/2/users/{MY_USER_ID}/following",
                 "-d", json.dumps({"target_user_id": user_id})])
    if data and "data" in data:
        return True
    if data and data.get("status") == 429:
        return False
    print(f"  ERROR following @{username}: {data}")
    return True


def main():
    done = load_done()

    # --- Unfollows ---
    remaining_unfollows = [u for u in UNFOLLOW if f"unfollowed:{u}" not in done]
    print(f"Unfollows remaining: {len(remaining_unfollows)}/{len(UNFOLLOW)}")

    count = 0
    for username in remaining_unfollows:
        if f"lookup:{username}" in done:
            # we looked up but didn't unfollow - need to look up again for ID
            pass

        print(f"  Looking up @{username}...", end=" ", flush=True)
        user_id = lookup_user_id(username)
        if not user_id:
            log_done(f"skip:{username}")
            print("skipped")
            continue

        print(f"id={user_id}, unfollowing...", end=" ", flush=True)
        success = unfollow(user_id, username)
        if not success:
            print("RATE LIMITED")
            print(f"  Hit rate limit after {count} unfollows. Waiting 15 minutes...")
            time.sleep(15 * 60 + 10)
            # retry this one
            success = unfollow(user_id, username)
            if not success:
                print("  Still rate limited. Exiting. Re-run to resume.")
                sys.exit(1)

        log_done(f"unfollowed:{username}")
        count += 1
        print("done")
        time.sleep(1)  # be nice

    # --- Follows ---
    remaining_follows = [u for u in FOLLOW if f"followed:{u}" not in done]
    print(f"\nFollows remaining: {len(remaining_follows)}/{len(FOLLOW)}")

    for username in remaining_follows:
        print(f"  Looking up @{username}...", end=" ", flush=True)
        user_id = lookup_user_id(username)
        if not user_id:
            log_done(f"skip:{username}")
            print("skipped")
            continue

        print(f"id={user_id}, following...", end=" ", flush=True)
        success = follow(user_id, username)
        if not success:
            print("RATE LIMITED")
            print(f"  Hit rate limit. Waiting 15 minutes...")
            time.sleep(15 * 60 + 10)
            success = follow(user_id, username)
            if not success:
                print("  Still rate limited. Exiting. Re-run to resume.")
                sys.exit(1)

        log_done(f"followed:{username}")
        print("done")
        time.sleep(1)

    print("\nAll done!")


if __name__ == "__main__":
    main()
