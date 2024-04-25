chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "showPopup") {
      chrome.runtime.sendMessage({ action: "showPopup" });
    }
  });
  