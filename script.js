// Database mapping for all subjects and papers
const database = {
    "Mathematics": [
        { label: "2026 P1", file: "2026-P1" },
        { label: "2026 P2", file: "2026-P2" },
        { label: "2026 P3", file: "2026-P3" },
        { label: "2025 P1", file: "2025-P1" },
        { label: "2025 P2", file: "2025-P2" },
        { label: "2024 P1", file: "2024-P1" },
        { label: "2024 P2", file: "2024-P2" },
        { label: "2024 P3", file: "2024-P3" },
        { label: "2023 P1", file: "2023-P1" },
        { label: "2023 P2", file: "2023-P2" },
        { label: "2022 P1", file: "2022-P1" },
        { label: "2022 P2", file: "2022-P2" },
        { label: "2022 P3", file: "2022-P3" },
        { label: "2019 P1", file: "2019-P1" },
        { label: "2019 P2", file: "2019-P2" }
    ],
    "Chemistry": [
        { label: "2026 P1", file: "2026-P1" },
        { label: "2026 P2", file: "2026-P2" },
        { label: "2026 P3", file: "2026-P3" },
        { label: "2025 P1", file: "2025-P1" },
        { label: "2025 P2", file: "2025-P2" },
        { label: "2025 P3", file: "2025-P3" },
        { label: "2024 P1", file: "2024-P1" },
        { label: "2024 P2", file: "2024-P2" },
        { label: "2024 P3", file: "2024-P3" },
        { label: "2023 P1", file: "2023-P1" },
        { label: "2023 P2", file: "2023-P2" },
        { label: "2023 P3", file: "2023-P3" },
        { label: "2022 P1", file: "2022-P1" },
        { label: "2022 P2", file: "2022-P2" },
        { label: "2022 P3", file: "2022-P3" }
    ],
    "Physics": [
        { label: "2026 P1", file: "2026-P1" },
        { label: "2026 P2", file: "2026-P2" },
        { label: "2026 P3", file: "2026-P3" },
        { label: "2025 P1", file: "2025-P1" },
        { label: "2025 P2", file: "2025-P2" },
        { label: "2025 P3", file: "2025-P3" },
        { label: "2024 P1", file: "2024-P1" },
        { label: "2024 P2", file: "2024-P2" },
        { label: "2024 P3", file: "2024-P3" },
        { label: "2023 P1", file: "2023-P1" },
        { label: "2023 P2", file: "2023-P2" },
        { label: "2023 P3", file: "2023-P3" },
        { label: "2022 P1", file: "2022-P1" },
        { label: "2022 P2", file: "2022-P2" },
        { label: "2022 P3", file: "2022-P3" },
        { label: "2019 P1", file: "2019-P1" }
    ]
};

document.addEventListener("DOMContentLoaded", () => {
    buildDirectoryNav();
    // Load Mathematics 2024 Paper 1 by default
    openPaper("Mathematics", "2024-P1", "2024 P1");

    const searchInput = document.getElementById("searchInput");
    const searchBtn = document.getElementById("searchBtn");
    const subjectSelect = document.getElementById("subjectSelect");
    const topicSelect = document.getElementById("topicSelect");

    if (searchInput) {
        searchInput.addEventListener("input", handleSearch);
        searchInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") handleSearch();
        });
    }

    if (searchBtn) {
        searchBtn.addEventListener("click", handleSearch);
    }

    if (subjectSelect) {
        subjectSelect.addEventListener("change", () => {
            populateTopicOptions();
            if (document.getElementById("searchInput")?.value.trim()) {
                handleSearch();
            }
        });
    }

    if (topicSelect) {
        topicSelect.addEventListener("change", () => {
            if (document.getElementById("searchInput")?.value.trim()) {
                handleSearch();
            }
        });
    }

    populateTopicOptions();
});

// Build directory grid UI dynamically
function buildDirectoryNav() {
    const navContainer = document.getElementById("directoryNav");
    if (!navContainer) return;
    navContainer.innerHTML = "";

    for (const [subject, papers] of Object.entries(database)) {
        const group = document.createElement("div");
        group.className = "subject-group";

        const title = document.createElement("div");
        title.className = "subject-title";
        title.innerText = subject;

        const btnContainer = document.createElement("div");
        btnContainer.className = "year-buttons";

        papers.forEach(paper => {
            const btn = document.createElement("button");
            btn.className = "year-btn";
            btn.id = `btn-${subject}-${paper.file}`;
            btn.innerText = paper.label;
            btn.onclick = () => openPaper(subject, paper.file, paper.label);
            btnContainer.appendChild(btn);
        });

        group.appendChild(title);
        group.appendChild(btnContainer);
        navContainer.appendChild(group);
    }
}

