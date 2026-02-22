// content.js
// ─────────────────────────────────────────────────────────────────────────────
// NO import/export statements — content scripts cannot be ES modules.
// firebase-app-compat.js, firebase-auth-compat.js, firebase-firestore-compat.js
// are all injected BEFORE this file via manifest.json content_scripts order.
// ─────────────────────────────────────────────────────────────────────────────

var FIREBASE_CONFIG = {
  apiKey:            "AIzaSyDvQwMpMwAUF5u94203yXxneEGKfEN8vxI",
  authDomain:        "applywise-web.firebaseapp.com",
  projectId:         "applywise-web",
  storageBucket:     "applywise-web.firebasestorage.app",
  messagingSenderId: "70281274655",
  appId:             "1:70281274655:web:b823988fe1e573176f7c2a"
};

// Initialize Firebase exactly once across all content script runs
if (!window._applyWiseFirebaseReady) {
  try {
    firebase.initializeApp(FIREBASE_CONFIG);
    window._applyWiseFirebaseReady = true;
    console.log("[ApplyWise] Firebase initialized");
  } catch (e) {
    if (e.code === 'app/duplicate-app') {
      window._applyWiseFirebaseReady = true; // Already init, that's fine
    } else {
      console.error("[ApplyWise] Firebase init error:", e);
    }
  }
}

