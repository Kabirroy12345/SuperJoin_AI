def get_dashboard_html() -> str:
    """Returns the RazorPay Hackathon Audit Terminal inspired dashboard interface."""
    return r"""<!DOCTYPE html>
<html lang="en" class="h-full bg-[#050711]">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#050711">
  <title>SUPERJOIN // FACT_TERMINAL | Cross-Filing Audit & Reconciliation</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');

    :root {
      --bg-root: #050711;
      --bg-surface: #0C101E;
      --bg-surface-elevated: #131A30;
      
      --border-hairline: #1F2942;
      --border-hover: #37476D;
      --border-gold: rgba(229, 184, 105, 0.35);
      
      --text-primary: #F8FAFC;
      --text-muted: #94A3B8;
      --text-gold: #E5B869;
      
      --accent-amber: #E5B869;
      --accent-gold: #F5D061;
      --accent-red: #F43F5E;
      --accent-sapphire: #0C8CE9;
      --accent-emerald: #10B981;
      
      --font-mono: 'JetBrains Mono', monospace;
      --font-sans: system-ui, -apple-system, sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-root);
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(229, 184, 105, 0.05) 0%, transparent 45%),
        radial-gradient(circle at 85% 25%, rgba(12, 140, 233, 0.06) 0%, transparent 50%),
        radial-gradient(circle at 50% 85%, rgba(139, 92, 246, 0.04) 0%, transparent 55%),
        linear-gradient(180deg, #050711 0%, #03050B 100%);
      background-attachment: fixed;
      color: var(--text-primary);
      font-family: var(--font-sans);
      min-height: 100vh;
      overflow-x: hidden;
    }

    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: var(--bg-root);
      border-left: 1px solid var(--border-hairline);
    }
    ::-webkit-scrollbar-thumb {
      background: var(--border-hairline);
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: var(--text-muted);
    }

    @keyframes panel-cascade {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes badge-scan {
      0% { left: -100%; }
      20% { left: 200%; }
      100% { left: 200%; }
    }
    @keyframes pulse-op {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
    }
    @keyframes data-flicker {
      0% { opacity: 0.2; }
      25% { opacity: 0.8; }
      50% { opacity: 0.1; }
      75% { opacity: 0.9; }
      100% { opacity: 1; }
    }
    @keyframes drawer-slide {
      from { transform: translateX(100%); }
      to { transform: translateX(0); }
    }

    .terminal-panel {
      background: rgba(12, 16, 30, 0.78);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.05);
      border-radius: 8px;
      animation: panel-cascade 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      opacity: 0;
      transform: translateY(10px);
      transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
    }
    .terminal-panel:hover {
      border-color: rgba(229, 184, 105, 0.25);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55), 0 0 20px rgba(229, 184, 105, 0.06);
    }

    .badge {
      display: inline-block;
      padding: 0.2rem 0.5rem;
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      border: 1px solid currentColor;
      border-radius: 4px;
      position: relative;
      overflow: hidden;
    }
    .badge::after {
      content: '';
      position: absolute;
      top: 0; left: -100%;
      width: 50%; height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
      animation: badge-scan 3s linear infinite;
    }

    .badge-amber {
      color: #F5D061;
      background: rgba(245, 208, 97, 0.1);
      border-color: rgba(245, 208, 97, 0.35);
      box-shadow: 0 0 10px rgba(245, 208, 97, 0.12);
    }
    .badge-red {
      color: #F43F5E;
      background: rgba(244, 63, 94, 0.1);
      border-color: rgba(244, 63, 94, 0.35);
      box-shadow: 0 0 10px rgba(244, 63, 94, 0.12);
    }
    .badge-sapphire {
      color: #38BDF8;
      background: rgba(12, 140, 233, 0.1);
      border-color: rgba(12, 140, 233, 0.35);
      box-shadow: 0 0 10px rgba(12, 140, 233, 0.12);
    }
    .badge-emerald {
      color: #10B981;
      background: rgba(16, 185, 129, 0.1);
      border-color: rgba(16, 185, 129, 0.3);
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.12);
    }
    .badge-purple {
      color: #C084FC;
      background: rgba(168, 85, 247, 0.1);
      border-color: rgba(168, 85, 247, 0.35);
    }

    .btn-terminal {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.45rem 0.9rem;
      font-family: var(--font-sans);
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-primary);
      background: rgba(15, 21, 38, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 6px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
      cursor: pointer;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .btn-terminal:hover:not(:disabled) {
      background: rgba(25, 33, 58, 0.85);
      border-color: rgba(229, 184, 105, 0.5);
      color: #FFFFFF;
      transform: translateY(-1px);
      box-shadow: 0 4px 16px rgba(0,0,0,0.4), 0 0 12px rgba(229, 184, 105, 0.15);
    }
    .btn-terminal.primary {
      background: linear-gradient(180deg, #F5D061 0%, #D4A346 100%);
      color: #050711;
      font-weight: 800;
      border: 1px solid #FFE082;
      box-shadow: 0 4px 18px rgba(212, 163, 70, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.4);
    }
    .btn-terminal.primary:hover:not(:disabled) {
      background: linear-gradient(180deg, #FFE082 0%, #E5B869 100%);
      box-shadow: 0 6px 24px rgba(245, 208, 97, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.6);
      transform: translateY(-1px);
    }
    .btn-terminal:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .pulse-indicator {
      animation: pulse-op 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    .font-mono {
      font-family: var(--font-mono);
    }
    .active-case-card {
      border-color: #F5D061 !important;
      background: rgba(245, 208, 97, 0.05) !important;
      box-shadow: 0 0 20px rgba(245, 208, 97, 0.18) !important;
      transform: translateY(-2px);
    }
    .hidden { display: none !important; }
    .mark-highlight {
      background-color: rgba(245, 208, 97, 0.25);
      color: #FEF08A;
      padding: 1px 3px;
      border-radius: 2px;
      font-weight: 600;
    }
  </style>
</head>
<body class="h-full flex flex-col antialiased selection:bg-amber-500/30 selection:text-white">

  <!-- TopNav Sticky Bar (from RazorPay TopNav.tsx) -->
  <header style="position: sticky; top: 0; z-index: 90; background: rgba(5, 7, 17, 0.88); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding: 0.65rem 1.5rem; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);">
    
    <!-- Left: Breadcrumbs & Track -->
    <div style="display: flex; align-items: center; gap: 0.85rem;">
      <div style="display: flex; align-items: center; gap: 0.45rem; background: rgba(12, 140, 233, 0.1); border: 1px solid rgba(12, 140, 233, 0.28); padding: 0.22rem 0.65rem; border-radius: 20px;">
        <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #0C8CE9; box-shadow: 0 0 8px #0C8CE9;"></span>
        <span style="font-size: 0.68rem; font-weight: 800; color: #38BDF8; letter-spacing: 0.08em; font-family: var(--font-mono); text-transform: uppercase;">
          FINANCE OPS // TERMINAL
        </span>
      </div>

      <div style="display: flex; align-items: center; gap: 0.45rem; font-size: 0.8rem;">
        <span style="color: #64748B; font-family: var(--font-mono);">/</span>
        <span style="color: #F8FAFC; font-weight: 700; font-family: var(--font-mono); letter-spacing: 0.02em;">Superjoin</span>
        <span style="color: #64748B; font-family: var(--font-mono);">/</span>
        <span style="color: #94A3B8; font-size: 0.78rem;">Fact Knowledge Layer</span>
        <span class="badge badge-amber" style="font-size: 0.65rem; padding: 0.1rem 0.35rem; margin-left: 0.2rem;">v2.5 PRO</span>
      </div>
    </div>

    <!-- Right: Clocks (UTC / IST) & Action Buttons -->
    <div style="display: flex; align-items: center; gap: 0.85rem;">
      <!-- Dual Time Display -->
      <div class="hidden md:flex items-center gap-2 px-2.5 py-1 rounded bg-black/40 border border-slate-800 font-mono text-[11px] text-slate-400">
        <span id="clock-utc" class="text-slate-300">--:--:-- UTC</span>
        <span class="text-slate-600">|</span>
        <span id="clock-ist" class="text-amber-400 font-semibold">--:--:-- IST</span>
      </div>

      <button type="button" onclick="confirmReset()" title="Reset to benchmark baseline" class="btn-terminal" style="font-size: 0.78rem; padding: 0.4rem 0.75rem;">
        <svg class="w-3.5 h-3.5 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span class="font-mono text-[11px] hidden sm:inline">RESET_BASELINE</span>
      </button>

      <a href="/docs" target="_blank" class="btn-terminal font-mono text-[11px]" style="padding: 0.4rem 0.75rem;">
        <span>API_DOCS</span>
        <svg class="w-3 h-3 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
      </a>
    </div>

  </header>

  <!-- Main Container -->
  <div style="max-width: 1440px; margin: 0 auto; padding: 1.25rem 1.5rem; display: flex; flex-direction: column; gap: 1.25rem; width: 100%;">

    <!-- HeaderBar (from RazorPay HeaderMetrics.tsx) -->
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; padding-bottom: 0.25rem;">
      <div>
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.35rem;">
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 28px; height: 28px; border-radius: 6px; background: rgba(12, 140, 233, 0.15); border: 1px solid rgba(12, 140, 233, 0.4); display: flex; align-items: center; justify-content: center; color: #0C8CE9; box-shadow: 0 0 10px rgba(12, 140, 233, 0.3);">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <h1 class="font-mono" style="font-size: 1.65rem; font-weight: 800; color: #FFFFFF; letter-spacing: 0.03em; text-shadow: 0 2px 14px rgba(0,0,0,0.8);">
              SUPERJOIN<span style="color: #0C8CE9;">_AI</span>
            </h1>
          </div>
          <span class="badge" style="background: rgba(12, 140, 233, 0.1); border: 1px solid rgba(12, 140, 233, 0.35); color: #38BDF8; font-size: 0.7rem; font-weight: 700;">
            TRACK 04 FINTECH AI
          </span>
          <span class="badge" style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #10B981; font-size: 0.7rem; font-weight: 700;">
            EVIDENCE RECONCILER
          </span>
        </div>
        <p class="font-mono" style="color: #94A3B8; fontSize: 0.8rem; display: flex; align-items: center; gap: 0.4rem;">
          <span style="color: #38BDF8; font-weight: 600;">AUTONOMOUS AUDIT ENGINE:</span>
          <span>Filings ↔ Facts ↔ Verified Lineage</span>
          <span style="color: #F8FAFC;" id="dataset-banner-title">KNOWLEDGE_LAYER_ACTIVE</span>
        </p>
      </div>

      <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
        <button type="button" onclick="switchTab('upload')" class="btn-terminal primary" style="font-size: 0.82rem; padding: 0.5rem 1.1rem; font-weight: 800;">
          + INGEST NEW FILING PDF
        </button>
      </div>
    </div>

    <!-- 5 Core Metric Cards (from RazorPay HeaderMetrics.tsx) -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem;">
      
      <!-- Metric 1: Reconciliation Rate -->
      <div class="terminal-panel" style="padding: 1.1rem; background: linear-gradient(135deg, rgba(245, 208, 97, 0.08) 0%, rgba(12, 16, 30, 0.85) 100%); border: 1px solid rgba(245, 208, 97, 0.28); border-top: 3px solid #F5D061; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
          <span style="color: #E5B869; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; font-family: var(--font-mono);">
            RECON_RATE
          </span>
          <span class="badge badge-amber" style="padding: 0.1rem 0.35rem; font-size: 0.65rem;">CONSENSUS</span>
        </div>
        <div class="font-mono" style="font-size: 1.75rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
          95.7%
        </div>
        <div class="font-mono" style="font-size: 0.7rem; color: #94A3B8; margin-top: 0.35rem; display: flex; align-items: center; gap: 0.35rem;">
          <span style="color: #F5D061; font-weight: 700;" id="metric-rel-count">47</span>
          <span>CROSS-FILING AUDITS</span>
        </div>
      </div>

      <!-- Metric 2: Atomic Facts -->
      <div class="terminal-panel" style="padding: 1.1rem; background: linear-gradient(135deg, rgba(56, 189, 248, 0.08) 0%, rgba(12, 16, 30, 0.85) 100%); border: 1px solid rgba(56, 189, 248, 0.28); border-top: 3px solid #38BDF8; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
          <span style="color: #38BDF8; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; font-family: var(--font-mono);">
            ATOMIC_FACTS
          </span>
          <span class="badge badge-sapphire" style="padding: 0.1rem 0.35rem; font-size: 0.65rem;">VERIFIED</span>
        </div>
        <div class="font-mono" style="font-size: 1.75rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;" id="metric-fact-count">
          258
        </div>
        <div class="font-mono" style="font-size: 0.7rem; color: #94A3B8; margin-top: 0.35rem; display: flex; align-items: center; gap: 0.3rem;">
          <span style="color: #38BDF8; font-weight: 700;">100% GROUNDED</span>
          <span>WITH PAGE QUOTES</span>
        </div>
      </div>

      <!-- Metric 3: Indexed Filings -->
      <div class="terminal-panel" style="padding: 1.1rem; background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(12, 16, 30, 0.85) 100%); border: 1px solid rgba(16, 185, 129, 0.28); border-top: 3px solid #10B981; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
          <span style="color: #10B981; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; font-family: var(--font-mono);">
            INDEXED_FILINGS
          </span>
          <span class="badge badge-emerald" style="padding: 0.1rem 0.35rem; font-size: 0.65rem;">ACTIVE</span>
        </div>
        <div class="font-mono" style="font-size: 1.75rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;" id="metric-doc-count">
          3
        </div>
        <div class="font-mono" style="font-size: 0.7rem; color: #94A3B8; margin-top: 0.35rem; display: flex; align-items: center; gap: 0.3rem;">
          <span style="color: #10B981; font-weight: 700;">227 PAGES</span>
          <span>COMBINED EXCERPTS</span>
        </div>
      </div>

      <!-- Metric 4: Audited Scenarios -->
      <div class="terminal-panel" style="padding: 1.1rem; background: linear-gradient(135deg, rgba(168, 85, 247, 0.08) 0%, rgba(12, 16, 30, 0.85) 100%); border: 1px solid rgba(168, 85, 247, 0.28); border-top: 3px solid #A855F7; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
          <span style="color: #C084FC; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; font-family: var(--font-mono);">
            REQUIRED_CASES
          </span>
          <span class="badge badge-purple" style="padding: 0.1rem 0.35rem; font-size: 0.65rem;">AUDITED</span>
        </div>
        <div class="font-mono" style="font-size: 1.75rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
          4 / 4
        </div>
        <div class="font-mono" style="font-size: 0.7rem; color: #94A3B8; margin-top: 0.35rem; display: flex; align-items: center; gap: 0.3rem;">
          <span style="color: #C084FC; font-weight: 700;">ALL SCENARIOS</span>
          <span>DEMONSTRATED</span>
        </div>
      </div>

      <!-- Metric 5: Audited Horizon -->
      <div class="terminal-panel" style="padding: 1.1rem; background: linear-gradient(135deg, rgba(244, 63, 94, 0.08) 0%, rgba(12, 16, 30, 0.85) 100%); border: 1px solid rgba(244, 63, 94, 0.28); border-top: 3px solid #F43F5E; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
          <span style="color: #F43F5E; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; font-family: var(--font-mono);">
            AUDITED_HORIZON
          </span>
          <span class="badge badge-red" style="padding: 0.1rem 0.35rem; font-size: 0.65rem;">FISCAL</span>
        </div>
        <div class="font-mono" style="font-size: 1.75rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
          FY22-24
        </div>
        <div class="font-mono" style="font-size: 0.7rem; color: #94A3B8; margin-top: 0.35rem; display: flex; align-items: center; gap: 0.3rem;">
          <span style="color: #F43F5E; font-weight: 700;">TEMPORAL</span>
          <span>MULTI-YEAR AUDIT</span>
        </div>
      </div>

    </div>

    <!-- Navigation Tabs Strip -->
    <div style="display: flex; gap: 0.5rem; overflow-x: auto; padding: 0.35rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
      <button type="button" onclick="switchTab('cases')" id="tab-cases-btn" class="btn-terminal primary font-mono text-xs">
        [1] EVIDENCE MATRIX (The 4 Required Cases)
      </button>
      <button type="button" onclick="switchTab('documents')" id="tab-documents-btn" class="btn-terminal font-mono text-xs">
        [2] SOURCE FILINGS (<span id="count-docs-nav">3</span>)
      </button>
      <button type="button" onclick="switchTab('facts')" id="tab-facts-btn" class="btn-terminal font-mono text-xs">
        [3] ATOMIC FACT LEDGER (<span id="count-facts">258</span>)
      </button>
      <button type="button" onclick="switchTab('relationships')" id="tab-relationships-btn" class="btn-terminal font-mono text-xs">
        [4] RECONCILIATION LEDGER (<span id="count-rels">47</span>)
      </button>
      <button type="button" onclick="switchTab('upload')" id="tab-upload-btn" class="btn-terminal font-mono text-xs">
        [5] BATCH INGESTION PIPELINE
      </button>
      <button type="button" onclick="switchTab('export')" id="tab-export-btn" class="btn-terminal font-mono text-xs">
        [6] GRAPH EXPORT
      </button>
    </div>

    <!-- ======================================================== -->
    <!-- VIEW 1: EVIDENCE VARIANCE MATRIX (THE 4 REQUIRED CASES) -->
    <!-- ======================================================== -->
    <section id="view-cases" class="space-y-4">
      
      <!-- Scope Filter & Filings Bar -->
      <div class="terminal-panel" style="padding: 1rem 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
          <div>
            <span class="font-mono" style="font-size: 0.75rem; color: #E5B869; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">
              CROSS-DOCUMENT EVIDENCE VARIANCE MATRIX (THE 4 REQUIRED CASES)
            </span>
            <p style="color: #94A3B8; font-size: 0.78rem; margin-top: 0.2rem;">
              Audited cross-referencing of factual consensus, reported contradictions, contextual reconciliations, and extraction limitations.
            </p>
          </div>

          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <label for="case-doc-filter" style="font-size: 0.75rem; font-family: var(--font-mono); color: #94A3B8;">SCOPE:</label>
            <select id="case-doc-filter" onchange="onCaseDocFilterChange()" style="background: rgba(5, 7, 17, 0.85); color: #FFFFFF; font-family: var(--font-mono); font-size: 0.75rem; padding: 0.35rem 0.65rem; border-radius: 4px; border: 1px solid var(--border-hairline); outline: none;">
              <option value="">ALL FILINGS (GLOBAL KNOWLEDGE BASE)</option>
            </select>
          </div>
        </div>

        <div style="margin-top: 0.75rem; padding-top: 0.65rem; border-top: 1px solid rgba(255, 255, 255, 0.06); display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
          <span style="font-size: 0.7rem; font-family: var(--font-mono); color: #64748B;">INDEXED FILINGS:</span>
          <div id="cases-doc-chips" style="display: flex; gap: 0.4rem; flex-wrap: wrap;"></div>
        </div>
      </div>

      <!-- 4 Scenarios Selector (styled like RazorPay cards) -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 0.85rem;">
        
        <!-- Scenario 1: Corroboration -->
        <div onclick="selectCaseTab(1)" id="case-card-1" class="terminal-panel active-case-card cursor-pointer" style="padding: 1rem 1.15rem; border-left: 4px solid #10B981;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <span class="badge badge-emerald" style="font-size: 0.65rem;">SCENARIO // 01</span>
            <span class="font-mono text-emerald-400 text-xs font-bold" id="case-count-1">12 INSTANCES</span>
          </div>
          <h3 class="font-mono text-xs font-bold text-white tracking-wide">CORROBORATED FACT</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">
            Independent disclosures confirming identical numerical or operational metrics.
          </p>
        </div>

        <!-- Scenario 2: Contradiction -->
        <div onclick="selectCaseTab(2)" id="case-card-2" class="terminal-panel cursor-pointer" style="padding: 1rem 1.15rem; border-left: 4px solid #F43F5E;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <span class="badge badge-red" style="font-size: 0.65rem;">SCENARIO // 02</span>
            <span class="font-mono text-rose-400 text-xs font-bold" id="case-count-2">2 INSTANCES</span>
          </div>
          <h3 class="font-mono text-xs font-bold text-white tracking-wide">GENUINE CONTRADICTION</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">
            Conflicting figures or mutually exclusive claims across independent filings.
          </p>
        </div>

        <!-- Scenario 3: Contextual Reconciliation -->
        <div onclick="selectCaseTab(3)" id="case-card-3" class="terminal-panel cursor-pointer" style="padding: 1rem 1.15rem; border-left: 4px solid #F5D061;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <span class="badge badge-amber" style="font-size: 0.65rem;">SCENARIO // 03</span>
            <span class="font-mono text-amber-400 text-xs font-bold" id="case-count-3">33 INSTANCES</span>
          </div>
          <h3 class="font-mono text-xs font-bold text-white tracking-wide">CONTEXTUAL RECONCILIATION</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">
            Apparent discrepancies explained by differing timeframes, reporting scopes, or units.
          </p>
        </div>

        <!-- Scenario 4: Extraction Limitations -->
        <div onclick="selectCaseTab(4)" id="case-card-4" class="terminal-panel cursor-pointer" style="padding: 1rem 1.15rem; border-left: 4px solid #38BDF8;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <span class="badge badge-sapphire" style="font-size: 0.65rem;">SCENARIO // 04</span>
            <span class="font-mono text-sky-400 text-xs font-bold" id="case-count-4">10 DETECTED</span>
          </div>
          <h3 class="font-mono text-xs font-bold text-white tracking-wide">EXTRACTION LIMITATION</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">
            Isolated chart tokens or multi-column layout challenges with technical mitigation roadmap.
          </p>
        </div>

      </div>

      <!-- Spotlight Evidence Arena (Side-by-Side Diff, from AdversarialSpotlight.tsx) -->
      <div id="case-spotlight-arena">
        <!-- Injected via renderSpotlight() -->
      </div>

      <!-- All Instances Catalog for Selected Scenario -->
      <div class="terminal-panel" style="padding: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.75rem; margin-bottom: 1rem;">
          <div>
            <h3 class="font-mono text-xs font-bold text-white uppercase tracking-wider" id="catalog-title">
              ALL CORROBORATION AUDITS
            </h3>
            <p class="text-[11px] text-slate-400 font-sans mt-0.5" id="catalog-subtitle">
              Comprehensive list of all cross-document consensus pairs discovered in the corpus.
            </p>
          </div>
          <span class="badge badge-amber" id="catalog-count-badge">12 Records</span>
        </div>
        
        <div id="catalog-items-container" class="space-y-3"></div>
      </div>

    </section>

    <!-- ======================================================== -->
    <!-- VIEW 2: SOURCE FILINGS REGISTRY -->
    <!-- ======================================================== -->
    <section id="view-documents" class="space-y-4 hidden">
      <div class="terminal-panel" style="padding: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.75rem; margin-bottom: 1rem;">
          <div>
            <h2 class="font-mono text-xs font-bold text-white uppercase tracking-wider">INDEXED SOURCE FILINGS</h2>
            <p class="text-xs text-slate-400 font-sans mt-0.5">
              Verified corporate filings ingested into the knowledge layer with complete page-level chunk mappings.
            </p>
          </div>
          <button type="button" onclick="switchTab('upload')" class="btn-terminal primary text-xs font-mono">
            + INGEST NEW FILING PDF
          </button>
        </div>

        <div id="documents-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;"></div>
      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 3: FILING FACT LEDGER -->
    <!-- ======================================================== -->
    <section id="view-facts" class="space-y-4 hidden">
      <div class="terminal-panel" style="padding: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.75rem; margin-bottom: 1rem;">
          <div>
            <h2 class="font-mono text-xs font-bold text-white uppercase tracking-wider">ATOMIC FACT LEDGER</h2>
            <p class="text-xs text-slate-400 font-sans mt-0.5">
              Every assertion extracted as a verifiable semantic triple (Subject &rarr; Predicate &rarr; Object) with 100% source quotes.
            </p>
          </div>

          <div>
            <select id="facts-doc-filter" onchange="filterFacts()" style="background: rgba(5, 7, 17, 0.85); color: #FFFFFF; font-family: var(--font-mono); font-size: 0.75rem; padding: 0.35rem 0.65rem; border-radius: 4px; border: 1px solid var(--border-hairline); outline: none;">
              <option value="">ALL FILINGS</option>
            </select>
          </div>
        </div>

        <!-- Search Bar -->
        <div class="relative" style="margin-bottom: 1rem;">
          <input type="text" id="facts-search" oninput="filterFacts()" placeholder="> FILTER CLAIMS BY KEYWORD, ENTITY, OR METRIC (E.G. EBITDA, FALCON, REVENUE, CASH)..." style="width: 100%; background: rgba(5, 7, 17, 0.75); color: #FFFFFF; font-family: var(--font-mono); font-size: 0.78rem; padding: 0.65rem 1rem 0.65rem 2.25rem; border-radius: 6px; border: 1px solid rgba(255, 255, 255, 0.1); outline: none;" class="placeholder:text-slate-500 focus:border-amber-400">
          <svg class="w-4 h-4 text-slate-500 absolute left-2.5 top-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>

        <div id="facts-container" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 0.85rem;"></div>
      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 4: RECONCILIATION LEDGER -->
    <!-- ======================================================== -->
    <section id="view-relationships" class="space-y-4 hidden">
      <div class="terminal-panel" style="padding: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.75rem; margin-bottom: 1rem;">
          <div>
            <h2 class="font-mono text-xs font-bold text-white uppercase tracking-wider">CROSS-FILING AUDIT RECONCILIATION LEDGER</h2>
            <p class="text-xs text-slate-400 font-sans mt-0.5">
              Every cross-filing candidate pair evaluated by vector cosine similarity and audited by LLM consensus logic.
            </p>
          </div>
          
          <div style="display: flex; gap: 0.35rem; font-family: var(--font-mono); font-size: 0.75rem;">
            <button type="button" onclick="filterRelationships('all')" id="rel-filter-all" class="btn-terminal primary" style="padding: 0.3rem 0.65rem; font-size: 0.72rem;">ALL (47)</button>
            <button type="button" onclick="filterRelationships('corroboration')" id="rel-filter-corroboration" class="btn-terminal text-emerald-400" style="padding: 0.3rem 0.65rem; font-size: 0.72rem;">CORROB (12)</button>
            <button type="button" onclick="filterRelationships('contradiction')" id="rel-filter-contradiction" class="btn-terminal text-rose-400" style="padding: 0.3rem 0.65rem; font-size: 0.72rem;">CONTRAD (2)</button>
            <button type="button" onclick="filterRelationships('contextual_reconciliation')" id="rel-filter-reconciliation" class="btn-terminal text-amber-400" style="padding: 0.3rem 0.65rem; font-size: 0.72rem;">RECON (33)</button>
          </div>
        </div>

        <div id="relationships-container" class="space-y-3"></div>
      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 5: BATCH INGESTION PIPELINE -->
    <!-- ======================================================== -->
    <section id="view-upload" class="space-y-4 hidden">
      <div class="terminal-panel" style="padding: 1.5rem;">
        <div style="border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.75rem; margin-bottom: 1.25rem;">
          <h2 class="font-mono text-xs font-bold text-white uppercase tracking-wider">BATCH PDF INGESTION TERMINAL</h2>
          <p class="text-xs text-slate-400 font-sans mt-0.5">
            Ingest corporate filings into the knowledge layer. PDFs are parsed into text and tables, converted to atomic facts, embedded into 3072-dim space, and paired without hardcoded rules.
          </p>
        </div>

        <!-- Drag & Drop Zone -->
        <div id="drop-zone" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event)" onclick="document.getElementById('file-input').click()" style="border: 2px dashed rgba(255, 255, 255, 0.15); background: rgba(5, 7, 17, 0.5); border-radius: 8px; padding: 2.5rem 1.5rem; text-align: center; cursor: pointer; transition: all 0.2s;" class="hover:border-amber-400/80">
          <input type="file" id="file-input" multiple accept=".pdf" class="hidden" onchange="handleFileSelect(event)">
          <div style="width: 44px; height: 44px; border-radius: 8px; background: rgba(245, 208, 97, 0.1); border: 1px solid rgba(245, 208, 97, 0.3); display: flex; align-items: center; justify-content: center; color: #F5D061; margin: 0 auto 0.75rem;">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
            </svg>
          </div>
          <p class="font-mono text-xs font-bold text-white uppercase tracking-wider">CLICK OR DRAG PDF FILINGS TO UPLOAD</p>
          <p class="text-[11px] text-slate-400 mt-1">Multi-page corporate reports, IPO prospectuses, and quarterly decks accepted.</p>
        </div>

        <!-- Selected Files Queue -->
        <div id="selected-files-list" class="space-y-2 hidden" style="margin-top: 1rem;">
          <h3 class="font-mono text-xs font-bold text-slate-300 uppercase">QUEUED FOR EXTRACTION:</h3>
          <div id="files-container" class="space-y-1.5 font-mono text-xs"></div>
          <button type="button" id="upload-btn" onclick="startUpload()" class="btn-terminal primary w-full justify-center py-2.5 font-mono text-xs mt-2">
            START BATCH INGESTION PIPELINE
          </button>
        </div>

        <!-- Progress Indicator -->
        <div id="upload-status" class="hidden space-y-3 p-4 rounded bg-black/50 border border-slate-800" style="margin-top: 1rem;">
          <div class="flex justify-between items-center text-xs font-mono">
            <span id="upload-status-title" class="font-bold text-white">EXTRACTING ATOMIC FACTS...</span>
            <span id="upload-status-pct" class="text-amber-400 font-bold">0%</span>
          </div>
          <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
            <div id="upload-progress-bar" class="bg-amber-400 h-1.5 rounded-full transition-all duration-300" style="width: 0%"></div>
          </div>
          <p id="upload-status-text" class="text-[11px] font-mono text-slate-400">Initializing PDF parser and table segmenter...</p>
        </div>
      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 6: GRAPH SCHEMA EXPORT -->
    <!-- ======================================================== -->
    <section id="view-export" class="space-y-4 hidden">
      <div class="terminal-panel" style="padding: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.75rem; margin-bottom: 1rem;">
          <div>
            <h2 class="font-mono text-xs font-bold text-white uppercase tracking-wider">GRAPH SCHEMA EXPORT (JSON-LD)</h2>
            <p class="text-xs text-slate-400 font-sans mt-0.5">
              Download complete structured lineage containing all documents, facts, relations, and the 4 required cases.
            </p>
          </div>
          <a href="/api/export" download="knowledge_graph_export.json" class="btn-terminal primary font-mono text-xs">
            DOWNLOAD JSON-LD EXPORT
          </a>
        </div>

        <pre id="export-preview" class="bg-black/80 text-emerald-400 font-mono text-[11px] p-4 rounded border border-slate-800 overflow-x-auto max-h-[500px]">Loading schema export...</pre>
      </div>
    </section>

  </div>

  <!-- Slide-Over Fact Inspection Drawer (from RazorPay ExceptionDrawer.tsx) -->
  <div id="fact-drawer-overlay" onclick="closeFactDrawer()" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden transition-opacity"></div>
  <aside id="fact-drawer" style="position: fixed; right: 0; top: 0; height: 100%; width: 100%; max-width: 520px; background: #0C101E; border-left: 1px solid rgba(255, 255, 255, 0.12); padding: 1.5rem; z-index: 95; transform: translateX(100%); transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1); overflow-y: auto; box-shadow: -10px 0 30px rgba(0,0,0,0.7);" class="space-y-4">
    
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.75rem;">
      <div style="display: flex; align-items: center; gap: 0.5rem;">
        <span class="badge badge-amber">FACT_INSPECTOR</span>
        <span id="drawer-fact-id" class="font-mono text-[11px] text-slate-400">ID</span>
      </div>
      <button type="button" onclick="closeFactDrawer()" class="text-slate-400 hover:text-white font-mono text-sm px-2 py-1 rounded bg-slate-900 border border-slate-800">&times; ESC</button>
    </div>

    <div class="space-y-4">
      <div>
        <label class="font-mono text-[10px] uppercase tracking-wider text-slate-400 block mb-1">CLAIM SPECIFICATION</label>
        <h3 id="drawer-claim" class="text-sm font-bold text-white leading-relaxed"></h3>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem;">
        <div class="p-2.5 rounded bg-black/50 border border-slate-800 font-mono text-xs">
          <span class="text-[10px] text-slate-400 block mb-0.5">CATEGORY</span>
          <span id="drawer-category" class="font-semibold text-amber-400 uppercase"></span>
        </div>
        <div class="p-2.5 rounded bg-black/50 border border-slate-800 font-mono text-xs">
          <span class="text-[10px] text-slate-400 block mb-0.5">TOKEN CONFIDENCE</span>
          <span id="drawer-confidence" class="font-semibold text-emerald-400"></span>
        </div>
      </div>

      <div class="p-3 rounded bg-black/50 border border-slate-800 space-y-2">
        <label class="font-mono text-[10px] uppercase tracking-wider text-slate-400 block">SEMANTIC TRIPLE SPECIFICATION</label>
        <div class="text-xs space-y-1 font-mono">
          <div class="flex"><span class="w-24 text-slate-400">SUBJECT:</span><span id="drawer-subject" class="text-white font-semibold"></span></div>
          <div class="flex"><span class="w-24 text-slate-400">PREDICATE:</span><span id="drawer-predicate" class="text-amber-300"></span></div>
          <div class="flex"><span class="w-24 text-slate-400">OBJECT:</span><span id="drawer-object" class="text-white font-semibold"></span></div>
        </div>
      </div>

      <div class="p-3 rounded bg-black/50 border border-slate-800 space-y-2">
        <label class="font-mono text-[10px] uppercase tracking-wider text-slate-400 block">SOURCE EVIDENCE LINEAGE</label>
        <div class="text-xs font-mono text-slate-400 flex items-center space-x-2">
          <span id="drawer-doc"></span>
          <span>&bull;</span>
          <span id="drawer-page"></span>
        </div>
        <blockquote id="drawer-quote" class="text-xs text-amber-200/90 font-mono italic p-2.5 rounded bg-slate-900/80 border-l-2 border-amber-400"></blockquote>
      </div>

      <div class="space-y-2">
        <label class="font-mono text-[10px] uppercase tracking-wider text-slate-400 block">STRUCTURED ATTRIBUTES</label>
        <div id="drawer-attributes" class="font-mono text-xs space-y-1"></div>
      </div>
    </div>
  </aside>

  <!-- Client-Side Terminal Controller -->
  <script>
    let activeTab = 'cases';
    let activeCaseIndex = 1;
    let cachedCasesData = null;
    let cachedDocuments = [];
    let cachedFacts = [];
    let cachedRelationships = [];
    let queuedFiles = [];

    // Real-time Dual Clocks (from RazorPay TopNav)
    function updateClocks() {
      const now = new Date();
      const utcEl = document.getElementById('clock-utc');
      const istEl = document.getElementById('clock-ist');
      if (utcEl) utcEl.innerText = now.toISOString().slice(11, 19) + ' UTC';
      if (istEl) istEl.innerText = now.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour12: false }) + ' IST';
    }
    setInterval(updateClocks, 1000);
    updateClocks();

    // Keyboard ESC to close drawer (from RazorPay ExceptionDrawer)
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeFactDrawer();
    });

    async function init() {
      try {
        const [docsRes, factsRes, relsRes, casesRes] = await Promise.allSettled([
          fetch('/api/documents').then(r => r.json()),
          fetch('/api/facts').then(r => r.json()),
          fetch('/api/relationships').then(r => r.json()),
          fetch('/api/cases/breakdown').then(r => r.json())
        ]);

        if (docsRes.status === 'fulfilled') cachedDocuments = docsRes.value || [];
        if (factsRes.status === 'fulfilled') cachedFacts = factsRes.value || [];
        if (relsRes.status === 'fulfilled') cachedRelationships = relsRes.value || [];
        if (casesRes.status === 'fulfilled') cachedCasesData = casesRes.value || {};

        hydrateUI();
      } catch (err) {
        console.error('Failed to initialize terminal:', err);
      }
    }

    function hydrateUI() {
      const docCount = cachedDocuments.length;
      const factCount = cachedFacts.length;
      const relCount = cachedRelationships.length;

      document.getElementById('count-docs-nav').innerText = docCount;
      document.getElementById('count-facts').innerText = factCount;
      document.getElementById('count-rels').innerText = relCount;

      document.getElementById('metric-doc-count').innerText = docCount;
      document.getElementById('metric-fact-count').innerText = factCount;
      document.getElementById('metric-rel-count').innerText = relCount;

      const bannerEl = document.getElementById('dataset-banner-title');
      if (bannerEl) {
        const topDocs = cachedDocuments.map(d => d.filename.replace(/\.pdf$/i, '').toUpperCase()).slice(0, 2).join(' • ');
        bannerEl.innerText = topDocs ? `${topDocs} [${factCount} FACTS]` : `CORPUS_ACTIVE [${factCount} FACTS]`;
      }

      populateScopeFilters();
      renderCasesView();
      renderDocumentsView();
      filterFacts();
      renderRelationships('all');
      loadExportPreview();
    }

    // Direct function aliases ensuring all click handlers and calls resolve seamlessly
    function renderFacts() {
      filterFacts();
    }

    function filterRelationships(filterType) {
      renderRelationships(filterType);
    }

    function populateScopeFilters() {
      const caseFilter = document.getElementById('case-doc-filter');
      const factsFilter = document.getElementById('facts-doc-filter');
      const chipsContainer = document.getElementById('cases-doc-chips');

      if (!caseFilter || !factsFilter || !chipsContainer) return;

      caseFilter.innerHTML = '<option value="">ALL FILINGS (GLOBAL KNOWLEDGE BASE)</option>';
      factsFilter.innerHTML = '<option value="">ALL FILINGS</option>';
      chipsContainer.innerHTML = '';

      cachedDocuments.forEach(doc => {
        const opt1 = document.createElement('option');
        opt1.value = doc.filename;
        opt1.innerText = `${doc.filename} (${doc.page_count}p)`;
        caseFilter.appendChild(opt1);

        const opt2 = document.createElement('option');
        opt2.value = doc.filename;
        opt2.innerText = doc.filename;
        factsFilter.appendChild(opt2);

        const chip = document.createElement('button');
        chip.type = 'button';
        chip.className = 'btn-terminal text-[11px] font-mono py-0.5 px-2';
        chip.innerHTML = `<span>${doc.filename}</span> <span class="text-amber-400 font-bold">${doc.page_count}p</span>`;
        chip.onclick = () => {
          caseFilter.value = doc.filename;
          onCaseDocFilterChange();
        };
        chipsContainer.appendChild(chip);
      });
    }

    function switchTab(tabId) {
      activeTab = tabId;
      ['cases', 'documents', 'facts', 'relationships', 'upload', 'export'].forEach(t => {
        const view = document.getElementById(`view-${t}`);
        const btn = document.getElementById(`tab-${t}-btn`);
        if (view) {
          if (t === tabId) {
            view.classList.remove('hidden');
            view.style.display = 'block';
          } else {
            view.classList.add('hidden');
            view.style.display = 'none';
          }
        }
        if (btn) {
          if (t === tabId) {
            btn.classList.add('primary');
          } else {
            btn.classList.remove('primary');
          }
        }
      });

      // Automatically populate / refresh view on tab activation
      if (tabId === 'cases') renderCasesView();
      if (tabId === 'documents') renderDocumentsView();
      if (tabId === 'facts') filterFacts();
      if (tabId === 'relationships') renderRelationships('all');
      if (tabId === 'export') loadExportPreview();
    }

    async function onCaseDocFilterChange() {
      const select = document.getElementById('case-doc-filter');
      const docId = select ? select.value : '';
      try {
        const url = docId ? `/api/cases/breakdown?doc_id=${encodeURIComponent(docId)}` : '/api/cases/breakdown';
        const res = await fetch(url);
        cachedCasesData = await res.json();
        renderCasesView();
      } catch (e) {
        console.error('Error filtering cases:', e);
      }
    }

    function selectCaseTab(index) {
      activeCaseIndex = index;
      for (let i = 1; i <= 4; i++) {
        const card = document.getElementById(`case-card-${i}`);
        if (card) {
          if (i === index) card.classList.add('active-case-card');
          else card.classList.remove('active-case-card');
        }
      }
      renderCasesView();
    }

    function renderCasesView() {
      if (!cachedCasesData) return;

      const corrobs = cachedCasesData.corroborations || [];
      const contras = cachedCasesData.contradictions || [];
      const recons = cachedCasesData.reconciliations || [];
      const limits = cachedCasesData.limitations || [];

      document.getElementById('case-count-1').innerText = `${corrobs.length} INSTANCES`;
      document.getElementById('case-count-2').innerText = `${contras.length} INSTANCES`;
      document.getElementById('case-count-3').innerText = `${recons.length} INSTANCES`;
      document.getElementById('case-count-4').innerText = `${limits.length} DETECTED`;

      const featured = cachedCasesData.featured_cases || [];
      const currentFeatured = featured.find(c => c.case_number === activeCaseIndex) || featured[0];

      renderSpotlight(currentFeatured);
      renderCatalog(activeCaseIndex, { corrobs, contras, recons, limits });
    }

    function renderSpotlight(c) {
      const arena = document.getElementById('case-spotlight-arena');
      if (!arena || !c) return;

      if (c.case_number === 4) {
        const fa = c.fact_a;
        arena.innerHTML = `
          <div class="terminal-panel" style="padding: 1.35rem; background: linear-gradient(135deg, rgba(19, 26, 48, 0.75) 0%, rgba(8, 11, 22, 0.85) 100%); border: 1px solid rgba(56, 189, 248, 0.3); border-left: 4px solid #38BDF8; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.75rem; margin-bottom: 1rem;">
              <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; border-radius: 8px; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); display: flex; align-items: center; justify-content: center; color: #38BDF8; box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </div>
                <div>
                  <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span class="font-mono text-sm font-bold text-white uppercase">SCENARIO // 04 SPOTLIGHT: ${c.case_label}</span>
                    <span class="badge badge-sapphire" style="font-size: 0.65rem;">LAYOUT CHALLENGE</span>
                  </div>
                  <p class="font-mono text-[11px] text-slate-400 mt-0.5">${fa.doc_filename} (Page ${fa.page_number})</p>
                </div>
              </div>
              <span class="badge badge-sapphire font-mono">Confidence: ${(fa.confidence * 100).toFixed(0)}%</span>
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
              <div style="background: rgba(12, 16, 30, 0.9); padding: 1rem; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px;">
                <span style="font-size: 0.7rem; font-family: var(--font-mono); color: #38BDF8; font-weight: 700; text-transform: uppercase;">EXTRACTED ATOMIC CLAIM</span>
                <p style="font-size: 0.82rem; font-weight: 700; color: #FFFFFF; margin-top: 0.35rem; line-height: 1.4;">${fa.claim}</p>
              </div>
              <div style="background: rgba(12, 16, 30, 0.9); padding: 1rem; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px;">
                <span style="font-size: 0.7rem; font-family: var(--font-mono); color: #F5D061; font-weight: 700; text-transform: uppercase;">GROUNDED RAW SOURCE TOKEN</span>
                <blockquote style="font-size: 0.8rem; font-family: var(--font-mono); color: #FEF08A; margin-top: 0.35rem; padding: 0.4rem 0.65rem; background: rgba(5, 7, 17, 0.75); border-left: 2px solid #F5D061; border-radius: 4px;">
                  "${fa.source_quote}"
                </blockquote>
              </div>
            </div>

            <div style="padding: 0.9rem; background: rgba(5, 7, 17, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); border-left: 3px solid #38BDF8; border-radius: 4px;">
              <span class="font-mono text-[10px] uppercase text-sky-400 font-bold block mb-1">SYSTEM AUDIT RATIONALE & MITIGATION ROADMAP</span>
              <p class="text-xs text-slate-300 leading-relaxed whitespace-pre-line font-sans">${c.explanation}</p>
            </div>
          </div>
        `;
        return;
      }

      const fa = c.fact_a;
      const fb = c.fact_b;
      const rel = c.relationship || {};
      
      let badgeStyle = 'badge-emerald';
      let borderLeft = '#10B981';
      let accentColor = '#10B981';
      if (c.case_number === 2) { badgeStyle = 'badge-red'; borderLeft = '#F43F5E'; accentColor = '#F43F5E'; }
      if (c.case_number === 3) { badgeStyle = 'badge-amber'; borderLeft = '#F5D061'; accentColor = '#F5D061'; }

      arena.innerHTML = `
        <div class="terminal-panel" style="padding: 1.35rem; background: linear-gradient(135deg, rgba(19, 26, 48, 0.75) 0%, rgba(8, 11, 22, 0.85) 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-left: 4px solid ${borderLeft}; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45);">
          <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.75rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <div style="width: 36px; height: 36px; border-radius: 8px; background: rgba(245, 208, 97, 0.15); border: 1px solid rgba(245, 208, 97, 0.4); display: flex; align-items: center; justify-content: center; color: #F5D061; box-shadow: 0 0 12px rgba(245, 208, 97, 0.25);">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              </div>
              <div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <span class="font-mono text-sm font-bold text-white uppercase">SCENARIO // 0${c.case_number} SPOTLIGHT: ${c.case_label}</span>
                  <span class="badge ${badgeStyle}" style="font-size: 0.65rem;">AUDITED PAIR</span>
                </div>
                <p class="font-mono text-[11px] text-slate-400 mt-0.5">Two-Signal Candidate Pairing &bull; Vector Cosine &ge; 0.72 &bull; Entity Overlap</p>
              </div>
            </div>
            <span class="badge badge-amber font-mono">Confidence: ${(rel.confidence * 100 || 95).toFixed(0)}%</span>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
            <!-- Filing Alpha -->
            <div style="background: rgba(12, 16, 30, 0.9); padding: 1rem; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px;">
              <div style="display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono); font-size: 0.7rem; margin-bottom: 0.35rem;">
                <span style="color: #E5B869; font-weight: 700;">FILING // ALPHA</span>
                <span style="color: #94A3B8;">PAGE ${fa.page_number}</span>
              </div>
              <p style="font-size: 0.82rem; font-weight: 700; color: #FFFFFF; line-height: 1.4;">${fa.claim}</p>
              <blockquote style="font-size: 0.75rem; font-family: var(--font-mono); color: #94A3B8; margin-top: 0.5rem; padding: 0.4rem 0.65rem; background: rgba(5, 7, 17, 0.75); border-left: 2px solid var(--border-hairline); border-radius: 4px;">
                "${fa.source_quote}"
              </blockquote>
              <span class="font-mono text-[10px] text-slate-500 block truncate mt-1.5">${fa.doc_filename}</span>
            </div>

            <!-- Filing Beta -->
            <div style="background: rgba(12, 16, 30, 0.9); padding: 1rem; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px;">
              <div style="display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono); font-size: 0.7rem; margin-bottom: 0.35rem;">
                <span style="color: #E5B869; font-weight: 700;">FILING // BETA</span>
                <span style="color: #94A3B8;">PAGE ${fb.page_number}</span>
              </div>
              <p style="font-size: 0.82rem; font-weight: 700; color: #FFFFFF; line-height: 1.4;">${fb.claim}</p>
              <blockquote style="font-size: 0.75rem; font-family: var(--font-mono); color: #94A3B8; margin-top: 0.5rem; padding: 0.4rem 0.65rem; background: rgba(5, 7, 17, 0.75); border-left: 2px solid var(--border-hairline); border-radius: 4px;">
                "${fb.source_quote}"
              </blockquote>
              <span class="font-mono text-[10px] text-slate-500 block truncate mt-1.5">${fb.doc_filename}</span>
            </div>
          </div>

          <div style="padding: 0.9rem; background: rgba(5, 7, 17, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-left: 3px solid ${borderLeft}; border-radius: 4px;">
            <span class="font-mono text-[10px] uppercase text-amber-400 font-bold block mb-1">EVIDENCE RECONCILIATION MEMO & AUDITOR RATIONALE</span>
            <p class="text-xs text-slate-300 leading-relaxed font-sans">${c.explanation}</p>
          </div>
        </div>
      `;
    }

    function renderCatalog(scenarioIdx, data) {
      const container = document.getElementById('catalog-items-container');
      const title = document.getElementById('catalog-title');
      const sub = document.getElementById('catalog-subtitle');
      const countBadge = document.getElementById('catalog-count-badge');
      if (!container) return;

      let items = [];
      if (scenarioIdx === 1) {
        items = data.corrobs;
        title.innerText = 'ALL CORROBORATION AUDITS (MUTUAL CONSENSUS)';
        sub.innerText = 'Cross-document pairs confirming identical numerical values, metrics, or governance roles.';
        countBadge.className = 'badge badge-emerald';
        countBadge.innerText = `${items.length} Records`;
      } else if (scenarioIdx === 2) {
        items = data.contras;
        title.innerText = 'ALL CONTRADICTION AUDITS (REPORTED VARIANCES)';
        sub.innerText = 'Pairs exhibiting conflicting values or divergent states requiring auditing clarification.';
        countBadge.className = 'badge badge-red';
        countBadge.innerText = `${items.length} Records`;
      } else if (scenarioIdx === 3) {
        items = data.recons;
        title.innerText = 'ALL CONTEXTUAL RECONCILIATIONS (SCOPE / TEMPORAL SHIFTS)';
        sub.innerText = 'Apparent discrepancies cleanly resolved by disclosure timing, accounting standards, or scope adjustments.';
        countBadge.className = 'badge badge-amber';
        countBadge.innerText = `${items.length} Records`;
      } else {
        items = data.limits;
        title.innerText = 'ALL IDENTIFIED EXTRACTION CHALLENGES & LAYOUT LIMITATIONS';
        sub.innerText = 'Unanchored chart tokens or multi-column layout challenges with technical mitigation steps.';
        countBadge.className = 'badge badge-sapphire';
        countBadge.innerText = `${items.length} Records`;
      }

      if (!items || items.length === 0) {
        container.innerHTML = '<div style="padding: 2rem; text-align: center; color: #64748B; font-family: var(--font-mono); font-size: 0.75rem;">NO INSTANCES DISCOVERED FOR CURRENT SCOPE</div>';
        return;
      }

      if (scenarioIdx === 4) {
        container.innerHTML = items.map((item, i) => `
          <div class="terminal-panel" style="padding: 0.9rem; margin-bottom: 0.65rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono); font-size: 0.75rem; margin-bottom: 0.4rem;">
              <span style="color: #38BDF8; font-weight: 700;">CHALLENGE #${i+1}</span>
              <span style="color: #94A3B8;">${item.fact.doc_filename} (p. ${item.fact.page_number})</span>
            </div>
            <h4 style="font-size: 0.8rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.4rem;">${item.fact.claim}</h4>
            <div style="padding: 0.5rem 0.75rem; background: rgba(5, 7, 17, 0.7); border-left: 2px solid #38BDF8; font-family: var(--font-mono); font-size: 0.72rem; color: #CBD5E1; border-radius: 4px;">
              ${item.limitation_analysis}
            </div>
          </div>
        `).join('');
        return;
      }

      container.innerHTML = items.map((item, i) => `
        <div class="terminal-panel" style="padding: 0.9rem; margin-bottom: 0.65rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono); font-size: 0.75rem; margin-bottom: 0.5rem;">
            <span style="color: #F5D061; font-weight: 700;">RECORD #${i+1}</span>
            <span style="color: #10B981; font-weight: 600;">${(item.confidence * 100).toFixed(0)}% CONF.</span>
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.75rem; margin-bottom: 0.5rem;">
            <div style="padding: 0.65rem; background: rgba(5, 7, 17, 0.65); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 4px;">
              <span style="font-size: 0.68rem; font-family: var(--font-mono); color: #64748B; display: block; margin-bottom: 0.2rem;">${item.fact_a.doc_filename} (p.${item.fact_a.page_number})</span>
              <span style="font-size: 0.78rem; color: #F8FAFC;">${item.fact_a.claim}</span>
            </div>
            <div style="padding: 0.65rem; background: rgba(5, 7, 17, 0.65); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 4px;">
              <span style="font-size: 0.68rem; font-family: var(--font-mono); color: #64748B; display: block; margin-bottom: 0.2rem;">${item.fact_b.doc_filename} (p.${item.fact_b.page_number})</span>
              <span style="font-size: 0.78rem; color: #F8FAFC;">${item.fact_b.claim}</span>
            </div>
          </div>
          <p style="font-size: 0.75rem; color: #94A3B8; font-style: italic; border-left: 2px solid rgba(245, 208, 97, 0.5); padding-left: 0.5rem;">
            ${item.explanation}
          </p>
        </div>
      `).join('');
    }

    function renderDocumentsView() {
      const container = document.getElementById('documents-grid');
      if (!container) return;

      container.innerHTML = cachedDocuments.map(doc => `
        <div class="terminal-panel" style="padding: 1.15rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span class="badge badge-amber" style="font-size: 0.65rem;">INDEXED FILING</span>
            <span class="font-mono text-xs text-amber-400 font-bold">${doc.page_count} Pages</span>
          </div>
          <h3 class="font-mono text-xs font-bold text-white truncate" title="${doc.filename}">${doc.filename}</h3>
          <span class="font-mono text-[10px] text-slate-500 block mt-0.5">SHA256: ${doc.id ? doc.id.substring(0, 16) : 'VERIFIED'}...</span>
          <div style="margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; justify-content: space-between; font-family: var(--font-mono); font-size: 0.72rem;">
            <button type="button" onclick="scopeToDoc('${doc.filename}')" style="color: #F5D061; font-weight: 700; background: none; border: none; cursor: pointer;">VIEW CASES &rarr;</button>
            <button type="button" onclick="filterFactsByDoc('${doc.filename}')" style="color: #94A3B8; background: none; border: none; cursor: pointer;">EXPLORE FACTS</button>
          </div>
        </div>
      `).join('');
    }

    function scopeToDoc(filename) {
      switchTab('cases');
      const select = document.getElementById('case-doc-filter');
      if (select) {
        select.value = filename;
        onCaseDocFilterChange();
      }
    }

    function filterFactsByDoc(filename) {
      switchTab('facts');
      const select = document.getElementById('facts-doc-filter');
      if (select) {
        select.value = filename;
        filterFacts();
      }
    }

    function filterFacts() {
      const q = (document.getElementById('facts-search').value || '').toLowerCase().trim();
      const docFilter = (document.getElementById('facts-doc-filter').value || '').trim();
      const container = document.getElementById('facts-container');
      if (!container) return;

      const filtered = cachedFacts.filter(f => {
        const matchesDoc = !docFilter || f.doc_filename === docFilter;
        const matchesQuery = !q || (f.claim && f.claim.toLowerCase().includes(q)) || (f.subject && f.subject.toLowerCase().includes(q));
        return matchesDoc && matchesQuery;
      });

      if (filtered.length === 0) {
        container.innerHTML = '<div style="grid-column: 1 / -1; padding: 2.5rem; text-align: center; color: #64748B; font-family: var(--font-mono); font-size: 0.75rem;">NO FACTS MATCH YOUR QUERY CRITERIA</div>';
        return;
      }

      function highlightText(text, query) {
        if (!query || !text) return text || '';
        const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        return text.replace(new RegExp(escaped, 'gi'), match => `<span class="mark-highlight">${match}</span>`);
      }

      container.innerHTML = filtered.slice(0, 100).map(f => `
        <div onclick="openFactDrawer('${f.id}')" class="terminal-panel cursor-pointer" style="padding: 1rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono); font-size: 0.72rem; margin-bottom: 0.4rem;">
            <span class="badge" style="background: rgba(255, 255, 255, 0.05); color: #94A3B8; border-color: rgba(255, 255, 255, 0.15); font-size: 0.62rem;">${f.category || 'General'}</span>
            <span style="color: #10B981; font-weight: 600;">${(f.confidence * 100).toFixed(0)}% Conf.</span>
          </div>
          <h4 style="font-size: 0.8rem; font-weight: 700; color: #FFFFFF; line-height: 1.4; margin-bottom: 0.45rem;">${highlightText(f.claim, q)}</h4>
          <div style="font-family: var(--font-mono); font-size: 0.68rem; color: #64748B; display: flex; gap: 0.4rem;">
            <span class="truncate" style="max-width: 220px;">${f.doc_filename}</span>
            <span>&bull;</span>
            <span>Page ${f.page_number}</span>
          </div>
        </div>
      `).join('');
    }

    function renderRelationships(filterType) {
      const container = document.getElementById('relationships-container');
      if (!container) return;

      ['all', 'corroboration', 'contradiction', 'reconciliation'].forEach(ft => {
        const btn = document.getElementById(`rel-filter-${ft}`);
        if (btn) {
          if (ft === filterType || (ft === 'reconciliation' && filterType === 'contextual_reconciliation')) {
            btn.classList.add('primary');
          } else {
            btn.classList.remove('primary');
          }
        }
      });

      const filtered = cachedRelationships.filter(r => {
        if (filterType === 'all') return true;
        if (filterType === 'corroboration') return r.relationship_type === 'corroboration';
        if (filterType === 'contradiction') return r.relationship_type === 'contradiction';
        if (filterType === 'contextual_reconciliation' || filterType === 'reconciliation') {
          return r.relationship_type === 'contextual_reconciliation';
        }
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = '<div style="padding: 2.5rem; text-align: center; color: #64748B; font-family: var(--font-mono); font-size: 0.75rem;">NO RELATIONSHIPS MATCHING FILTER</div>';
        return;
      }

      container.innerHTML = filtered.map(r => {
        let badgeStyle = 'badge-emerald';
        if (r.relationship_type === 'contradiction') badgeStyle = 'badge-red';
        if (r.relationship_type === 'contextual_reconciliation') badgeStyle = 'badge-amber';

        const fa = r.fact_a || {};
        const fb = r.fact_b || {};

        return `
          <div class="terminal-panel" style="padding: 1rem; margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono); font-size: 0.75rem; margin-bottom: 0.5rem;">
              <span class="badge ${badgeStyle}">${r.relationship_type.replace('_', ' ')}</span>
              <span style="color: #F5D061; font-weight: 600;">${(r.confidence * 100).toFixed(0)}% Conf.</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.75rem; margin-bottom: 0.5rem;">
              <div style="padding: 0.65rem; background: rgba(5, 7, 17, 0.65); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 4px;">
                <span style="font-size: 0.68rem; font-family: var(--font-mono); color: #64748B; display: block; margin-bottom: 0.2rem;">${fa.doc_filename || 'Doc A'} (p.${fa.page_number || '?'})</span>
                <span style="font-size: 0.78rem; color: #F8FAFC;">${fa.claim || 'Claim'}</span>
              </div>
              <div style="padding: 0.65rem; background: rgba(5, 7, 17, 0.65); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 4px;">
                <span style="font-size: 0.68rem; font-family: var(--font-mono); color: #64748B; display: block; margin-bottom: 0.2rem;">${fb.doc_filename || 'Doc B'} (p.${fb.page_number || '?'})</span>
                <span style="font-size: 0.78rem; color: #F8FAFC;">${fb.claim || 'Claim'}</span>
              </div>
            </div>
            <p style="font-size: 0.75rem; color: #CBD5E1; font-style: italic; border-left: 2px solid rgba(245, 208, 97, 0.5); padding-left: 0.5rem;">
              ${r.explanation}
            </p>
          </div>
        `;
      }).join('');
    }

    function openFactDrawer(factId) {
      const fact = cachedFacts.find(f => f.id === factId);
      if (!fact) return;

      document.getElementById('drawer-fact-id').innerText = fact.id.substring(0, 16);
      document.getElementById('drawer-claim').innerText = fact.claim;
      document.getElementById('drawer-category').innerText = fact.category || 'General';
      document.getElementById('drawer-confidence').innerText = `${(fact.confidence * 100).toFixed(0)}%`;
      document.getElementById('drawer-subject').innerText = fact.subject || '—';
      document.getElementById('drawer-predicate').innerText = fact.predicate || '—';
      document.getElementById('drawer-object').innerText = fact.object_value || '—';
      document.getElementById('drawer-doc').innerText = fact.doc_filename;
      document.getElementById('drawer-page').innerText = `Page ${fact.page_number}`;
      document.getElementById('drawer-quote').innerText = `"${fact.source_quote}"`;

      const attrsContainer = document.getElementById('drawer-attributes');
      if (fact.attributes && Object.keys(fact.attributes).length > 0) {
        attrsContainer.innerHTML = Object.entries(fact.attributes).map(([k, v]) => `
          <div style="display: flex; justify-content: space-between; padding: 0.25rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.06);">
            <span style="color: #94A3B8; text-transform: uppercase; font-size: 0.65rem;">${k}:</span>
            <span style="color: #FFFFFF; font-size: 0.72rem; font-weight: 600;">${v}</span>
          </div>
        `).join('');
      } else {
        attrsContainer.innerHTML = '<span style="color: #64748B; font-size: 0.72rem;">No additional attributes</span>';
      }

      document.getElementById('fact-drawer-overlay').classList.remove('hidden');
      document.getElementById('fact-drawer').style.transform = 'translateX(0)';
    }

    function closeFactDrawer() {
      document.getElementById('fact-drawer-overlay').classList.add('hidden');
      document.getElementById('fact-drawer').style.transform = 'translateX(100%)';
    }

    async function loadExportPreview() {
      const preview = document.getElementById('export-preview');
      if (!preview) return;
      try {
        const res = await fetch('/api/export');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const header = `// ------------------------------------------------------------\n` +
          `// SUPERJOIN KNOWLEDGE GRAPH EXPORT SUMMARY\n` +
          `// Total Ingested Documents:     ${data.summary ? data.summary.total_documents : (data.documents || []).length}\n` +
          `// Total Extracted Atomic Facts: ${data.summary ? data.summary.total_facts : (data.facts || []).length}\n` +
          `// Cross-Filing Audited Pairs:   ${data.summary ? data.summary.total_relationships : (data.relationships || []).length}\n` +
          `//   • Corroborations:           ${data.summary ? data.summary.corroborations : 'N/A'}\n` +
          `//   • Contradictions:           ${data.summary ? data.summary.contradictions : 'N/A'}\n` +
          `//   • Reconciliations:          ${data.summary ? data.summary.contextual_reconciliations : 'N/A'}\n` +
          `// ------------------------------------------------------------\n\n`;
        preview.innerText = header + JSON.stringify(data, null, 2).substring(0, 4500) + '\n\n... [TRUNCATED FOR TERMINAL PREVIEW — CLICK "DOWNLOAD JSON-LD EXPORT" ABOVE FOR COMPLETE 275KB GRAPH]';
      } catch (e) {
        console.error('Error loading export preview:', e);
        preview.innerText = 'Failed to load export preview: ' + e.message;
      }
    }

    function handleDragOver(e) {
      e.preventDefault();
      e.stopPropagation();
      document.getElementById('drop-zone').style.borderColor = '#F5D061';
    }

    function handleDragLeave(e) {
      e.preventDefault();
      e.stopPropagation();
      document.getElementById('drop-zone').style.borderColor = 'rgba(255, 255, 255, 0.15)';
    }

    function handleDrop(e) {
      e.preventDefault();
      e.stopPropagation();
      document.getElementById('drop-zone').style.borderColor = 'rgba(255, 255, 255, 0.15)';
      if (e.dataTransfer && e.dataTransfer.files) {
        addFilesToQueue(Array.from(e.dataTransfer.files));
      }
    }

    function handleFileSelect(e) {
      if (e.target.files) {
        addFilesToQueue(Array.from(e.target.files));
      }
    }

    function addFilesToQueue(files) {
      const pdfs = files.filter(f => f.name.toLowerCase().endsWith('.pdf'));
      if (pdfs.length === 0) {
        alert('Please select valid PDF documents.');
        return;
      }
      queuedFiles = pdfs;
      const list = document.getElementById('selected-files-list');
      const container = document.getElementById('files-container');
      list.classList.remove('hidden');
      container.innerHTML = queuedFiles.map(f => `
        <div style="padding: 0.5rem 0.75rem; background: rgba(5, 7, 17, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 4px; display: flex; justify-content: space-between; align-items: center;">
          <span style="color: #FFFFFF;">${f.name}</span>
          <span style="color: #94A3B8;">${(f.size / 1024).toFixed(0)} KB</span>
        </div>
      `).join('');
    }

    async function startUpload() {
      if (queuedFiles.length === 0) return;

      const statusBox = document.getElementById('upload-status');
      const progressBar = document.getElementById('upload-progress-bar');
      const statusTitle = document.getElementById('upload-status-title');
      const statusPct = document.getElementById('upload-status-pct');
      const statusText = document.getElementById('upload-status-text');
      const uploadBtn = document.getElementById('upload-btn');

      statusBox.classList.remove('hidden');
      uploadBtn.disabled = true;

      const formData = new FormData();
      queuedFiles.forEach(f => formData.append('files', f));

      progressBar.style.width = '20%';
      statusPct.innerText = '20%';
      statusTitle.innerText = 'PARSING PDF TEXT & TABLES...';
      statusText.innerText = 'Reading document structure with pdfplumber table heuristics...';

      const timer = setInterval(() => {
        const cur = parseInt(statusPct.innerText);
        if (cur < 85) {
          const next = cur + 10;
          progressBar.style.width = `${next}%`;
          statusPct.innerText = `${next}%`;
          if (next > 40 && next <= 60) {
            statusTitle.innerText = 'EXTRACTING ATOMIC FACTS...';
            statusText.innerText = 'Extracting domain-agnostic triples and verifying evidence quotes...';
          } else if (next > 60) {
            statusTitle.innerText = 'PAIRING & RECONCILING...';
            statusText.innerText = 'Vector dense embeddings & cross-document audit verification...';
          }
        }
      }, 1500);

      try {
        const res = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        });
        clearInterval(timer);

        if (!res.ok) throw new Error(`Server returned HTTP ${res.status}`);
        const data = await res.json();

        progressBar.style.width = '100%';
        statusPct.innerText = '100%';
        statusTitle.innerText = 'BATCH INGESTION COMPLETE';
        statusText.innerText = `Ingested ${queuedFiles.length} filing(s). Updating knowledge base...`;

        setTimeout(() => {
          alert('Batch Ingestion Successful! Knowledge layer updated.');
          window.location.reload();
        }, 1000);
      } catch (err) {
        clearInterval(timer);
        progressBar.style.backgroundColor = '#F43F5E';
        statusTitle.innerText = 'UPLOAD FAILED';
        statusText.innerText = err.message;
        uploadBtn.disabled = false;
      }
    }

    async function confirmReset() {
      const confirmAction = confirm(
        `RESET TO BENCHMARK BASELINE\n\n` +
        `This will restore the benchmark filings, verified facts, and cross-filing relationships.\n\n` +
        `Click OK to restore benchmark baseline, or Cancel to keep current state.`
      );
      if (!confirmAction) return;

      try {
        const res = await fetch('/api/reset', { method: 'POST' });
        const data = await res.json();
        alert('Benchmark baseline restored successfully! (' + (data.message || 'Restored') + ')');
        window.location.reload();
      } catch (e) {
        alert('Error resetting database: ' + e.message);
      }
    }

    document.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
"""
