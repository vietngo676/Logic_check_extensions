chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log("Received message:", request); // Debug

    if (request.text) {
        console.log("Sending text to server:", request.text); // Debug

        fetch("http://localhost:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: request.text })
        })
            .then(response => response.json())
            .then(data => {
                console.log("Server response:", data); // Debug
                sendResponse({ success: true, data: data.analysis });
            })
            .catch(error => {
                console.error("Fetch error:", error); // Debug
                sendResponse({ success: false, error: error.message });
            });

        return true; // Giữ kết nối async
    }
});
