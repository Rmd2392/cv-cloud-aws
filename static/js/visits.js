(async function () {
  const el = document.getElementById("visits-count");
  if (!el) return;

  const API_URL = "https://5nhitvdej1.execute-api.us-east-1.amazonaws.com/count";

  try {
    const res = await fetch(API_URL, { method: "GET", cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    el.textContent =
      data && typeof data.count !== "undefined" ? data.count : "—";
  } catch (err) {
    console.error("Visits counter error:", err);
    el.textContent = "—";
  }
})();