// Open exact paper sequentially
async function openPaper(subject, fileName, paperLabel) {
    const container = document.getElementById("questionsContainer");
    const searchInput = document.getElementById("searchInput");
    if (searchInput) searchInput.value = ""; 

    // Update active button state
    document.querySelectorAll(".year-btn").forEach(b => b.classList.remove("active"));
    const activeBtn = document.getElementById(`btn-${subject}-${fileName}`);
    if (activeBtn) activeBtn.classList.add("active");

    const viewTitle = document.getElementById("viewTitle");
    if (viewTitle) viewTitle.innerText = `${subject} - ${paperLabel}`;
    if (container) container.innerHTML = "Loading paper...";

    try {
        const response = await fetch(`data/${subject}/${fileName}.json`);
        if (!response.ok) throw new Error("File not found");
        const questions = await response.json();

        if (questions.length === 0) {
            container.innerHTML = `<p style="color:#777;">No questions added yet for ${subject} ${paperLabel}.</p>`;
        } else {
            renderQuestions(questions, subject, paperLabel);
        }
    } catch (err) {
        if (container) container.innerHTML = `<p style="color:red;">Could not load ${subject} ${paperLabel}.</p>`;
    }
}

async function populateTopicOptions() {
    const subjectSelect = document.getElementById("subjectSelect");
    const topicSelect = document.getElementById("topicSelect");
    if (!topicSelect) return;

    const selectedSubject = subjectSelect ? subjectSelect.value : "All";
    const subjectsToScan = selectedSubject === "All" ? Object.keys(database) : [selectedSubject];
    const topics = new Set(["All Topics"]);

    for (const subject of subjectsToScan) {
        for (const paper of database[subject] || []) {
            try {
                const res = await fetch(`data/${subject}/${paper.file}.json`);
                if (!res.ok) continue;
                const questions = await res.json();
                for (const q of questions || []) {
                    if (q.topic) topics.add(q.topic.trim());
                }
            } catch (e) {}
        }
    }

    const currentValue = topicSelect.value;
    topicSelect.innerHTML = "";

    [...topics].sort().forEach(topic => {
        const option = document.createElement("option");
        option.value = topic;
        option.textContent = topic;
        if (topic === currentValue || (currentValue === "" && topic === "All Topics")) {
            option.selected = true;
        }
        topicSelect.appendChild(option);
    });

    if (![...topicSelect.options].some(option => option.value === currentValue)) {
        topicSelect.value = "All Topics";
    }
}

// Global Keyword Search Mode (searches question text, number, topic, and subject scope)
async function handleSearch() {
    const searchInput = document.getElementById("searchInput");
    const subjectSelect = document.getElementById("subjectSelect");
    const topicSelect = document.getElementById("topicSelect");
    const container = document.getElementById("questionsContainer");
    const viewTitle = document.getElementById("viewTitle");

    if (!searchInput || !container) return;

    const query = searchInput.value.trim().toLowerCase();
    const selectedSubject = subjectSelect ? subjectSelect.value : "All";
    const selectedTopic = topicSelect ? topicSelect.value : "All Topics";

    if (!query) {
        if (viewTitle) viewTitle.innerText = "Select a paper above";
        container.innerHTML = "";
        return;
    }

    document.querySelectorAll(".year-btn").forEach(b => b.classList.remove("active"));

    if (viewTitle) viewTitle.innerText = `Search Results for "${query}"`;
    container.innerHTML = "Searching questions...";

    let matches = [];
    const subjectsToSearch = selectedSubject === "All" ? Object.keys(database) : [selectedSubject];

    for (const subject of subjectsToSearch) {
        for (const paper of database[subject] || []) {
            try {
                const res = await fetch(`data/${subject}/${paper.file}.json`);
                if (res.ok) {
                    const questions = await res.json();
                    questions.forEach(q => {
                        const topic = q.topic ? String(q.topic).trim() : "";
                        const matchesTopic = selectedTopic === "All Topics" || topic === selectedTopic;
                        const matchesQuery =
                            (q.question && q.question.toLowerCase().includes(query)) ||
                            (q.number && q.number.toLowerCase().includes(query)) ||
                            (q.topic && q.topic.toLowerCase().includes(query));

                        if (matchesTopic && matchesQuery) {
                            matches.push({ ...q, subject: subject, paperLabel: paper.label });
                        }
                    });
                }
            } catch (e) {}
        }
    }

    if (matches.length === 0) {
        container.innerHTML = "<p>No matching questions found.</p>";
    } else {
        renderQuestions(matches, null, null, true);
    }
}

// Render Questions
function renderQuestions(items, defaultSubject, defaultPaperLabel, isSearch = false) {
    const container = document.getElementById("questionsContainer");
    if (!container) return;
    container.innerHTML = "";

    items.forEach(item => {
        const sub = isSearch ? item.subject : defaultSubject;
        const paper = isSearch ? item.paperLabel : defaultPaperLabel;

        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
            <div class="card-header">
                <span class="badge">${sub}</span>
                <span class="badge">${paper}</span>
                <span>${item.number}</span>
                ${item.topic ? `<span class="badge topic-badge" style="background:#e0f2fe; color:#0369a1; padding:2px 6px; border-radius:4px; font-size:12px;">${item.topic}</span>` : ''}
            </div>
            <div class="question">${item.question}</div>
        `;

        container.appendChild(card);
    });

    if (window.MathJax && window.MathJax.typesetPromise) {
        MathJax.typesetPromise([container]);
    }
}