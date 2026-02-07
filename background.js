// background.js
console.log("[JobTracker] Background script initialized");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("[JobTracker] Background received message:", message);
  
  if (message.action === 'getGoogleToken') {
    console.log("[JobTracker] Getting Google auth token...");
    
    chrome.identity.getAuthToken({ interactive: true }, (token) => {
      if (chrome.runtime.lastError) {
        console.error("[JobTracker] Auth error:", chrome.runtime.lastError);
        sendResponse({ 
          error: chrome.runtime.lastError.message || 'Authentication failed' 
        });
        return;
      }

      if (!token) {
        console.error("[JobTracker] No token received from Chrome Identity API");
        sendResponse({ error: 'No token received from authentication' });
        return;
      }

      console.log("[JobTracker] Token received successfully, length:", token.length);
      sendResponse({ token: token });
    });
    
    return true; // Required for async sendResponse
  }
});

// Optional: Handle extension icon click to open dialog
chrome.action.onClicked.addListener((tab) => {
  console.log("[JobTracker] Extension icon clicked on tab:", tab.id);
  
  // Check if we can run on this page
  if (tab.url.startsWith('chrome://') || 
      tab.url.startsWith('chrome-extension://') || 
      tab.url.startsWith('edge://') ||
      tab.url.startsWith('about:')) {
    console.log("[JobTracker] Cannot run on browser internal pages");
    return;
  }
  
  // Send message to content script
  chrome.tabs.sendMessage(tab.id, { action: 'showDialog' }, (response) => {
    if (chrome.runtime.lastError) {
      console.error("[JobTracker] Error sending message:", chrome.runtime.lastError);
    } else {
      console.log("[JobTracker] Dialog opened successfully:", response);
    }
  });
});

// Optional: Handle keyboard shortcut
chrome.commands.onCommand.addListener((command) => {
  if (command === 'open-dialog') {
    console.log("[JobTracker] Keyboard shortcut triggered");
    
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.tabs.sendMessage(tabs[0].id, { action: 'showDialog' });
      }
    });
  }
});