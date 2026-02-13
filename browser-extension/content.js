if (window.jobTrackerExtensionLoaded) {
  console.log("[JobTracker] Already loaded, skipping");
} else {
  window.jobTrackerExtensionLoaded = true;
  console.log("[JobTracker] Content script loaded successfully");

  var jobTrackerModal = null;

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("[JobTracker] Message received:", message);
    
    if (message.action === 'showDialog') {
      console.log("[JobTracker] Showing dialog");
      showDialog();
      sendResponse({ status: "success", message: "Dialog opened" });
    }
    return true;
  });

  function showDialog() {
    if (jobTrackerModal) {
      console.log("[JobTracker] Modal already open");
      return;
    }

    const modal = document.createElement('div');
    modal.id = 'job-tracker-modal';
    modal.style.cssText = `
      position: fixed !important;
      top: 50px !important;
      left: 50% !important;
      transform: translateX(-50%) !important;
      width: 360px !important;
      max-width: 90vw !important;
      max-height: 85vh !important;
      overflow-y: auto !important;
      background: #ffffff !important;
      border: 1px solid #d1d5db !important;
      border-radius: 12px !important;
      padding: 24px !important;
      box-shadow: 0 10px 40px rgba(0,0,0,0.25) !important;
      z-index: 2147483647 !important;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
      color: #111827 !important;
    `;

    // Title
    const title = document.createElement('h2');
    title.textContent = 'Log Job Application';
    title.style.cssText = 'margin: 0 0 20px 0; font-size: 20px; color: #1f2937;';
    modal.appendChild(title);

    // Form
    const form = document.createElement('form');
    form.style.cssText = 'display: flex; flex-direction: column; gap: 16px;';

    function createField(labelText, id, type, value, rows) {
      type = type || 'text';
      value = value || '';
      
      const wrapper = document.createElement('div');

      const label = document.createElement('label');
      label.textContent = labelText;
      label.htmlFor = id;
      label.style.cssText = 'display: block; margin-bottom: 6px; font-weight: 600; font-size: 14px; color: #374151;';

      let input;
      if (type === 'textarea') {
        input = document.createElement('textarea');
        input.rows = rows || 4;
      } else {
        input = document.createElement('input');
        input.type = type;
      }

      input.id = id;
      input.value = value;
      input.style.cssText = `
        width: 100%;
        padding: 10px 12px;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        font-size: 14px;
        background: #f9fafb;
        transition: border-color 0.15s;
        box-sizing: border-box;
      `;
      
      input.addEventListener('focus', function() { 
        this.style.borderColor = '#3b82f6';
        this.style.background = '#ffffff';
      });
      input.addEventListener('blur', function() { 
        this.style.borderColor = '#d1d5db';
        this.style.background = '#f9fafb';
      });

      wrapper.appendChild(label);
      wrapper.appendChild(input);
      return { wrapper: wrapper, input: input };
    }

    // Fields
    const today = new Date().toISOString().split('T')[0];

    const dateField = createField('Date Applied', 'dateApplied', 'date', today);
    const companyField = createField('Company Name', 'companyName');
    const stipendField = createField('Stipend / Package', 'stipend');
    const descField = createField('Job Description (short)', 'jobDesc', 'textarea', '', 3);
    const roleField = createField('Role Applied For', 'role');
    const emailField = createField('Your Email', 'email', 'email');
    const noteField = createField('Extra Note', 'extraNote', 'textarea', '', 2);
    const linkField = createField('Company Website Link', 'companyLink', 'url');

    form.appendChild(dateField.wrapper);
    form.appendChild(companyField.wrapper);
    form.appendChild(stipendField.wrapper);
    form.appendChild(descField.wrapper);
    form.appendChild(roleField.wrapper);
    form.appendChild(emailField.wrapper);
    form.appendChild(noteField.wrapper);
    form.appendChild(linkField.wrapper);

    // Try auto-fill from page
    try {
      const pageTitle = document.title || '';
      const selectedText = window.getSelection().toString().trim();

      if (pageTitle && !selectedText) {
        const parts = pageTitle.split(/[-|•]/);
        if (parts[0]) companyField.input.value = parts[0].trim();
        if (parts[1]) roleField.input.value = parts[1].trim();
      }
      if (selectedText && selectedText.length < 100) {
        companyField.input.value = selectedText.split(' ')[0] || companyField.input.value;
      }
      
      // Auto-fill current page URL
      linkField.input.value = window.location.href;
    } catch (e) {
      console.log("[JobTracker] Auto-fill error:", e);
    }

    // Save button
    const saveBtn = document.createElement('button');
    saveBtn.textContent = 'Save to Google Sheets';
    saveBtn.type = 'button';
    saveBtn.style.cssText = `
      background: #10b981;
      color: white;
      padding: 12px;
      border: none;
      border-radius: 8px;
      font-weight: 600;
      font-size: 15px;
      cursor: pointer;
      margin-top: 12px;
      transition: background 0.2s;
    `;
    
    saveBtn.addEventListener('mouseover', function() { 
      this.style.background = '#059669'; 
    });
    saveBtn.addEventListener('mouseout', function() { 
      this.style.background = '#10b981'; 
    });
    
    saveBtn.addEventListener('click', function() {
      console.log("[JobTracker] Save button clicked");
      
      // Collect all form data
      const jobData = {
        dateApplied: dateField.input.value,
        company: companyField.input.value,
        stipend: stipendField.input.value,
        description: descField.input.value,
        role: roleField.input.value,
        email: emailField.input.value,
        notes: noteField.input.value,
        link: linkField.input.value,
        timestamp: new Date().toISOString()
      };

      // Validate required fields
      if (!jobData.company || !jobData.role) {
        alert('Please fill in at least Company Name and Role');
        return;
      }

      console.log("[JobTracker] Requesting Google token...");
      
      // Ask background.js for the Google token
      chrome.runtime.sendMessage({ action: 'getGoogleToken' }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("[JobTracker] Runtime error:", chrome.runtime.lastError);
          alert('Communication error with extension background: ' + chrome.runtime.lastError.message);
          return;
        }

        console.log("[JobTracker] Token response received:", response);

        if (!response) {
          console.error("[JobTracker] No response from background");
          alert('No response from background script. Please try again.');
          return;
        }

        if (response.error) {
          console.error("[JobTracker] Token error:", response.error);
          alert('Google sign-in failed: ' + response.error);
          return;
        }

        if (!response.token) {
          console.error("[JobTracker] No token in response");
          alert('No token received. Please try again.');
          return;
        }

        const accessToken = response.token;
        console.log("[JobTracker] Token received, length:", accessToken.length);

        // Extract spreadsheet ID from URL
        const spreadsheetUrl = 'https://docs.google.com/spreadsheets/d/1uQrBhS9XwXMXKffAM-OU3us4Hm2r25YgcDRzEOOx1dU/edit';
        let spreadsheetId;
        
        // Check if it's a URL or just an ID
        if (spreadsheetUrl.includes('docs.google.com')) {
          // Extract ID from URL
          const match = spreadsheetUrl.match(/\/d\/([a-zA-Z0-9-_]+)/);
          if (match && match[1]) {
            spreadsheetId = match[1];
            console.log("[JobTracker] Extracted spreadsheet ID:", spreadsheetId);
          } else {
            alert('Invalid Google Sheets URL format');
            return;
          }
        } else {
          // Assume it's already just the ID
          spreadsheetId = spreadsheetUrl;
        }

        const values = [[
          jobData.dateApplied || '',
          jobData.company || '',
          jobData.role || '',
          jobData.stipend || '',
          jobData.description || '',
          jobData.email || '',
          jobData.notes || '',
          jobData.link || '',
          jobData.timestamp || ''
        ]];

        const apiUrl = `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values/Sheet1!A:I:append?valueInputOption=RAW`;
        console.log("[JobTracker] Making API request to:", apiUrl);

        // Disable button during save
        saveBtn.disabled = true;
        saveBtn.textContent = 'Saving...';
        saveBtn.style.background = '#6b7280';

        fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ values })
        })
        .then(response => {
          console.log("[JobTracker] API response status:", response.status);
          if (!response.ok) {
            return response.json().then(err => {
              console.error("[JobTracker] API error details:", err);
              throw new Error(`Sheets API error: ${response.status} - ${err.error?.message || response.statusText}`);
            }).catch(parseError => {
              // If we can't parse the error JSON
              if (parseError.message && parseError.message.includes('Sheets API error')) {
                throw parseError;
              }
              throw new Error(`Sheets API error: ${response.status} ${response.statusText}`);
            });
          }
          return response.json();
        })
        .then(data => {
          console.log("[JobTracker] Row appended successfully:", data);
          alert('✅ Job application saved to Google Sheet!');
          modal.remove();
          jobTrackerModal = null;
        })
        .catch(error => {
          console.error("[JobTracker] Save failed:", error);
          alert('❌ Failed to save to Google Sheet:\n' + error.message);
          
          // Re-enable button
          saveBtn.disabled = false;
          saveBtn.textContent = 'Save to Google Sheets';
          saveBtn.style.background = '#10b981';
        });
      });
    });
    
    form.appendChild(saveBtn);
    modal.appendChild(form);

    // Close button
    const closeBtn = document.createElement('button');
    closeBtn.textContent = '×';
    closeBtn.style.cssText = `
      position: absolute;
      top: 12px;
      right: 16px;
      background: none;
      border: none;
      font-size: 24px;
      color: #6b7280;
      cursor: pointer;
      line-height: 1;
    `;
    closeBtn.addEventListener('click', function() {
      modal.remove();
      jobTrackerModal = null;
    });
    modal.appendChild(closeBtn);

    document.body.appendChild(modal);
    jobTrackerModal = modal;
    
    console.log("[JobTracker] Modal created and appended to body");
    
    // Focus on first input
    setTimeout(function() {
      companyField.input.focus();
    }, 100);
  }
}