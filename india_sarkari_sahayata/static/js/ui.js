window.IS_UI = {
  bookmarksKey: "is_bookmarks_v1",
  dashboardItems: [],

  escapeHtml(s) {
    return String(s ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  },

  card({ title, subtitle, href, badge, body, saveUrl, tags, linkLabel }) {
    const t = this.escapeHtml(title);
    const sub = this.escapeHtml(subtitle || "");
    const b = this.escapeHtml(badge || "");
    const text = this.escapeHtml(body || "");
    const link = href && href !== "#" ? href : null;
    const safeTags = Array.isArray(tags) ? tags.filter(Boolean).slice(0, 4) : [];

    const bookmarkMeta = {
      title: title || "",
      subtitle: subtitle || "",
      href: link || "",
      badge: badge || "",
      body: body || "",
    };
    const encodedMeta = encodeURIComponent(JSON.stringify(bookmarkMeta));
    const isSaved = this.isBookmarked(link);
    const profileSaveEnabled = Boolean(saveUrl);

    const inner = `
      <div class="flex items-start justify-between gap-3">
        <div class="min-w-0 flex-1">
          <div class="text-base font-semibold">${t}</div>
          ${sub ? `<div class="mt-1 text-sm text-slate-600">${sub}</div>` : ""}
        </div>
        ${b ? `<span class="shrink-0 rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">${b}</span>` : ""}
      </div>
      ${text ? `<div class="mt-3 min-h-[3rem] line-clamp-3 text-sm text-slate-600">${text}</div>` : `<div class="mt-3 min-h-[3rem]"></div>`}
      ${
        safeTags.length
          ? `<div class="mt-3 flex flex-wrap gap-2">${safeTags
              .map(
                (tag) =>
                  `<span class="rounded-full bg-indigo-50 px-2.5 py-1 text-xs font-medium text-indigo-700">${this.escapeHtml(tag)}</span>`
              )
              .join("")}</div>`
          : ""
      }
      <div class="mt-4 flex items-center justify-between gap-2">
        <button type="button" data-bookmark data-bookmark-item="${encodedMeta}" ${profileSaveEnabled ? `data-save-url="${this.escapeHtml(saveUrl)}"` : ""} class="shrink-0 rounded-lg border px-2 py-1 text-xs font-semibold ${isSaved ? "border-emerald-300 bg-emerald-50 text-emerald-700" : "border-slate-200 bg-white text-slate-600"}">
          ${profileSaveEnabled ? "Save to Profile" : (isSaved ? "Saved" : "Save")}
        </button>
        ${
          link
            ? `<a class="text-sm font-semibold text-brand-700 hover:underline" href="${this.escapeHtml(link)}" target="_blank" rel="noreferrer">${this.escapeHtml(linkLabel || "Official website")} →</a>`
            : ""
        }
      </div>
    `;

    if (link) {
      return `
        <div data-search-item data-search-text="${(t + " " + sub + " " + b).toLowerCase()}" data-type="${(badge || "").toLowerCase()}" class="overflow-hidden rounded-2xl border border-slate-200 bg-white p-4 hover:bg-slate-50">
          ${inner}
        </div>
      `;
    }

    return `
      <div data-search-item data-search-text="${(t + " " + sub + " " + b).toLowerCase()}" data-type="${(badge || "").toLowerCase()}" class="overflow-hidden rounded-2xl border border-slate-200 bg-white p-4">
        ${inner}
      </div>
    `;
  },

  skeletonCards(n) {
    return Array.from({ length: n })
      .map(
        () => `
        <div class="animate-pulse rounded-2xl border border-slate-200 bg-white p-4">
          <div class="h-4 w-2/3 rounded bg-slate-200"></div>
          <div class="mt-3 h-3 w-1/2 rounded bg-slate-200"></div>
          <div class="mt-4 h-3 w-full rounded bg-slate-200"></div>
          <div class="mt-2 h-3 w-5/6 rounded bg-slate-200"></div>
        </div>
      `
      )
      .join("");
  },

  errorBox(title, details) {
    const t = this.escapeHtml(title);
    const d = this.escapeHtml(details);
    return `
      <div class="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800">
        <div class="font-semibold">${t}</div>
        <pre class="mt-2 whitespace-pre-wrap text-xs text-rose-900">${d}</pre>
      </div>
    `;
  },

  emptyState(title, details) {
    return `
      <div class="rounded-2xl border border-slate-200 bg-slate-50 p-6 text-center">
        <p class="text-base font-semibold text-slate-800">${this.escapeHtml(title)}</p>
        <p class="mt-1 text-sm text-slate-600">${this.escapeHtml(details)}</p>
      </div>
    `;
  },

  async fetchJson(url) {
    const response = await fetch(url);
    if (!response.ok) {
      const details = await response.text();
      throw new Error(details || `Request failed: ${response.status}`);
    }
    return response.json();
  },

  extractApiMessage(error) {
    const raw = String(error?.message || "");
    try {
      const parsed = JSON.parse(raw);
      return parsed?.detail || raw;
    } catch (_e) {
      return raw;
    }
  },

  compactCard({ title, subtitle, type }) {
    const t = this.escapeHtml(title || "");
    const s = this.escapeHtml(subtitle || "");
    const cardType = this.escapeHtml((type || "").toLowerCase());
    return `
      <div data-search-item data-type="${cardType}" data-search-text="${(t + " " + s).toLowerCase()}" class="rounded-xl border border-slate-200 bg-slate-50 p-3">
        <div class="text-sm font-semibold text-slate-800">${t}</div>
        ${s ? `<div class="mt-1 text-xs text-slate-600">${s}</div>` : ""}
      </div>
    `;
  },

  getBookmarks() {
    try {
      return JSON.parse(localStorage.getItem(this.bookmarksKey) || "[]");
    } catch (e) {
      return [];
    }
  },

  isBookmarked(href) {
    if (!href) return false;
    return this.getBookmarks().some((item) => item.href === href);
  },

  toggleBookmarkFromButton(button) {
    const saveUrl = button.getAttribute("data-save-url");
    if (saveUrl) {
      return this.toggleProfileSave(button, saveUrl);
    }

    const encoded = button.getAttribute("data-bookmark-item");
    if (!encoded) return;
    const decoded = decodeURIComponent(encoded);
    const item = JSON.parse(decoded);
    if (!item.href) return;
    const bookmarks = this.getBookmarks();
    const idx = bookmarks.findIndex((entry) => entry.href === item.href);
    if (idx >= 0) {
      bookmarks.splice(idx, 1);
      button.className = "rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs font-semibold text-slate-600";
      button.textContent = "Save";
    } else {
      bookmarks.unshift(item);
      button.className = "rounded-lg border border-emerald-300 bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-700";
      button.textContent = "Saved";
    }
    localStorage.setItem(this.bookmarksKey, JSON.stringify(bookmarks.slice(0, 100)));
  },

  getCsrfToken() {
    const cookie = document.cookie
      .split(";")
      .map((entry) => entry.trim())
      .find((entry) => entry.startsWith("csrftoken="));
    return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
  },

  async toggleProfileSave(button, saveUrl) {
    const previousText = button.textContent;
    const previousClass = button.className;
    button.disabled = true;
    button.textContent = "Saving...";
    try {
      const response = await fetch(saveUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": this.getCsrfToken(),
        },
      });
      if (!response.ok) {
        throw new Error(`Save failed (${response.status})`);
      }
      const nowSaved = previousText !== "Saved to Profile";
      button.className = nowSaved
        ? "rounded-lg border border-emerald-300 bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-700"
        : "rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs font-semibold text-slate-600";
      button.textContent = nowSaved ? "Saved to Profile" : "Save to Profile";
    } catch (_error) {
      button.className = previousClass;
      button.textContent = previousText;
    } finally {
      button.disabled = false;
    }
  },

  setCount(elId, value, fallbackText) {
    const el = document.getElementById(elId);
    if (!el) return;
    // Handle string values like "∞" or numeric values
    if (typeof value === 'string') {
      el.textContent = value;
    } else if (Number.isFinite(value)) {
      el.textContent = String(value);
    } else {
      el.textContent = fallbackText;
    }
  },

  bindDashboardSearch() {
    const input = document.getElementById("global-search");
    const suggestionsBox = document.getElementById("global-suggestions");
    const typeFilter = document.getElementById("global-type-filter");
    if (!input) return;

    let searchTimeout;
    input.addEventListener("input", () => {
      const q = input.value.trim();
      
      clearTimeout(searchTimeout);
      
      if (!q) {
        if (suggestionsBox) {
          suggestionsBox.classList.add("hidden");
          suggestionsBox.innerHTML = "";
        }
        return;
      }

      if (suggestionsBox) {
        suggestionsBox.innerHTML = '<div class="px-3 py-2 text-xs text-slate-500">Searching...</div>';
        suggestionsBox.classList.remove("hidden");
      }

      searchTimeout = setTimeout(async () => {
        try {
          const results = [];
          const type = (typeFilter?.value || "").toLowerCase();

          // Search jobs
          if (!type || type === "jobs") {
            try {
              const data = await this.fetchJson(`/api/jobs/search/?q=${encodeURIComponent(q)}&limit=3`);
              const items = data.results || [];
              results.push(...items.map(item => ({
                title: item.title || "Job",
                type: "Jobs",
                subtitle: item.company || item.location || ""
              })));
            } catch (e) {}
          }

          // Search schemes
          if (!type || type === "schemes") {
            try {
              const data = await this.fetchJson(`/api/schemes/?search=${encodeURIComponent(q)}&limit=3`);
              const items = data.results || [];
              results.push(...items.map(item => ({
                title: item.title || "Scheme",
                type: "Schemes",
                subtitle: item.category?.name || item.state || ""
              })));
            } catch (e) {}
          }

          // Search scholarships
          if (!type || type === "scholarships") {
            try {
              const data = await this.fetchJson(`/api/scholarships/?search=${encodeURIComponent(q)}&limit=3`);
              const items = data.results || [];
              results.push(...items.map(item => ({
                title: item.title || "Scholarship",
                type: "Scholarships",
                subtitle: item.provider || item.level || ""
              })));
            } catch (e) {}
          }

          if (!suggestionsBox) return;

          if (!results.length) {
            suggestionsBox.innerHTML = '<div class="px-3 py-2 text-xs text-slate-500">No results found</div>';
            return;
          }

          suggestionsBox.innerHTML = results
            .slice(0, 8)
            .map(item => `
              <button type="button" data-suggestion="${this.escapeHtml(item.title)}" class="block w-full px-3 py-2 text-left text-sm hover:bg-slate-100 border-b border-slate-100 last:border-b-0">
                <div class="font-medium text-slate-900">${this.escapeHtml(item.title)}</div>
                <div class="text-xs text-slate-500">${this.escapeHtml(item.subtitle)} • ${this.escapeHtml(item.type)}</div>
              </button>
            `)
            .join("");
        } catch (error) {
          if (suggestionsBox) {
            suggestionsBox.innerHTML = '<div class="px-3 py-2 text-xs text-red-600">Error loading results</div>';
          }
        }
      }, 300);
    });

    suggestionsBox?.addEventListener("click", (event) => {
      const btn = event.target.closest("[data-suggestion]");
      if (!btn) return;
      input.value = btn.getAttribute("data-suggestion") || "";
      suggestionsBox.classList.add("hidden");
    });

    document.addEventListener("click", (event) => {
      if (!suggestionsBox || !input) return;
      if (suggestionsBox.contains(event.target) || input.contains(event.target)) return;
      suggestionsBox.classList.add("hidden");
    });
  },

  bindBookmarkClicks() {
    document.addEventListener("click", async (event) => {
      const button = event.target.closest("[data-bookmark]");
      if (!button) return;
      event.preventDefault();
      await this.toggleBookmarkFromButton(button);
    });
  },

  bindMobileNav() {
    const closeBtn = document.getElementById("mobileNavClose");
    const panel = document.getElementById("mobileNav");
    if (!closeBtn || !panel) return;
    closeBtn.addEventListener("click", () => {
      panel.classList.add("hidden");
    });
  },

  async initDashboardRealtime() {
    this.bindDashboardSearch();
    this.bindBookmarkClicks();
    this.bindMobileNav();
  },

  initDashboardSearch() {
    const searchInput = document.getElementById("dashboard-search-input");
    const typeFilter = document.getElementById("dashboard-type-filter");
    const searchBtn = document.getElementById("dashboard-search-btn");
    const resultsBox = document.getElementById("dashboard-search-results");
    
    if (!searchInput || !searchBtn || !resultsBox) {
      console.warn("Dashboard search elements not found");
      return;
    }

    // Load counts - jobs shows "Available via live search"
    this.setCount("dashboardJobsCount", "∞", "--");
    
    this.fetchJson("/api/schemes/?is_active=true&limit=1")
      .then(data => this.setCount("dashboardSchemesCount", data.count ?? 0, "--"))
      .catch(err => {
        console.error("Failed to fetch schemes count:", err);
        this.setCount("dashboardSchemesCount", NaN, "--");
      });
    
    this.fetchJson("/api/scholarships/?is_active=true&limit=1")
      .then(data => this.setCount("dashboardScholarshipsCount", data.count ?? 0, "--"))
      .catch(err => {
        console.error("Failed to fetch scholarships count:", err);
        this.setCount("dashboardScholarshipsCount", NaN, "--");
      });

    // Use arrow function to preserve 'this' binding
    const performSearch = async () => {
      console.log("🔍 Search initiated");
      const query = searchInput.value.trim();
      const type = typeFilter?.value || "";
      
      if (!query) {
        resultsBox.classList.add("hidden");
        resultsBox.innerHTML = "";
        return;
      }
      
      console.log("Searching for:", { query, type });
      resultsBox.innerHTML = '<div class="p-4 text-center text-sm text-slate-500">Searching...</div>';
      resultsBox.classList.remove("hidden");
      
      try {
        const results = [];
        
        // Search in jobs
        if (!type || type === "jobs") {
          try {
            console.log("Fetching jobs for query:", query);
            const jobsData = await this.fetchJson(`/api/jobs/search/?q=${encodeURIComponent(query)}&limit=5`);
            console.log("Jobs response:", jobsData);
            const jobs = jobsData?.results || [];
            console.log("Extracted jobs array:", jobs);
            results.push(...jobs.map(j => ({
              title: j.title || "Job Listing",
              subtitle: [j.company, j.location].filter(Boolean).join(" • "),
              type: "job",
              href: j.url || "/jobs/",
              icon: "💼"
            })));
          } catch (e) {
            console.error("Jobs search error:", e);
          }
        }
        
        // Search in schemes
        if (!type || type === "schemes") {
          try {
            console.log("Fetching schemes for query:", query);
            const schemesData = await this.fetchJson(`/api/schemes/?search=${encodeURIComponent(query)}&limit=5`);
            console.log("Schemes response:", schemesData);
            const schemes = schemesData?.results || [];
            console.log("Extracted schemes array:", schemes);
            results.push(...schemes.map(s => ({
              title: s.title || "Scheme",
              subtitle: [s.category?.name, s.state].filter(Boolean).join(" • "),
              type: "scheme",
              href: "/schemes/",
              icon: "📋"
            })));
          } catch (e) {
            console.error("Schemes search error:", e);
          }
        }
        
        // Search in scholarships
        if (!type || type === "scholarships") {
          try {
            console.log("Fetching scholarships for query:", query);
            const scholData = await this.fetchJson(`/api/scholarships/?search=${encodeURIComponent(query)}&limit=5`);
            console.log("Scholarships response:", scholData);
            const scholarships = scholData?.results || [];
            console.log("Extracted scholarships array:", scholarships);
            results.push(...scholarships.map(s => ({
              title: s.title || "Scholarship",
              subtitle: [s.provider, s.level].filter(Boolean).join(" • "),
              type: "scholarship",
              href: "/scholarships/",
              icon: "🎓"
            })));
          } catch (e) {
            console.error("Scholarships search error:", e);
          }
        }
        
        console.log("Total results found:", results.length, results);
        
        if (results.length === 0) {
          resultsBox.innerHTML = '<div class="p-4 text-center text-sm text-slate-500">No results found for "' + this.escapeHtml(query) + '"</div>';
          return;
        }
        
        const resultsHtml = results
          .slice(0, 10)
          .map(item => `
            <a href="${this.escapeHtml(item.href)}" class="flex items-start gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 transition">
              <span class="text-lg shrink-0 mt-0.5">${item.icon}</span>
              <div class="min-w-0 flex-1">
                <div class="font-medium text-slate-900 text-sm line-clamp-1">${this.escapeHtml(item.title)}</div>
                <div class="text-xs text-slate-500 line-clamp-1">${this.escapeHtml(item.subtitle || "-")}</div>
              </div>
              <span class="text-xs font-semibold text-slate-400 shrink-0 capitalize whitespace-nowrap ml-2">${item.type}</span>
            </a>
          `)
          .join("");
        
        resultsBox.innerHTML = `
          <div class="p-2 space-y-1">
            <div class="px-4 py-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">Results (${results.length})</div>
            ${resultsHtml}
          </div>
        `;
        console.log("✅ Results rendered successfully");
      } catch (error) {
        console.error("Search error:", error);
        resultsBox.innerHTML = '<div class="p-4 text-center text-sm text-red-600">Error loading results</div>';
      }
    };
    
    // Use arrow function to preserve 'this'
    searchBtn.addEventListener("click", () => performSearch());
    searchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        performSearch();
      }
    });
    
    searchInput.addEventListener("input", () => {
      if (searchInput.value.trim().length === 0) {
        resultsBox.classList.add("hidden");
        resultsBox.innerHTML = "";
      }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener("click", (e) => {
      if (!resultsBox.contains(e.target) && !searchInput.contains(e.target) && !searchBtn.contains(e.target) && !typeFilter.contains(e.target)) {
        resultsBox.classList.add("hidden");
      }
    });

    this.bindBookmarkClicks();
    this.bindMobileNav();
  },

  initSharedUI() {
    this.bindBookmarkClicks();
    this.bindMobileNav();
  },
};

