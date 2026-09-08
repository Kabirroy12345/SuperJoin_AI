def get_dashboard_html() -> str:
    """Returns the standalone HTML/JS dashboard interface with modern enterprise styling."""
    return """<!DOCTYPE html>
<html lang="en" class="h-full bg-slate-900">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fact Knowledge Layer | Superjoin Enterprise Studio</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            brand: {
              50: '#eff6ff',
              100: '#dbeafe',
              500: '#3b82f6',
              600: '#2563eb',
              700: '#1d4ed8',
              900: '#1e3a8a',
            }
          }
        }
      }
    }
  </script>
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .glass-nav {
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #0f172a;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 9999px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
      background: #475569;
    }
    .case-card.active-case {
      border-color: #3b82f6;
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25), 0 10px 25px -5px rgba(0, 0, 0, 0.3);
      transform: translateY(-2px);
    }
  </style>
</head>
<body class="h-full text-slate-100 bg-slate-950 flex flex-col antialiased selection:bg-blue-500 selection:text-white">

  <!-- Top Navigation Bar -->
  <header class="glass-nav border-b border-slate-800/80 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 gap-4">
        
        <!-- Logo & Title -->
        <div class="flex items-center space-x-3.5">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-500 flex items-center justify-center text-white shadow-lg shadow-blue-500/20 ring-1 ring-white/20">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <h1 class="text-base font-bold text-white tracking-tight">Fact Knowledge Layer</h1>
              <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">
                Superjoin Studio
              </span>
            </div>
            <p class="text-[11px] text-slate-400 hidden sm:block">Automated Cross-Document Evidence Reconciliation & Verification</p>
          </div>
        </div>

        <!-- Global Action Controls -->
        <div class="flex items-center space-x-3">
          <div class="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900/90 border border-slate-800 text-xs">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span class="text-slate-300 font-medium">Engine Active</span>
            <span class="text-slate-600">|</span>
            <span class="text-slate-400 font-mono" id="header-stats">3 Docs &bull; 258 Facts</span>
          </div>

          <button onclick="confirmReset()" title="Restore benchmark Delhivery dataset" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700/80 text-xs font-semibold transition">
            <svg class="w-3.5 h-3.5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>Reset to Benchmark</span>
          </button>

          <a href="/docs" target="_blank" class="inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-sm transition">
            <span>API Docs</span>
            <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </a>
        </div>

      </div>

      <!-- Navigation Tabs -->
      <nav class="flex space-x-1 border-t border-slate-800/70 overflow-x-auto py-2 custom-scrollbar">
        <button onclick="switchTab('cases')" id="tab-cases-btn" class="nav-tab active px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 shadow-sm transition whitespace-nowrap flex items-center space-x-1.5">
          <span>✨</span> <span>The 4 Required Cases</span>
        </button>
        <button onclick="switchTab('facts')" id="tab-facts-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition whitespace-nowrap flex items-center space-x-1.5">
          <span>🔍</span> <span>Facts Explorer (<span id="count-facts">0</span>)</span>
        </button>
        <button onclick="switchTab('relationships')" id="tab-relationships-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition whitespace-nowrap flex items-center space-x-1.5">
          <span>🔗</span> <span>All Relationships (<span id="count-rels">0</span>)</span>
        </button>
        <button onclick="switchTab('upload')" id="tab-upload-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition whitespace-nowrap flex items-center space-x-1.5">
          <span>📤</span> <span>Multi-PDF Ingestion (<span id="count-docs">0</span>)</span>
        </button>
        <button onclick="switchTab('export')" id="tab-export-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition whitespace-nowrap flex items-center space-x-1.5">
          <span>📊</span> <span>Knowledge Graph JSON</span>
        </button>
      </nav>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

    <!-- ======================================================== -->
    <!-- VIEW 1: THE 4 REQUIRED CASES (SHOWCASE VIEW) -->
    <!-- ======================================================== -->
    <section id="view-cases" class="space-y-6">
      
      <!-- Scope Filter Header -->
      <div class="bg-slate-900 border border-slate-800/90 rounded-2xl p-5 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center space-x-2">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              Evaluation Center
            </span>
            <span class="text-xs text-slate-400">&bull; Ground-Truth Cross-Document Verification</span>
          </div>
          <h2 class="text-lg font-extrabold text-white mt-1">Superjoin Four Analytical Scenarios</h2>
          <p class="text-xs text-slate-400 mt-0.5">
            Click any scenario card below to inspect side-by-side evidence diffs, verbatim quotes, and system reasoning.
          </p>
        </div>

        <div class="flex items-center space-x-3 w-full md:w-auto">
          <label for="case-doc-filter" class="text-xs font-semibold text-slate-300 whitespace-nowrap flex items-center space-x-1.5">
            <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            <span>Document Scope:</span>
          </label>
          <select id="case-doc-filter" onchange="onCaseDocFilterChange()" class="w-full md:w-72 bg-slate-950 text-white text-xs rounded-xl border border-slate-700 px-3.5 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none">
            <option value="">All Documents (Global Knowledge Base)</option>
          </select>
        </div>
      </div>

      <!-- The 4 Scenario Switcher Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="scenario-selector-grid">
        
        <!-- Case 1 Card -->
        <div onclick="selectCaseByIndex(0)" id="case-btn-0" class="case-card active-case cursor-pointer bg-slate-900 border border-slate-800 hover:border-emerald-500/60 rounded-xl p-4 transition duration-200 relative overflow-hidden group">
          <div class="flex justify-between items-start">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              Case 1
            </span>
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-sm shadow-emerald-500/50"></span>
          </div>
          <h3 class="font-bold text-sm text-white mt-2 group-hover:text-emerald-300 transition">Corroborated Fact</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">Independent documents confirm the identical metric or event.</p>
          <div class="mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Discovered:</span>
            <span class="font-semibold text-emerald-400" id="badge-corrobs-count">12 instances</span>
          </div>
        </div>

        <!-- Case 2 Card -->
        <div onclick="selectCaseByIndex(1)" id="case-btn-1" class="case-card cursor-pointer bg-slate-900 border border-slate-800 hover:border-rose-500/60 rounded-xl p-4 transition duration-200 relative overflow-hidden group">
          <div class="flex justify-between items-start">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-rose-500/10 text-rose-400 border border-rose-500/30">
              Case 2
            </span>
            <span class="w-2.5 h-2.5 rounded-full bg-rose-500 shadow-sm shadow-rose-500/50"></span>
          </div>
          <h3 class="font-bold text-sm text-white mt-2 group-hover:text-rose-300 transition">Genuine Contradiction</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">Conflicting metrics reported for the same date/scope.</p>
          <div class="mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Discovered:</span>
            <span class="font-semibold text-rose-400" id="badge-contras-count">2 instances</span>
          </div>
        </div>

        <!-- Case 3 Card -->
        <div onclick="selectCaseByIndex(2)" id="case-btn-2" class="case-card cursor-pointer bg-slate-900 border border-slate-800 hover:border-amber-500/60 rounded-xl p-4 transition duration-200 relative overflow-hidden group">
          <div class="flex justify-between items-start">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-amber-500/10 text-amber-400 border border-amber-500/30">
              Case 3
            </span>
            <span class="w-2.5 h-2.5 rounded-full bg-amber-500 shadow-sm shadow-amber-500/50"></span>
          </div>
          <h3 class="font-bold text-sm text-white mt-2 group-hover:text-amber-300 transition">Contextual Reconciliation</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">Apparent conflict resolved by period, scope, or definition.</p>
          <div class="mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Discovered:</span>
            <span class="font-semibold text-amber-400" id="badge-recs-count">33 instances</span>
          </div>
        </div>

        <!-- Case 4 Card -->
        <div onclick="selectCaseByIndex(3)" id="case-btn-3" class="case-card cursor-pointer bg-slate-900 border border-slate-800 hover:border-purple-500/60 rounded-xl p-4 transition duration-200 relative overflow-hidden group">
          <div class="flex justify-between items-start">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-purple-500/10 text-purple-400 border border-purple-500/30">
              Case 4
            </span>
            <span class="w-2.5 h-2.5 rounded-full bg-purple-500 shadow-sm shadow-purple-500/50"></span>
          </div>
          <h3 class="font-bold text-sm text-white mt-2 group-hover:text-purple-300 transition">Extraction Limitation</h3>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">PDF spatial layout challenge & architectural mitigation.</p>
          <div class="mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Analyzed:</span>
            <span class="font-semibold text-purple-400" id="badge-limits-count">10 instances</span>
          </div>
        </div>

      </div>

      <!-- Spotlight Evidence Arena (Side-by-Side Comparison) -->
      <div id="spotlight-display-arena" class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-6">
        <div class="p-8 text-center text-slate-500 animate-pulse">Loading verified case evidence...</div>
      </div>

      <!-- Instance Drawer / Categorized Browser -->
      <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h4 class="font-bold text-sm text-white flex items-center space-x-2">
              <span>📚</span> <span id="category-drawer-title">All Discovered Corroborations</span>
            </h4>
            <p class="text-xs text-slate-400 mt-0.5">Explore every verified instance identified by the reconciliation engine.</p>
          </div>
          <div class="flex flex-wrap gap-1.5" id="category-filter-pills">
            <button onclick="switchCategoryView('corroborations')" id="cat-btn-corroborations" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 transition">Corroborations</button>
            <button onclick="switchCategoryView('contradictions')" id="cat-btn-contradictions" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:text-white border border-slate-700 transition">Contradictions</button>
            <button onclick="switchCategoryView('reconciliations')" id="cat-btn-reconciliations" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:text-white border border-slate-700 transition">Reconciliations</button>
            <button onclick="switchCategoryView('limitations')" id="cat-btn-limitations" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:text-white border border-slate-700 transition">Limitations</button>
          </div>
        </div>

        <div id="category-instances-container" class="space-y-3 max-h-[480px] overflow-y-auto pr-1 custom-scrollbar"></div>
      </div>

    </section>

    <!-- ======================================================== -->
    <!-- VIEW 2: FACTS EXPLORER -->
    <!-- ======================================================== -->
    <section id="view-facts" class="space-y-6 hidden">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
        <div class="flex flex-col sm:flex-row gap-3">
          <div class="relative flex-1">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
              <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input type="text" id="fact-search" oninput="filterFacts()" placeholder="Search extracted claims, entities, or metrics (e.g. revenue, EBITDA, appointed)..." class="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 text-white text-xs border border-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none">
          </div>
          <div class="w-full sm:w-72">
            <select id="doc-filter" onchange="filterFacts()" class="w-full bg-slate-950 text-white text-xs rounded-xl border border-slate-700 px-3.5 py-2.5 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none">
              <option value="all">All Documents</option>
            </select>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 border-t border-slate-800/80 pt-3">
          <span id="facts-counter-text">Showing 0 facts</span>
          <span class="text-[11px] text-slate-500">Atomic factual triples with verbatim ground quotes</span>
        </div>
      </div>

      <div id="facts-container" class="grid grid-cols-1 md:grid-cols-2 gap-4"></div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 3: ALL RELATIONSHIPS -->
    <!-- ======================================================== -->
    <section id="view-relationships" class="space-y-6 hidden">
      <div class="flex flex-wrap items-center justify-between gap-3 bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
        <div class="flex flex-wrap gap-2">
          <button onclick="filterRelationships('all')" id="filter-rel-all" class="rel-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 text-white shadow-sm transition">All Relationships</button>
          <button onclick="filterRelationships('corroboration')" id="filter-rel-corroboration" class="rel-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition">Corroborations</button>
          <button onclick="filterRelationships('contradiction')" id="filter-rel-contradiction" class="rel-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition">Contradictions</button>
          <button onclick="filterRelationships('contextual_reconciliation')" id="filter-rel-contextual_reconciliation" class="rel-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition">Reconciliations</button>
        </div>
        <span class="text-xs text-slate-400 font-mono" id="rel-filter-count">Showing 0 relationships</span>
      </div>

      <div id="relationships-container" class="space-y-4"></div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 4: MULTI-PDF BATCH INGESTION -->
    <!-- ======================================================== -->
    <section id="view-upload" class="space-y-6 hidden">
      <div class="max-w-3xl mx-auto bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl space-y-6">
        <div class="text-center space-y-2">
          <div class="w-14 h-14 mx-auto rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-blue-500/30 ring-1 ring-white/20">
            <svg class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h3 class="text-xl font-extrabold text-white">Batch Document Ingestion Studio</h3>
          <p class="text-xs text-slate-400 max-w-md mx-auto">
            Upload single or multiple PDFs at once. The engine will parse tables, extract facts, generate 3,072-dim embeddings, and reconcile against all indexed documents.
          </p>
        </div>

        <form onsubmit="handleBatchUpload(event)" class="space-y-4">
          <div onclick="document.getElementById('pdf-file-input').click()" class="border-2 border-dashed border-slate-700 hover:border-blue-500 rounded-2xl p-8 text-center cursor-pointer bg-slate-950/60 hover:bg-slate-950 transition duration-200 group">
            <input type="file" id="pdf-file-input" multiple accept=".pdf" onchange="handleFileSelect(event)" class="hidden">
            <div class="w-12 h-12 mx-auto rounded-xl bg-slate-800 group-hover:bg-blue-600/20 text-slate-400 group-hover:text-blue-400 flex items-center justify-center transition">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <p class="text-sm font-semibold text-slate-200 mt-3">Click to select or drag & drop PDF files</p>
            <p class="text-[11px] text-slate-500 mt-1">Accepts multiple corporate disclosures, annual reports, earnings calls, or macro filings</p>
          </div>

          <!-- File selection preview -->
          <div id="selected-files-container" class="space-y-2 hidden bg-slate-950 p-4 rounded-xl border border-slate-800">
            <div class="flex justify-between items-center text-xs font-semibold text-slate-400">
              <span>Selected PDFs (<span id="selected-files-count">0</span>)</span>
              <button type="button" onclick="clearSelectedFiles()" class="text-rose-400 hover:text-rose-300 transition">Clear All</button>
            </div>
            <div id="file-chips-list" class="flex flex-wrap gap-2 pt-1"></div>
          </div>

          <button type="submit" id="upload-btn" class="w-full py-3.5 px-5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-xs uppercase tracking-wider shadow-lg shadow-blue-500/25 transition flex items-center justify-center space-x-2">
            <span>⚡ Start Ingestion & Reconciliation</span>
          </button>
        </form>

        <!-- Progress Tracker -->
        <div id="upload-status" class="hidden bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
          <div class="flex justify-between items-center text-xs">
            <span id="upload-status-title" class="font-semibold text-slate-200">Processing queue...</span>
            <span id="upload-status-pct" class="font-mono text-blue-400">0%</span>
          </div>
          <div class="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div id="upload-progress-bar" class="bg-gradient-to-r from-blue-500 to-indigo-500 h-2 rounded-full w-0 transition-all duration-300"></div>
          </div>
          <p id="upload-status-text" class="text-[11px] text-slate-400 font-mono"></p>
        </div>

        <!-- Ingested Documents Registry -->
        <div class="border-t border-slate-800 pt-5 space-y-3">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-400">Indexed Knowledge Repositories</span>
            <span class="font-mono text-slate-500" id="ingested-docs-count">0 documents</span>
          </div>
          <div id="ingested-docs-list" class="space-y-2"></div>
        </div>

      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 5: EXPORT & KNOWLEDGE GRAPH JSON -->
    <!-- ======================================================== -->
    <section id="view-export" class="space-y-6 hidden">
      <!-- KPI Stats -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Ingested Filings</span>
          <div class="text-3xl font-extrabold text-white mt-1" id="stat-docs">0</div>
          <span class="text-[11px] text-slate-500 mt-1 block">Full document store</span>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Semantic Facts</span>
          <div class="text-3xl font-extrabold text-blue-400 mt-1" id="stat-facts">0</div>
          <span class="text-[11px] text-slate-500 mt-1 block">Atomic verified triples</span>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Relationships</span>
          <div class="text-3xl font-extrabold text-emerald-400 mt-1" id="stat-rels">0</div>
          <span class="text-[11px] text-slate-500 mt-1 block">Cross-filing links</span>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Contradictions</span>
          <div class="text-3xl font-extrabold text-rose-400 mt-1" id="stat-contras">0</div>
          <span class="text-[11px] text-slate-500 mt-1 block">Direct conflicts resolved</span>
        </div>
      </div>

      <!-- JSON Viewer -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
          <div>
            <h3 class="font-bold text-white text-base">Knowledge Graph Export & Serialization</h3>
            <p class="text-xs text-slate-400 mt-0.5">Full machine-readable snapshot containing documents, grounded facts, and reconciliation graph.</p>
          </div>
          <div class="flex items-center space-x-2">
            <button onclick="copyExportJson()" class="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition border border-slate-700">
              📋 Copy JSON
            </button>
            <a href="/api/export" download="results.json" class="px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition shadow-sm">
              📥 Download results.json
            </a>
          </div>
        </div>

        <pre id="json-preview" class="bg-slate-950 p-4 rounded-xl text-xs font-mono text-slate-300 overflow-x-auto max-h-[500px] border border-slate-800/80 custom-scrollbar"></pre>
      </div>
    </section>

  </main>

  <!-- Javascript Controller -->
  <script>
    let rawFacts = [];
    let rawRelationships = [];
    let rawDocuments = [];
    let casesBreakdown = null;
    let selectedCaseIndex = 0;
    let currentCategoryView = 'corroborations';
    let selectedFiles = [];

    async function init() {
      await loadDocuments();
      await loadCasesBreakdown();
      await loadFacts();
      await loadRelationships();
      await loadExport();
    }

    function switchTab(tabId) {
      ['cases', 'facts', 'relationships', 'upload', 'export'].forEach(t => {
        const view = document.getElementById(`view-${t}`);
        const btn = document.getElementById(`tab-${t}-btn`);
        if (t === tabId) {
          view.classList.remove('hidden');
          btn.classList.add('active', 'bg-blue-600', 'text-white');
          btn.classList.remove('text-slate-400', 'hover:bg-slate-800/60');
        } else {
          view.classList.add('hidden');
          btn.classList.remove('active', 'bg-blue-600', 'text-white');
          btn.classList.add('text-slate-400', 'hover:bg-slate-800/60');
        }
      });
    }

    async function loadDocuments() {
      try {
        const res = await fetch('/api/documents');
        rawDocuments = await res.json();
        document.getElementById('count-docs').innerText = rawDocuments.length;
        document.getElementById('ingested-docs-count').innerText = `${rawDocuments.length} documents`;

        const caseDocSelect = document.getElementById('case-doc-filter');
        const prevVal = caseDocSelect.value;
        caseDocSelect.innerHTML = '<option value="">All Documents (Global Knowledge Base)</option>' +
          rawDocuments.map(d => `<option value="${d.id}">${d.filename} (${d.page_count} pgs)</option>`).join('');
        if (prevVal) caseDocSelect.value = prevVal;

        const docSelect = document.getElementById('doc-filter');
        docSelect.innerHTML = '<option value="all">All Documents</option>' +
          rawDocuments.map(d => `<option value="${d.filename}">${d.filename}</option>`).join('');

        const listDiv = document.getElementById('ingested-docs-list');
        if (!rawDocuments.length) {
          listDiv.innerHTML = '<div class="text-xs text-slate-500 italic p-3 rounded-lg bg-slate-950 border border-slate-800">No documents ingested. Upload PDFs above.</div>';
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
      } catch (e) {
        console.error('Failed to load documents', e);
      }
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
        document.getElementById('badge-corrobs-count').innerText = `${counts.corroborations || 0} instances`;
        document.getElementById('badge-contras-count').innerText = `${counts.contradictions || 0} instances`;
        document.getElementById('badge-recs-count').innerText = `${counts.reconciliations || 0} instances`;
        document.getElementById('badge-limits-count').innerText = `${counts.limitations || 0} instances`;

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
        if (i === index) {
          btn.classList.add('active-case');
        } else {
          btn.classList.remove('active-case');
        }
      }
      renderSpotlightArena();
    }

    function renderSpotlightArena() {
      const arena = document.getElementById('spotlight-display-arena');
      if (!casesBreakdown || !casesBreakdown.featured_cases || casesBreakdown.featured_cases.length === 0) {
        arena.innerHTML = '<div class="p-8 text-center text-slate-500">No cases match the selected filter.</div>';
        return;
      }

      const caseItem = casesBreakdown.featured_cases[selectedCaseIndex] || casesBreakdown.featured_cases[0];
      const fa = caseItem.fact_a;
      const fb = caseItem.fact_b;
      const rel = caseItem.relationship;

      let badgeColor = 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      let statusIcon = '🤝 Consensus';
      if (caseItem.case_label.includes('Corroborat')) {
        badgeColor = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
        statusIcon = '✅ Cross-Verified Fact Agreement';
      } else if (caseItem.case_label.includes('Contradiction')) {
        badgeColor = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
        statusIcon = '❌ Direct Numerical / Factual Conflict';
      } else if (caseItem.case_label.includes('Reconciliation')) {
        badgeColor = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
        statusIcon = '🔄 Contextually Reconciled Resolution';
      } else if (caseItem.case_label.includes('Limitation') || caseItem.case_label.includes('Failure')) {
        badgeColor = 'bg-purple-500/10 text-purple-400 border-purple-500/30';
        statusIcon = '⚙️ Document Layout / Spatial Challenge';
      }

      arena.innerHTML = `
        <!-- Top Status Bar -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
          <div class="flex items-center space-x-3">
            <span class="w-8 h-8 rounded-xl bg-slate-800 flex items-center justify-center font-extrabold text-sm text-white">#${caseItem.case_number}</span>
            <div>
              <div class="flex items-center space-x-2">
                <h3 class="font-extrabold text-base text-white">${caseItem.case_label}</h3>
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold border ${badgeColor}">
                  ${statusIcon}
                </span>
              </div>
              <p class="text-xs text-slate-400 mt-0.5">High-confidence analytical demonstration grounded directly in filing evidence.</p>
            </div>
          </div>
          <div class="text-xs text-slate-400 font-mono bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800 flex items-center space-x-2">
            <span>Confidence:</span>
            <span class="text-emerald-400 font-bold">${rel ? (rel.confidence * 100).toFixed(0) : (fa.confidence * 100).toFixed(0)}%</span>
          </div>
        </div>

        <!-- Evidence Side-by-Side Diff Arena -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          
          <!-- Document Evidence A -->
          <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 space-y-3 relative overflow-hidden">
            <div class="flex items-center justify-between text-xs">
              <span class="font-extrabold text-blue-400 uppercase tracking-wider text-[11px] flex items-center space-x-1.5">
                <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                <span>Source Filing A</span>
              </span>
              <span class="px-2.5 py-0.5 rounded-full bg-slate-900 text-slate-300 border border-slate-800 font-mono text-[11px]">
                📄 ${fa.doc_filename} &bull; Page ${fa.page_number}
              </span>
            </div>

            <div class="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800/80">
              <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block mb-1">Stated Claim:</span>
              <p class="text-sm font-semibold text-white leading-snug">${fa.claim}</p>
            </div>

            <div class="p-3.5 rounded-xl bg-slate-900/40 border border-slate-800/60 text-xs">
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center space-x-1 mb-1">
                <span>💬</span> <span>Verbatim Source Quote:</span>
              </span>
              <p class="text-slate-300 italic leading-relaxed text-xs pl-2 border-l-2 border-blue-500/60">
                "${fa.source_quote}"
              </p>
            </div>
          </div>

          <!-- Document Evidence B (or Failure Mode Explanation) -->
          ${fb ? `
          <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 space-y-3 relative overflow-hidden">
            <div class="flex items-center justify-between text-xs">
              <span class="font-extrabold text-indigo-400 uppercase tracking-wider text-[11px] flex items-center space-x-1.5">
                <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
                <span>Source Filing B</span>
              </span>
              <span class="px-2.5 py-0.5 rounded-full bg-slate-900 text-slate-300 border border-slate-800 font-mono text-[11px]">
                📄 ${fb.doc_filename} &bull; Page ${fb.page_number}
              </span>
            </div>

            <div class="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800/80">
              <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block mb-1">Stated Claim:</span>
              <p class="text-sm font-semibold text-white leading-snug">${fb.claim}</p>
            </div>

            <div class="p-3.5 rounded-xl bg-slate-900/40 border border-slate-800/60 text-xs">
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center space-x-1 mb-1">
                <span>💬</span> <span>Verbatim Source Quote:</span>
              </span>
              <p class="text-slate-300 italic leading-relaxed text-xs pl-2 border-l-2 border-indigo-500/60">
                "${fb.source_quote}"
              </p>
            </div>
          </div>
          ` : `
          <div class="bg-purple-950/20 border border-purple-500/30 rounded-xl p-5 space-y-3 flex flex-col justify-center text-xs">
            <span class="font-extrabold text-purple-300 uppercase tracking-wider text-[11px] flex items-center space-x-1.5">
              <span class="w-2 h-2 rounded-full bg-purple-400"></span>
              <span>Layout & Token Vulnerability Assessment</span>
            </span>
            <p class="text-slate-300 text-xs leading-relaxed">
              Standard PDF text extractors discard two-dimensional bounding coordinates. In multi-column slides and dense financial matrices, spatial titles lose explicit attachment to their metrics.
            </p>
            <div class="p-3 bg-purple-900/20 border border-purple-500/20 rounded-lg text-purple-200 text-[11px]">
              <strong>Engineering Mitigation:</strong> Integrating LayoutLMv3 spatial token coordinates or Gemini Vision multimodal rasterization anchors un-nested headers accurately to their cells.
            </div>
          </div>
          `}

        </div>

        <!-- AI Auditor Reasoning Box -->
        <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1.5">
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-blue-400 flex items-center space-x-1.5">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Automated Reconciliation Reasoning & Evidence Analysis:</span>
          </span>
          <p class="text-xs text-slate-300 leading-relaxed font-normal">${caseItem.explanation}</p>
        </div>
      `;
    }

    function switchCategoryView(category) {
      currentCategoryView = category;
      ['corroborations', 'contradictions', 'reconciliations', 'limitations'].forEach(c => {
        const btn = document.getElementById(`cat-btn-${c}`);
        if (c === category) {
          btn.className = 'px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-600 text-white shadow-sm transition';
        } else {
          btn.className = 'px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:text-white border border-slate-700 transition';
        }
      });

      const titleMap = {
        'corroborations': 'All Discovered Corroborations',
        'contradictions': 'All Discovered Contradictions',
        'reconciliations': 'All Discovered Contextual Reconciliations',
        'limitations': 'Identified Extraction Limitations & Edge Cases'
      };
      document.getElementById('category-drawer-title').innerText = titleMap[category];
      renderCategoryInstances();
    }

    function renderCategoryInstances() {
      const container = document.getElementById('category-instances-container');
      if (!casesBreakdown) return;

      if (currentCategoryView === 'limitations') {
        const items = casesBreakdown.limitations || [];
        if (!items.length) {
          container.innerHTML = '<div class="text-xs text-slate-500 italic p-4 text-center">No extraction limitations recorded.</div>';
          return;
        }
        container.innerHTML = items.map((lim, i) => `
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs space-y-2">
            <div class="flex justify-between items-center">
              <span class="text-[11px] font-bold text-purple-400">#${i + 1} &bull; Layout Vulnerability</span>
              <span class="text-[11px] text-slate-400 font-mono">Confidence: ${(lim.confidence * 100).toFixed(0)}%</span>
            </div>
            <div class="font-semibold text-white text-xs">${lim.fact.claim}</div>
            <div class="text-slate-400 text-[11px] italic bg-slate-900 p-2 rounded border border-slate-800/80">"${lim.fact.source_quote}"</div>
            <div class="text-[11px] text-slate-400 border-t border-slate-800/80 pt-2"><strong class="text-slate-300">Analysis:</strong> ${lim.limitation_analysis}</div>
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
        <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs space-y-2">
          <div class="flex justify-between items-center">
            <span class="text-[11px] font-bold text-blue-400">#${i + 1} &bull; ${item.relationship_type.replace('_', ' ').toUpperCase()}</span>
            <span class="text-[11px] text-slate-400 font-mono">Confidence: ${(item.confidence * 100).toFixed(0)}% &bull; Signal: ${item.score}</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-[11px]">
            <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800/70">
              <span class="text-[10px] font-bold text-slate-400 block mb-0.5">Doc A (${item.fact_a.doc_filename}, Pg ${item.fact_a.page_number}):</span>
              <span class="text-slate-200 font-medium">${item.fact_a.claim}</span>
            </div>
            <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800/70">
              <span class="text-[10px] font-bold text-slate-400 block mb-0.5">Doc B (${item.fact_b.doc_filename}, Pg ${item.fact_b.page_number}):</span>
              <span class="text-slate-200 font-medium">${item.fact_b.claim}</span>
            </div>
          </div>
          <div class="text-[11px] text-slate-400 border-t border-slate-800/80 pt-2"><strong class="text-slate-300">Reasoning:</strong> ${item.explanation}</div>
        </div>
      `).join('');
    }

    async function loadFacts() {
      try {
        const res = await fetch('/api/facts');
        rawFacts = await res.json();
        document.getElementById('count-facts').innerText = rawFacts.length;
        document.getElementById('header-stats').innerText = `${rawDocuments.length} Docs &bull; ${rawFacts.length} Facts`;
        filterFacts();
      } catch (e) {
        console.error('Failed to load facts', e);
      }
    }

    function filterFacts() {
      const q = (document.getElementById('fact-search').value || '').toLowerCase();
      const doc = document.getElementById('doc-filter').value;

      const filtered = rawFacts.filter(f => {
        const matchesDoc = doc === 'all' || f.doc_filename === doc;
        const matchesQuery = !q ||
          (f.claim && f.claim.toLowerCase().includes(q)) ||
          (f.subject && f.subject.toLowerCase().includes(q)) ||
          (f.entities && f.entities.some(e => e.toLowerCase().includes(q)));
        return matchesDoc && matchesQuery;
      });

      document.getElementById('facts-counter-text').innerText = `Showing ${filtered.length} of ${rawFacts.length} verified facts`;
      const container = document.getElementById('facts-container');

      container.innerHTML = filtered.slice(0, 100).map(f => `
        <div class="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-4 shadow-md space-y-2.5 transition">
          <div class="flex justify-between items-center text-xs">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-blue-400 border border-slate-700">${f.category || 'General'}</span>
            <span class="text-[11px] font-mono text-emerald-400 font-semibold">${(f.confidence * 100).toFixed(0)}% Conf.</span>
          </div>
          <h4 class="font-bold text-white text-xs leading-snug">${f.claim}</h4>
          <div class="text-[11px] text-slate-400 flex items-center space-x-2">
            <span>📄 ${f.doc_filename}</span>
            <span>&bull;</span>
            <span>Page ${f.page_number}</span>
          </div>
          <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800/80 text-[11px] text-slate-400 italic">
            "${f.source_quote}"
          </div>
        </div>
      `).join('');
    }

    async function loadRelationships() {
      try {
        const res = await fetch('/api/relationships');
        rawRelationships = await res.json();
        document.getElementById('count-rels').innerText = rawRelationships.length;
        filterRelationships('all');
      } catch (e) {
        console.error('Failed to load relationships', e);
      }
    }

    function filterRelationships(type) {
      ['all', 'corroboration', 'contradiction', 'contextual_reconciliation'].forEach(t => {
        const btn = document.getElementById(`filter-rel-${t}`);
        if (t === type) {
          btn.className = 'rel-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 text-white shadow-sm transition';
        } else {
          btn.className = 'rel-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition';
        }
      });

      const filtered = rawRelationships.filter(r => {
        if (type === 'all') return true;
        return (r.relationship_type || '').toLowerCase().includes(type.toLowerCase());
      });

      document.getElementById('rel-filter-count').innerText = `Showing ${filtered.length} of ${rawRelationships.length} relationships`;
      const container = document.getElementById('relationships-container');

      container.innerHTML = filtered.map(r => {
        const fa = r.fact_a;
        const fb = r.fact_b;
        let badgeColor = 'bg-blue-500/10 text-blue-400 border-blue-500/30';
        if (r.relationship_type.includes('corroboration')) badgeColor = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
        if (r.relationship_type.includes('contradiction')) badgeColor = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
        if (r.relationship_type.includes('reconciliation')) badgeColor = 'bg-amber-500/10 text-amber-400 border-amber-500/30';

        return `
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-3">
            <div class="flex justify-between items-center">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider border ${badgeColor}">${r.relationship_type.replace('_', ' ')}</span>
              <span class="text-xs font-mono text-slate-400">Confidence: ${(r.confidence * 100).toFixed(0)}%</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1">
                <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Fact A</span>
                <p class="font-semibold text-white leading-snug">${fa ? fa.claim : r.fact_a_id}</p>
                <span class="text-blue-400 text-[11px] block">${fa ? `📄 ${fa.doc_filename} (Page ${fa.page_number})` : ''}</span>
              </div>
              <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1">
                <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Fact B</span>
                <p class="font-semibold text-white leading-snug">${fb ? fb.claim : r.fact_b_id}</p>
                <span class="text-indigo-400 text-[11px] block">${fb ? `📄 ${fb.doc_filename} (Page ${fb.page_number})` : ''}</span>
              </div>
            </div>

            <div class="bg-slate-950 p-3 rounded-lg border border-slate-800/70 text-xs text-slate-300 leading-relaxed">
              <strong class="text-slate-400 font-bold block mb-0.5 text-[10px] uppercase tracking-wider">Reconciliation Reasoning:</strong>
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
        document.getElementById('stat-docs').innerText = data.summary.total_documents;
        document.getElementById('stat-facts').innerText = data.summary.total_facts;
        document.getElementById('stat-rels').innerText = data.summary.total_relationships;
        document.getElementById('stat-contras').innerText = data.summary.contradictions;
        document.getElementById('json-preview').innerText = JSON.stringify(data, null, 2);
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
        container.classList.add('hidden');
        return;
      }
      container.classList.remove('hidden');
      count.innerText = selectedFiles.length;
      list.innerHTML = selectedFiles.map((f, i) => `
        <span class="inline-flex items-center px-3 py-1 rounded-lg text-xs font-medium bg-blue-500/10 text-blue-300 border border-blue-500/20">
          📄 ${f.name} (${(f.size / 1024).toFixed(0)} KB)
          <button type="button" onclick="removeFile(${i})" class="ml-2 text-blue-400 hover:text-rose-400 font-bold">&times;</button>
        </span>
      `).join('');
    }

    function removeFile(index) {
      selectedFiles.splice(index, 1);
      renderSelectedFiles();
    }

    function clearSelectedFiles() {
      selectedFiles = [];
      document.getElementById('pdf-file-input').value = '';
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

      statusDiv.classList.remove('hidden');
      uploadBtn.disabled = true;
      uploadBtn.classList.add('opacity-50', 'cursor-not-allowed');

      progressBar.style.width = '30%';
      statusPct.innerText = '30%';
      statusTitle.innerText = `Ingesting ${selectedFiles.length} PDF(s)...`;
      statusText.innerText = 'Parsing text streams, extracting markdown tables, and calling LLM fact triples...';

      try {
        const res = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        });

        if (!res.ok) throw new Error(`Upload error: ${res.status}`);
        const data = await res.json();

        progressBar.style.width = '100%';
        statusPct.innerText = '100%';
        statusTitle.innerText = 'Batch Processing & Reconciliation Complete!';
        statusText.innerText = `Successfully ingested ${data.results.length} files. Refreshing facts and cases...`;

        setTimeout(async () => {
          clearSelectedFiles();
          await init();
          uploadBtn.disabled = false;
          uploadBtn.classList.remove('opacity-50', 'cursor-not-allowed');
          statusDiv.classList.add('hidden');
          switchTab('cases');
          alert('Documents successfully ingested! Cases and relationships have been updated.');
        }, 1200);

      } catch (err) {
        progressBar.style.backgroundColor = '#ef4444';
        statusTitle.innerText = 'Upload Error';
        statusText.innerText = err.message;
        uploadBtn.disabled = false;
        uploadBtn.classList.remove('opacity-50', 'cursor-not-allowed');
      }
    }

    async function confirmReset() {
      const confirmAction = confirm(
        "🔄 RESET TO BENCHMARK BASELINE\n\n" +
        "This will restore the 3 benchmark Delhivery filings, 258 verified facts, and 47 relationships.\n\n" +
        "Click OK to restore benchmark baseline, or Cancel to keep current state."
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
