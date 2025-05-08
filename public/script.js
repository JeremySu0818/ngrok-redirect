document.addEventListener("DOMContentLoaded", () => {
  const list = document.getElementById("quotesList");
  const saveBtn = document.getElementById("saveBtn");
  const addBtn = document.getElementById("addBtn");

  function createQuoteItem(text = "（新增語錄）") {
    const li = document.createElement("li");
    li.className = "quote-item";

    const span = document.createElement("span");
    span.textContent = text;
    span.contentEditable = true;

    const delBtn = document.createElement("button");
    delBtn.textContent = "🗑️";
    delBtn.className = "del-btn";
    delBtn.addEventListener("click", () => li.remove());

    li.appendChild(span);
    li.appendChild(delBtn);
    list.appendChild(li);
  }

  fetch("/quotes")
    .then(res => res.json())
    .then(quotes => {
      quotes.forEach(text => createQuoteItem(text));
    });

  saveBtn.addEventListener("click", () => {
    const allQuotes = [...document.querySelectorAll("#quotesList span")].map(span => span.textContent.trim());
    fetch("/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(allQuotes)
    }).then(res => res.json()).then(result => {
      alert("已儲存語錄！");
    });
  });

  addBtn.addEventListener("click", () => createQuoteItem());
});
