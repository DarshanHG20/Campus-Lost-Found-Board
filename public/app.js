const itemsEl = document.getElementById("items");
const emptyEl = document.getElementById("empty");
const countEl = document.getElementById("resultCount");
const modeEl = document.getElementById("boardMode");
const searchEl = document.getElementById("search");
const categoryEl = document.getElementById("category");
const locationEl = document.getElementById("location");
const form = document.getElementById("itemForm");
const message = document.getElementById("formMessage");
const photoInput = document.getElementById("photo");
const uploadBox = document.getElementById("uploadBox");
const uploadText = document.getElementById("uploadText");
let showArchived = false;
let activeController = null;

function escapeHtml(value = "") {
  return String(value).replace(/[&<>"']/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" })[c]);
}

function formatDate(value) {
  const raw = value && typeof value === "object" && "$date" in value ? value.$date : value;
  const date = new Date(raw);
  return Number.isNaN(date.getTime()) ? "Unknown date" : date.toLocaleDateString();
}

async function loadItems() {
  if (activeController) activeController.abort();
  activeController = new AbortController();
  const { signal } = activeController;

  const params = new URLSearchParams({
    q: searchEl.value,
    category: categoryEl.value,
    location: locationEl.value,
    status: showArchived ? "archived" : "active"
  });

  try {
    const response = await fetch(`/api/items?${params.toString()}`, { signal });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not load listings.");

    const items = Array.isArray(data) ? data : [];
    countEl.textContent = `${items.length} LISTING${items.length === 1 ? "" : "S"}`;
    modeEl.textContent = showArchived ? "ARCHIVED ITEMS" : "ACTIVE ITEMS";
    itemsEl.innerHTML = items.map(item => `
      <article class="item-card">
        <div class="item-photo">${item.photoUrl ? `<img src="${escapeHtml(item.photoUrl)}" alt="${escapeHtml(item.title)}">` : "✳"}</div>
        <div class="item-body">
          <div class="item-tags"><span class="tag ${item.type === "Found" ? "found" : ""}">${escapeHtml((item.type || "").toUpperCase())}</span><span class="tag">${escapeHtml(item.category)}</span>${item.archived ? '<span class="tag archived">CLAIMED</span>' : ""}</div>
          <h3>${escapeHtml(item.title)}</h3>
          <p>${escapeHtml(item.description)}</p>
          <div class="item-location">⌖ &nbsp;${escapeHtml(item.location)} · ${escapeHtml(formatDate(item.createdAt))}</div>
          ${item.contact ? `<p class="item-location">Contact: ${escapeHtml(item.contact)}</p>` : ""}
          ${!item.archived ? `<button class="claim-btn" data-claim="${escapeHtml(item.id || item._id)}">Mark as claimed / returned ✓</button>` : ""}
        </div>
      </article>`).join("");
    emptyEl.hidden = items.length !== 0;
  } catch (error) {
    if (error.name === "AbortError") return;
    countEl.textContent = "UNAVAILABLE";
    itemsEl.innerHTML = "";
    emptyEl.hidden = false;
  }
}

[searchEl, categoryEl, locationEl].forEach(el => el.addEventListener("input", loadItems));
document.getElementById("toggleArchived").addEventListener("click", () => {
  showArchived = !showArchived;
  document.getElementById("toggleArchived").innerHTML = showArchived ? 'View active <span>↗</span>' : 'View archived <span>↗</span>';
  loadItems();
});

itemsEl.addEventListener("click", async event => {
  const button = event.target.closest("[data-claim]");
  if (!button || button.disabled) return;
  if (!confirm("Archive this listing as claimed or returned?")) return;

  button.disabled = true;
  try {
    const response = await fetch(`/api/items/${encodeURIComponent(button.dataset.claim)}/claim`, { method: "PATCH" });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Could not update listing.");
    await loadItems();
  } catch (error) {
    button.disabled = false;
    alert(error.message || "Could not update listing.");
  }
});

form.addEventListener("submit", async event => {
  event.preventDefault();
  message.textContent = "Publishing…";
  const data = new FormData(form);
  try {
    const response = await fetch("/api/items", { method: "POST", body: data });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Could not publish listing.");
    form.reset();
    uploadText.textContent = "Choose a photo or drag it here";
    message.textContent = "Your listing is live on the board.";
    showArchived = false;
    document.getElementById("toggleArchived").innerHTML = 'View archived <span>↗</span>';
    await loadItems();
    document.getElementById("board").scrollIntoView({ behavior: "smooth" });
  } catch (error) {
    message.textContent = error.message;
  }
});

photoInput.addEventListener("change", event => {
  const file = event.target.files[0];
  uploadText.textContent = file ? file.name : "Choose a photo or drag it here";
});

uploadBox.addEventListener("dragover", event => {
  event.preventDefault();
  uploadBox.classList.add("dragover");
});

uploadBox.addEventListener("dragleave", () => {
  uploadBox.classList.remove("dragover");
});

uploadBox.addEventListener("drop", event => {
  event.preventDefault();
  uploadBox.classList.remove("dragover");
  const file = event.dataTransfer?.files?.[0];
  if (!file) return;
  const transfer = new DataTransfer();
  transfer.items.add(file);
  photoInput.files = transfer.files;
  uploadText.textContent = file.name;
});
loadItems();
