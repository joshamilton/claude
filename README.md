# README: claude
Copyright (c) 2026, Joshua J. Hamilton  
Email: <joshamilton@gmail.com>  
URL: <https://www.linkedin.com/in/joshamilton/>  
URL: <https://github.com/joshamilton/claude>  
All rights reserved.

## Overview

This repo describes how I configure and use Claude. I use Claude both for personal projects and for client-facing work through my consulting business, Trophic Nexus. For clients, I typically use Claude to conduct reproducible data analysis tasks, and for writing scientific software and workflows. For personal use, I use Claude to vibe-code software or agentically perform tasks I'm too lazy to do myself.

This repo contains:

- `claude/`: `CLAUDE.md` and `SKILL.md` files. Contains three folders:
    - `global`, applies everywhere
    - `joshamilton`, personal projects
    - `trophicnexus`, consulting, with one subfolder per client

- `config/`: Configuration files

- `scripts/`: Scripts

### How I Use Claude

1. I use Claude via a consumer plan (Pro / Max) and do not allow the use of chats and coding sessions to train my models (https://claude.ai/settings/data-privacy-controls).

2. I set a number of other privacy-protecting features in `~/.claude/settings.json`.

3. I use Claude throughout the day: morning, afternoon, and evening. I automatically send a prompt to Claude Code at 7am, enabling me to have three 5-hour sessions a day: 7-12, 12-5, and 5-10. 

4. I only use the Claude CLI (including through Claude Code) via my personal MacBook Pro, never through the web interface or desktop/mobile apps. This gives me a single configuration across all interactions, and ensures all interactions are associated with a Project.

5. Claude Projects are only allowed in certain folders. I maintain a project allowlist, and automatically remove projects that were accidentally created outside the allowlist. This keeps things tidy.

6. Project history gets pruned after 48 hours. I use the Claude setup `cleanupPeriodDays` for this. It keeps things tidy.

7. All Claude configuration goes into this standalone Git repo. I manually symlink into the appropriate folders as described in this document. Currently supported:
    - settings.json
    - global `CLAUDE.md` and skills
    - personal `CLAUDE.md` and skills
    - consulting `CLAUDE.md` files and client-specific skills

8. Do not use the `~/.claude/plans/` folder. All plans go in the root of the repo being worked on, in a file named `plan-<topic>.md`.

9. Do not use MEMORY.md (`autoMemoryEnabled: false`). Instead, I instruct Claude to create or update `CLAUDE.md` or `SKILL.md` files. This provides visibility and control.

#### Available Skills

The following skills are available:

Global skills (`claude/global/skills/`), available in every session:

- `extend-skill-creator` — extends the Anthropic `skill-creator` skill with my personal rules for writing and organizing skills

- `project-setup` — establishes shared conventions for all projects, personal and consulting

- `readme` — establishes the structure of a project's `README.md`

- `scripting` — establishes shared conventions for command-line scripts in any language

- `python` — expands upon `scripting` with conventions for Python projects and code

- `r` — expands upon `scripting` with conventions for R projects and code

- `r-markdown` — expands upon `scripting` and `r` with conventions for R Markdown reports

- `nextflow` — establishes conventions shared by every Nextflow pipeline

Client skills (`claude/trophicnexus/<client>/skills/`) hold only what belongs to one client. Anything that any client could need goes into a global skill instead.

### Where I use Claude

#### Personal Projects: ~/Documents/repos

#### Consulting Projects:  ~/Documents/Employment/

Each client gets its own folder of the form `YYYY-<client>`. Completed projects are stored in `~/Documents/Employment/_Archives`

## Setup

### 1. Automatically send a prompt to Claude Code at 7am

This uses a macOS LaunchAgent to run `claude -p "hey"` every morning at 7am, based on this blogpost from Stephen Turner: [Sessionmaxxing Claude Code](https://blog.stephenturner.us/p/sessionmaxxing). 

The LaunchAgent config lives in this repo at `config/claudeping.plist`.

A LaunchAgent only fires while the Mac is awake. A sleeping laptop will not run it and will not wake itself up on its own, so the Mac also needs a scheduled wake set a few minutes before 7am. This uses `pmset repeat wake`, which is a separate macOS setting from the LaunchAgent and needs to be set up on its own.

The prompt runs from its own empty folder, `/Users/joshamilton/.local/share/claudeping`. This is necessary, because macOS does not let a background job read the `Documents` folder. A job that starts in Documents fails with `Operation not permitted`. Furthermore, Claude files every session under the folder it starts in, so that folder is also on the project allowlist (`config/project-allowlist.txt`), which keeps the daily cleanup in section 2 from deleting it. Finally, the plist also raises the number of files the job may keep open to 512. A LaunchAgent starts with a limit of 256, and Claude stops with a `low max file descriptors` error at that limit.

To setup: 

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
    cp /Users/joshamilton/Documents/repos/claude/config/claudeping.plist /Users/joshamilton/Library/LaunchAgents/claudeping.plist
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

7. Perform a test run:
    ```bash
    rm -rf /tmp/claudeping.log
    rm -rf /tmp/claudeping.err
    launchctl kickstart -k gui/$(id -u)/claudeping
    sleep 30
    ```

8. Check the results:
    ```bash
    launchctl list | grep claudeping
    cat /tmp/claudeping.log
    cat /tmp/claudeping.err
    ```
    The `launchctl list` line should show `0` in the middle column, which is the exit status of the last run. The log should hold one line of reply from Claude, and the error file should be empty.

9. 24 hours after setup, check if the 7am prompt is firing:

    ```bash
    cat /tmp/claudeping.log
    Hey! How can I help you today?
    Hello! How can I help you today?
    Hello! How can I help you today?
    ```
    Should have one line for every 7am prompt.

    ```bash
    cat /tmp/claudeping.err
    ```
    Should be empty.

10. To disable this feature, unload the LaunchAgent, remove the copy from LaunchAgents, and cancel the scheduled wake:

    ```bash
    launchctl unload /Users/joshamilton/Library/LaunchAgents/claudeping.plist
    rm /Users/joshamilton/Library/LaunchAgents/claudeping.plist
    sudo pmset repeat cancel
    ```

### 2. Automatically cleanup the `~/.claude` folder

This uses a macOS LaunchAgent to run a cleanup every morning at 6:58am, two minutes before the 7am prompt in section 1 above. The script removes all projects created outside an allowlist (`config/project-allowlist.txt`).

For a project outside the allowlist, the script deletes:
    - `~/.claude/projects/<sanitized-path>/` and its contents
    - For every session UUID found in that folder (the `.jsonl` file names), the matching entries in:
        - `~/.claude/session-env/<uuid>/`
        - `~/.claude/file-history/<uuid>/`
        - `~/.claude/debug/<uuid>.txt`
        - `~/.claude/todos/<uuid>*.json`
    - The project's own `.claude/` folder

Regardless of the allowlist, the script also deletes these folders in their entirety:
    - `~/.claude/plans/`: Plan files live in each repo, so anything in `~/.claude/plans/` was created by error
    - `~/.claude/sessions/`: Forces a fresh session each day, forcing me to start a new day's work with maximum attention to detail. Context from the previous day is lost.
    - `~/.claude/ide/`: Created when the IDE starts. Removed for same reason as `~/.claude/sessions/`
    - `~/.claude/shell-snapshots/`: Created when a session starts. Removed for same reason as `~/.claude/sessions/`

This script uses a runner for security reasons. The script must delete things in folders macOS protects (e.g., `Documents`). macOS blocks background jobs from those folders unless the program has Full Disk Access. Giving Full Disk Access to `/bin/bash` would apply to every bash script on the Mac. Instead, the job starts a small program built for this one task (the runner). The runner `scripts/claude-cleanup-runner.c`  starts `/bin/bash` and calls the script, `/Users/joshamilton/.local/bin/cleanup-claude-projects.sh`. Only the runner is given Full Disk Access.

The script and the allowlist also run from copies, not from this repo, because macOS also blocks the background job from reading the Documents folder. The copies are:

- `/Users/joshamilton/.local/bin/claude-cleanup-runner`: the runner, built from `scripts/claude-cleanup-runner.c`
- `/Users/joshamilton/.local/bin/cleanup-claude-projects.sh`: copy of `scripts/cleanup-claude-projects.sh`
- `/Users/joshamilton/.local/share/claude-cleanup/project-allowlist.txt`: copy of `config/project-allowlist.txt`

To setup:

1. Review `config/project-allowlist.txt` and confirm the allowed folders and patterns are correct. Add a line for any new root as needed.

2. Make sure only I can change the folders that hold the runner and the script:
    ```bash
    chmod go-w /Users/joshamilton/.local /Users/joshamilton/.local/share
    ```

3. Check the results:
    ```bash
    ls -ld /Users/joshamilton/.local /Users/joshamilton/.local/bin /Users/joshamilton/.local/share
    ```
    All three lines show the permissions `drwxr-xr-x`.

4. Build the runner:
    ```bash
    clang -O2 -Wall -Wextra -o /Users/joshamilton/.local/bin/claude-cleanup-runner /Users/joshamilton/Documents/repos/claude/scripts/claude-cleanup-runner.c
    codesign -f -s - /Users/joshamilton/.local/bin/claude-cleanup-runner
    chmod 755 /Users/joshamilton/.local/bin/claude-cleanup-runner
    ```
    The build should print no warnings.

5. Check the results:
    ```bash
    codesign -dv /Users/joshamilton/.local/bin/claude-cleanup-runner 2>&1 | grep Signature
    Signature=adhoc
    ls -l /Users/joshamilton/.local/bin/claude-cleanup-runner
    -rwxr-xr-x  1 joshamilton  staff  33776 Nov  8 15:59 /Users/joshamilton/.local/bin/claude-cleanup-runner
    ```

6. Give the runner Full Disk Access:
    - Open System Settings, then Privacy & Security, then Full Disk Access.
    - Click `+`. In the file picker, press `Cmd+Shift+G` and type `/Users/joshamilton/.local/bin/`.
    - Choose `claude-cleanup-runner.c`, click Open, and make sure its switch is on.

7. Copy the script and the allowlist into place:
    ```bash
    cp /Users/joshamilton/Documents/repos/claude/scripts/cleanup-claude-projects.sh /Users/joshamilton/.local/bin/cleanup-claude-projects.sh
    chmod 755 /Users/joshamilton/.local/bin/cleanup-claude-projects.sh
    mkdir -p /Users/joshamilton/.local/share/claude-cleanup
    cp /Users/joshamilton/Documents/repos/claude/config/project-allowlist.txt /Users/joshamilton/.local/share/claude-cleanup/project-allowlist.txt
    chmod 644 /Users/joshamilton/.local/share/claude-cleanup/project-allowlist.txt
    ```

8. Check the results. Each `diff` should print nothing, and the `echo` after it should print its message:
    ```bash
    diff /Users/joshamilton/Documents/repos/claude/scripts/cleanup-claude-projects.sh /Users/joshamilton/.local/bin/cleanup-claude-projects.sh && echo script-copy-matches
    script-copy-matches
    diff /Users/joshamilton/Documents/repos/claude/config/project-allowlist.txt /Users/joshamilton/.local/share/claude-cleanup/project-allowlist.txt && echo allowlist-copy-matches
    allowlist-copy-matches
    ```

9. Copy the plist into the LaunchAgents folder:
    ```bash
    cp /Users/joshamilton/Documents/repos/claude/config/claude-project-cleanup.plist /Users/joshamilton/Library/LaunchAgents/claude-project-cleanup.plist
    ```

10. Load it so it starts running:
    ```bash
    launchctl load /Users/joshamilton/Library/LaunchAgents/claude-project-cleanup.plist
    ```

11. Check that it is loaded:
    ```bash
    launchctl list | grep claude-project-cleanup
    ```

12. Perform a test run:
    ```bash
    ls ~/.claude/projects > /tmp/projects-before.txt
    rm -rf /tmp/claude-project-cleanup.out
    rm -rf /tmp/claude-project-cleanup.err
    launchctl kickstart -k gui/$(id -u)/claude-project-cleanup
    sleep 30
    ```

13. Check the results:
    ```bash
    launchctl list | grep claude-project-cleanup
    cat /tmp/claude-project-cleanup.out
    cat /tmp/claude-project-cleanup.err
    ls ~/.claude/projects | diff /tmp/projects-before.txt - && echo projects-unchanged
    ```
    The `launchctl list` line should show `0` in the middle column, which is the exit status of the last run. The output should be one line such as `Removed 0 project(s) outside the allowlist and 0 on-disk .claude folder(s).` The error file should be empty. If no project is outside the allowlist, `projects-unchanged` is printed.

14. 24 hours after setup, check if the cleanup ran:
    ```bash
    cat /tmp/claude-project-cleanup.out
    Removed 1 project(s) outside the allowlist and 0 on-disk .claude folder(s).
    ```
    Should have one line per day.

    ```bash
    cat /tmp/claude-project-cleanup.err
    ```
    Should be empty.

15. To disable this feature, unload the LaunchAgent, remove the copy from LaunchAgents, and remove the runner, the script copy and the allowlist copy. Then remove `claude-cleanup-runner` from Full Disk Access by hand in System Settings (select it in the list and click `-`):
    ```bash
    launchctl unload /Users/joshamilton/Library/LaunchAgents/claude-project-cleanup.plist
    rm /Users/joshamilton/Library/LaunchAgents/claude-project-cleanup.plist
    rm /Users/joshamilton/.local/bin/claude-cleanup-runner /Users/joshamilton/.local/bin/cleanup-claude-projects.sh
    rm -r /Users/joshamilton/.local/share/claude-cleanup
    ```

### 3. Symlink `settings.json`

`config/settings.json` holds the global Claude Code settings, symlinked to `~/.claude/settings.json`. The settings are saved in the order used by Claude Code, so I can easily spot differences.

To setup:

1. Symlink the repo copy into place:
    ```bash
    ln -s /Users/joshamilton/Documents/repos/claude/config/settings.json ~/.claude/settings.json
    ```

2. Check that it resolved:
    ```bash
    ls -la ~/.claude/settings.json
    /Users/joshamilton/.claude/settings.json -> /Users/joshamilton/Documents/repos/claude/config/settings.json
    ```

### 4. Set the spinner word in the VS Code panel

`spinnerVerbs` in `config/settings.json` changes the spinner word in the terminal only. The Claude Code panel in VS Code draws its own spinner and reads its own VS Code setting, `claudeCode.spinnerVerbs`. This setting has to be set by hand.

To setup:

1. Open the VS Code user settings file: press `Cmd+Shift+P`, then choose `Preferences: Open User Settings (JSON)`.

2. Add this entry inside the top-level braces:
    ```json
    "claudeCode.spinnerVerbs": {
        "mode": "replace",
        "verbs": [
            "Working"
        ]
    },
    ```

3. Save the file.

4. Check the results: send any prompt in the Claude Code panel. The spinner should say `Working`.

### 5. Link the CLAUDE.md and SKILL.md files

Every `CLAUDE.md` and every skill is deployed as a symlink that points into the `claude/` folder of this repo.

To setup:

1. Link the global `CLAUDE.md`, and each global skill. The whole `~/.claude/skills` folder cannot be linked, because Claude keeps its own `~/.claude/skills/synced/` folder there. Therefore, link each file individually:

    ```bash
    ln -s "$PWD"/claude/global/CLAUDE.md ~/.claude/CLAUDE.md
    for skill in "$PWD"/claude/global/skills/*/; do
        ln -s "${skill%/}" ~/.claude/skills/"$(basename "$skill")"
    done
    ```

2. Link the personal `CLAUDE.md`. It goes in the folder that holds my personal repos:

    ```bash
    ln -s "$PWD"/claude/joshamilton/CLAUDE.md ~/Documents/repos/CLAUDE.md
    ```

3. Link the personal skills into every personal repo (every project in `~/Documents/repos/`):

    ```bash
    mkdir -p <repo>/.claude
    ln -s "$PWD"/claude/joshamilton/skills <repo>/.claude/skills
    ```

4. Link the consulting `CLAUDE.md`, and the `CLAUDE.md` of each client:

    ```bash
    ln -s "$PWD"/claude/trophicnexus/CLAUDE.md ~/Documents/Employment/CLAUDE.md
    ln -s "$PWD"/claude/trophicnexus/<client>/CLAUDE.md ~/Documents/Employment/YYYY-<client>/CLAUDE.md
    ```

5. Link each client's skills into every project for that client:

    ```bash
    mkdir -p ~/Documents/Employment/YYYY-<client>/repos/<repo>/.claude
    ln -s "$PWD"/claude/trophicnexus/<client>/skills ~/Documents/Employment/YYYY-<client>/repos/<repo>/.claude/skills
    ```

## Development 

### Guidelines for skills

The rules for writing and organizing skills live in the global skill `extend-skill-creator` (`claude/global/skills/extend-skill-creator/`). It extends the Anthropic `skill-creator` skill.

### Publishing this repo

This repo contains private client secrets that should never be published. To prevent their publication, a redacted version of the repo is built and pushed to GitHub by the script `scripts/make_public_mirror.py`.

How the script works:

1. It clones the commit history into `../claude-public`.

2. It runs `git-filter-repo` so that only the allowed paths (`config/github-allowlist.yml`) remain in every commit. Commits keep their message, date and author.

3. It scans the commit history of the copy for the names in `config/github-blocklist.yml`, ignoring case. A name matches as plain text anywhere, so `fooBar`, `foo_bar` and `FOO` all match `foo`. The blocklist is committed in this repo, but it is not on the allowlist, so it is never part of the copy.

4. If a name is found, the copy is deleted and the script stops. The matching lines are shown for review. If a match is an ordinary word (example: the name `foo` matches the word `foobar`), add that word to `exceptions` in the blocklist.

5. It sets the remote `origin` to `git@joshamilton-github.com:joshamilton/claude.git`, but does not push.

#### Setup:

Create the environment and check it:

```bash
mamba env create -f config/claude.yml
mamba run -n claude git filter-repo --version
```

#### Usage:

Run the script:

```bash
mamba run -n claude python scripts/make_public_mirror.py
cd ../claude-public
git push -u origin main
```

## About Claude:

### The `~/.claude` folder

The `~/.claude` folder contains many files and subfolders:
    - .last-cleanup: global configuration file
    - backups: config/settings backups
    - cache: global cache (changelog, model catalog)
    - CLAUDE.md: global configuration file
    - debug/<uuid>.txt: the debug log for that session.
    - file-history/<uuid>/: per-session file-edit history.
    - ide: lock files keyed by process ID, for IDE integration
    - plans: plan-mode output files, named randomly
    - plugins: installed plugins
    - projects: one folder per project. Contains that project's session transcripts, one .jsonl file per session, named by session UUID.
    - session-env/<uuid>/: per-session environment state.
    - sessions: auth/key files keyed by process ID, for the running CLI process itself
    - settings.json: global configuration file
    - shell-snapshots: shell environment snapshots, named by timestamp, not by project or session.
    - skills: global configuration file
    - stats-cache.json: global configuration file
    - statsig: telemetry and feature-flag state
    - todos/<uuid>-agent-<uuid>.json: the task list for that session or a subagent spawned within it.

Based on my requirements, a full cleanup of a disallowed project needs to: 
    - Identify disallowed projects in `~/.claude.projects`
    - Read the session UUIDs
    - Delete the disallowed projects from `~/.claude.projects`
    - Remove matching entries from session-env/, file-history/, todos/, and debug/.

Because the the utility can remove these folders in their entirety:
    - ide: lock files keyed by process ID, for IDE integration
    - plans: plan-mode output files, named randomly
    - sessions: auth/key files keyed by process ID, for the running CLI process itself
    - shell-snapshots: shell environment snapshots, named by timestamp, not by project or session.

### How Claude finds files

1. Claude loads `CLAUDE.md` from the folder where the session starts and from every folder above it, all the way up. It does not stop at the root of the Git repo. This is why one `CLAUDE.md` in a client folder applies to every project repo inside it.

2. Personal skills are loaded from `~/.claude/skills/`. Project skills are loaded from `.claude/skills/` in the start folder and in each parent folder, up to the root of the Git repo. The search stops there. A skill in a client folder above the repo is not loaded, so each project repo needs its own link. The link is the folder: `.claude/skills` in the repo points to the `skills` folder in this repo.

Those behaviors establish how this repo's symlinks work:

- The global files apply everywhere, so they are linked from `~/.claude/`.

- The personal `CLAUDE.md` is linked from the folder that holds my personal repos. Its `skills` folder is linked into every personal repo.

- The consulting `CLAUDE.md` is linked from the folder that holds all client folders. Each client folder gets its own `CLAUDE.md`. Each client's `skills` folder is linked into each project repo for that client.

### Settings and Environmental Variables: `~/.claude/settings.json`

#### Environmental Variables
Claude Environmental Variables are documented here: [Environment variables](https://code.claude.com/docs/en/env-vars).

The following variables are enabled in `~/.claude/settings.json`:

- CLAUDE_CODE_DISABLE_ERROR_REPORTING: turn off error reporting
- CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY: turn off "how is Claude doing" survey
- CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: disable nonessential network traffic: auto-updates, telemetry, error reporting, the /feedback command, Claude-drafted feedback, release notes, the PR and MR status badge checks, and availability checks
- DISABLE_ERROR_REPORTING: turn off sending error reports
- DISABLE_FEEDBACK_COMMAND: turn off `feedback` command
- DISABLE_TELEMETRY: turn off telemetry data collection 
- DO_NOT_TRACK: general opt-out signal

The following variables are not enabled in `~/.claude/settings.json`, but are worth knowing about:
- CLAUDE_CODE_SKIP_PROMPT_HISTORY": session transcripts are ephemeral, never stored on disk

#### Settings
Claude settings are documented here: [Settings](https://code.claude.com/docs/en/settings-reference). I identified the following settings as being of relevance, as of October 2026:

**Global config settings**
- copyOnSelect: prevent Claude from copying selected text to its context. I hate it when it does that.

**Interface and terminal**
- prefersReducedMotion: reduce/turn off animations
- spinnerTipsEnabled: disable tips about Claude Code features
- spinnerVerbs: change the verbs the spinner shows. This works in the terminal only. The VS Code panel ignores it and has its own setting (see section 4 of Setup).

**Memory and context**
- autoMemoryEnabled: turn autoMemory off. Necessary to isolate configuration to this repo
- env: set environment variables for every session and subprocesses
- fileCheckpointingEnabled: turn on file snapshots

**Model and responses**
- model: default model to start with
- effortLevel: default effort to start with
- outputStyle: set of instructions that sets Claude’s role, tone, and response format for every response in a session. 
- showThinkingSummaries: see summaries of Claude’s extended thinking

**Permission settings**
- TBD

**Plugins and skills**
- disableArtifact: turn off the Artifact tool. I don't use them.
- disableBundledSkills: disabled bundled skills. Not set, but worth knowing about.
- disableWorkflows: turn off dynamic workflows. I don't use them.

**Privacy and telemetry**
- cleanupPeriodDays: how many days Claude keeps transcripts
- desktopSessionCleanupPeriodDays: how many days Claude Desktop and Cowork keep transcripts
- feedbackDrafts: whether Claude queues feedback drafts
- feedbackSurveyRate: how often the Claude survey appears
- skipWebFetchPreflight: skip the WebFetch hostname check when Anthropic is unreachable
