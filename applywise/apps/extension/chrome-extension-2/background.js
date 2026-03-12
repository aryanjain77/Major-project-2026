// background.js
// Handles Google OAuth via chrome.identity.
// Returns the access token + user email so content.js can sign into Firebase.

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("[Background] Received message:", message.action);

  if (message.action === 'getGoogleToken') {

    // Step 1: Get OAuth access token interactively (opens Google sign-in if needed)
    chrome.identity.getAuthToken({ interactive: true }, (token) => {
      if (chrome.runtime.lastError || !token) {
        console.error("[Background] getAuthToken failed:", chrome.runtime.lastError?.message);
        sendResponse({ error: chrome.runtime.lastError?.message || 'Failed to get token' });
        return;
      }

      console.log("[Background] Got access token. Fetching user info...");

      // Step 2: Fetch user's email from Google — content.js needs this
      // because your React app queries Firestore by email
      fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
        headers: { Authorization: 'Bearer ' + token }
      })
      .then(res => res.json())
      .then(userInfo => {
        console.log("[Background] Got user info for:", userInfo.email);
        sendResponse({
          token: token,
          email: userInfo.email,
          name: userInfo.name,
          userId: userInfo.id
        });
      })
      .catch(err => {
        console.error("[Background] Userinfo fetch failed:", err);
        // Still send token even if userinfo fails — content.js will handle it
        sendResponse({ token: token, email: null });
      });
    });

    return true; // Keep message channel open for async response
  }
});

// Handle keyboard shortcut Ctrl+Shift+J
chrome.commands.onCommand.addListener((command) => {
  if (command === 'open-dialog') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs && tabs[0] && tabs[0].id) {
        chrome.tabs.sendMessage(tabs[0].id, { action: 'showDialog' });
      }
    });
  }
});