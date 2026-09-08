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
      background: rgba(15, 23, 42, 0.92);
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
      border-color: #3b82f6 !important;
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3), 0 10px 25px -5px rgba(0, 0, 0, 0.4);
      transform: translateY(-2px);
    }
    .hidden { display: none !important; }
    .nav-tab.active { background-color: #2563eb !important; color: #ffffff !important; }
  </style>
</head>
<body class="h-full text-slate-100 bg-slate-950 flex flex-col antialiased selection:bg-blue-500 selection:text-white">

  <!-- Top Navigation Bar -->
  <header class="glass-nav border-b border-slate-800/80 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 gap-4">
        
        <!-- Logo & Title -->
        <div class="flex items-center space-x-3.5 cursor-pointer" onclick="switchTab('cases')">
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
            <p class="text-[11px] text-slate-400 hidden sm:block">Cross-Document Evidence Grounding & Automated Reconciliation</p>
          </div>
        </div>

        <!-- Global Action Controls -->
        <div class="flex items-center space-x-3">
          <div class="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900/90 border border-slate-800 text-xs">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span class="text-slate-300 font-medium">Ready</span>
            <span class="text-slate-600">|</span>
            <span class="text-slate-400 font-mono" id="header-stats">3 Docs • 258 Facts • 47 Rels</span>
          </div>

          <button onclick="confirmReset()" title="Restore benchmark Delhivery dataset" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/90 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700/80 text-xs font-semibold transition shadow-sm">
            <svg class="w-3.5 h-3.5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>Reset to Benchmark</span>
          </button>

          <a href="/docs" target="_blank" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/90 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700/80 text-xs font-semibold transition shadow-sm">
            <span>API Docs</span>
            <svg class="w-3 h-3 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </a>
        </div>

      </div>

      <!-- Navigation Tabs -->
      <nav class="flex space-x-1 border-t border-slate-800/70 overflow-x-auto py-2 custom-scrollbar">
        <button type="button" onclick="switchTab('cases')" id="tab-cases-btn" class="nav-tab active px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 shadow-sm transition whitespace-nowrap flex items-center space-x-1.5">
          <span>✨</span> <span>The 4 Required Cases</span>
        </button>
        <button type="button" onclick="switchTab('documents')" id="tab-documents-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition whitespace-nowrap flex items-center space-x-1.5">
          <span>📄</span> <span>Data PDFs (<span id="count-docs-nav">3</span>)</span>
        </button>
        <button type="button" onclick="switchTab('facts')" id="tab-facts-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition whitespace-nowrap flex items-center space-x-1.5">
          <span>🔍</span> <span>Facts Explorer (<span id="count-facts">258</span>)</span>
        </button>
        <button type="button" onclick="switchTab('relationships')" id="tab-relationships-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition whitespace-nowrap flex items-center space-x-1.5">
          <span>🔗</span> <span>All Relationships (<span id="count-rels">47</span>)</span>
        </button>
        <button type="button" onclick="switchTab('upload')" id="tab-upload-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition whitespace-nowrap flex items-center space-x-1.5">
          <span>📤</span> <span>Upload & Ingestion</span>
        </button>
        <button type="button" onclick="switchTab('export')" id="tab-export-btn" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition whitespace-nowrap flex items-center space-x-1.5">
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
      
      <!-- Scope Filter Header & Quick Doc Badges -->
      <div class="bg-slate-900 border border-slate-800/90 rounded-2xl p-5 shadow-xl space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 class="text-lg font-bold text-white tracking-tight flex items-center space-x-2">
              <span>Executive Verification Suite</span>
            </h2>
            <p class="text-xs text-slate-400 mt-0.5">
              Interactive demonstration of the 4 required analytical scenarios with side-by-side evidence diffs.
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

        <!-- Ingested Data Filings Quick Bar -->
        <div class="pt-3 border-t border-slate-800/80">
          <div class="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center justify-between">
            <span>📚 Ingested Data Filings (Ground-Truth Corpus):</span>
            <button type="button" onclick="switchTab('documents')" class="text-blue-400 hover:text-blue-300 normal-case font-medium">View detailed PDF cards &rarr;</button>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5" id="active-docs-banner">
            <!-- Rendered by JS -->
          </div>
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
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2">Visual layout / tabular challenges & engineering mitigations.</p>
          <div class="mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Identified:</span>
            <span class="font-semibold text-purple-400" id="badge-limits-count">10 instances</span>
          </div>
        </div>

      </div>

      <!-- Spotlight Comparison Arena -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-5" id="spotlight-display-arena">
        <div class="p-8 text-center text-slate-500">Loading verified scenario evidence diff...</div>
      </div>

      <!-- Instance Drawer (Expandable Categorized List) -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
          <div>
            <h3 class="font-bold text-sm text-white" id="category-drawer-title">All Discovered Corroborations</h3>
            <p class="text-xs text-slate-400">Browse every reconciled evidence pair discovered across filings.</p>
          </div>
          <div class="flex items-center space-x-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800">
            <button type="button" onclick="switchCategoryView('corroborations')" id="cat-btn-corroborations" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-600 text-white shadow-sm transition">Corroborations</button>
            <button type="button" onclick="switchCategoryView('contradictions')" id="cat-btn-contradictions" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:text-white border border-slate-700 transition">Contradictions</button>
            <button type="button" onclick="switchCategoryView('reconciliations')" id="cat-btn-reconciliations" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:text-white border border-slate-700 transition">Reconciliations</button>
            <button type="button" onclick="switchCategoryView('limitations')" id="cat-btn-limitations" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:text-white border border-slate-700 transition">Limitations</button>
          </div>
        </div>

        <div class="space-y-3 max-h-96 overflow-y-auto custom-scrollbar pr-1" id="category-instances-container">
          <div class="p-4 text-center text-slate-500 text-xs">Loading instances...</div>
        </div>
      </div>

    </section>

    <!-- ======================================================== -->
    <!-- VIEW 2: DATA PDFS (SOURCE FILINGS VIEW) -->
    <!-- ======================================================== -->
    <section id="view-documents" class="space-y-6 hidden">
      <div class="bg-slate-900 border border-slate-800/90 rounded-2xl p-5 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 class="text-lg font-bold text-white tracking-tight flex items-center space-x-2">
            <span>📄</span> <span>Ingested Knowledge Base Filings</span>
          </h2>
          <p class="text-xs text-slate-400 mt-0.5">
            Full repository of source documents parsed, chunked, and indexed with ground-truth evidence quotes and page numbers.
          </p>
        </div>
        <button type="button" onclick="switchTab('upload')" class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-lg shadow-blue-600/20 transition flex items-center space-x-1.5 self-start md:self-auto">
          <span>+ Ingest Additional PDFs</span>
        </button>
      </div>

      <!-- Detailed Documents Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5" id="documents-showcase-grid">
        <div class="p-8 text-center text-slate-500 col-span-3">Loading documents...</div>
      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 3: FACTS EXPLORER -->
    <!-- ======================================================== -->
    <section id="view-facts" class="space-y-6 hidden">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 class="text-lg font-bold text-white tracking-tight">Facts Explorer</h2>
            <p class="text-xs text-slate-400 mt-0.5">Browse atomic extracted facts with citations, entities, and attributes.</p>
          </div>
          <span class="text-xs text-slate-400 font-mono" id="facts-counter-text">Showing facts...</span>
        </div>

        <!-- Filter Controls -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="md:col-span-2 relative">
            <input type="text" id="fact-search" oninput="filterFacts()" placeholder="Search claims, subjects, entities, or keywords..." class="w-full bg-slate-950 text-white text-xs rounded-xl border border-slate-800 px-4 py-2.5 pl-9 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none">
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
      </div>

      <!-- Facts Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="facts-container">
        <div class="p-8 text-center text-slate-500 col-span-2">Loading facts...</div>
      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 4: ALL RELATIONSHIPS -->
    <!-- ======================================================== -->
    <section id="view-relationships" class="space-y-6 hidden">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 class="text-lg font-bold text-white tracking-tight">Cross-Document Relationships</h2>
          <p class="text-xs text-slate-400 mt-0.5">Semantic pairings evaluated and classified by the reconciliation engine.</p>
        </div>

        <!-- Type Filter Buttons -->
        <div class="flex items-center space-x-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800">
          <button type="button" onclick="filterRelationships('all')" id="filter-rel-all" class="rel-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 text-white shadow-sm transition">All</button>
          <button type="button" onclick="filterRelationships('corroboration')" id="filter-rel-corroboration" class="rel-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition">Corroborations</button>
          <button type="button" onclick="filterRelationships('contradiction')" id="filter-rel-contradiction" class="rel-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition">Contradictions</button>
          <button type="button" onclick="filterRelationships('contextual_reconciliation')" id="filter-rel-contextual_reconciliation" class="rel-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition">Reconciliations</button>
        </div>
      </div>

      <div class="text-xs text-slate-400 font-mono" id="rel-filter-count">Showing relationships...</div>

      <div class="space-y-4" id="relationships-container">
        <div class="p-8 text-center text-slate-500">Loading relationships...</div>
      </div>
    </section>

    <!-- ======================================================== -->
    <!-- VIEW 5: MULTI-PDF INGESTION STUDIO -->
    <!-- ======================================================== -->
    <section id="view-upload" class="space-y-6 hidden">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Upload Studio Box -->
        <div class="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
          <div>
            <h2 class="text-lg font-bold text-white tracking-tight">Batch PDF Ingestion Studio</h2>
            <p class="text-xs text-slate-400 mt-0.5">Select or drop one or multiple PDF documents to parse, extract facts, and reconcile.</p>
          </div>

          <!-- Dropzone -->
          <form id="upload-form" onsubmit="handleBatchUpload(event)">
            <label for="pdf-file-input" class="flex flex-col items-center justify-center p-8 border-2 border-dashed border-slate-700 hover:border-blue-500 rounded-2xl cursor-pointer bg-slate-950/60 hover:bg-slate-950 transition group">
              <div class="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center group-hover:scale-110 transition duration-200 mb-3">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <p class="text-xs font-semibold text-slate-200 mb-1">Click to browse or drag and drop PDFs here</p>
              <p class="text-[11px] text-slate-500">Supports batch selection (.pdf format)</p>
              <input type="file" id="pdf-file-input" multiple accept=".pdf" class="hidden" onchange="handleFileSelect(event)">
            </label>

            <!-- File List Chips -->
            <div id="selected-files-container" class="mt-4 hidden space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-semibold text-slate-300">Selected Files (<span id="selected-files-count">0</span>):</span>
                <button type="button" onclick="clearSelectedFiles()" class="text-rose-400 hover:text-rose-300 text-[11px]">Clear All</button>
              </div>
              <div id="file-chips-list" class="flex flex-wrap gap-2"></div>
            </div>

            <!-- Ingest Action Button -->
            <div class="mt-5 flex justify-end">
              <button type="submit" id="upload-btn" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-lg shadow-blue-600/20 transition flex items-center space-x-2">
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
              <span class="font-semibold text-white" id="upload-status-title">Ingesting PDFs...</span>
              <span class="text-blue-400 font-mono" id="upload-status-pct">0%</span>
            </div>
            <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div id="upload-progress-bar" class="bg-gradient-to-r from-blue-500 to-indigo-500 h-full w-0 transition-all duration-300"></div>
            </div>
            <p class="text-[11px] text-slate-400" id="upload-status-text">Parsing text and extracting facts...</p>
          </div>
        </div>

        <!-- Ingested Documents List Sidecard -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
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
    <!-- VIEW 6: KNOWLEDGE GRAPH JSON & EXPORT -->
    <!-- ======================================================== -->
    <section id="view-export" class="space-y-6 hidden">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 class="text-lg font-bold text-white tracking-tight">Knowledge Graph Export</h2>
            <p class="text-xs text-slate-400 mt-0.5">Machine-readable JSON schema containing documents, facts, and relationships.</p>
          </div>
          <div class="flex items-center space-x-2">
            <button type="button" onclick="copyExportJson()" class="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700 text-xs font-semibold transition">
              📋 Copy JSON
            </button>
            <a href="/api/export" download="knowledge_graph_export.json" class="px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition shadow-sm">
              ⬇️ Download File
            </a>
          </div>
        </div>

        <!-- Metric Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Documents</span>
            <span class="text-xl font-extrabold text-white" id="stat-docs">3</span>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Facts</span>
            <span class="text-xl font-extrabold text-white" id="stat-facts">258</span>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Relationships</span>
            <span class="text-xl font-extrabold text-white" id="stat-rels">47</span>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Contradictions</span>
            <span class="text-xl font-extrabold text-rose-400" id="stat-contras">2</span>
          </div>
        </div>

        <pre class="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-slate-300 max-h-96 overflow-y-auto custom-scrollbar" id="json-preview">Loading Knowledge Graph JSON...</pre>
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
      // Parallel fetch using Promise.allSettled for maximum resilience & speed
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
            btn.className = 'nav-tab active px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 shadow-sm transition whitespace-nowrap flex items-center space-x-1.5';
          } else {
            btn.className = 'nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition whitespace-nowrap flex items-center space-x-1.5';
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
            <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between text-xs group hover:border-slate-700 transition">
              <div class="flex items-center space-x-2.5 min-w-0">
                <span class="w-6 h-6 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center font-bold text-[10px]">PDF</span>
                <div class="min-w-0 truncate">
                  <div class="font-bold text-white truncate" title="${d.filename}">${d.filename}</div>
                  <div class="text-[10px] text-slate-400">${d.page_count} Pages &bull; Indexed</div>
                </div>
              </div>
              <button type="button" onclick="inspectDocCases('${d.id}')" class="ml-2 px-2 py-1 rounded bg-slate-900 hover:bg-blue-600 text-slate-300 hover:text-white text-[10px] font-semibold border border-slate-700 transition whitespace-nowrap">Filter</button>
            </div>
          `).join('');
        }

        // Update dedicated documents showcase grid
        const grid = document.getElementById('documents-showcase-grid');
        if (grid) {
          grid.innerHTML = rawDocuments.map((d, i) => `
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4 hover:border-slate-700 transition flex flex-col justify-between">
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-blue-500/10 text-blue-400 border border-blue-500/20">
                    Filing #${i + 1}
                  </span>
                  <span class="text-[11px] text-slate-500 font-mono">${(d.upload_time || '').split('T')[0]}</span>
                </div>
                <div>
                  <h4 class="font-bold text-sm text-white leading-snug break-words">${d.filename}</h4>
                  <p class="text-xs text-slate-400 mt-1">Ground-truth PDF ingested with page-indexed text & table chunks.</p>
                </div>
                <div class="grid grid-cols-2 gap-2 pt-2 border-t border-slate-800/80 text-xs">
                  <div class="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                    <span class="text-[10px] font-bold text-slate-500 block">Total Pages:</span>
                    <span class="text-sm font-extrabold text-white font-mono">${d.page_count}</span>
                  </div>
                  <div class="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                    <span class="text-[10px] font-bold text-slate-500 block">Status:</span>
                    <span class="text-xs font-bold text-emerald-400">Indexed &bull; Active</span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2 pt-3 border-t border-slate-800/80">
                <button type="button" onclick="inspectDocCases('${d.id}')" class="flex-1 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition text-center shadow-sm">
                  ✨ View Cases
                </button>
                <button type="button" onclick="inspectDocFacts('${d.filename}')" class="flex-1 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700 text-xs font-semibold transition text-center">
                  🔍 View Facts
                </button>
              </div>
            </div>
          `).join('');
        }

        // Update list on upload tab
        const listDiv = document.getElementById('ingested-docs-list');
        if (listDiv) {
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
            btn.classList.add('active-case');
          } else {
            btn.classList.remove('active-case');
          }
        }
      }
      renderSpotlightArena();
    }

    function renderSpotlightArena() {
      const arena = document.getElementById('spotlight-display-arena');
      if (!arena) return;

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
            <span class="text-emerald-400 font-bold">${rel ? (rel.confidence * 100).toFixed(0) : (fa && fa.confidence ? (fa.confidence * 100).toFixed(0) : 100)}%</span>
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
                📄 ${fa ? fa.doc_filename : 'Document A'} &bull; Page ${fa ? fa.page_number : 'N/A'}
              </span>
            </div>

            <div class="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800/80">
              <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block mb-1">Stated Claim:</span>
              <p class="text-sm font-semibold text-white leading-snug">${fa ? fa.claim : 'No claim statement available.'}</p>
            </div>

            <div class="p-3.5 rounded-xl bg-slate-900/40 border border-slate-800/60 text-xs">
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center space-x-1 mb-1">
                <span>💬</span> <span>Verbatim Source Quote:</span>
              </span>
              <p class="text-slate-300 italic leading-relaxed text-xs pl-2 border-l-2 border-blue-500/60">
                "${fa ? fa.source_quote : ''}"
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
        if (btn) {
          if (c === category) {
            btn.className = 'px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-600 text-white shadow-sm transition';
          } else {
            btn.className = 'px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:text-white border border-slate-700 transition';
          }
        }
      });

      const titleMap = {
        'corroborations': 'All Discovered Corroborations',
        'contradictions': 'All Discovered Contradictions',
        'reconciliations': 'All Discovered Contextual Reconciliations',
        'limitations': 'Identified Extraction Limitations & Edge Cases'
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
              <span class="text-[10px] font-bold text-slate-400 block mb-0.5">Doc A (${item.fact_a ? item.fact_a.doc_filename : 'A'}, Pg ${item.fact_a ? item.fact_a.page_number : ''}):</span>
              <span class="text-slate-200 font-medium">${item.fact_a ? item.fact_a.claim : ''}</span>
            </div>
            <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800/70">
              <span class="text-[10px] font-bold text-slate-400 block mb-0.5">Doc B (${item.fact_b ? item.fact_b.doc_filename : 'B'}, Pg ${item.fact_b ? item.fact_b.page_number : ''}):</span>
              <span class="text-slate-200 font-medium">${item.fact_b ? item.fact_b.claim : ''}</span>
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
        const fCount = document.getElementById('count-facts');
        if (fCount) fCount.innerText = rawFacts.length;
        
        const hStats = document.getElementById('header-stats');
        if (hStats) hStats.innerText = `${rawDocuments.length} Docs • ${rawFacts.length} Facts • ${rawRelationships.length} Rels`;
        
        filterFacts();
      } catch (e) {
        console.error('Failed to load facts', e);
      }
    }

    function filterFacts() {
      const q = (document.getElementById('fact-search') ? document.getElementById('fact-search').value : '').toLowerCase();
      const doc = document.getElementById('doc-filter') ? document.getElementById('doc-filter').value : 'all';

      const filtered = rawFacts.filter(f => {
        const matchesDoc = doc === 'all' || f.doc_filename === doc;
        const matchesQuery = !q ||
          (f.claim && f.claim.toLowerCase().includes(q)) ||
          (f.subject && f.subject.toLowerCase().includes(q)) ||
          (f.entities && f.entities.some(e => e.toLowerCase().includes(q)));
        return matchesDoc && matchesQuery;
      });

      const counter = document.getElementById('facts-counter-text');
      if (counter) counter.innerText = `Showing ${filtered.length} of ${rawFacts.length} verified facts`;
      
      const container = document.getElementById('facts-container');
      if (!container) return;

      if (!filtered.length) {
        container.innerHTML = '<div class="col-span-2 p-8 text-center text-slate-500 text-xs">No facts match your search criteria.</div>';
        return;
      }

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
        const rCount = document.getElementById('count-rels');
        if (rCount) rCount.innerText = rawRelationships.length;
        
        const hStats = document.getElementById('header-stats');
        if (hStats) hStats.innerText = `${rawDocuments.length} Docs • ${rawFacts.length} Facts • ${rawRelationships.length} Rels`;

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
            btn.className = 'rel-btn px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition';
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
            📄 ${f.name} (${(f.size / 1024).toFixed(0)} KB)
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
      if (statusTitle) statusTitle.innerText = `Ingesting ${selectedFiles.length} PDF(s)...`;
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
