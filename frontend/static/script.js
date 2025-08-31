(() => {
  const $ = (s)=>document.querySelector(s);
  const messages = $("#messages");
  const input = $("#userInput");
  const form = $("#chatForm");
  const cidEl = $("#cid");
  const resetBtn = $("#resetBtn");
  const apiBaseInput = $("#apiBase");
  const saveBaseBtn = $("#saveBase");

  let conversationId = null;
  let apiBase = localStorage.getItem("debatebot.apiBase") || apiBaseInput.value;
  apiBaseInput.value = apiBase;

  function addMsg(role, text){
    const div = document.createElement("div");
    div.className = "msg " + (role === "user" ? "user" : "bot");
    div.textContent = text;
    messages.appendChild(div);
    messages.parentElement.scrollTop = messages.parentElement.scrollHeight;
  }

  saveBaseBtn.onclick = () => {
    apiBase = apiBaseInput.value.trim();
    localStorage.setItem("debatebot.apiBase", apiBase);
    saveBaseBtn.textContent = "Saved";
    setTimeout(()=>saveBaseBtn.textContent="Save", 1000);
  };

  resetBtn.onclick = () => {
    conversationId = null;
    cidEl.textContent = "(new)";
    messages.innerHTML = "";
    input.focus();
  };

  form.onsubmit = async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if(!text) return;
    addMsg("user", text);
    input.value = "";
    try {
      const res = await fetch(apiBase + "/api/v1/chat/webhook", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ conversation_id: conversationId, message: text })
      });
      const data = await res.json();
      conversationId = data.conversation_id;
      cidEl.textContent = conversationId;
      const last = data.message[data.message.length-1];
      if(last && last.role === "bot") addMsg("bot", last.message);
    } catch(err){
      addMsg("bot", "Error contacting API: " + err.message);
    }
  };
})();
