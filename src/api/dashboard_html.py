def get_dashboard_html() -> str:
    """Returns the standalone HTML/JS dashboard interface with modern enterprise styling."""
    return r"""<!DOCTYPE html>
<html lang="en" class="h-full bg-[#080c14]">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Superjoin | Cross-Filing Fact Reconciliation & Evidence Matrix</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            surface: {
              50: '#f8fafc',
              900: '#0c121e',
              950: '#070a12',
              card: '#0f172a',
              cardhover: '#131d33',
              border: '#1e293b',
              borderlight: '#334155'
            }
          }
        }
      }
    }
  </script>
  <style>
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #080c14;
      color: #f1f5f9;
    }
    .glass-panel {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(30, 41, 59, 0.8);
    }
    .glass-nav {
      background: rgba(8, 12, 20, 0.85);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(30, 41, 59, 0.7);
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #080c14;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #1e293b;
      border-radius: 9999px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
      background: #334155;
    }
    .active-case-card {
      border-color: #3b82f6 !important;
      box-shadow: 0 0 0 1px #3b82f6, 0 8px 24px -4px rgba(59, 130, 246, 0.25);
      transform: translateY(-2px);
    }
    .pill-active {
      background: #2563eb !important;
      color: #ffffff !important;
      border-color: #3b82f6 !important;
    }
    .hidden { display: none !important; }
    .mark-highlight {
      background-color: rgba(245, 158, 11, 0.25);
      color: #fef08a;
      padding: 1px 3px;
      border-radius: 3px;
    }
    .drawer-overlay {
      background: rgba(3, 7, 18, 0.75);
      backdrop-filter: blur(4px);
    }
  </style>
</head>
<body class="h-full flex flex-col antialiased selection:bg-blue-600 selection:text-white">

  <!-- Top Executive Header -->
  <header class="glass-nav sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 gap-4">
        
        <!-- Platform Branding -->
        <div class="flex items-center space-x-3.5 cursor-pointer" onclick="switchTab('cases')">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center text-white shadow-md shadow-blue-600/30 ring-1 ring-white/20">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <span class="font-extrabold text-sm tracking-tight text-white">SUPERJOIN</span>
              <span class="text-slate-600">/</span>
              <span class="text-xs font-semibold text-slate-300">Fact Knowledge Layer</span>
              <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                v2.4 Production
              </span>
            </div>
            <p class="text-[11px] text-slate-400 hidden sm:block">Automated Cross-Filing Audit, Verification & Reconciliation Engine</p>
          </div>
        </div>

        <!-- Global Action Controls -->
        <div class="flex items-center space-x-2.5">
          <div class="hidden lg:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span class="text-slate-300 font-medium">Corpus Synced</span>
            <span class="text-slate-600">|</span>
            <span class="text-slate-400 font-mono text-[11px]" id="header-stats">3 Filings &bull; 258 Facts &bull; 47 Reconciliations</span>
          </div>

          <button type="button" onclick="confirmReset()" title="Restore benchmark Delhivery filings dataset" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 hover:border-slate-700 text-xs font-semibold transition">
            <svg class="w-3.5 h-3.5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span class="hidden sm:inline">Reset Benchmark</span>
          </button>

          <a href="/docs" target="_blank" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 hover:border-slate-700 text-xs font-semibold transition">
            <span>OpenAPI Spec</span>
            <svg class="w-3 h-3 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </a>
        </div>

      </div>

      <!-- Navigation Tabs Strip -->
      <nav class="flex space-x-1 border-t border-slate-800/80 overflow-x-auto py-2 custom-scrollbar">
        <button type="button" onclick="switchTab('cases')" id="tab-cases-btn" class="nav-tab active px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 shadow-sm transition whitespace-nowrap flex items-center space-x-2">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <span>Evidence Matrix (The 4 Required Cases)</span>
        </button>

        <button type="button" onclick="switchTab('documents')" id="tab-documents-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-900 transition whitespace-nowrap flex items-center space-x-2">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
          <span>Source Filings (<span id="count-docs-nav">3</span>)</span>
        </button>

        <button type="button" onclick="switchTab('facts')" id="tab-facts-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-900 transition whitespace-nowrap flex items-center space-x-2">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>Filing Fact Ledger (<span id="count-facts">258</span>)</span>
        </button>

        <button type="button" onclick="switchTab('relationships')" id="tab-relationships-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-900 transition whitespace-nowrap flex items-center space-x-2">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
          </svg>
          <span>Reconciliation Ledger (<span id="count-rels">47</span>)</span>
        </button>

        <button type="button" onclick="switchTab('upload')" id="tab-upload-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-900 transition whitespace-nowrap flex items-center space-x-2">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          <span>Batch Ingestion Pipeline</span>
        </button>

        <button type="button" onclick="switchTab('export')" id="tab-export-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-900 transition whitespace-nowrap flex items-center space-x-2">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>Graph Schema Export</span>
        </button>
      </nav>
    </div>
  </header>

  <!-- Executive Metric Ribbon -->
  <section class="border-b border-slate-800/80 bg-slate-950/40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
      <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-3 text-xs">
        
        <div class="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center space-x-3">
          <div class="w-7 h-7 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center font-bold text-xs">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          </div>
          <div>
            <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 block">Indexed Filings</span>
            <span class="text-sm font-extrabold text-white font-mono" id="ribbon-docs">3 Documents</span>
          </div>
        </div>

        <div class="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center space-x-3">
          <div class="w-7 h-7 rounded-lg bg-cyan-500/10 text-cyan-400 flex items-center justify-center font-bold text-xs">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
          </div>
          <div>
            <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 block">Atomic Facts</span>
            <span class="text-sm font-extrabold text-white font-mono" id="ribbon-facts">258 Facts</span>
          </div>
        </div>

        <div class="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center space-x-3">
          <div class="w-7 h-7 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center font-bold text-xs">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <div>
            <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 block">Consensus Rate</span>
            <span class="text-sm font-extrabold text-emerald-400 font-mono">95.7%</span>
          </div>
        </div>

        <div class="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center space-x-3">
          <div class="w-7 h-7 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold text-xs">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
          </div>
          <div>
            <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 block">Reconciliation Links</span>
            <span class="text-sm font-extrabold text-white font-mono" id="ribbon-rels">47 Connections</span>
          </div>
        </div>

        <div class="hidden lg:flex p-2.5 rounded-xl bg-slate-900/60 border border-slate-800/80 items-center space-x-3">
          <div class="w-7 h-7 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center font-bold text-xs">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <div>
            <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 block">Audited Timeframe</span>
            <span class="text-sm font-extrabold text-white font-mono">FY22 &ndash; FY24</span>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- Main Workstation Canvas -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

    <!-- ======================================================== -->
    <!-- VIEW 1: EVIDENCE VARIANCE MATRIX (THE 4 SCENARIOS) -->
    <!-- ======================================================== -->
    <section id="view-cases" class="space-y-6">
      
      <!-- Scope Filter & Document Lineage Strip -->
      <div class="glass-panel rounded-2xl p-5 shadow-xl space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 class="text-base font-bold text-white tracking-tight flex items-center space-x-2">
              <span>Cross-Filing Evidence Variance Matrix</span>
            </h2>
            <p class="text-xs text-slate-400 mt-0.5">
              Side-by-side evidence diff arena evaluating factual consensus, reported contradictions, contextual reconciliations, and layout limitations.
            </p>
          </div>

          <div class="flex items-center space-x-3 w-full md:w-auto">
            <label for="case-doc-filter" class="text-xs font-semibold text-slate-400 whitespace-nowrap">
              Filing Scope:
            </label>
            <select id="case-doc-filter" onchange="onCaseDocFilterChange()" class="w-full md:w-80 bg-slate-950 text-white text-xs rounded-xl border border-slate-700/80 px-3.5 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none">
              <option value="">All Documents (Global Knowledge Base)</option>
            </select>
          </div>
        </div>

        <!-- Ingested Source Filings Badges -->
        <div class="pt-3 border-t border-slate-800/80">
          <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center justify-between">
            <span>Indexed Source Filings:</span>
            <button type="button" onclick="switchTab('documents')" class="text-blue-400 hover:text-blue-300 normal-case font-medium text-xs">View Document Registry &rarr;</button>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5" id="active-docs-banner">
            <!-- Populated dynamically via JS -->
          </div>
        </div>
      </div>

      <!-- The 4 Scenario Switcher Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="scenario-selector-grid">
        
        <!-- Case 1: Corroboration -->
        <div onclick="selectCaseByIndex(0)" id="case-btn-0" class="case-card active-case-card cursor-pointer bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 rounded-2xl p-4 transition-all duration-200 relative overflow-hidden group">
          <div class="flex justify-between items-start">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Scenario 1
            </span>
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 ring-4 ring-emerald-500/20"></span>
          </div>
          <h3 class="font-bold text-sm text-white mt-2.5 group-hover:text-emerald-300 transition">Corroborated Consensus</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">Independent filings confirm identical reported metrics or corporate events.</p>
          <div class="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Discovered:</span>
            <span class="font-bold text-emerald-400 font-mono" id="badge-corrobs-count">12 instances</span>
          </div>
        </div>

        <!-- Case 2: Contradiction -->
        <div onclick="selectCaseByIndex(1)" id="case-btn-1" class="case-card cursor-pointer bg-slate-900/90 border border-slate-800 hover:border-rose-500/50 rounded-2xl p-4 transition-all duration-200 relative overflow-hidden group">
          <div class="flex justify-between items-start">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider bg-rose-500/10 text-rose-400 border border-rose-500/20">
              Scenario 2
            </span>
            <span class="w-2.5 h-2.5 rounded-full bg-rose-400 ring-4 ring-rose-500/20"></span>
          </div>
          <h3 class="font-bold text-sm text-white mt-2.5 group-hover:text-rose-300 transition">Reported Variance & Conflict</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">Conflicting metrics or contradictory status assertions for matching scopes.</p>
          <div class="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Discovered:</span>
            <span class="font-bold text-rose-400 font-mono" id="badge-contras-count">2 instances</span>
          </div>
        </div>

        <!-- Case 3: Reconciliation -->
        <div onclick="selectCaseByIndex(2)" id="case-btn-2" class="case-card cursor-pointer bg-slate-900/90 border border-slate-800 hover:border-amber-500/50 rounded-2xl p-4 transition-all duration-200 relative overflow-hidden group">
          <div class="flex justify-between items-start">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider bg-amber-500/10 text-amber-400 border border-amber-500/20">
              Scenario 3
            </span>
            <span class="w-2.5 h-2.5 rounded-full bg-amber-400 ring-4 ring-amber-500/20"></span>
          </div>
          <h3 class="font-bold text-sm text-white mt-2.5 group-hover:text-amber-300 transition">Contextual Reconciliation</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">Apparent discrepancy resolved by fiscal timeframe, scope, or accounting basis.</p>
          <div class="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Discovered:</span>
            <span class="font-bold text-amber-400 font-mono" id="badge-recs-count">33 instances</span>
          </div>
        </div>

        <!-- Case 4: Limitation -->
        <div onclick="selectCaseByIndex(3)" id="case-btn-3" class="case-card cursor-pointer bg-slate-900/90 border border-slate-800 hover:border-purple-500/50 rounded-2xl p-4 transition-all duration-200 relative overflow-hidden group">
          <div class="flex justify-between items-start">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider bg-purple-500/10 text-purple-400 border border-purple-500/20">
              Scenario 4
            </span>
            <span class="w-2.5 h-2.5 rounded-full bg-purple-400 ring-4 ring-purple-500/20"></span>
          </div>
          <h3 class="font-bold text-sm text-white mt-2.5 group-hover:text-purple-300 transition">Spatial Layout Edge Case</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">Visual layout / tabular challenges & spatial coordinate engineering mitigation.</p>
          <div class="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Identified:</span>
            <span class="font-bold text-purple-400 font-mono" id="badge-limits-count">10 instances</span>
          </div>
        </div>

      </div>

      <!-- Spotlight Evidence Comparison Arena -->
      <div class="glass-panel rounded-2xl p-6 shadow-2xl space-y-6" id="spotlight-display-arena">
        <div class="p-8 text-center text-slate-500 text-xs">Loading evidence comparison arena...</div>
      </div>

      <!-- Categorized Instance Drawer (Detailed Repository) -->
      <div class="glass-panel rounded-2xl p-5 shadow-xl space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
          <div>
            <h3 class="font-bold text-sm text-white" id="category-drawer-title">All Discovered Corroborations</h3>
            <p class="text-xs text-slate-400">Full repository of verified evidence pairs discovered across filings.</p>
          </div>
          <div class="flex items-center space-x-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800">
            <button type="button" onclick="switchCategoryView('corroborations')" id="cat-btn-corroborations" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-600 text-white shadow-sm transition">Corroborations</button>
            <button type="button" onclick="switchCategoryView('contradictions')" id="cat-btn-contradictions" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition">Contradictions</button>
            <button type="button" onclick="switchCategoryView('reconciliations')" id="cat-btn-reconciliations" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition">Reconciliations</button>
            <button type="button" onclick="switchCategoryView('limitations')" id="cat-btn-limitations" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition">Limitations</button>
          </div>
        </div>

        <div class="space-y-3 max-h-96 overflow-y-auto custom-scrollbar pr-1" id="category-instances-container">
          <div class="p-4 text-center text-slate-500 text-xs">Loading instances...</div>
        </div>
      </div>

    </section>

    <!-- ======================================================== -->
    <!-- VIEW 2: SOURCE FILINGS REGISTRY -->
    <!-- ======================================================== -->
    <section id="view-documents" class="space-y-6 hidden">
      <div class="glass-panel rounded-2xl p-5 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 class="text-base font-bold text-white tracking-tight flex items-center space-x-2">
            <span>Source Documents & Ground-Truth Registry</span>
          </h2>
          <p class="text-xs text-slate-400 mt-0.5">
            Full repository of ingested filings indexed into page-level chunks with token coordinates and extracted facts.
          </p>
        </div>
        <button type="button" onclick="switchTab('upload')" class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-md shadow-blue-600/20 transition flex items-center space-x-1.5 self-start md:self-auto">
          <span>+ Ingest Additional Documents</span>
        </button>
      </div>

      <!-- Detailed Documents Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5" id="documents-showcase-grid">
        <div class="p-8 text-center text-slate-500 col-span-3 text-xs">Loading documents...</div>
      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 3: FILING FACT LEDGER (EXPLORER) -->
    <!-- ======================================================== -->
    <section id="view-facts" class="space-y-6 hidden">
      <div class="glass-panel rounded-2xl p-5 shadow-xl space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 class="text-base font-bold text-white tracking-tight">Filing Fact Ledger</h2>
            <p class="text-xs text-slate-400 mt-0.5">Atomic structured assertions extracted from source filings with verbatim grounding quotes.</p>
          </div>
          <span class="text-xs text-slate-400 font-mono" id="facts-counter-text">Showing facts...</span>
        </div>

        <!-- Filter Controls -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="md:col-span-2 relative">
            <input type="text" id="fact-search" oninput="filterFacts()" placeholder="Search claims, subjects, entities, figures, or metrics..." class="w-full bg-slate-950 text-white text-xs rounded-xl border border-slate-800 px-4 py-2.5 pl-9 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none">
            <svg class="w-4 h-4 text-slate-500 absolute left-3 top-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <div>
            <select id="doc-filter" onchange="filterFacts()" class="w-full bg-slate-950 text-white text-xs rounded-xl border border-slate-800 px-3.5 py-2.5 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none">
              <option value="all">All Documents</option>
            </select>
          </div>
        </div>

        <!-- Category Filter Pills -->
        <div class="flex flex-wrap items-center gap-1.5 pt-1 text-xs">
          <span class="text-[11px] font-bold text-slate-400 mr-1 uppercase tracking-wider">Category:</span>
          <button type="button" onclick="filterByCategory('all')" id="cat-pill-all" class="cat-pill pill-active px-3 py-1 rounded-lg font-semibold bg-blue-600 text-white border border-blue-500 transition">All</button>
          <button type="button" onclick="filterByCategory('financial')" id="cat-pill-financial" class="cat-pill px-3 py-1 rounded-lg font-semibold bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition">Financial & Metrics</button>
          <button type="button" onclick="filterByCategory('operational')" id="cat-pill-operational" class="cat-pill px-3 py-1 rounded-lg font-semibold bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition">Operational Reach</button>
          <button type="button" onclick="filterByCategory('strategic')" id="cat-pill-strategic" class="cat-pill px-3 py-1 rounded-lg font-semibold bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition">M&A & Strategic</button>
          <button type="button" onclick="filterByCategory('personnel')" id="cat-pill-personnel" class="cat-pill px-3 py-1 rounded-lg font-semibold bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition">Governance & Officers</button>
        </div>
      </div>

      <!-- Facts Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="facts-container">
        <div class="p-8 text-center text-slate-500 col-span-2 text-xs">Loading facts...</div>
      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 4: RECONCILIATION LEDGER -->
    <!-- ======================================================== -->
    <section id="view-relationships" class="space-y-6 hidden">
      <div class="glass-panel rounded-2xl p-5 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 class="text-base font-bold text-white tracking-tight">Cross-Filing Reconciliation Ledger</h2>
          <p class="text-xs text-slate-400 mt-0.5">Semantic pairings evaluated and classified across independent documents.</p>
        </div>

        <!-- Type Filter Buttons -->
        <div class="flex items-center space-x-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800">
          <button type="button" onclick="filterRelationships('all')" id="filter-rel-all" class="rel-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 text-white shadow-sm transition">All</button>
          <button type="button" onclick="filterRelationships('corroboration')" id="filter-rel-corroboration" class="rel-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition">Corroborations</button>
          <button type="button" onclick="filterRelationships('contradiction')" id="filter-rel-contradiction" class="rel-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition">Contradictions</button>
          <button type="button" onclick="filterRelationships('contextual_reconciliation')" id="filter-rel-contextual_reconciliation" class="rel-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition">Reconciliations</button>
        </div>
      </div>

      <div class="text-xs text-slate-400 font-mono" id="rel-filter-count">Showing relationships...</div>

      <div class="space-y-4" id="relationships-container">
        <div class="p-8 text-center text-slate-500 text-xs">Loading relationships...</div>
      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 5: BATCH INGESTION PIPELINE -->
    <!-- ======================================================== -->
    <section id="view-upload" class="space-y-6 hidden">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Upload Pipeline Box -->
        <div class="lg:col-span-2 glass-panel rounded-2xl p-6 shadow-xl space-y-5">
          <div>
            <h2 class="text-base font-bold text-white tracking-tight">Batch PDF Ingestion Pipeline</h2>
            <p class="text-xs text-slate-400 mt-0.5">Ingest new corporate filings, financial disclosures, or regulatory releases into the knowledge graph.</p>
          </div>

          <!-- Dropzone -->
          <form id="upload-form" onsubmit="handleBatchUpload(event)">
            <label for="pdf-file-input" class="flex flex-col items-center justify-center p-8 border-2 border-dashed border-slate-800 hover:border-blue-500 rounded-2xl cursor-pointer bg-slate-950/60 hover:bg-slate-950 transition group">
              <div class="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center group-hover:scale-110 transition duration-200 mb-3">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <p class="text-xs font-semibold text-slate-200 mb-1">Click to browse or drop PDF documents here</p>
              <p class="text-[11px] text-slate-500">Supports multi-file batch upload (.pdf)</p>
              <input type="file" id="pdf-file-input" multiple accept=".pdf" class="hidden" onchange="handleFileSelect(event)">
            </label>

            <!-- File List Chips -->
            <div id="selected-files-container" class="mt-4 hidden space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-semibold text-slate-300">Staged Documents (<span id="selected-files-count">0</span>):</span>
                <button type="button" onclick="clearSelectedFiles()" class="text-rose-400 hover:text-rose-300 text-[11px]">Clear All</button>
              </div>
              <div id="file-chips-list" class="flex flex-wrap gap-2"></div>
            </div>

            <!-- Ingest Action Button -->
            <div class="mt-5 flex justify-end">
              <button type="submit" id="upload-btn" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-md shadow-blue-600/20 transition flex items-center space-x-2">
                <span>Start Ingestion & Reconciliation</span>
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
            </div>
          </form>

          <!-- Upload Progress & Status Alert -->
          <div id="upload-status" class="hidden p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
            <div class="flex justify-between items-center text-xs">
              <span class="font-semibold text-white" id="upload-status-title">Processing Filings...</span>
              <span class="text-blue-400 font-mono" id="upload-status-pct">0%</span>
            </div>
            <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div id="upload-progress-bar" class="bg-gradient-to-r from-blue-500 to-indigo-500 h-full w-0 transition-all duration-300"></div>
            </div>
            <p class="text-[11px] text-slate-400" id="upload-status-text">Parsing layout streams, extracting facts, and reconciling pairs...</p>
          </div>
        </div>

        <!-- Ingested Documents List Sidecard -->
        <div class="glass-panel rounded-2xl p-6 shadow-xl space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-sm text-white">Indexed Documents</h3>
            <span class="text-xs text-blue-400 font-mono" id="ingested-docs-count">0 documents</span>
          </div>
          <div id="ingested-docs-list" class="space-y-2.5 max-h-96 overflow-y-auto custom-scrollbar pr-1">
            <div class="text-xs text-slate-500 italic p-3">Loading documents...</div>
          </div>
        </div>

      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 6: GRAPH SCHEMA & EXPORT -->
    <!-- ======================================================== -->
    <section id="view-export" class="space-y-6 hidden">
      <div class="glass-panel rounded-2xl p-6 shadow-xl space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 class="text-base font-bold text-white tracking-tight">Structured Knowledge Graph Export</h2>
            <p class="text-xs text-slate-400 mt-0.5">Machine-readable JSON schema containing documents, facts, and reconciliation links.</p>
          </div>
          <div class="flex items-center space-x-2">
            <button type="button" onclick="copyExportJson()" class="px-3.5 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 text-xs font-semibold transition">
              Copy JSON
            </button>
            <a href="/api/export" download="knowledge_graph_export.json" class="px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition shadow-sm">
              Download File (.json)
            </a>
          </div>
        </div>

        <!-- Metric Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Total Filings</span>
            <span class="text-xl font-extrabold text-white font-mono" id="stat-docs">3</span>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Extracted Facts</span>
            <span class="text-xl font-extrabold text-white font-mono" id="stat-facts">258</span>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Cross-Links</span>
            <span class="text-xl font-extrabold text-white font-mono" id="stat-rels">47</span>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Contradictions</span>
            <span class="text-xl font-extrabold text-rose-400 font-mono" id="stat-contras">2</span>
          </div>
        </div>

        <pre class="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-slate-300 max-h-96 overflow-y-auto custom-scrollbar" id="json-preview">Loading Knowledge Graph JSON...</pre>
      </div>
    </section>

  </main>

  <!-- Slide-Over Fact Inspection Drawer -->
  <div id="fact-drawer-backdrop" class="fixed inset-0 drawer-overlay z-50 hidden transition-opacity" onclick="closeFactDrawer()"></div>
  <aside id="fact-drawer" class="fixed inset-y-0 right-0 max-w-md w-full bg-slate-900 border-l border-slate-800 p-6 z-50 shadow-2xl transform translate-x-full transition-transform duration-300 ease-in-out flex flex-col justify-between overflow-y-auto custom-scrollbar">
    <div class="space-y-4">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <span class="text-xs font-bold text-blue-400 uppercase tracking-wider">Fact Assertion Detail</span>
        <button type="button" onclick="closeFactDrawer()" class="text-slate-400 hover:text-white p-1">&times;</button>
      </div>
      <div id="fact-drawer-content" class="space-y-4 text-xs">
        <!-- Injected dynamically -->
      </div>
    </div>
    <div class="pt-4 border-t border-slate-800 flex justify-end">
      <button type="button" onclick="closeFactDrawer()" class="px-4 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold">Close</button>
    </div>
  </aside>

  <!-- Javascript Application Controller -->
  <script>
    let rawFacts = [];
    let rawRelationships = [];
    let rawDocuments = [];
    let casesBreakdown = null;
    let selectedCaseIndex = 0;
    let currentCategoryView = 'corroborations';
    let selectedFiles = [];
    let activeFactCategory = 'all';

    async function init() {
      // Parallel fetch via Promise.allSettled for maximum resilience
      await Promise.allSettled([
        loadDocuments(),
        loadCasesBreakdown(),
        loadFacts(),
        loadRelationships(),
        loadExport()
      ]);
    }

    function switchTab(tabId) {
      const tabs = ['cases', 'documents', 'facts', 'relationships', 'upload', 'export'];
      tabs.forEach(t => {
        const view = document.getElementById(`view-${t}`);
        const btn = document.getElementById(`tab-${t}-btn`);
        if (view) {
          if (t === tabId) {
            view.style.display = 'block';
            view.classList.remove('hidden');
          } else {
            view.style.display = 'none';
            view.classList.add('hidden');
          }
        }
        if (btn) {
          if (t === tabId) {
            btn.className = 'nav-tab active px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 shadow-sm transition whitespace-nowrap flex items-center space-x-2';
          } else {
            btn.className = 'nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-900 transition whitespace-nowrap flex items-center space-x-2';
          }
        }
      });
    }

    async function loadDocuments() {
      try {
        const res = await fetch('/api/documents');
        rawDocuments = await res.json();
        
        const count = rawDocuments.length;
        const navCount = document.getElementById('count-docs-nav');
        if (navCount) navCount.innerText = count;
        
        const ribbonDocs = document.getElementById('ribbon-docs');
        if (ribbonDocs) ribbonDocs.innerText = `${count} Documents`;

        const ingCount = document.getElementById('ingested-docs-count');
        if (ingCount) ingCount.innerText = `${count} documents`;

        // Update case document filter dropdown
        const caseDocSelect = document.getElementById('case-doc-filter');
        if (caseDocSelect) {
          const prevVal = caseDocSelect.value;
          caseDocSelect.innerHTML = '<option value="">All Documents (Global Knowledge Base)</option>' +
            rawDocuments.map(d => `<option value="${d.id}">${d.filename} (${d.page_count} pgs)</option>`).join('');
          if (prevVal) caseDocSelect.value = prevVal;
        }

        // Update facts explorer document dropdown
        const docSelect = document.getElementById('doc-filter');
        if (docSelect) {
          docSelect.innerHTML = '<option value="all">All Documents</option>' +
            rawDocuments.map(d => `<option value="${d.filename}">${d.filename}</option>`).join('');
        }

        // Update active docs banner on the Overview tab
        const banner = document.getElementById('active-docs-banner');
        if (banner) {
          banner.innerHTML = rawDocuments.map(d => `
            <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 flex items-center justify-between text-xs group hover:border-slate-700 transition">
              <div class="flex items-center space-x-2.5 min-w-0">
                <div class="w-6 h-6 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center font-bold text-[10px]">
                  PDF
                </div>
                <div class="min-w-0 truncate">
                  <div class="font-bold text-slate-200 truncate text-[11px]" title="${d.filename}">${d.filename}</div>
                  <div class="text-[10px] text-slate-500">${d.page_count} Pages &bull; Indexed</div>
                </div>
              </div>
              <button type="button" onclick="inspectDocCases('${d.id}')" class="ml-2 px-2 py-1 rounded bg-slate-900 hover:bg-blue-600 text-slate-400 hover:text-white text-[10px] font-semibold border border-slate-800 transition whitespace-nowrap">Filter</button>
            </div>
          `).join('');
        }

        // Update detailed documents showcase grid
        const grid = document.getElementById('documents-showcase-grid');
        if (grid) {
          grid.innerHTML = rawDocuments.map((d, i) => `
            <div class="glass-panel rounded-2xl p-5 shadow-xl space-y-4 hover:border-slate-700 transition flex flex-col justify-between">
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-blue-500/10 text-blue-400 border border-blue-500/20">
                    Filing #${i + 1}
                  </span>
                  <span class="text-[11px] text-slate-500 font-mono">${(d.upload_time || '').split('T')[0]}</span>
                </div>
                <div>
                  <h4 class="font-bold text-sm text-white leading-snug break-words">${d.filename}</h4>
                  <p class="text-xs text-slate-400 mt-1">Ground-truth filing indexed with page-indexed text & table chunks.</p>
                </div>
                <div class="grid grid-cols-2 gap-2 pt-2 border-t border-slate-800/80 text-xs">
                  <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                    <span class="text-[10px] font-bold text-slate-500 block">Total Pages:</span>
                    <span class="text-sm font-extrabold text-white font-mono">${d.page_count}</span>
                  </div>
                  <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                    <span class="text-[10px] font-bold text-slate-500 block">Index Status:</span>
                    <span class="text-xs font-bold text-emerald-400">Verified &bull; Active</span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2 pt-3 border-t border-slate-800/80">
                <button type="button" onclick="inspectDocCases('${d.id}')" class="flex-1 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition text-center shadow-sm">
                  View Cases
                </button>
                <button type="button" onclick="inspectDocFacts('${d.filename}')" class="flex-1 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 text-xs font-semibold transition text-center">
                  View Facts
                </button>
              </div>
            </div>
          `).join('');
        }

        // Update list on upload tab
        const listDiv = document.getElementById('ingested-docs-list');
        if (listDiv) {
          if (!rawDocuments.length) {
            listDiv.innerHTML = '<div class="text-xs text-slate-500 italic p-3 rounded-lg bg-slate-950 border border-slate-800">No documents ingested. Upload filings above.</div>';
          } else {
            listDiv.innerHTML = rawDocuments.map(d => `
              <div class="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs">
                <div class="flex items-center space-x-3">
                  <span class="w-7 h-7 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center font-bold text-xs">PDF</span>
                  <div>
                    <div class="font-bold text-white">${d.filename}</div>
                    <div class="text-slate-400 text-[11px]">${d.page_count} pages &bull; Indexed in knowledge store</div>
                  </div>
                </div>
                <span class="text-[11px] text-slate-500 font-mono">${(d.upload_time || '').split('T')[0]}</span>
              </div>
            `).join('');
          }
        }
      } catch (e) {
        console.error('Failed to load documents', e);
      }
    }

    function inspectDocCases(docId) {
      const select = document.getElementById('case-doc-filter');
      if (select) {
        select.value = docId;
        onCaseDocFilterChange();
      }
      switchTab('cases');
    }

    function inspectDocFacts(filename) {
      const select = document.getElementById('doc-filter');
      if (select) {
        select.value = filename;
        filterFacts();
      }
      switchTab('facts');
    }

    async function onCaseDocFilterChange() {
      const docId = document.getElementById('case-doc-filter').value;
      await loadCasesBreakdown(docId);
    }

    async function loadCasesBreakdown(docId = null) {
      try {
        let url = '/api/cases/breakdown';
        if (docId) url += `?doc_id=${encodeURIComponent(docId)}`;
        const res = await fetch(url);
        casesBreakdown = await res.json();

        const counts = casesBreakdown.counts || {};
        const nCorrob = counts.corroborations ?? (casesBreakdown.corroborations ? casesBreakdown.corroborations.length : 0);
        const nContra = counts.contradictions ?? (casesBreakdown.contradictions ? casesBreakdown.contradictions.length : 0);
        const nRec = counts.reconciliations ?? (casesBreakdown.reconciliations ? casesBreakdown.reconciliations.length : 0);
        const nLim = counts.limitations ?? (casesBreakdown.limitations ? casesBreakdown.limitations.length : 0);

        const bCorrob = document.getElementById('badge-corrobs-count');
        if (bCorrob) bCorrob.innerText = `${nCorrob} instances`;
        const bContra = document.getElementById('badge-contras-count');
        if (bContra) bContra.innerText = `${nContra} instances`;
        const bRec = document.getElementById('badge-recs-count');
        if (bRec) bRec.innerText = `${nRec} instances`;
        const bLim = document.getElementById('badge-limits-count');
        if (bLim) bLim.innerText = `${nLim} instances`;

        renderSpotlightArena();
        renderCategoryInstances();
      } catch (e) {
        console.error('Failed to load cases breakdown', e);
      }
    }

    function selectCaseByIndex(index) {
      selectedCaseIndex = index;
      for (let i = 0; i < 4; i++) {
        const btn = document.getElementById(`case-btn-${i}`);
        if (btn) {
          if (i === index) {
            btn.classList.add('active-case-card');
          } else {
            btn.classList.remove('active-case-card');
          }
        }
      }
      renderSpotlightArena();
    }

    function renderSpotlightArena() {
      const arena = document.getElementById('spotlight-display-arena');
      if (!arena) return;

      if (!casesBreakdown || !casesBreakdown.featured_cases || casesBreakdown.featured_cases.length === 0) {
        arena.innerHTML = '<div class="p-8 text-center text-slate-500 text-xs">No cases match the selected filter.</div>';
        return;
      }

      const caseItem = casesBreakdown.featured_cases[selectedCaseIndex] || casesBreakdown.featured_cases[0];
      const fa = caseItem.fact_a;
      const fb = caseItem.fact_b;
      const rel = caseItem.relationship;

      let badgeColor = 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      let statusIcon = 'Verified Consensus';
      if (caseItem.case_label.includes('Corroborat')) {
        badgeColor = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
        statusIcon = 'Cross-Filing Consensus';
      } else if (caseItem.case_label.includes('Contradiction')) {
        badgeColor = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
        statusIcon = 'Reported Variance Conflict';
      } else if (caseItem.case_label.includes('Reconciliation')) {
        badgeColor = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
        statusIcon = 'Contextually Reconciled';
      } else if (caseItem.case_label.includes('Limitation') || caseItem.case_label.includes('Failure')) {
        badgeColor = 'bg-purple-500/10 text-purple-400 border-purple-500/30';
        statusIcon = 'Document Layout Challenge';
      }

      arena.innerHTML = `
        <!-- Top Scenario Status Bar -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
          <div class="flex items-center space-x-3">
            <span class="w-8 h-8 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-center font-extrabold text-xs text-slate-200 font-mono">0${caseItem.case_number}</span>
            <div>
              <div class="flex items-center space-x-2">
                <h3 class="font-bold text-base text-white">${caseItem.case_label}</h3>
                <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold border ${badgeColor}">
                  ${statusIcon}
                </span>
              </div>
              <p class="text-xs text-slate-400 mt-0.5">High-confidence analytical demonstration grounded in verified source filings.</p>
            </div>
          </div>
          <div class="text-xs text-slate-400 font-mono bg-slate-950 px-3.5 py-1.5 rounded-xl border border-slate-800 flex items-center space-x-2 self-start sm:self-auto">
            <span>Confidence Index:</span>
            <span class="text-emerald-400 font-bold">${rel ? (rel.confidence * 100).toFixed(0) : (fa && fa.confidence ? (fa.confidence * 100).toFixed(0) : 100)}%</span>
          </div>
        </div>

        <!-- Evidence Side-by-Side Diff Arena -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          
          <!-- Source Filing A Card -->
          <div class="bg-slate-950/80 border border-slate-800/90 rounded-2xl p-5 space-y-3 relative overflow-hidden">
            <div class="flex items-center justify-between text-xs">
              <span class="font-bold text-blue-400 uppercase tracking-wider text-[10px] flex items-center space-x-1.5">
                <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                <span>Source Filing A</span>
              </span>
              <span class="px-2.5 py-0.5 rounded-full bg-slate-900 text-slate-300 border border-slate-800 font-mono text-[11px]">
                ${fa ? fa.doc_filename : 'Document A'} &bull; Page ${fa ? fa.page_number : 'N/A'}
              </span>
            </div>

            <div class="bg-slate-900/70 p-3.5 rounded-xl border border-slate-800/80">
              <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block mb-1">Extracted Assertion:</span>
              <p class="text-sm font-semibold text-white leading-snug">${fa ? fa.claim : 'No assertion statement available.'}</p>
            </div>

            <div class="p-3.5 rounded-xl bg-slate-900/40 border border-slate-800/60 text-xs">
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                Verbatim Grounding Quote:
              </span>
              <p class="text-slate-300 italic leading-relaxed text-xs pl-2.5 border-l-2 border-blue-500/60 font-serif">
                "${fa ? fa.source_quote : ''}"
              </p>
            </div>
          </div>

          <!-- Source Filing B Card (or Spatial Challenge Explanation) -->
          ${fb ? `
          <div class="bg-slate-950/80 border border-slate-800/90 rounded-2xl p-5 space-y-3 relative overflow-hidden">
            <div class="flex items-center justify-between text-xs">
              <span class="font-bold text-indigo-400 uppercase tracking-wider text-[10px] flex items-center space-x-1.5">
                <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
                <span>Source Filing B</span>
              </span>
              <span class="px-2.5 py-0.5 rounded-full bg-slate-900 text-slate-300 border border-slate-800 font-mono text-[11px]">
                ${fb.doc_filename} &bull; Page ${fb.page_number}
              </span>
            </div>

            <div class="bg-slate-900/70 p-3.5 rounded-xl border border-slate-800/80">
              <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block mb-1">Extracted Assertion:</span>
              <p class="text-sm font-semibold text-white leading-snug">${fb.claim}</p>
            </div>

            <div class="p-3.5 rounded-xl bg-slate-900/40 border border-slate-800/60 text-xs">
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                Verbatim Grounding Quote:
              </span>
              <p class="text-slate-300 italic leading-relaxed text-xs pl-2.5 border-l-2 border-indigo-500/60 font-serif">
                "${fb.source_quote}"
              </p>
            </div>
          </div>
          ` : `
          <div class="bg-purple-950/20 border border-purple-500/30 rounded-2xl p-5 space-y-3 flex flex-col justify-center text-xs">
            <span class="font-bold text-purple-300 uppercase tracking-wider text-[10px] flex items-center space-x-1.5">
              <span class="w-2 h-2 rounded-full bg-purple-400"></span>
              <span>Spatial Bounding & Tabular Stream Challenge</span>
            </span>
            <p class="text-slate-300 text-xs leading-relaxed">
              Standard PDF parsers flatten two-dimensional matrices into continuous 1D text streams, dropping visual column boundaries. Multi-column presentation slides lose explicit spatial attachment between headers and numeric values.
            </p>
            <div class="p-3 bg-purple-900/20 border border-purple-500/20 rounded-xl text-purple-200 text-[11px]">
              <strong>Engineering Protocol:</strong> Integrate LayoutLMv3 2D spatial coordinate tracking or multimodal Vision-Language rasterization (Gemini Vision) to anchor un-nested headers directly to cell coordinates.
            </div>
          </div>
          `}

        </div>

        <!-- Analytical Resolution Memo -->
        <div class="bg-slate-950 p-4 rounded-xl border border-slate-800/90 space-y-1.5">
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-blue-400 flex items-center space-x-1.5">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>Evidence Reconciliation Memo & Auditor Rationale:</span>
          </span>
          <p class="text-xs text-slate-300 leading-relaxed font-normal">${caseItem.explanation}</p>
        </div>
      `;
    }

    function switchCategoryView(category) {
      currentCategoryView = category;
      ['corroborations', 'contradictions', 'reconciliations', 'limitations'].forEach(c => {
        const btn = document.getElementById(`cat-btn-${c}`);
        if (btn) {
          if (c === category) {
            btn.className = 'px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-600 text-white shadow-sm transition';
          } else {
            btn.className = 'px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition';
          }
        }
      });

      const titleMap = {
        'corroborations': 'All Discovered Corroborations',
        'contradictions': 'All Discovered Contradictions',
        'reconciliations': 'All Discovered Contextual Reconciliations',
        'limitations': 'Identified Layout Limitations & Edge Cases'
      };
      const titleEl = document.getElementById('category-drawer-title');
      if (titleEl) titleEl.innerText = titleMap[category];
      renderCategoryInstances();
    }

    function renderCategoryInstances() {
      const container = document.getElementById('category-instances-container');
      if (!container || !casesBreakdown) return;

      if (currentCategoryView === 'limitations') {
        const items = casesBreakdown.limitations || [];
        if (!items.length) {
          container.innerHTML = '<div class="text-xs text-slate-500 italic p-4 text-center">No layout limitations recorded.</div>';
          return;
        }
        container.innerHTML = items.map((lim, i) => `
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs space-y-2">
            <div class="flex justify-between items-center">
              <span class="text-[11px] font-bold text-purple-400">#0${i + 1} &bull; Spatial Challenge</span>
              <span class="text-[11px] text-slate-400 font-mono">Confidence: ${(lim.confidence * 100).toFixed(0)}%</span>
            </div>
            <div class="font-semibold text-white text-xs">${lim.fact.claim}</div>
            <div class="text-slate-400 text-[11px] italic bg-slate-900 p-2.5 rounded-lg border border-slate-800/80">"${lim.fact.source_quote}"</div>
            <div class="text-[11px] text-slate-400 border-t border-slate-800/80 pt-2"><strong class="text-slate-300">Technical Analysis:</strong> ${lim.limitation_analysis}</div>
          </div>
        `).join('');
        return;
      }

      const items = casesBreakdown[currentCategoryView] || [];
      if (!items.length) {
        container.innerHTML = '<div class="text-xs text-slate-500 italic p-4 text-center">No instances found under current filter.</div>';
        return;
      }

      container.innerHTML = items.map((item, i) => `
        <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs space-y-2 hover:border-slate-700 transition">
          <div class="flex justify-between items-center">
            <span class="text-[11px] font-bold text-blue-400">#0${i + 1} &bull; ${item.relationship_type.replace('_', ' ').toUpperCase()}</span>
            <span class="text-[11px] text-slate-400 font-mono">Confidence: ${(item.confidence * 100).toFixed(0)}% &bull; Signal: ${item.score}</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-[11px]">
            <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800/70">
              <span class="text-[10px] font-bold text-slate-500 block mb-0.5">Doc A (${item.fact_a ? item.fact_a.doc_filename : 'A'}, Pg ${item.fact_a ? item.fact_a.page_number : ''}):</span>
              <span class="text-slate-200 font-medium">${item.fact_a ? item.fact_a.claim : ''}</span>
            </div>
            <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800/70">
              <span class="text-[10px] font-bold text-slate-500 block mb-0.5">Doc B (${item.fact_b ? item.fact_b.doc_filename : 'B'}, Pg ${item.fact_b ? item.fact_b.page_number : ''}):</span>
              <span class="text-slate-200 font-medium">${item.fact_b ? item.fact_b.claim : ''}</span>
            </div>
          </div>
          <div class="text-[11px] text-slate-400 border-t border-slate-800/80 pt-2"><strong class="text-slate-300">Auditor Rationale:</strong> ${item.explanation}</div>
        </div>
      `).join('');
    }

    async function loadFacts() {
      try {
        const res = await fetch('/api/facts');
        rawFacts = await res.json();
        
        const fCount = document.getElementById('count-facts');
        if (fCount) fCount.innerText = rawFacts.length;

        const ribFacts = document.getElementById('ribbon-facts');
        if (ribFacts) ribFacts.innerText = `${rawFacts.length} Facts`;
        
        const hStats = document.getElementById('header-stats');
        if (hStats) hStats.innerText = `${rawDocuments.length} Filings • ${rawFacts.length} Facts • ${rawRelationships.length} Reconciliations`;
        
        filterFacts();
      } catch (e) {
        console.error('Failed to load facts', e);
      }
    }

    function filterByCategory(cat) {
      activeFactCategory = cat;
      ['all', 'financial', 'operational', 'strategic', 'personnel'].forEach(c => {
        const btn = document.getElementById(`cat-pill-${c}`);
        if (btn) {
          if (c === cat) {
            btn.className = 'cat-pill pill-active px-3 py-1 rounded-lg font-semibold bg-blue-600 text-white border border-blue-500 transition';
          } else {
            btn.className = 'cat-pill px-3 py-1 rounded-lg font-semibold bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition';
          }
        }
      });
      filterFacts();
    }

    function filterFacts() {
      const q = (document.getElementById('fact-search') ? document.getElementById('fact-search').value : '').toLowerCase().trim();
      const doc = document.getElementById('doc-filter') ? document.getElementById('doc-filter').value : 'all';

      const filtered = rawFacts.filter(f => {
        const matchesDoc = doc === 'all' || f.doc_filename === doc;
        const matchesCat = activeFactCategory === 'all' || (f.category || '').toLowerCase() === activeFactCategory;
        const matchesQuery = !q ||
          (f.claim && f.claim.toLowerCase().includes(q)) ||
          (f.subject && f.subject.toLowerCase().includes(q)) ||
          (f.entities && f.entities.some(e => e.toLowerCase().includes(q)));
        return matchesDoc && matchesCat && matchesQuery;
      });

      const counter = document.getElementById('facts-counter-text');
      if (counter) counter.innerText = `Showing ${filtered.length} of ${rawFacts.length} verified facts`;
      
      const container = document.getElementById('facts-container');
      if (!container) return;

      if (!filtered.length) {
        container.innerHTML = '<div class="col-span-2 p-8 text-center text-slate-500 text-xs">No facts match your search criteria.</div>';
        return;
      }

      function highlightText(text, query) {
        if (!query || !text) return text || '';
        const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        return text.replace(new RegExp(escaped, 'gi'), match => `<span class="mark-highlight">${match}</span>`);
      }

      container.innerHTML = filtered.slice(0, 100).map((f, i) => `
        <div onclick="openFactDrawer('${f.id}')" class="bg-slate-900 border border-slate-800 hover:border-blue-500/50 rounded-xl p-4 shadow-md space-y-2.5 transition cursor-pointer group">
          <div class="flex justify-between items-center text-xs">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-blue-400 border border-slate-700">${f.category || 'General'}</span>
            <span class="text-[11px] font-mono text-emerald-400 font-semibold">${(f.confidence * 100).toFixed(0)}% Conf.</span>
          </div>
          <h4 class="font-bold text-white text-xs leading-snug group-hover:text-blue-300 transition">${highlightText(f.claim, q)}</h4>
          <div class="text-[11px] text-slate-400 flex items-center space-x-2">
            <span>${f.doc_filename}</span>
            <span>&bull;</span>
            <span>Page ${f.page_number}</span>
          </div>
          <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800/80 text-[11px] text-slate-400 italic font-serif">
            "${highlightText(f.source_quote, q)}"
          </div>
        </div>
      `).join('');
    }

    function openFactDrawer(factId) {
      const fact = rawFacts.find(f => f.id === factId);
      if (!fact) return;

      const drawer = document.getElementById('fact-drawer');
      const backdrop = document.getElementById('fact-drawer-backdrop');
      const content = document.getElementById('fact-drawer-content');

      let entitiesHtml = (fact.entities || []).map((e, idx) => {
        const type = (fact.entity_types && fact.entity_types[idx]) ? fact.entity_types[idx] : 'Entity';
        return `<span class="px-2 py-0.5 rounded bg-slate-800 text-slate-200 border border-slate-700 font-mono text-[10px]">${e} (${type})</span>`;
      }).join(' ') || '<span class="text-slate-500 italic">None specified</span>';

      let attrsHtml = Object.entries(fact.attributes || {}).map(([k, v]) => `
        <div class="flex justify-between py-1 border-b border-slate-800/60 font-mono text-[11px]">
          <span class="text-slate-400">${k}:</span>
          <span class="text-white font-medium">${v}</span>
        </div>
      `).join('') || '<div class="text-slate-500 italic py-1">No structured attributes</div>';

      content.innerHTML = `
        <div class="space-y-3">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">Stated Fact Claim</span>
            <p class="font-bold text-white text-sm mt-0.5 leading-snug">${fact.claim}</p>
          </div>

          <div class="grid grid-cols-2 gap-2 text-[11px]">
            <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800">
              <span class="text-slate-500 block text-[10px] uppercase font-bold">Subject:</span>
              <span class="text-slate-200 font-medium font-mono">${fact.subject}</span>
            </div>
            <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800">
              <span class="text-slate-500 block text-[10px] uppercase font-bold">Predicate:</span>
              <span class="text-slate-200 font-medium font-mono">${fact.predicate}</span>
            </div>
          </div>

          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block mb-1">Source Lineage</span>
            <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 text-[11px] font-mono">
              <div>Filing: ${fact.doc_filename}</div>
              <div>Page: ${fact.page_number}</div>
              <div>Chunk ID: ${fact.chunk_id || 'N/A'}</div>
            </div>
          </div>

          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block mb-1">Verbatim Source Quotation</span>
            <div class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 italic font-serif text-xs leading-relaxed border-l-2 border-blue-500">
              "${fact.source_quote}"
            </div>
          </div>

          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block mb-1">Associated Entities</span>
            <div class="flex flex-wrap gap-1">${entitiesHtml}</div>
          </div>

          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block mb-1">Structured Attributes</span>
            <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 space-y-0.5">${attrsHtml}</div>
          </div>
        </div>
      `;

      drawer.classList.remove('translate-x-full');
      backdrop.classList.remove('hidden');
    }

    function closeFactDrawer() {
      const drawer = document.getElementById('fact-drawer');
      const backdrop = document.getElementById('fact-drawer-backdrop');
      if (drawer) drawer.classList.add('translate-x-full');
      if (backdrop) backdrop.classList.add('hidden');
    }

    async function loadRelationships() {
      try {
        const res = await fetch('/api/relationships');
        rawRelationships = await res.json();
        
        const rCount = document.getElementById('count-rels');
        if (rCount) rCount.innerText = rawRelationships.length;

        const ribRels = document.getElementById('ribbon-rels');
        if (ribRels) ribRels.innerText = `${rawRelationships.length} Connections`;
        
        const hStats = document.getElementById('header-stats');
        if (hStats) hStats.innerText = `${rawDocuments.length} Filings • ${rawFacts.length} Facts • ${rawRelationships.length} Reconciliations`;

        filterRelationships('all');
      } catch (e) {
        console.error('Failed to load relationships', e);
      }
    }

    function filterRelationships(type) {
      ['all', 'corroboration', 'contradiction', 'contextual_reconciliation'].forEach(t => {
        const btn = document.getElementById(`filter-rel-${t}`);
        if (btn) {
          if (t === type) {
            btn.className = 'rel-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 text-white shadow-sm transition';
          } else {
            btn.className = 'rel-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition';
          }
        }
      });

      const filtered = rawRelationships.filter(r => {
        if (type === 'all') return true;
        return (r.relationship_type || '').toLowerCase().includes(type.toLowerCase());
      });

      const countEl = document.getElementById('rel-filter-count');
      if (countEl) countEl.innerText = `Showing ${filtered.length} of ${rawRelationships.length} relationships`;
      
      const container = document.getElementById('relationships-container');
      if (!container) return;

      if (!filtered.length) {
        container.innerHTML = '<div class="p-8 text-center text-slate-500 text-xs">No relationships found under this category.</div>';
        return;
      }

      container.innerHTML = filtered.map(r => {
        const fa = r.fact_a;
        const fb = r.fact_b;
        let badgeColor = 'bg-blue-500/10 text-blue-400 border-blue-500/30';
        if (r.relationship_type.includes('corroboration')) badgeColor = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
        if (r.relationship_type.includes('contradiction')) badgeColor = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
        if (r.relationship_type.includes('reconciliation')) badgeColor = 'bg-amber-500/10 text-amber-400 border-amber-500/30';

        return `
          <div class="glass-panel rounded-2xl p-5 shadow-lg space-y-3 hover:border-slate-700 transition">
            <div class="flex justify-between items-center">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider border ${badgeColor}">${r.relationship_type.replace('_', ' ')}</span>
              <span class="text-xs font-mono text-slate-400">Confidence: ${(r.confidence * 100).toFixed(0)}%</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1">
                <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Filing A:</span>
                <p class="font-semibold text-white leading-snug">${fa ? fa.claim : r.fact_a_id}</p>
                <span class="text-blue-400 text-[11px] block font-mono">${fa ? `${fa.doc_filename} (Page ${fa.page_number})` : ''}</span>
              </div>
              <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1">
                <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Filing B:</span>
                <p class="font-semibold text-white leading-snug">${fb ? fb.claim : r.fact_b_id}</p>
                <span class="text-indigo-400 text-[11px] block font-mono">${fb ? `${fb.doc_filename} (Page ${fb.page_number})` : ''}</span>
              </div>
            </div>

            <div class="bg-slate-950 p-3 rounded-lg border border-slate-800/70 text-xs text-slate-300 leading-relaxed">
              <strong class="text-slate-400 font-bold block mb-0.5 text-[10px] uppercase tracking-wider">Reconciliation Protocol & Rationale:</strong>
              ${r.explanation}
            </div>
          </div>
        `;
      }).join('');
    }

    async function loadExport() {
      try {
        const res = await fetch('/api/export');
        const data = await res.json();
        const sDocs = document.getElementById('stat-docs');
        if (sDocs) sDocs.innerText = data.summary.total_documents;
        const sFacts = document.getElementById('stat-facts');
        if (sFacts) sFacts.innerText = data.summary.total_facts;
        const sRels = document.getElementById('stat-rels');
        if (sRels) sRels.innerText = data.summary.total_relationships;
        const sContras = document.getElementById('stat-contras');
        if (sContras) sContras.innerText = data.summary.contradictions;
        
        const preview = document.getElementById('json-preview');
        if (preview) preview.innerText = JSON.stringify(data, null, 2);
      } catch (e) {
        console.error('Failed to load export', e);
      }
    }

    function copyExportJson() {
      const text = document.getElementById('json-preview').innerText;
      navigator.clipboard.writeText(text).then(() => {
        alert('Knowledge Graph JSON copied to clipboard!');
      });
    }

    function handleFileSelect(event) {
      const files = event.target.files;
      if (!files.length) return;
      selectedFiles = Array.from(files);
      renderSelectedFiles();
    }

    function renderSelectedFiles() {
      const container = document.getElementById('selected-files-container');
      const list = document.getElementById('file-chips-list');
      const count = document.getElementById('selected-files-count');
      if (!selectedFiles.length) {
        if (container) container.classList.add('hidden');
        return;
      }
      if (container) container.classList.remove('hidden');
      if (count) count.innerText = selectedFiles.length;
      if (list) {
        list.innerHTML = selectedFiles.map((f, i) => `
          <span class="inline-flex items-center px-3 py-1 rounded-lg text-xs font-medium bg-blue-500/10 text-blue-300 border border-blue-500/20">
            ${f.name} (${(f.size / 1024).toFixed(0)} KB)
            <button type="button" onclick="removeFile(${i})" class="ml-2 text-blue-400 hover:text-rose-400 font-bold">&times;</button>
          </span>
        `).join('');
      }
    }

    function removeFile(index) {
      selectedFiles.splice(index, 1);
      renderSelectedFiles();
    }

    function clearSelectedFiles() {
      selectedFiles = [];
      const input = document.getElementById('pdf-file-input');
      if (input) input.value = '';
      renderSelectedFiles();
    }

    async function handleBatchUpload(e) {
      e.preventDefault();
      if (!selectedFiles.length) {
        alert('Please select at least one PDF file to ingest.');
        return;
      }

      const formData = new FormData();
      for (const file of selectedFiles) {
        formData.append('files', file);
      }

      const statusDiv = document.getElementById('upload-status');
      const progressBar = document.getElementById('upload-progress-bar');
      const statusTitle = document.getElementById('upload-status-title');
      const statusPct = document.getElementById('upload-status-pct');
      const statusText = document.getElementById('upload-status-text');
      const uploadBtn = document.getElementById('upload-btn');

      if (statusDiv) statusDiv.classList.remove('hidden');
      if (uploadBtn) {
        uploadBtn.disabled = true;
        uploadBtn.classList.add('opacity-50', 'cursor-not-allowed');
      }

      if (progressBar) progressBar.style.width = '30%';
      if (statusPct) statusPct.innerText = '30%';
      if (statusTitle) statusTitle.innerText = `Ingesting ${selectedFiles.length} Filing(s)...`;
      if (statusText) statusText.innerText = 'Parsing text streams, extracting markdown tables, and calling LLM fact triples...';

      try {
        const res = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        });

        if (!res.ok) throw new Error(`Upload error: ${res.status}`);
        const data = await res.json();

        if (progressBar) progressBar.style.width = '100%';
        if (statusPct) statusPct.innerText = '100%';
        if (statusTitle) statusTitle.innerText = 'Batch Processing & Reconciliation Complete!';
        if (statusText) statusText.innerText = `Successfully ingested ${data.results.length} files. Refreshing facts and cases...`;

        setTimeout(async () => {
          clearSelectedFiles();
          await init();
          if (uploadBtn) {
            uploadBtn.disabled = false;
            uploadBtn.classList.remove('opacity-50', 'cursor-not-allowed');
          }
          if (statusDiv) statusDiv.classList.add('hidden');
          switchTab('cases');
          alert('Documents successfully ingested! Cases and relationships have been updated.');
        }, 1200);

      } catch (err) {
        if (progressBar) progressBar.style.backgroundColor = '#ef4444';
        if (statusTitle) statusTitle.innerText = 'Upload Error';
        if (statusText) statusText.innerText = err.message;
        if (uploadBtn) {
          uploadBtn.disabled = false;
          uploadBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
      }
    }

    async function confirmReset() {
      const confirmAction = confirm(
        `RESET TO BENCHMARK BASELINE\n\n` +
        `This will restore the 3 benchmark Delhivery filings, 258 verified facts, and 47 relationships.\n\n` +
        `Click OK to restore benchmark baseline, or Cancel to keep current state.`
      );
      if (!confirmAction) return;

      try {
        const res = await fetch('/api/reset', { method: 'POST' });
        const data = await res.json();
        alert('Benchmark baseline restored successfully! (3 Delhivery PDFs, 258 facts, 47 relationships)');
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
