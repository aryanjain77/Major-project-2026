// popup.js

document.getElementById('openDialog').addEventListener('click', function() {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    if (!tabs || !tabs[0]) {
      alert('No active tab found. Open a webpage first.');
      return;
    }

    var url = tabs[0].url || '';

    if (url.startsWith('chrome://') ||
        url.startsWith('chrome-extension://') ||
        url.startsWith('edge://') ||
        url.startsWith('about:') ||
        url === '') {
      alert('Cannot run on browser system pages. Navigate to any regular webpage first.');
      return;
    }

    chrome.tabs.sendMessage(tabs[0].id, { action: 'showDialog' }, function(response) {
      if (chrome.runtime.lastError) {
        console.error("[Popup] Error:", chrome.runtime.lastError.message);
      }
    });

    setTimeout(function() { window.close(); }, 80);
  });
});