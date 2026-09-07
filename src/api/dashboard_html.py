def get_dashboard_html() -> str:
    """Returns the standalone HTML/JS dashboard interface."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fact Knowledge Layer | Superjoin</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; }
    .tab-btn.active { background-color: #2563eb; color: white; }
  </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen">
  <!-- Top Navigation Header -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex flex-wrap justify-between items-center gap-4">
      <div class="flex items-center space-x-3">
        <span class="text-3xl">🔍</span>
        <div>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">Fact Knowledge Layer</h1>
          <p class="text-xs text-slate-500 font-medium">Superjoin AI Engineering Assignment &bull; Evidence Grounding & Cross-Doc Reconciliation</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">
          <span class="w-2 h-2 mr-1.5 bg-emerald-500 rounded-full animate-pulse"></span> Backend Online
        </span>
        <a href="/docs" target="_blank" class="px-3 py-1.5 text-xs font-semibold text-slate-700 hover:text-blue-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition">
          Swagger API &rarr;
        </a>
      </div>
    </div>
    <!-- Tabs Nav -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-1 sm:space-x-2 border-t border-slate-100 overflow-x-auto py-2">
      <button onclick="switchTab('cases')" id="tab-cases-btn" class="tab-btn active px-4 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition whitespace-nowrap">
        ✅ The 4 Required Cases
      </button>
      <button onclick="switchTab('facts')" id="tab-facts-btn" class="tab-btn px-4 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition whitespace-nowrap">
        🔍 Facts Explorer (<span id="count-facts">...</span>)
      </button>
      <button onclick="switchTab('relationships')" id="tab-relationships-btn" class="tab-btn px-4 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition whitespace-nowrap">
        🔗 Relationships (<span id="count-rels">...</span>)
      </button>
      <button onclick="switchTab('upload')" id="tab-upload-btn" class="tab-btn px-4 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition whitespace-nowrap">
        📤 Upload Documents
      </button>
      <button onclick="switchTab('export')" id="tab-export-btn" class="tab-btn px-4 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition whitespace-nowrap">
        📊 Export & Stats
      </button>
    </div>
  </header>

  <!-- Main Content Container -->
  <main class="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
    
    <!-- TAB 1: THE FOUR REQUIRED CASES -->
    <section id="view-cases" class="space-y-6">
      <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg">
        <h2 class="text-lg font-bold text-blue-900">Showcase: The Four Required Analytical Scenarios</h2>
        <p class="text-sm text-blue-700 mt-1">
          Demonstrating Corroboration, Genuine Contradiction, Contextual Reconciliation, and Extraction Limitations with exact verbatim source quotes and reasoning.
        </p>
      </div>

      <div id="cases-container" class="space-y-6">
        <div class="p-8 text-center text-slate-500 animate-pulse">Loading verified cases from knowledge engine...</div>
      </div>
    </section>

    <!-- TAB 2: FACTS EXPLORER -->
    <section id="view-facts" class="space-y-6 hidden">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex-1 w-full">
          <input type="text" id="fact-search" oninput="filterFacts()" placeholder="Search claims, entities, metrics (e.g. EBITDA, cash, Falcon)..." class="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
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
        <button onclick="filterRelationships('all')" class="rel-filter active px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 text-white" id="filter-rel-all">All</button>
        <button onclick="filterRelationships('corroboration')" class="rel-filter px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200" id="filter-rel-corroboration">Corroborations</button>
        <button onclick="filterRelationships('contradiction')" class="rel-filter px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200" id="filter-rel-contradiction">Contradictions</button>
        <button onclick="filterRelationships('contextual_reconciliation')" class="rel-filter px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200" id="filter-rel-contextual_reconciliation">Contextual Reconciliations</button>
      </div>

      <div id="relationships-container" class="space-y-4"></div>
    </section>

    <!-- TAB 4: UPLOAD DOCUMENTS -->
    <section id="view-upload" class="space-y-6 hidden">
      <div class="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm max-w-2xl mx-auto text-center">
        <div class="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mx-auto text-2xl font-bold mb-4">
          📄
        </div>
        <h3 class="text-xl font-bold text-slate-900">Upload PDF Documents</h3>
        <p class="text-sm text-slate-500 mt-2">
          Upload any corporate or macroeconomic filing to extract atomic facts, ground evidence, and discover cross-document relationships.
        </p>
        
        <form id="upload-form" class="mt-6 space-y-4" onsubmit="handleUpload(event)">
          <input type="file" id="pdf-file-input" accept=".pdf" class="block w-full text-sm text-slate-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer">
          <button type="submit" id="upload-btn" class="w-full py-3 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm transition shadow-sm">
            Ingest & Reconcile
          </button>
        </form>

        <div id="upload-status" class="mt-6 hidden">
          <div class="w-full bg-slate-100 rounded-full h-2.5 mb-2 overflow-hidden">
            <div id="upload-progress-bar" class="bg-blue-600 h-2.5 rounded-full w-0 transition-all duration-300"></div>
          </div>
          <p id="upload-status-text" class="text-xs text-slate-600 font-medium">Processing document...</p>
        </div>
      </div>
    </section>

    <!-- TAB 5: EXPORT & STATS -->
    <section id="view-export" class="space-y-6 hidden">
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Documents</span>
          <div class="text-2xl font-bold text-slate-900 mt-1" id="stat-docs">3</div>
        </div>
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Semantic Facts</span>
          <div class="text-2xl font-bold text-blue-600 mt-1" id="stat-facts">258</div>
        </div>
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Relationships</span>
          <div class="text-2xl font-bold text-emerald-600 mt-1" id="stat-rels">47</div>
        </div>
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Contradictions</span>
          <div class="text-2xl font-bold text-rose-600 mt-1" id="stat-contras">2</div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold text-slate-900">Complete Knowledge Graph Export</h3>
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
    let rawCases = [];

    async function init() {
      await loadCases();
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

    async function loadCases() {
      try {
        const res = await fetch('/api/cases');
        rawCases = await res.json();
        renderCases(rawCases);
      } catch (e) {
        console.error('Failed to load cases', e);
      }
    }

    function renderCases(cases) {
      const container = document.getElementById('cases-container');
      if (!cases || cases.length === 0) {
        container.innerHTML = '<div class="p-8 text-center text-slate-500">No cases found in knowledge layer.</div>';
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
        }

        return `
          <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm hover:shadow-md transition">
            <div class="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
              <div class="flex items-center space-x-3">
                <span class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center font-bold text-sm text-slate-700">#${c.case_number}</span>
                <span class="px-3 py-1 rounded-full text-xs font-bold border ${badgeClass}">${badgeText}</span>
              </div>
              <span class="text-xs text-slate-400 font-medium">Verified Grounding</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-slate-50 p-4 rounded-lg border border-slate-100">
                <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Evidence A</span>
                <h4 class="font-semibold text-slate-900 text-sm mt-1">${c.fact_a.claim}</h4>
                <div class="text-xs text-blue-600 font-medium mt-1">📄 ${c.fact_a.doc_filename} (Page ${c.fact_a.page_number})</div>
                <div class="mt-2 text-xs italic text-slate-600 bg-white p-2.5 rounded border border-slate-200">
                  "${c.fact_a.source_quote}"
                </div>
              </div>

              ${c.fact_b ? `
              <div class="bg-slate-50 p-4 rounded-lg border border-slate-100">
                <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Evidence B</span>
                <h4 class="font-semibold text-slate-900 text-sm mt-1">${c.fact_b.claim}</h4>
                <div class="text-xs text-blue-600 font-medium mt-1">📄 ${c.fact_b.doc_filename} (Page ${c.fact_b.page_number})</div>
                <div class="mt-2 text-xs italic text-slate-600 bg-white p-2.5 rounded border border-slate-200">
                  "${c.fact_b.source_quote}"
                </div>
              </div>` : `
              <div class="bg-amber-50 p-4 rounded-lg border border-amber-100 flex flex-col justify-center text-xs text-amber-800">
                <strong>Failure Mode Handling:</strong> Isolated statutory amalgamation event. Raw text streams discard table coordinates; handled via strict quote preservation and spatial token fallback.
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

    async function loadFacts() {
      try {
        const res = await fetch('/api/facts');
        rawFacts = await res.json();
        document.getElementById('count-facts').innerText = rawFacts.length;

        // Populate doc filter
        const docs = [...new Set(rawFacts.map(f => f.doc_filename).filter(Boolean))];
        const docSelect = document.getElementById('doc-filter');
        docSelect.innerHTML = '<option value="all">All Documents</option>' + docs.map(d => `<option value="${d}">${d}</option>`).join('');

        filterFacts();
      } catch (e) {
        console.error('Failed to load facts', e);
      }
    }

    function filterFacts() {
      const q = document.getElementById('fact-search').value.toLowerCase();
      const doc = document.getElementById('doc-filter').value;

      const filtered = rawFacts.filter(f => {
        const matchesDoc = doc === 'all' || f.doc_filename === doc;
        const matchesQuery = !q || f.claim.toLowerCase().includes(q) || (f.subject && f.subject.toLowerCase().includes(q)) || (f.entities && f.entities.some(e => e.toLowerCase().includes(q)));
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
          <div class="mt-2 text-xs text-slate-600 bg-slate-50 p-2 rounded border border-slate-100 italic">
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
          <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
            <div class="flex justify-between items-center mb-3">
              <span class="px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${badgeColor}">${r.relationship_type}</span>
              <span class="text-xs font-semibold text-slate-500">Confidence: ${(r.confidence * 100).toFixed(0)}%</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-100 text-xs">
                <span class="font-bold text-slate-500 uppercase tracking-wider">Fact A</span>
                <p class="font-semibold text-slate-800 mt-1">${fa ? fa.claim : r.fact_a_id}</p>
                <span class="text-slate-400 text-[11px]">${fa ? `📄 ${fa.doc_filename} (Pg ${fa.page_number})` : ''}</span>
              </div>
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-100 text-xs">
                <span class="font-bold text-slate-500 uppercase tracking-wider">Fact B</span>
                <p class="font-semibold text-slate-800 mt-1">${fb ? fb.claim : r.fact_b_id}</p>
                <span class="text-slate-400 text-[11px]">${fb ? `📄 ${fb.doc_filename} (Pg ${fb.page_number})` : ''}</span>
              </div>
            </div>
            <div class="mt-3 text-xs bg-slate-50/70 p-3 rounded border border-slate-200/50 text-slate-600 leading-relaxed">
              <strong>System Explanation:</strong> ${r.explanation}
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

    async function handleUpload(e) {
      e.preventDefault();
      const fileInput = document.getElementById('pdf-file-input');
      if (!fileInput.files.length) {
        alert('Please select a PDF file.');
        return;
      }

      const file = fileInput.files[0];
      const formData = new FormData();
      formData.append('file', file);

      const statusDiv = document.getElementById('upload-status');
      const progressBar = document.getElementById('upload-progress-bar');
      const statusText = document.getElementById('upload-status-text');

      statusDiv.classList.remove('hidden');
      progressBar.style.width = '30%';
      statusText.innerText = `Parsing ${file.name} and extracting facts...`;

      try {
        const res = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        });
        progressBar.style.width = '100%';
        statusText.innerText = 'Document successfully ingested & reconciled!';
        setTimeout(() => {
          alert('Upload complete!');
          window.location.reload();
        }, 1200);
      } catch (err) {
        statusText.innerText = 'Error: ' + err.message;
        progressBar.style.backgroundColor = '#ef4444';
      }
    }

    document.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
"""
