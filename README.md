# 🥗 EcoMealAI – Hackathon Submission

## 📌 Category

**Educational Apps** — Helping users learn about sustainable eating while planning weekly meals.

---

## 🚀 What We Built

EcoMealAI is a **Streamlit web app** that makes weekly meal planning sustainable and simple. It integrates with **TheMealDB API** to fetch real recipes, then overlays an **estimated carbon footprint** for each meal to educate users on eco-friendly choices.

### Key Features

* **Weekly Planner**: Build a 7-day plan (Breakfast, Lunch, Dinner).
* **Recipe Candidates**: Pick from top 3 suggested recipes per slot, avoiding duplicates.
* **Preferences**: Set diet, allergies, and sustainability goals.
* **Shopping List**: Auto-generate and export to CSV/PDF.
* **Save/Load Plans**: Unique UID per user session + JSON export for persistence.

---

## 🤖 How We Used Kiro

Kiro was essential for streamlining development:

* **Spec-to-Code Workflow**: We wrote high-level specifications in `/.kiro/requirements.md` (e.g., “weekly planner with candidate picker, no duplicate recipes”) using EARS notation. Kiro generated production-ready Streamlit components, like the recipe search UI, from these specs.
* **Agent Hooks**: Kiro’s hooks in `/.kiro/hooks/` automated updates to `tasks.md` when `app.py` changed, keeping documentation in sync and reducing manual overhead.
* **Vibe Coding**: We used Kiro’s chat interface to refactor deprecated Streamlit calls (e.g., `experimental_rerun` to `st.query_params`) and polish the UI, saving hours of debugging.

Kiro’s AI-driven approach let us focus on user experience and sustainability logic, cutting development time significantly.

---

## 🎥 Demo Video

👉 [Video](https://youtu.be/4V7pPMEnuRo)

---

## 💻 Tech Stack

* **Streamlit**: UI framework
* **TheMealDB API**: Recipe database
* **Python**: Core logic, carbon estimation
* **ReportLab**: PDF export
* **Kiro**: Spec-to-code and refactoring assistance

---

## 📂 Repo Structure

```
EcoMealAI/
├── app.py            # Main Streamlit app
├── requirements.txt  # Dependencies
├── saved_plans/      # Server-saved JSON plans (ignored in .gitignore)
├── .kiro/            # Kiro specs + hooks (required for submission)
```

---

## 📝 Submission Notes

* **Live Demo**: Try EcoMealAI at [https://ecomealai.streamlit.app/](https://ecomealai.streamlit.app/)
* **Run Instructions**:
  ```bash
  pip install -r requirements.txt
  streamlit run app.py
  ```
* **Testing**: Use UID bookmarking or JSON upload to test meal plan persistence.
* **Focus**: Educational impact through sustainable meal choices, teaching users about carbon footprints.

---

**Made with 🌱 during the Hackathon — powered by Kiro.**

**License**: MIT (see [LICENSE](https://github.com/AB2511/EcoMealAI/blob/main/LICENSE))
