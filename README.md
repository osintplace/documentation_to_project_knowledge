# 📘 documentation_to_project_knowledge_genAI_tool

A flexible Python tool that scrapes documentation websites and converts their contents into clean Markdown and structured JSON.  
Designed specifically to create "project knowledge" for GenAI systems like Claude 4.0, ChatGPT, and other LLMs in RAG workflows.

---

## ✅ Features

- 🌐 Supports any documentation site with sidebar navigation
- ✍️ Converts clean HTML into structured Markdown
- 📄 Automatically converts Markdown into structured JSON
- 🧭 Dynamically names output based on domain and timestamp
- 🕒 Configurable crawl delay and output location
- 📁 JSON output ideal for GenAI project embedding (Claude 4.0, LangChain, etc.)
- 💾 Logs failed fetches and saves partial output during scraping
- ⛔ Graceful handling of interruptions

---

## 🤖 Use with GenAI & Project Knowledge

This tool is designed to extract clean, structured documentation from a website and convert it into **project knowledge** for use in GenAI systems such as **Claude 4.0**, **ChatGPT**, or other LLM-based assistants.

Once converted to Markdown or JSON, the documentation can be embedded, indexed, or referenced within your RAG (Retrieval-Augmented Generation) pipeline.

### 📌 Example Use Case: `n8n.io` + Claude 4.0

By ingesting the n8n documentation using this scraper:
- You can teach Claude 4.0 how to **understand and build n8n workflows**
- JSON output enables mapping workflows into **drag-and-drop visual builders**
- Structured Markdown and JSON enhances **semantic retrieval and question answering**

Ideal for:
- Autonomous agents
- Workflow assistants
- Documentation bots
- Knowledge base indexing

> 🔧 Use the `docs_<domain>.json` output as a structured foundation for any system needing precise, contextual understanding of a platform.

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/documentation_to_project_knowledge_genAI_tool.git
cd documentation_to_project_knowledge_genAI_tool
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
python doc_scraper.py https://docs.n8n.io/ --delay 1 --output-dir ./output
```

Outputs:
- `docs_<domain>_<date>.md` (human-readable Markdown)
- `docs_<domain>_<date>.json` (structured GenAI-friendly format)
- `docs_partial.md` (in-progress log)
- `errors.log` (any fetch or parse issues)

---

## 🧪 Example JSON Output

```json
[
  {
    "title": "Webhooks",
    "content": [
      "Webhooks allow n8n to receive real-time data...",
      "You can configure triggers using..."
    ]
  }
]
```

This format can be indexed into vector databases, used in prompt augmentation, or embedded as contextual memory for your GenAI applications.

---

## 🛠 Dependencies

Listed in `requirements.txt`:
- `requests`
- `beautifulsoup4`
- `markdownify`
- `tqdm`

---

## 🤝 Contributing

Feel free to fork and submit pull requests. Suggestions for async support, sitemap integration, or vector DB integrations welcome!

---

## ⚖️ License

MIT License

---

## 📊 Architecture Overview

```
Documentation URL
        ↓
[doc_scraper.py]
        ↓
Markdown (.md) + JSON (.json)
        ↓
GenAI Systems (Claude, ChatGPT, LangChain)
```

---

Built with ❤️ for developers and researchers creating knowledge-enhanced AI.
