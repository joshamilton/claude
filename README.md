# README: claude
Copyright (c) 2026, Joshua J. Hamilton  
Email: <joshamilton@gmail.com>  
URL: <https://www.linkedin.com/in/joshamilton/>  
URL: <https://github.com/joshamilton/claude>
All rights reserved.

## Overview

This repo describes how I configure and use Claude. I use Claude both for personal projects and for client-facing work through my consulting business, Trophic Nexus. For clients, I typically use Claude to conduct reproducible data analysis tasks, and for writing scientific software and workflows. For personal use, I use Claude to vibe-code software or agentically perform tasks I'm too lazy to do myself.

This repo contains ... [TBD]

## How I Use Claude

1. I use Claude throughout the day: morning, afternoon, and evening. I automatically send a prompt to Claude Code at 7am, enabling me to have three 5-hour sessions a day: 7-12, 12-5, and 5-10. 

2. I only use the Claude CLI (including through Claude Code) via my personal MacBook Pro, never through the web interface or desktop/mobile apps. This gives me a single configuration across all interactions, and ensures all interactions are associated with a Project.

3. Claude Projects are only allowed in certain folders. I maintain a project allowlist, and automatically remove projects that were accidentally created outside the allowlist. This keeps things tidy.

4. Project history gets pruned after 48 hours. I use the Claude setup `cleanupPeriodDays` for this. It keeps things tidy.

5. All Claude configuration goes into this standalone Git repo. I manually symlink into the appropriate folders as described in this document.
    - To include: CLAUDE.md, SKILLS.md,
    - Possibly styles, rules, as I begin to use them

6. Do not use `~/.claude/plans.md`. All plans go in the 

7. Do not use Memory.md. Instead, memory should should be stored in the same Github repo, so that I have visibility into it and control over it.

8. As part of the above, I do not use Claude memory (`autoMemoryEnabled: false`). Instead, I instruct Claude to create or update CLAUDE.md or SKILLS.md files instead. This provides visibility and control.

## Where I use Claude

### Personal Project: ~/Documents/repos

### Consulting Projects:  ~/Documents/Employment/

Each client gets its own folder of the form `YYYY-<client>`. Completed projects are stored in `~/Documents/Employment/_Archives`

## Setup

### 1. Automatically send a prompt to Claude Code at 7am

This uses a macOS LaunchAgent to run `claude -p "hey"` every morning at 7am, based on this blogpost from Stephen Turner: [Sessionmaxxing Claude Code](https://blog.stephenturner.us/p/sessionmaxxing). 

The LaunchAgent config lives in this repo at `config/claudeping.plist`.

A LaunchAgent only fires while the Mac is awake. A sleeping laptop will not run it and will not wake itself up on its own, so the Mac also needs a scheduled wake set a few minutes before 7am. This uses `pmset repeat wake`, which is a separate macOS setting from the LaunchAgent and needs to be set up on its own.

To set it up again on a Mac:

1. Confirm the Claude CLI is installed at `/Users/joshamilton/.local/bin/claude`:
    ```bash
    which claude
    /Users/joshamilton/.local/bin/claude
    ```
If it is installed somewhere else, update the path in `config/claudeping.plist` to match.

2. Schedule the Mac to wake every day at 6:55am, five minutes before the prompt fires:
    ```bash
    sudo pmset repeat wake MTWRFSU 06:55:00
    ```

3. Check that the wake schedule is set:
    ```bash
    pmset -g sched
    Repeating power events:
        wake at 6:55AM every day
    ```

4. Copy the plist into the LaunchAgents folder:
    ```bash
    cp /Users/joshamilton/Documents/repos/claude-v2/config/claudeping.plist /Users/joshamilton/Library/LaunchAgents/claudeping.plist
    ```

5. Load it so it starts running:
    ```bash
    launchctl load /Users/joshamilton/Library/LaunchAgents/claudeping.plist
    ```

6. Check that it is loaded:
    ```bash
    launchctl list | grep claudeping
    ```
Logs from each run go to `/tmp/claudeping.log` (output) and `/tmp/claudeping.err` (errors).

7. 24 hours after setup, check if the 7am prompt is firing:

    ```bash
    cat /tmp/claudeping.log
    Hey! How can I help you today?
    Hello! How can I help you today?
    Hello! How can I help you today?
    ```
    Should have one line for every 7am prompt.

    ```bash
    /tmp/claudeping.err
    ```
    Should be empty.


8. To disable this feature, unload the LaunchAgent, remove the copy from LaunchAgents, and cancel the scheduled wake:

    ```bash
    launchctl unload /Users/joshamilton/Library/LaunchAgents/claudeping.plist
    rm /Users/joshamilton/Library/LaunchAgents/claudeping.plist
    sudo pmset repeat cancel
    ```

