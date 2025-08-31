(() => {
  const $ = (s) => document.querySelector(s);
  const messages = $("#messages");
  const input = $("#userInput");
  const form = $("#chatForm");
  const cidEl = $("#cid");
  const resetBtn = $("#resetBtn");

  let conversationId = null;

  function addMsg(role, text) {
    const div = document.createElement("div");
    div.className = "msg " + (role === "user" ? "user" : "bot");
    div.textContent = text;
    messages.appendChild(div);
    messages.parentElement.scrollTop = messages.parentElement.scrollHeight;
  }

  resetBtn.onclick = () => {
    conversationId = null;
    cidEl.textContent = "(new)";
    messages.innerHTML = "";
    input.focus();
  };

  form.onsubmit = async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    addMsg("user", text);
    input.value = "";
    try {
      const res = await fetch("/api/v1/chat/webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: text,
        }),
      });

      if (!res.ok) {
        const errText = await res.text();
        addMsg("bot", `API error (${res.status}): ${errText || "no body"}`);
        return;
      }

      const data = await res.json();

      if (data.conversation_id) {
        conversationId = data.conversation_id;
        cidEl.textContent = conversationId;
      }

      if (Array.isArray(data.message) && data.message.length > 0) {
        const last = data.message[data.message.length - 1];
        if (last && last.role === "bot" && typeof last.message === "string") {
          addMsg("bot", last.message);
        } else {
          addMsg("bot", "No bot message in response.");
        }
      } else {
        addMsg("bot", "Empty or unrecognized response from API.");
      }
    } catch (err) {
      addMsg("bot", "Error contacting API: " + (err?.message || String(err)));
    }
  };
})();
