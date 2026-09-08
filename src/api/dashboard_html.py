def get_dashboard_html() -> str:
    """Returns the standalone HTML/JS dashboard interface."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fact Knowledge Layer | Superjoin Enterprise</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; }
    .tab-btn.active { background-color: #2563eb; color: white; }
    .case-subtab.active { border-color: #2563eb; color: #2563eb; font-weight: 700; }
    .quote-box { border-left: 3px solid #cbd5e1; }
  </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col">

  <!-- Top Navigation Header -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 py-3 sm:px-6 lg:px-8 flex flex-wrap justify-between items-center gap-4">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-md text-xl">
          🔍
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h1 class="text-xl font-extrabold text-slate-900 tracking-tight">Fact Knowledge Layer</h1>
            <span class="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider bg-blue-100 text-blue-800 rounded-full">v1.0 Production</span>
          </div>
          <p class="text-xs text-slate-500 font-medium">Cross-Document Evidence Grounding &bull; Verifiable Reconciliation &bull; Zero Hardcoding</p>
        </div>
      </div>
      <div class="flex items-center space-x-3">
        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
          <span class="w-2 h-2 mr-1.5 bg-emerald-500 rounded-full animate-pulse"></span> Engine Ready
        </span>
        <button onclick="confirmReset()" class="px-3 py-1.5 text-xs font-semibold text-rose-700 hover:text-white hover:bg-rose-600 border border-rose-200 rounded-lg transition flex items-center space-x-1">
          <span>🗑️</span> <span>Reset DB</span>
        </button>
        <a href="/docs" target="_blank" class="px-3 py-1.5 text-xs font-semibold text-slate-700 hover:text-blue-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition">
          API Specs &rarr;
        </a>
      </div>
    </div>

    <!-- Tabs Nav -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-1 sm:space-x-2 border-t border-slate-100 overflow-x-auto py-2">
      <button onclick="switchTab('cases')" id="tab-cases-btn" class="tab-btn active px-4 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition whitespace-nowrap">
        ✅ The 4 Required Cases
      </button>
      <button onclick="switchTab('facts')" id="tab-facts-btn" class="tab-btn px-4 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition whitespace-nowrap">
        🔍 Facts Explorer (<span id="count-facts">0</span>)
      </button>
      <button onclick="switchTab('relationships')" id="tab-relationships-btn" class="tab-btn px-4 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition whitespace-nowrap">
        🔗 Relationships (<span id="count-rels">0</span>)
      </button>
      <button onclick="switchTab('upload')" id="tab-upload-btn" class="tab-btn px-4 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition whitespace-nowrap">
        📤 Upload PDFs (<span id="count-docs">0</span>)
      </button>
      <button onclick="switchTab('export')" id="tab-export-btn" class="tab-btn px-4 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition whitespace-nowrap">
        📊 Export & Graph JSON
      </button>
    </div>
  </header>

  <!-- Main Content Container -->
  <main class="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex-1 w-full">
    
    <!-- TAB 1: THE FOUR REQUIRED CASES -->
    <section id="view-cases" class="space-y-6">
      
      <!-- Top banner with Document Filter -->
      <div class="bg-gradient-to-r from-blue-900 to-indigo-900 rounded-2xl p-6 text-white shadow-md flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <span class="px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-blue-500/30 text-blue-200 border border-blue-400/30">
            Core Assignment Showcase
          </span>
          <h2 class="text-xl font-bold mt-2">The Four Required Analytical Scenarios</h2>
          <p class="text-xs text-blue-200 mt-1 max-w-2xl">
            Strict ground-truth extraction demonstrating Corroboration, Contradiction, Contextual Reconciliation, and Extraction Limitations with verbatim quotes.
          </p>
        </div>
        <div class="w-full md:w-72 bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/20">
          <label for="case-doc-filter" class="block text-xs font-semibold text-blue-200 uppercase tracking-wider mb-1">
            Filter by Document:
          </label>
          <select id="case-doc-filter" onchange="onCaseDocFilterChange()" class="w-full bg-white text-slate-800 text-xs font-medium rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-400">
            <option value="">All Documents (Global Knowledge Graph)</option>
          </select>
        </div>
      </div>

      <!-- Spotlight Summary Cards -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div onclick="filterCaseCategory('corroborations')" class="cursor-pointer bg-white p-4 rounded-xl border border-slate-200 hover:border-emerald-400 hover:shadow transition">
          <div class="flex justify-between items-center">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Case 1: Corroborations</span>
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
          </div>
          <div class="text-2xl font-black text-emerald-700 mt-2" id="count-case-corrobs">0</div>
          <span class="text-[11px] text-slate-500">Cross-verified agreements</span>
        </div>
        <div onclick="filterCaseCategory('contradictions')" class="cursor-pointer bg-white p-4 rounded-xl border border-slate-200 hover:border-rose-400 hover:shadow transition">
          <div class="flex justify-between items-center">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Case 2: Contradictions</span>
            <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
          </div>
          <div class="text-2xl font-black text-rose-700 mt-2" id="count-case-contras">0</div>
          <span class="text-[11px] text-slate-500">Genuine factual conflicts</span>
        </div>
        <div onclick="filterCaseCategory('reconciliations')" class="cursor-pointer bg-white p-4 rounded-xl border border-slate-200 hover:border-amber-400 hover:shadow transition">
          <div class="flex justify-between items-center">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Case 3: Reconciliations</span>
            <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
          </div>
          <div class="text-2xl font-black text-amber-700 mt-2" id="count-case-recs">0</div>
          <span class="text-[11px] text-slate-500">Contextual / timing nuances</span>
        </div>
        <div onclick="filterCaseCategory('limitations')" class="cursor-pointer bg-white p-4 rounded-xl border border-slate-200 hover:border-purple-400 hover:shadow transition">
          <div class="flex justify-between items-center">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Case 4: Limitations</span>
            <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
          </div>
          <div class="text-2xl font-black text-purple-700 mt-2" id="count-case-limits">0</div>
          <span class="text-[11px] text-slate-500">Layout & table challenges</span>
        </div>
      </div>

      <!-- Sub-tab Bar to toggle between Featured Showcase and Full Lists -->
      <div class="border-b border-slate-200 flex space-x-6">
        <button onclick="filterCaseCategory('spotlight')" id="csub-spotlight" class="case-subtab active py-2.5 text-sm border-b-2 border-transparent transition">
          🌟 4 Spotlight Cases
        </button>
        <button onclick="filterCaseCategory('corroborations')" id="csub-corroborations" class="case-subtab py-2.5 text-sm border-b-2 border-transparent text-slate-500 hover:text-slate-800 transition">
          All Corroborations (<span id="csub-corrobs-badge">0</span>)
        </button>
        <button onclick="filterCaseCategory('contradictions')" id="csub-contradictions" class="case-subtab py-2.5 text-sm border-b-2 border-transparent text-slate-500 hover:text-slate-800 transition">
          All Contradictions (<span id="csub-contras-badge">0</span>)
        </button>
        <button onclick="filterCaseCategory('reconciliations')" id="csub-reconciliations" class="case-subtab py-2.5 text-sm border-b-2 border-transparent text-slate-500 hover:text-slate-800 transition">
          All Reconciliations (<span id="csub-recs-badge">0</span>)
        </button>
        <button onclick="filterCaseCategory('limitations')" id="csub-limitations" class="case-subtab py-2.5 text-sm border-b-2 border-transparent text-slate-500 hover:text-slate-800 transition">
          All Limitations (<span id="csub-limits-badge">0</span>)
        </button>
      </div>

      <!-- Cases Content List -->
      <div id="cases-container" class="space-y-6">
        <div class="p-8 text-center text-slate-500 animate-pulse">Loading verified cases from knowledge engine...</div>
      </div>
    </section>

    <!-- TAB 2: FACTS EXPLORER -->
    <section id="view-facts" class="space-y-6 hidden">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex-1 w-full">
          <input type="text" id="fact-search" oninput="filterFacts()" placeholder="Search claims, entities, metrics (e.g. EBITDA, revenue, director, appointed)..." class="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
        <div class="w-full sm:w-64">
          <select id="doc-filter" onchange="filterFacts()" class="w-full px-3 py-2.5 rounded-lg border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="all">All Documents</option>
          </select>
        </div>
      </div>

      <div class="text-sm text-slate-500 font-medium" id="facts-counter-text">Showing facts...</div>
      <div id="facts-container" class="grid grid-cols-1 md:grid-cols-2 gap-4"></div>
    </section>

    <!-- TAB 3: RELATIONSHIPS -->
    <section id="view-relationships" class="space-y-6 hidden">
      <div class="flex flex-wrap gap-2 bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
        <button onclick="filterRelationships('all')" class="rel-filter active px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 text-white" id="filter-rel-all">All Relationships</button>
        <button onclick="filterRelationships('corroboration')" class="rel-filter px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200" id="filter-rel-corroboration">Corroborations</button>
        <button onclick="filterRelationships('contradiction')" class="rel-filter px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200" id="filter-rel-contradiction">Contradictions</button>
        <button onclick="filterRelationships('contextual_reconciliation')" class="rel-filter px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200" id="filter-rel-contextual_reconciliation">Contextual Reconciliations</button>
      </div>

      <div id="relationships-container" class="space-y-4"></div>
    </section>

    <!-- TAB 4: UPLOAD DOCUMENTS (MULTI-FILE BATCH) -->
    <section id="view-upload" class="space-y-6 hidden">
      <div class="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm max-w-3xl mx-auto">
        <div class="text-center">
          <div class="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mx-auto text-2xl font-bold mb-3 shadow-inner">
            📄
          </div>
          <h3 class="text-xl font-extrabold text-slate-900">Multi-PDF Ingestion Engine</h3>
          <p class="text-xs text-slate-500 mt-1 max-w-md mx-auto">
            Select one or multiple PDF documents simultaneously. The engine will extract facts, compute embeddings, run cross-document reconciliation, and update the 4 cases.
          </p>
        </div>

        <form id="upload-form" class="mt-6 space-y-4" onsubmit="handleBatchUpload(event)">
          <div class="border-2 border-dashed border-slate-300 rounded-xl p-6 text-center hover:border-blue-500 transition cursor-pointer" onclick="document.getElementById('pdf-file-input').click()">
            <input type="file" id="pdf-file-input" multiple accept=".pdf" onchange="handleFileSelect(event)" class="hidden">
            <div class="text-3xl mb-2">📁</div>
            <p class="text-sm font-semibold text-slate-700">Click to browse or drag & drop PDF files</p>
            <p class="text-xs text-slate-400 mt-1">Accepts multiple corporate filings, annual reports, or investor releases</p>
          </div>

          <!-- File Chips Preview -->
          <div id="selected-files-container" class="space-y-2 hidden">
            <div class="flex justify-between items-center">
              <span class="text-xs font-bold text-slate-600 uppercase tracking-wider">Selected Files:</span>
              <button type="button" onclick="clearSelectedFiles()" class="text-xs text-rose-600 hover:underline">Clear list</button>
            </div>
            <div id="file-chips-list" class="flex flex-wrap gap-2"></div>
          </div>

          <button type="submit" id="upload-btn" class="w-full py-3.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm transition shadow-sm flex items-center justify-center space-x-2">
            <span>⚡ Start Ingestion & Reconciliation</span>
          </button>
        </form>

        <!-- Upload Status & Progress -->
        <div id="upload-status" class="mt-6 hidden bg-slate-50 p-4 rounded-xl border border-slate-200">
          <div class="flex justify-between items-center text-xs font-semibold text-slate-700 mb-1.5">
            <span id="upload-status-title">Processing queue...</span>
            <span id="upload-status-pct">0%</span>
          </div>
          <div class="w-full bg-slate-200 rounded-full h-2.5 overflow-hidden">
            <div id="upload-progress-bar" class="bg-blue-600 h-2.5 rounded-full w-0 transition-all duration-300"></div>
          </div>
          <p id="upload-status-text" class="text-xs text-slate-500 mt-2 font-mono"></p>
        </div>

        <!-- Ingested Documents List -->
        <div class="mt-8 border-t border-slate-100 pt-6">
          <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Currently Ingested Documents (<span id="ingested-docs-count">0</span>)</h4>
          <div id="ingested-docs-list" class="space-y-2"></div>
        </div>
      </div>
    </section>

    <!-- TAB 5: EXPORT & STATS -->
    <section id="view-export" class="space-y-6 hidden">
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Documents</span>
          <div class="text-2xl font-bold text-slate-900 mt-1" id="stat-docs">0</div>
        </div>
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Semantic Facts</span>
          <div class="text-2xl font-bold text-blue-600 mt-1" id="stat-facts">0</div>
        </div>
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Relationships</span>
          <div class="text-2xl font-bold text-emerald-600 mt-1" id="stat-rels">0</div>
        </div>
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Contradictions</span>
          <div class="text-2xl font-bold text-rose-600 mt-1" id="stat-contras">0</div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex justify-between items-center mb-4">
          <div>
            <h3 class="font-bold text-slate-900">Complete Knowledge Graph Export</h3>
            <p class="text-xs text-slate-500 mt-0.5">Fully structured JSON artifact containing all documents, facts, and reconciled relationships.</p>
          </div>
          <a href="/api/export" download="results.json" class="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-sm font-semibold transition">
            📥 Download results.json
          </a>
        </div>
        <pre id="json-preview" class="bg-slate-900 text-slate-200 p-4 rounded-lg text-xs overflow-x-auto max-h-96 font-mono"></pre>
      </div>
    </section>

  </main>

  <script>
    let rawFacts = [];
    let rawRelationships = [];
    let rawDocuments = [];
    let casesBreakdown = null;
    let currentCaseCategory = 'spotlight';
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
        document.getElementById(`view-${t}`).classList.add('hidden');
        document.getElementById(`tab-${t}-btn`).classList.remove('active', 'bg-blue-600', 'text-white');
      });
      document.getElementById(`view-${tabId}`).classList.remove('hidden');
      document.getElementById(`tab-${tabId}-btn`).classList.add('active', 'bg-blue-600', 'text-white');
    }

    async function loadDocuments() {
      try {
        const res = await fetch('/api/documents');
        rawDocuments = await res.json();
        document.getElementById('count-docs').innerText = rawDocuments.length;
        document.getElementById('ingested-docs-count').innerText = rawDocuments.length;
        
        // Populate case doc filter dropdown
        const caseDocSelect = document.getElementById('case-doc-filter');
        const prevCaseVal = caseDocSelect.value;
        caseDocSelect.innerHTML = '<option value="">All Documents (Global Knowledge Graph)</option>' + 
          rawDocuments.map(d => `<option value="${d.id}">${d.filename} (${d.page_count} pgs)</option>`).join('');
        if (prevCaseVal) caseDocSelect.value = prevCaseVal;

        // Populate doc filter dropdown in facts tab
        const docSelect = document.getElementById('doc-filter');
        docSelect.innerHTML = '<option value="all">All Documents</option>' + 
          rawDocuments.map(d => `<option value="${d.filename}">${d.filename}</option>`).join('');

        // Render Ingested Docs List in Upload tab
        const listDiv = document.getElementById('ingested-docs-list');
        if (!rawDocuments.length) {
          listDiv.innerHTML = '<div class="text-xs text-slate-400 italic">No documents ingested yet. Upload PDFs above.</div>';
        } else {
          listDiv.innerHTML = rawDocuments.map(d => `
            <div class="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200/70 text-xs">
              <div class="flex items-center space-x-2">
                <span class="text-base">📄</span>
                <div>
                  <span class="font-bold text-slate-800">${d.filename}</span>
                  <span class="text-slate-400 ml-2">${d.page_count} pages</span>
                </div>
              </div>
              <span class="text-slate-400 text-[11px]">${(d.upload_time || '').split('T')[0]}</span>
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
        if (docId) {
          url += `?doc_id=${encodeURIComponent(docId)}`;
        }
        const res = await fetch(url);
        casesBreakdown = await res.json();

        // Update counts
        const c = casesBreakdown.counts || {};
        document.getElementById('count-case-corrobs').innerText = c.corroborations || 0;
        document.getElementById('count-case-contras').innerText = c.contradictions || 0;
        document.getElementById('count-case-recs').innerText = c.reconciliations || 0;
        document.getElementById('count-case-limits').innerText = c.limitations || 0;

        document.getElementById('csub-corrobs-badge').innerText = c.corroborations || 0;
        document.getElementById('csub-contras-badge').innerText = c.contradictions || 0;
        document.getElementById('csub-recs-badge').innerText = c.reconciliations || 0;
        document.getElementById('csub-limits-badge').innerText = c.limitations || 0;

        renderCurrentCaseCategory();
      } catch (e) {
        console.error('Failed to load cases breakdown', e);
      }
    }

    function filterCaseCategory(cat) {
      currentCaseCategory = cat;
      ['spotlight', 'corroborations', 'contradictions', 'reconciliations', 'limitations'].forEach(k => {
        const btn = document.getElementById(`csub-${k}`);
        if (btn) {
          if (k === cat) {
            btn.classList.add('active', 'border-blue-600', 'text-blue-600', 'font-bold');
            btn.classList.remove('text-slate-500');
          } else {
            btn.classList.remove('active', 'border-blue-600', 'text-blue-600', 'font-bold');
            btn.classList.add('text-slate-500');
          }
        }
      });
      renderCurrentCaseCategory();
    }

    function renderCurrentCaseCategory() {
      const container = document.getElementById('cases-container');
      if (!casesBreakdown) {
        container.innerHTML = '<div class="p-8 text-center text-slate-400">Loading cases...</div>';
        return;
      }

      if (currentCaseCategory === 'spotlight') {
        renderFeaturedSpotlight(casesBreakdown.featured_cases || []);
      } else if (currentCaseCategory === 'corroborations') {
        renderRelationshipList(casesBreakdown.corroborations || [], 'Corroboration', 'bg-emerald-100 text-emerald-800 border-emerald-200');
      } else if (currentCaseCategory === 'contradictions') {
        renderRelationshipList(casesBreakdown.contradictions || [], 'Contradiction', 'bg-rose-100 text-rose-800 border-rose-200');
      } else if (currentCaseCategory === 'reconciliations') {
        renderRelationshipList(casesBreakdown.reconciliations || [], 'Contextual Reconciliation', 'bg-amber-100 text-amber-800 border-amber-200');
      } else if (currentCaseCategory === 'limitations') {
        renderLimitationsList(casesBreakdown.limitations || []);
      }
    }

    function renderFeaturedSpotlight(cases) {
      const container = document.getElementById('cases-container');
      if (!cases || cases.length === 0) {
        container.innerHTML = '<div class="p-8 text-center text-slate-500">No cases matching the current document filter.</div>';
        return;
      }

      container.innerHTML = cases.map(c => {
        let badgeClass = 'bg-blue-100 text-blue-800 border-blue-200';
        let badgeText = c.case_label;
        if (c.case_label.includes('Corroborat')) {
          badgeClass = 'bg-emerald-100 text-emerald-800 border-emerald-200';
        } else if (c.case_label.includes('Contradiction')) {
          badgeClass = 'bg-rose-100 text-rose-800 border-rose-200';
        } else if (c.case_label.includes('Reconciliation')) {
          badgeClass = 'bg-amber-100 text-amber-800 border-amber-200';
        } else if (c.case_label.includes('Limitation') || c.case_label.includes('Failure')) {
          badgeClass = 'bg-purple-100 text-purple-800 border-purple-200';
        }

        return `
          <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm hover:shadow-md transition">
            <div class="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
              <div class="flex items-center space-x-3">
                <span class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center font-bold text-sm text-slate-700">#${c.case_number}</span>
                <span class="px-3 py-1 rounded-full text-xs font-bold border ${badgeClass}">${badgeText}</span>
              </div>
              <span class="text-xs text-slate-400 font-medium">Verifiable Citation Grounding</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-slate-50 p-4 rounded-lg border border-slate-100">
                <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500">Evidence A</span>
                <h4 class="font-semibold text-slate-900 text-sm mt-1">${c.fact_a.claim}</h4>
                <div class="text-xs text-blue-600 font-medium mt-1">📄 ${c.fact_a.doc_filename} (Page ${c.fact_a.page_number})</div>
                <div class="mt-2 text-xs italic text-slate-600 bg-white p-2.5 rounded border border-slate-200 quote-box">
                  "${c.fact_a.source_quote}"
                </div>
              </div>

              ${c.fact_b ? `
              <div class="bg-slate-50 p-4 rounded-lg border border-slate-100">
                <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500">Evidence B</span>
                <h4 class="font-semibold text-slate-900 text-sm mt-1">${c.fact_b.claim}</h4>
                <div class="text-xs text-blue-600 font-medium mt-1">📄 ${c.fact_b.doc_filename} (Page ${c.fact_b.page_number})</div>
                <div class="mt-2 text-xs italic text-slate-600 bg-white p-2.5 rounded border border-slate-200 quote-box">
                  "${c.fact_b.source_quote}"
                </div>
              </div>` : `
              <div class="bg-purple-50 p-4 rounded-lg border border-purple-100 flex flex-col justify-center text-xs text-purple-900">
                <strong class="font-bold">Extraction Challenge Assessment:</strong>
                <p class="mt-1 leading-relaxed text-[11px]">Un-nested title sequence in PDF layout. Standard spatial bounding coordinates were discarded during text streaming, requiring spatial bounding or Multimodal VLM fallback.</p>
              </div>`}
            </div>

            <div class="mt-4 p-3.5 bg-slate-50 rounded-lg border border-slate-200/60">
              <span class="text-xs font-bold text-slate-700 uppercase tracking-wider">System Reasoning & Explanation:</span>
              <p class="text-xs text-slate-600 mt-1 leading-relaxed">${c.explanation}</p>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderRelationshipList(items, label, badgeClass) {
      const container = document.getElementById('cases-container');
      if (!items || items.length === 0) {
        container.innerHTML = `<div class="p-8 text-center text-slate-500 bg-white rounded-xl border border-slate-200">No ${label.toLowerCase()} cases discovered under current document selection.</div>`;
        return;
      }

      container.innerHTML = `
        <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Showing all ${items.length} discovered instances of ${label}</div>
        ` + items.map((r, idx) => {
          const fa = r.fact_a;
          const fb = r.fact_b;
          return `
            <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition mb-4">
              <div class="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
                <div class="flex items-center space-x-2">
                  <span class="text-xs font-bold text-slate-400">#${idx + 1}</span>
                  <span class="px-2.5 py-0.5 rounded-full text-xs font-bold border ${badgeClass}">${label}</span>
                </div>
                <div class="text-xs text-slate-500 font-medium">Confidence: ${(r.confidence * 100).toFixed(0)}% &bull; Signal Score: ${r.score}</div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div class="bg-slate-50 p-3 rounded-lg border border-slate-100">
                  <span class="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Document A</span>
                  <p class="font-semibold text-slate-900 mt-1">${fa.claim}</p>
                  <span class="text-blue-600 font-medium text-[11px] block mt-1">📄 ${fa.doc_filename} (Page ${fa.page_number})</span>
                  <div class="mt-2 text-slate-600 bg-white p-2 rounded border border-slate-200 italic quote-box text-[11px]">
                    "${fa.source_quote}"
                  </div>
                </div>

                <div class="bg-slate-50 p-3 rounded-lg border border-slate-100">
                  <span class="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Document B</span>
                  <p class="font-semibold text-slate-900 mt-1">${fb.claim}</p>
                  <span class="text-blue-600 font-medium text-[11px] block mt-1">📄 ${fb.doc_filename} (Page ${fb.page_number})</span>
                  <div class="mt-2 text-slate-600 bg-white p-2 rounded border border-slate-200 italic quote-box text-[11px]">
                    "${fb.source_quote}"
                  </div>
                </div>
              </div>

              <div class="mt-3 text-xs bg-slate-50 p-3 rounded border border-slate-200/70 text-slate-700 leading-relaxed">
                <span class="font-bold uppercase tracking-wider text-[10px] text-slate-500 block mb-1">Reconciliation Reasoning:</span>
                ${r.explanation}
              </div>
            </div>
          `;
        }).join('');
    }

    function renderLimitationsList(items) {
      const container = document.getElementById('cases-container');
      if (!items || items.length === 0) {
        container.innerHTML = '<div class="p-8 text-center text-slate-500 bg-white rounded-xl border border-slate-200">No layout limitations recorded.</div>';
        return;
      }

      container.innerHTML = `
        <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Identified Extraction Challenges & Failure Modes (${items.length})</div>
      ` + items.map((item, idx) => {
        const f = item.fact;
        return `
          <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm mb-4">
            <div class="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
              <div class="flex items-center space-x-2">
                <span class="text-xs font-bold text-slate-400">#${idx + 1}</span>
                <span class="px-2.5 py-0.5 rounded-full text-xs font-bold border bg-purple-100 text-purple-800 border-purple-200">Layout Vulnerability</span>
              </div>
              <span class="text-xs font-semibold text-purple-700">Extractor Confidence: ${(item.confidence * 100).toFixed(0)}%</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <span class="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Extracted Claim Triple</span>
                <p class="font-semibold text-slate-900 mt-1">${f.claim}</p>
                <div class="text-slate-500 mt-1 text-[11px]">
                  <strong>Subject:</strong> ${f.subject} &bull; <strong>Predicate:</strong> ${f.predicate} &bull; <strong>Value:</strong> ${f.object_value}
                </div>
                <span class="text-blue-600 font-medium text-[11px] block mt-1">📄 ${f.doc_filename} (Page ${f.page_number})</span>
              </div>

              <div class="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <span class="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Verbatim Source Quote</span>
                <div class="mt-1 text-slate-600 bg-white p-2 rounded border border-slate-200 italic quote-box text-[11px]">
                  "${f.source_quote}"
                </div>
              </div>
            </div>

            <div class="mt-3 text-xs bg-purple-50/70 p-3 rounded border border-purple-200/60 text-purple-900 leading-relaxed">
              <span class="font-bold uppercase tracking-wider text-[10px] text-purple-700 block mb-1">Architecture Limitation Analysis & Future Mitigation:</span>
              ${item.limitation_analysis}
            </div>
          </div>
        `;
      }).join('');
    }

    async function loadFacts() {
      try {
        const res = await fetch('/api/facts');
        rawFacts = await res.json();
        document.getElementById('count-facts').innerText = rawFacts.length;
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

      document.getElementById('facts-counter-text').innerText = `Showing ${filtered.length} of ${rawFacts.length} facts`;
      const container = document.getElementById('facts-container');
      
      container.innerHTML = filtered.slice(0, 100).map(f => `
        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:shadow transition">
          <div class="flex justify-between items-start gap-2">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-600">${f.category || 'General'}</span>
            <span class="text-[11px] font-semibold text-blue-600">${(f.confidence * 100).toFixed(0)}% Conf.</span>
          </div>
          <h4 class="font-semibold text-slate-900 text-sm mt-2">${f.claim}</h4>
          <div class="text-[11px] text-slate-500 mt-1">📄 ${f.doc_filename} &bull; Page ${f.page_number}</div>
          <div class="mt-2 text-xs text-slate-600 bg-slate-50 p-2 rounded border border-slate-100 italic quote-box">
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
      document.querySelectorAll('.rel-filter').forEach(b => {
        b.classList.remove('bg-blue-600', 'text-white');
        b.classList.add('bg-slate-100', 'text-slate-700');
      });
      document.getElementById(`filter-rel-${type}`).classList.add('bg-blue-600', 'text-white');
      document.getElementById(`filter-rel-${type}`).classList.remove('bg-slate-100', 'text-slate-700');

      const filtered = rawRelationships.filter(r => {
        if (type === 'all') return true;
        return (r.relationship_type || '').toLowerCase().includes(type.toLowerCase());
      });

      const container = document.getElementById('relationships-container');
      container.innerHTML = filtered.map(r => {
        const fa = r.fact_a;
        const fb = r.fact_b;
        let badgeColor = 'bg-blue-100 text-blue-800';
        if (r.relationship_type.includes('corroboration')) badgeColor = 'bg-emerald-100 text-emerald-800';
        if (r.relationship_type.includes('contradiction')) badgeColor = 'bg-rose-100 text-rose-800';
        if (r.relationship_type.includes('reconciliation')) badgeColor = 'bg-amber-100 text-amber-800';

        return `
          <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition">
            <div class="flex justify-between items-center mb-3">
              <span class="px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${badgeColor}">${r.relationship_type}</span>
              <span class="text-xs font-semibold text-slate-500">Confidence: ${(r.confidence * 100).toFixed(0)}%</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-100 text-xs">
                <span class="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Fact A</span>
                <p class="font-semibold text-slate-800 mt-1">${fa ? fa.claim : r.fact_a_id}</p>
                <span class="text-blue-600 text-[11px] block mt-1">${fa ? `📄 ${fa.doc_filename} (Pg ${fa.page_number})` : ''}</span>
              </div>
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-100 text-xs">
                <span class="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Fact B</span>
                <p class="font-semibold text-slate-800 mt-1">${fb ? fb.claim : r.fact_b_id}</p>
                <span class="text-blue-600 text-[11px] block mt-1">${fb ? `📄 ${fb.doc_filename} (Pg ${fb.page_number})` : ''}</span>
              </div>
            </div>
            <div class="mt-3 text-xs bg-slate-50 p-3 rounded border border-slate-200/50 text-slate-600 leading-relaxed">
              <strong class="text-slate-700 uppercase tracking-wider text-[10px] block mb-1">Grounding Reasoning:</strong> ${r.explanation}
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

    function handleFileSelect(event) {
      const files = event.target.files;
      if (!files.length) return;
      selectedFiles = Array.from(files);
      renderSelectedFiles();
    }

    function renderSelectedFiles() {
      const container = document.getElementById('selected-files-container');
      const list = document.getElementById('file-chips-list');
      if (!selectedFiles.length) {
        container.classList.add('hidden');
        return;
      }
      container.classList.remove('hidden');
      list.innerHTML = selectedFiles.map((f, i) => `
        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200">
          📄 ${f.name} (${(f.size / 1024).toFixed(0)} KB)
          <button type="button" onclick="removeFile(${i})" class="ml-2 text-blue-500 hover:text-rose-600 font-bold">&times;</button>
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
        alert('Please select one or more PDF files to ingest.');
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

      progressBar.style.width = '25%';
      statusPct.innerText = '25%';
      statusTitle.innerText = `Ingesting ${selectedFiles.length} Document(s)...`;
      statusText.innerText = 'Extracting pages, generating semantic chunks, and prompting LLM...';

      try {
        const res = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        });

        if (!res.ok) {
          throw new Error(`Upload failed with status ${res.status}`);
        }

        const data = await res.json();
        progressBar.style.width = '100%';
        statusPct.innerText = '100%';
        statusTitle.innerText = 'Ingestion & Reconciliation Complete!';
        statusText.innerText = `Processed ${data.results.length} files. Refreshing knowledge graphs...`;

        setTimeout(async () => {
          clearSelectedFiles();
          await init();
          uploadBtn.disabled = false;
          uploadBtn.classList.remove('opacity-50', 'cursor-not-allowed');
          statusDiv.classList.add('hidden');
          switchTab('cases');
          alert('Batch ingestion and reconciliation complete! The 4 cases have been refreshed.');
        }, 1200);

      } catch (err) {
        progressBar.style.backgroundColor = '#ef4444';
        statusTitle.innerText = 'Error occurred during processing';
        statusText.innerText = err.message;
        uploadBtn.disabled = false;
        uploadBtn.classList.remove('opacity-50', 'cursor-not-allowed');
      }
    }

    async function confirmReset() {
      const confirmAction = confirm(
        "⚠️ RESET DATABASE CONFIRMATION\\n\\n" +
        "Are you sure you want to completely clear all documents, facts, and relationships?\\n" +
        "This is recommended when testing fresh document sets."
      );
      if (!confirmAction) return;

      try {
        const res = await fetch('/api/reset', { method: 'POST' });
        const data = await res.json();
        alert('Database cleared successfully! You can now upload new documents.');
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
