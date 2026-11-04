# ⚡ Shortslip Lab (Unified Viral Studio)

Shortslip Lab is a high-performance, locally hosted multi-file Python/Flask automation suite engineered for creators to ingest long-form YouTube videos or Instagram Reels, compile AI instruction packages, slice high-retention segments using FFmpeg, manage a strict 4-slot daily publishing cadence, and securely push private drafts to YouTube via zero-persistence OAuth.

---

## 🏗️ Architecture & Design Philosophy

Unlike bulky monolithic scripts, Shortslip Lab utilizes a clean **modular backend design**. This ensures high maintainability, isolated debugging, and smooth scaling. 

```text
Shortslip_Lab/
├── start.bat               # Master environment bootstrapper & launcher
├── update.bat              # Smart GitHub sync script (preserves local state)
├── requirements.txt        # Python dependency manifest
├── app.py                  # Core Flask server & API route dispatcher
├── clipping.py             # Mode 1: YouTube ingestion & transcript extraction
├── reels.py                # Mode 2: Instagram reel batch handling
├── renderer.py             # FFmpeg video trimming, watermarking & subtitles
-── scheduler.py            # Independent 4-slot daily cadence engine
├── youtube_auth.py         # Zero-token-persistence Google OAuth & uploader
├── schedule_tracker.json   # Local slot occupancy & booking state
└── templates/
    └── index.html          # Modern dark-mode dashboard interface


    🧩 Component Breakdown & Functions
1. app.py (The Flask Core)
Role: Acts as the central nervous system tying all backend modules to the frontend interface.

Key Routes:

GET /: Serves the single-page dashboard interface.

POST /api/fetch-youtube: Ingests a YouTube URL, retrieves metadata, and builds the Master AI prompt pack.

POST /api/fetch-reels: Parses Instagram links and compiles reel AI packaging metadata.

POST /api/schedule: Computes and reserves the next available publishing slot based on mode rules.

POST /api/upload-youtube: Initiates a fresh OAuth session and pushes the rendered MP4 as a private scheduled draft.

2. clipping.py (Mode 1: YouTube Ingestion & Transcription)
Role: Handles video data harvesting without downloading bulky source files upfront.

Core Logic: Uses yt-dlp to extract titles and IDs cleanly while bypassing format errors (ignore_no_formats_error). Integrates youtube-transcript-api to pull real timestamped transcripts, formatting them into structured blocks for AI analysis.

3. reels.py (Mode 2: Instagram Reel Grabber)
Role: Manages social link parsing for short-form content.

Core Logic: Extracts individual or batch reel sources via yt-dlp and compiles metadata payloads ready for formatting and quick local rendering.

4. renderer.py (FFmpeg Processing Engine)
Role: Handles video manipulation, encoding, and brand styling.

Core Logic: Invokes system ffmpeg subprocesses to slice exact time windows (-ss, -to), burn dynamic text overlays (such as draggable @ChannelName watermarks with coordinate mapping), apply subtitle styling, and output high-retention MP4 clips.

5. scheduler.py (The 4-Slot Interleaved Cadence Engine)
Role: Enforces a rigid daily publishing rhythm without letting modes steal each other's slots.

Cadence Rules:

Mode 1 (Clipping): Locked to 12:00 AM and 12:00 PM daily.

Mode 2 (Reels): Locked to 06:00 AM and 06:30 PM daily.

State Management: Persists slot reservation history in schedule_tracker.json to prevent double-booking across restarts.

6. youtube_auth.py (Zero-Persistence OAuth & Uploader)
Role: Interfaces securely with the YouTube Data API v3.

Security Design: Zero Token Storage. No token.pickle or credential files are ever written to disk. Every launch and upload triggers a live, local loopback server (flow.run_local_server) forcing a fresh Google browser consent prompt.

Upload Payload: Automatically injects selfDeclaredMadeForKids: false, maps custom tags, formats descriptions, and sets strict private scheduling states.

🎨 Dashboard UI (templates/index.html)
Built with Tailwind CSS, the interface mirrors professional editing suites:

Sidebar Navigation: Seamlessly switches between Clipper Studio, Reel Grabber, and Settings & Schedule.

Split Top Panels: Clean side-by-side workflow for generating AI prompt packages and pasting AI JSON responses.

Dynamic Clip Grid: Step 3 generates modular interactive cards for every AI-extracted clip complete with Virality Score badges, video preview blocks, editable title fields, layout selectors, caption styles, hook banner toggles, and direct Render High-Quality MP4 triggers.

🚀 Setup, Launch, and Updates
Launching the Studio
Double-click start.bat.

Automatically checks/upgrades dependencies via requirements.txt.

Boots the Flask server on http://127.0.0.1:5000.

Automatically fires up your default browser to the dashboard.

Updating via GitHub (update.bat)
Double-click update.bat whenever code changes are pushed to your repository:

Automatically fetches updates from GitHub.

Safeguards local state: Backs up and restores schedule_tracker.json and client_secret.json so your slot history and Google credentials are never overwritten.

Refreshes Python packages automatically if requirements.txt changes.