// ─── Guard against double-loading ────────────────────────────────────────────
if (window._applyWiseLoaded) {
  console.log("[ApplyWise] Already loaded, skipping");
} else {
  window._applyWiseLoaded = true;
  console.log("[ApplyWise] Content script ready");

  var _modal = null;

  // Listen for messages from popup.js or background.js
  chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === 'showDialog') {
      showDialog();
      sendResponse({ status: 'ok' });
    }
    return true;
  });

  // ─── Build and show the modal ───────────────────────────────────────────────
  function showDialog() {
    if (_modal) {
      _modal.style.display = 'block';
      return;
    }

    // ── Overlay backdrop
    var overlay = document.createElement('div');
    overlay.id = 'aw-overlay';
    overlay.style.cssText = [
      'position:fixed!important', 'inset:0!important',
      'background:rgba(0,0,0,0.35)!important', 'z-index:2147483646!important'
    ].join(';');
    overlay.addEventListener('click', closeModal);

    // ── Modal container
    var modal = document.createElement('div');
    modal.id = 'aw-modal';
    modal.style.cssText = [
      'position:fixed!important', 'top:50%!important', 'left:50%!important',
      'transform:translate(-50%,-50%)!important',
      'width:420px!important', 'max-width:94vw!important',
      'max-height:90vh!important', 'overflow-y:auto!important',
      'background:#fff!important', 'border-radius:14px!important',
      'padding:28px!important', 'box-shadow:0 16px 56px rgba(0,0,0,0.28)!important',
      'z-index:2147483647!important',
      'font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif!important',
      'color:#111827!important', 'box-sizing:border-box!important'
    ].join(';');

    // ── Close button
    var closeBtn = mk('button', {
      textContent: '×',
      style: 'position:absolute!important;top:10px!important;right:14px!important;background:none!important;border:none!important;font-size:28px!important;color:#9ca3af!important;cursor:pointer!important;padding:0!important;line-height:1!important;'
    });
    closeBtn.onclick = closeModal;
    modal.appendChild(closeBtn);

    // ── Header
    var header = mk('div', { style: 'margin-bottom:20px!important;' });
    header.appendChild(mk('h2', {
      textContent: '📋 Add to ApplyWise',
      style: 'margin:0 0 4px 0!important;font-size:18px!important;font-weight:700!important;color:#1e3a5f!important;'
    }));
    header.appendChild(mk('p', {
      textContent: 'Saved jobs appear instantly on your dashboard',
      style: 'margin:0!important;font-size:12px!important;color:#6b7280!important;'
    }));
    modal.appendChild(header);

    // ── Status message bar
    var statusBar = mk('div', {
      id: 'aw-status',
      style: 'display:none!important;padding:10px 14px!important;border-radius:8px!important;margin-bottom:14px!important;font-size:13px!important;font-weight:500!important;'
    });
    modal.appendChild(statusBar);

    // ── Form fields — MUST match exactly what Dashboard.jsx saves/reads
    var today = new Date().toISOString().split('T')[0];

    var dateField    = field('Date Applied *',          'aw_date',    'date',     today);
    var companyField = field('Company Name *',          'aw_company', 'text',     '');
    var roleField    = field('Role Applied For *',      'aw_role',    'text',     '');
    var statusField  = field('Status *',                'aw_status',  'select',   'Applied', null,
      ['Applied','OA','Technical','HR','Offer','Rejected']);
    var stipendField = field('Stipend / Package',       'aw_stipend', 'text',     '');
    var linkField    = field('Job Link',                'aw_link',    'url',      '');
    var descField    = field('Description (short)',     'aw_desc',    'textarea', '', 2);
    var noteField    = field('Notes',                   'aw_notes',   'textarea', '', 2);

    var form = mk('div', { style: 'display:flex!important;flex-direction:column!important;gap:12px!important;' });
    // Two-column layout for compact fields
    var row1 = twoCol(dateField.wrapper, statusField.wrapper);
    var row2 = twoCol(companyField.wrapper, roleField.wrapper);
    var row3 = twoCol(stipendField.wrapper, linkField.wrapper);
    form.appendChild(row1);
    form.appendChild(row2);
    form.appendChild(row3);
    form.appendChild(descField.wrapper);
    form.appendChild(noteField.wrapper);

    // ── Save button
    var saveBtn = mk('button', {
      textContent: '💾 Save to ApplyWise',
      style: 'width:100%!important;padding:13px!important;margin-top:6px!important;background:#2563eb!important;color:#fff!important;border:none!important;border-radius:9px!important;font-size:15px!important;font-weight:700!important;cursor:pointer!important;letter-spacing:0.3px!important;'
    });
    saveBtn.onmouseover = function(){ this.style.background='#1d4ed8'; };
    saveBtn.onmouseout  = function(){ this.style.background='#2563eb'; };
    saveBtn.onclick     = function(){ handleSave(saveBtn, statusBar, {
      dateField, companyField, roleField, statusField,
      stipendField, linkField, descField, noteField
    }); };
    form.appendChild(saveBtn);

    modal.appendChild(form);
    document.body.appendChild(overlay);
    document.body.appendChild(modal);
    _modal = modal;

    // ── Auto-fill from current page
    try {
      linkField.input.value = window.location.href;
      var parts = document.title.split(/[-|•–]/);
      if (parts[0]) companyField.input.value = parts[0].trim();
      if (parts[1]) roleField.input.value    = parts[1].trim();
    } catch(e) {}

    setTimeout(function(){ companyField.input.focus(); }, 80);
  }

  function closeModal() {
    var m = document.getElementById('aw-modal');
    var o = document.getElementById('aw-overlay');
    if (m) m.remove();
    if (o) o.remove();
    _modal = null;
  }

  // ─── Save handler ───────────────────────────────────────────────────────────
  function handleSave(saveBtn, statusBar, fields) {
    var company = fields.companyField.input.value.trim();
    var role    = fields.roleField.input.value.trim();
    var status  = fields.statusField.input.value;

    if (!company || !role || !status) {
      showStatus(statusBar, '⚠️ Please fill in Company, Role, and Status', 'warn');
      return;
    }

    setBtnState(saveBtn, true, '⏳ Signing in...');
    showStatus(statusBar, '🔐 Requesting Google sign-in...', 'info');

    // Ask background.js for a Google OAuth token + user email
    chrome.runtime.sendMessage({ action: 'getGoogleToken' }, function(response) {
      if (chrome.runtime.lastError) {
        showStatus(statusBar, '❌ Extension error: ' + chrome.runtime.lastError.message, 'error');
        setBtnState(saveBtn, false);
        return;
      }
      if (!response || response.error) {
        showStatus(statusBar, '❌ Sign-in failed: ' + (response ? response.error : 'no response'), 'error');
        setBtnState(saveBtn, false);
        return;
      }

      var accessToken = response.token;
      var userEmail   = response.email;
      var userName    = response.name;

      console.log("[ApplyWise] Got token for:", userEmail);
      showStatus(statusBar, '🔥 Saving to Firestore...', 'info');
      setBtnState(saveBtn, true, '⏳ Saving...');

      // Sign into Firebase with the Google credential
      var credential = firebase.auth.GoogleAuthProvider.credential(null, accessToken);
      firebase.auth().signInWithCredential(credential)
        .then(function(userCredential) {
          var user = userCredential.user;
          console.log("[ApplyWise] Firebase signed in as:", user.email);

          // ── Build the job document — EXACTLY matching Dashboard.jsx fields
          var jobDoc = {
            userId:      user.uid,
            email:       user.email,                          // Dashboard queries by this!
            dateApplied: fields.dateField.input.value || today(),
            company:     company,
            role:        role,
            status:      status,
            stipend:     fields.stipendField.input.value.trim() || '',
            description: fields.descField.input.value.trim()    || '',
            link:        fields.linkField.input.value.trim()    || '',
            notes:       fields.noteField.input.value.trim()    || '',
            timestamp:   new Date().toISOString(),
            source:      'extension'   // helpful to know it came from the extension
          };

          // Save to Firestore collection 'jobs' (same as React app)
          return firebase.firestore().collection('jobs').add(jobDoc);
        })
        .then(function(docRef) {
          console.log("[ApplyWise] Saved! Doc ID:", docRef.id);
          showStatus(statusBar, '✅ Saved! Check your ApplyWise dashboard.', 'success');
          setBtnState(saveBtn, false, '✅ Saved!');
          saveBtn.style.background = '#10b981';
          setTimeout(closeModal, 1800);
        })
        .catch(function(err) {
          console.error("[ApplyWise] Save error:", err);
          showStatus(statusBar, '❌ Failed: ' + err.message, 'error');
          setBtnState(saveBtn, false);
        });
    });
  }

  // ─── Helpers ────────────────────────────────────────────────────────────────

  function today() {
    return new Date().toISOString().split('T')[0];
  }

  function mk(tag, props) {
    var el = document.createElement(tag);
    Object.keys(props || {}).forEach(function(k) { el[k] = props[k]; });
    return el;
  }

  function twoCol(a, b) {
    var row = mk('div', { style: 'display:grid!important;grid-template-columns:1fr 1fr!important;gap:12px!important;' });
    row.appendChild(a);
    row.appendChild(b);
    return row;
  }

  // Creates a labelled form field (input, textarea, or select)
  function field(labelText, id, type, defaultVal, rows, options) {
    var wrapper = mk('div', {});

    var lbl = mk('label', {
      textContent: labelText,
      style: 'display:block!important;font-size:12px!important;font-weight:600!important;color:#374151!important;margin-bottom:4px!important;'
    });

    var input;
    if (type === 'select') {
      input = mk('select', {});
      (options || []).forEach(function(opt) {
        var o = mk('option', { value: opt, textContent: opt });
        if (opt === defaultVal) o.selected = true;
        input.appendChild(o);
      });
    } else if (type === 'textarea') {
      input = mk('textarea', { rows: rows || 2 });
      input.style.resize = 'vertical';
      input.value = defaultVal || '';
    } else {
      input = mk('input', { type: type });
      input.value = defaultVal || '';
    }

    var baseStyle = [
      'width:100%!important', 'padding:8px 10px!important',
      'border:1.5px solid #d1d5db!important', 'border-radius:7px!important',
      'font-size:13px!important', 'background:#f9fafb!important',
      'box-sizing:border-box!important', 'color:#111827!important',
      'font-family:inherit!important', 'outline:none!important'
    ].join(';');
    input.style.cssText = baseStyle;

    input.addEventListener('focus', function() {
      this.style.borderColor = '#2563eb';
      this.style.background  = '#fff';
    });
    input.addEventListener('blur', function() {
      this.style.borderColor = '#d1d5db';
      this.style.background  = '#f9fafb';
    });

    wrapper.appendChild(lbl);
    wrapper.appendChild(input);
    return { wrapper: wrapper, input: input };
  }

  function setBtnState(btn, disabled, text) {
    btn.disabled = disabled;
    if (text) btn.textContent = text;
    btn.style.background = disabled ? '#6b7280' : '#2563eb';
    btn.style.cursor     = disabled ? 'not-allowed' : 'pointer';
  }

  function showStatus(bar, msg, type) {
    var colors = {
      info:    { bg: '#eff6ff', color: '#1d4ed8', border: '#bfdbfe' },
      success: { bg: '#f0fdf4', color: '#166534', border: '#bbf7d0' },
      warn:    { bg: '#fffbeb', color: '#92400e', border: '#fde68a' },
      error:   { bg: '#fef2f2', color: '#991b1b', border: '#fecaca' }
    };
    var c = colors[type] || colors.info;
    bar.style.cssText = [
      'display:block!important', 'padding:10px 14px!important',
      'border-radius:8px!important', 'margin-bottom:14px!important',
      'font-size:13px!important', 'font-weight:500!important',
      'background:' + c.bg + '!important',
      'color:' + c.color + '!important',
      'border:1px solid ' + c.border + '!important'
    ].join(';');
    bar.textContent = msg;
  }

} // end guard