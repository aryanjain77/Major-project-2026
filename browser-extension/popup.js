document.getElementById('openDialog').addEventListener('click', () => {
  console.log("[Popup] Button clicked");

  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    if (!tabs || !tabs[0]) {
      console.log("[Popup] No active tab found");
      alert('No active tab found. Please open a webpage first.');
      return;
    }

    const tabId = tabs[0].id;
    const url = tabs[0].url || '';

    // Check if we can inject scripts into this page
    if (url.startsWith('chrome://') || 
        url.startsWith('chrome-extension://') || 
        url.startsWith('edge://') ||
        url.startsWith('about:') ||
        url === '') {
      alert('Cannot run on browser internal pages. Please open a regular webpage.');
      return;
    }

    console.log("[Popup] Sending message to tab:", tabId);

    // Send the message - content script is already injected via manifest
    chrome.tabs.sendMessage(tabId, {action: 'showDialog'}, (response) => {
      if (chrome.runtime.lastError) {
        console.error("[Popup] Error:", chrome.runtime.lastError.message);
        // Don't show alert for common errors, just log them
      } else {
        console.log("[Popup] Response:", response);
      }
    });

    // Close popup after sending message
    setTimeout(() => window.close(), 100);
  });
});