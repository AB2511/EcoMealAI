# app.py
# EcoMealAI - focused on Recipes, Preferences, Shopping List, Weekly Planner
# Features:
# - Single-click "Pick" candidate flow (top 3 suggestions) using TheMealDB
# - Exclude already-picked recipes so you don't get the same recipe repeated
# - Save / Load plan: local download + server-side folder "saved_plans/{uid}.json"
# - CSV + PDF shopping export (reportlab fallback / plain text fallback)
# - Session-state driven, no experimental_rerun usage
# - Landing page with mission and how-to
# - Persistent UID per session using session_state
# - Uses st.query_params instead of deprecated experimental calls
# - Updated use_column_width to use_container_width
# - Increased instruction display limit to 1000 characters

import os
import json
import random
import uuid
import requests
import datetime
from collections import defaultdict

import streamlit as st
import pandas as pd

# ---------------------------
# Config & API keys
# ---------------------------
CLIMATIQ_API_KEY = os.getenv("CLIMATIQ_API_KEY", "")
THEMEALDB_API_KEY = os.getenv("THEMEALDB_API_KEY", "1")  # default free/test key "1"

MEALDB_BASE = "https://www.themealdb.com/api/json/v1"
MEALDB_KEY = THEMEALDB_API_KEY
MEALDB_ROOT = f"{MEALDB_BASE}/{MEALDB_KEY}"

SAVE_DIR = "saved_plans"
os.makedirs(SAVE_DIR, exist_ok=True)

st.set_page_config(page_title="EcoMealAI", page_icon="🥗", layout="wide")

# ---------------------------
# Helper Functions (Moved to Top)
# ---------------------------
def server_save_plan(uid: str):
    payload = {
        "weekly_plan": st.session_state.get("weekly_plan", {}),
        "shopping_list": st.session_state.get("shopping_list", {}),
        "preferences": st.session_state.get("preferences", {}),
        "saved_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    path = os.path.join(SAVE_DIR, f"{uid}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        return True, path
    except Exception as e:
        return False, str(e)

def server_load_plan(uid: str):
    path = os.path.join(SAVE_DIR, f"{uid}.json")
    if not os.path.exists(path):
        return False, "No saved plan for this uid"
    try:
        with open(path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        if "weekly_plan" in obj:
            st.session_state["weekly_plan"] = obj["weekly_plan"]
        if "shopping_list" in obj:
            st.session_state["shopping_list"] = obj["shopping_list"]
        if "preferences" in obj:
            st.session_state["preferences"] = obj["preferences"]
        return True, path
    except Exception as e:
        return False, str(e)

# ---------------------------
# Session-state initialization
# ---------------------------
if "preferences" not in st.session_state:
    st.session_state["preferences"] = {
        "diet": "Any",
        "allergies": [],
        "sustainability": True
    }

if "weekly_plan" not in st.session_state:
    st.session_state["weekly_plan"] = {
        d: {"Breakfast": None, "Lunch": None, "Dinner": None}
        for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    }

if "shopping_list" not in st.session_state:
    st.session_state["shopping_list"] = defaultdict(list)

if "__candidate_picker" not in st.session_state:
    st.session_state["__candidate_picker"] = None

if "planner_max_carbon" not in st.session_state:
    st.session_state["planner_max_carbon"] = 5.0
if "planner_cuisine" not in st.session_state:
    st.session_state["planner_cuisine"] = "Any"
if "planner_diet" not in st.session_state:
    st.session_state["planner_diet"] = "Any"

if "uid" not in st.session_state:
    query_uid = st.query_params.get("uid")
    if query_uid:
        st.session_state["uid"] = query_uid
    else:
        st.session_state["uid"] = str(uuid.uuid4())[:8]
        st.query_params["uid"] = st.session_state["uid"]
USER_UID = st.session_state["uid"]

# ---------------------------
# TheMealDB integration helpers
# ---------------------------
def mealdb_search_by_name(query: str):
    try:
        url = f"{MEALDB_ROOT}/search.php"
        r = requests.get(url, params={"s": query}, timeout=8)
        if r.status_code == 200:
            data = r.json()
            return data.get("meals") or []
    except Exception:
        pass
    return []

def mealdb_lookup_id(meal_id: str):
    try:
        url = f"{MEALDB_ROOT}/lookup.php"
        r = requests.get(url, params={"i": meal_id}, timeout=8)
        if r.status_code == 200:
            data = r.json()
            meals = data.get("meals")
            if meals:
                return meals[0]
    except Exception:
        pass
    return None

def mealdb_list_categories():
    try:
        url = f"{MEALDB_ROOT}/list.php"
        r = requests.get(url, params={"c": "list"}, timeout=8)
        if r.status_code == 200:
            data = r.json()
            return [c["strCategory"] for c in (data.get("meals") or [])]
    except Exception:
        pass
    return []

def mealdb_filter_by_category(cat: str):
    try:
        url = f"{MEALDB_ROOT}/filter.php"
        r = requests.get(url, params={"c": cat}, timeout=8)
        if r.status_code == 200:
            data = r.json()
            return data.get("meals") or []
    except Exception:
        pass
    return []

def parse_mealdb_details(meal_obj):
    if not meal_obj:
        return None
    try:
        rid = meal_obj.get("idMeal")
        title = meal_obj.get("strMeal")
        image = meal_obj.get("strMealThumb")
        instructions = meal_obj.get("strInstructions") or ""
        category = meal_obj.get("strCategory") or "Other"
        area = meal_obj.get("strArea") or "Unknown"
        ingredients = []
        for i in range(1, 21):
            name_k = f"strIngredient{i}"
            measure_k = f"strMeasure{i}"
            name = meal_obj.get(name_k)
            measure = meal_obj.get(measure_k)
            if name and name.strip():
                ingredients.append({
                    "name": name.strip(),
                    "amount": (measure or "").strip()
                })
        return {
            "id": str(rid),
            "title": title,
            "image": image,
            "instructions": instructions,
            "category": category,
            "area": area,
            "ingredients": ingredients
        }
    except Exception:
        return None

# ---------------------------
# Carbon estimation (heuristic)
# ---------------------------
CARBON_KEYWORDS = {
    "beef": 5.0,
    "lamb": 6.0,
    "pork": 4.0,
    "chicken": 2.5,
    "fish": 3.0,
    "salmon": 4.0,
    "avocado": 0.3,
    "rice": 0.5,
    "cheese": 1.0,
    "milk": 0.6,
    "butter": 1.5,
    "olive oil": 0.2
}

def estimate_recipe_carbon_from_ingredients(ingredients):
    total = 0.0
    for ing in ingredients:
        name = (ing.get("name") or "").lower()
        matched = False
        for k, v in CARBON_KEYWORDS.items():
            if k in name:
                total += v
                matched = True
                break
        if not matched:
            total += 0.1
    return round(total, 2)

# ---------------------------
# Candidate selection & helper functions
# ---------------------------
def current_weekly_plan_ids():
    used = set()
    wp = st.session_state.get("weekly_plan", {})
    for d in wp.values():
        if isinstance(d, dict):
            for recipe in d.values():
                if isinstance(recipe, dict) and recipe.get("id"):
                    used.add(str(recipe.get("id")))
    return used

def get_candidates_for_preferences(meal_type, cuisine_pref, diet_pref, max_carbon, top_n=3, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = set()
    pool = []
    tried = set()
    meal_low = (meal_type or "").lower()
    if "breakfast" in meal_low:
        keywords = ["Breakfast", "Egg", "Pancake", "Toast", "Omelet"]
    elif "lunch" in meal_low:
        keywords = ["Salad", "Sandwich", "Soup", "Rice"]
    elif "dinner" in meal_low:
        keywords = ["Curry", "Stew", "Pasta", "Chicken", "Fish"]
    else:
        keywords = ["Meal", "Rice", "Pasta", "Salad"]
    for kw in keywords:
        results = mealdb_search_by_name(kw)
        for r in results:
            mid = r.get("idMeal")
            if not mid or mid in tried or mid in exclude_ids:
                continue
            tried.add(mid)
            detail = mealdb_lookup_id(mid)
            doc = parse_mealdb_details(detail)
            if not doc:
                continue
            doc["carbon"] = estimate_recipe_carbon_from_ingredients(doc.get("ingredients", []))
            if cuisine_pref and cuisine_pref != "Any" and doc.get("area", "").lower() != cuisine_pref.lower():
                doc["_score_penalty"] = 0.5
            else:
                doc["_score_penalty"] = 0.0
            pool.append(doc)
        if len(pool) >= top_n * 4:
            break
    if len(pool) < top_n:
        categories = ["Vegetarian", "Seafood", "Chicken", "Pasta", "Beef"]
        for cat in categories:
            res = mealdb_filter_by_category(cat)
            for r in (res or [])[:40]:
                mid = r.get("idMeal")
                if not mid or mid in tried or mid in exclude_ids:
                    continue
                tried.add(mid)
                detail = mealdb_lookup_id(mid)
                doc = parse_mealdb_details(detail)
                if not doc:
                    continue
                doc["carbon"] = estimate_recipe_carbon_from_ingredients(doc.get("ingredients", []))
                doc["_score_penalty"] = 0.0
                pool.append(doc)
            if len(pool) >= top_n * 4:
                break
    random.shuffle(pool)
    if st.session_state.get("preferences", {}).get("sustainability", True):
        pool = sorted(pool, key=lambda c: (c.get("carbon", 999.0) + c.get("_score_penalty", 0.0)))
    candidates = []
    seen = set()
    for p in pool:
        if p["id"] in exclude_ids or p["id"] in seen:
            continue
        candidates.append(p)
        seen.add(p["id"])
        if len(candidates) >= top_n:
            break
    return candidates

# ---------------------------
# Candidate picker callbacks
# ---------------------------
def open_candidate_picker(day, meal_type):
    max_carbon = st.session_state.get("planner_max_carbon", 5.0)
    cuisine_pref = st.session_state.get("planner_cuisine", "Any")
    diet_pref = st.session_state.get("planner_diet", "Any")
    exclude = current_weekly_plan_ids()
    candidates = get_candidates_for_preferences(meal_type, cuisine_pref, diet_pref, max_carbon, top_n=3, exclude_ids=exclude)
    st.session_state["__candidate_picker"] = {"day": day, "meal_type": meal_type, "candidates": candidates}

def confirm_candidate_pick(selected_id):
    if not st.session_state.get("__candidate_picker"):
        return
    info = st.session_state["__candidate_picker"]
    day = info["day"]
    meal_type = info["meal_type"]
    candidate = None
    for c in info.get("candidates", []):
        if c["id"] == selected_id:
            candidate = c
            break
    if candidate is None:
        st.warning("No candidate selected or candidate not available.")
        st.session_state["__candidate_picker"] = None
        return
    if "weekly_plan" not in st.session_state:
        st.session_state["weekly_plan"] = {
            d: {"Breakfast": None, "Lunch": None, "Dinner": None}
            for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        }
    st.session_state["weekly_plan"][day][meal_type] = candidate
    for ing in candidate.get("ingredients", []):
        cat = "Uncategorized"
        ingredient_entry = {"name": ing.get("name"), "amount": ing.get("amount")}
        if cat not in st.session_state["shopping_list"]:
            st.session_state["shopping_list"][cat] = []
        if ingredient_entry not in st.session_state["shopping_list"][cat]:
            st.session_state["shopping_list"][cat].append(ingredient_entry)
    st.session_state["__candidate_picker"] = None
    st.success(f"Added {candidate.get('title')} to {day} — {meal_type}")

# ---------------------------
# Export helpers
# ---------------------------
def export_shopping_list_csv_bytes(shopping_list):
    rows = []
    for cat, items in shopping_list.items():
        for it in items:
            if isinstance(it, dict):
                rows.append({"Category": cat, "Ingredient": it.get("name"), "Amount": it.get("amount")})
            else:
                rows.append({"Category": cat, "Ingredient": it, "Amount": ""})
    df = pd.DataFrame(rows)
    return df.to_csv(index=False).encode("utf-8")

def export_shopping_list_pdf_bytes(shopping_list):
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.pagesizes import letter
        import io as _io
        buf = _io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)
        styles = getSampleStyleSheet()
        elems = [Paragraph("Shopping List", styles["Title"]), Spacer(1, 8)]
        for cat, items in shopping_list.items():
            elems.append(Paragraph(f"<b>{cat}</b>", styles["Heading2"]))
            for it in items:
                if isinstance(it, dict):
                    elems.append(Paragraph(f"- {it.get('name')} {it.get('amount','')}", styles["Normal"]))
                else:
                    elems.append(Paragraph(f"- {it}", styles["Normal"]))
            elems.append(Spacer(1, 6))
        doc.build(elems)
        buf.seek(0)
        return buf.read()
    except Exception:
        lines = ["Shopping List\n"]
        for cat, items in shopping_list.items():
            lines.append(f"{cat}:")
            for it in items:
                if isinstance(it, dict):
                    lines.append(f"  - {it.get('name')} {it.get('amount','')}")
                else:
                    lines.append(f"  - {it}")
            lines.append("")
        return ("\n".join(lines)).encode("utf-8")

# ---------------------------
# Landing Page UI
# ---------------------------
def landing_page_ui():
    st.header("🥗 Welcome to EcoMealAI")
    st.markdown("""
    ### Our Mission
    EcoMealAI is dedicated to helping you plan delicious, sustainable meals tailored to your preferences. By integrating environmental awareness with personalized meal planning, we aim to reduce your carbon footprint while making meal prep simple, enjoyable, and aligned with your dietary needs.

    ### How to Get Started
    1. **Set Your Preferences**: Go to the *Preferences* page to customize your diet, allergies, and sustainability goals.
    2. **Explore Recipes**: Use the *Recipes* page to search for meals that match your tastes.
    3. **Plan Your Week**: Visit the *Weekly Planner* to build a meal plan with low-carbon recipe suggestions.
    4. **Manage Your Shopping List**: Check the *Shopping List* page to download your ingredients as a CSV or PDF.
    5. **Save Your Plan**: Bookmark this page or save your plan to the server using your unique ID (shown in the sidebar).

    Start planning your eco-friendly meals now!
    """)
    if st.button("Get Started"):
        st.session_state["page"] = "Preferences"

# ---------------------------
# Preferences UI
# ---------------------------
def preferences_ui():
    st.header("⚙️ Preferences")
    prefs = st.session_state.get("preferences", {})
    with st.form("prefs_form"):
        diet = st.selectbox("Diet preference", ["Any", "Vegetarian", "Vegan", "Pescatarian", "Keto", "Gluten Free"], index=0 if prefs.get("diet","Any")=="Any" else None)
        allergies = st.multiselect("Allergies / intolerances", ["Dairy", "Egg", "Gluten", "Peanut", "Seafood", "Sesame", "Shellfish", "Soy", "Tree Nut", "Wheat"], default=prefs.get("allergies", []))
        sustainability = st.checkbox("Prefer sustainable / low carbon meals", value=prefs.get("sustainability", True))
        submitted = st.form_submit_button("Save Preferences")
        if submitted:
            st.session_state["preferences"] = {"diet": diet, "allergies": allergies, "sustainability": sustainability}
            st.success("Preferences saved")

# ---------------------------
# Recipe Finder UI
# ---------------------------
def recipe_search_ui():
    st.header("🍲 Recipe Finder")
    col1, col2, col3 = st.columns([3,1,1])
    with col1:
        q = st.text_input("Search recipes (name)", placeholder="e.g. curry, pasta, chicken")
    with col2:
        max_results = st.slider("Number of recipes", 1, 12, 5)
    with col3:
        use_prefs = st.checkbox("Apply Preferences", value=True)
    prefs = st.session_state.get("preferences", {})
    diet = prefs.get("diet") if use_prefs else None
    intolerances = prefs.get("allergies") if use_prefs else None
    if q:
        results = mealdb_search_by_name(q)
        if not results:
            st.warning("No recipes found. Try different search terms.")
            return
        for r in results[:max_results]:
            detail = mealdb_lookup_id(r.get("idMeal"))
            parsed = parse_mealdb_details(detail)
            if not parsed:
                continue
            with st.expander(parsed.get("title")):
                if parsed.get("image"):
                    st.image(parsed.get("image"), use_container_width=False, width=250)
                st.markdown(f"**Cuisine / Area:** {parsed.get('area')}")
                st.markdown("**Ingredients:**")
                for ing in parsed.get("ingredients", []):
                    st.write(f"- {ing.get('name')} — {ing.get('amount')}")
                st.markdown("**Instructions:**")
                st.write(parsed.get("instructions")[:1000] + ("..." if len(parsed.get("instructions", ""))>1000 else ""))
                carbon_est = estimate_recipe_carbon_from_ingredients(parsed.get("ingredients", []))
                st.info(f"Estimated recipe carbon footprint (heuristic): {carbon_est:.2f} kg CO₂")
                pick_col1, pick_col2 = st.columns([1,3])
                with pick_col1:
                    st.caption("Quick add to plan:")
                    day = st.selectbox("Day", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], key=f"quick_day_{parsed['id']}")
                    meal_type = st.selectbox("Meal", ["Breakfast","Lunch","Dinner"], key=f"quick_meal_{parsed['id']}")
                    if st.button("➕ Add to Plan", key=f"quick_add_{parsed['id']}"):
                        st.session_state["weekly_plan"][day][meal_type] = parsed
                        for ing in parsed.get("ingredients", []):
                            entry = {"name": ing.get("name"), "amount": ing.get("amount")}
                            if "Uncategorized" not in st.session_state["shopping_list"]:
                                st.session_state["shopping_list"]["Uncategorized"] = []
                            if entry not in st.session_state["shopping_list"]["Uncategorized"]:
                                st.session_state["shopping_list"]["Uncategorized"].append(entry)
                        st.success(f"Added {parsed.get('title')} to {day} — {meal_type}")

# ---------------------------
# Shopping List UI
# ---------------------------
def shopping_list_ui():
    st.header("🛒 Shopping List")
    shopping_list = st.session_state.get("shopping_list", {})
    if not shopping_list:
        st.info("Shopping list is empty. Add recipes or pick into weekly plan to populate this.")
        return
    for cat, items in shopping_list.items():
        with st.expander(f"{cat} ({len(items)})", expanded=False):
            for it in items:
                if isinstance(it, dict):
                    st.write(f"- {it.get('name')} — {it.get('amount')}")
                else:
                    st.write(f"- {it}")
    col1, col2 = st.columns(2)
    with col1:
        csv_bytes = export_shopping_list_csv_bytes(shopping_list)
        st.download_button("⬇️ Download CSV", data=csv_bytes, file_name="shopping_list.csv", mime="text/csv")
    with col2:
        pdf_bytes = export_shopping_list_pdf_bytes(shopping_list)
        st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name="shopping_list.pdf", mime="application/pdf")

# ---------------------------
# Weekly Planner UI
# ---------------------------
def weekly_planner_ui():
    st.header("📅 Weekly Meal Planner")
    prefs = st.session_state.get("preferences", {})
    st.markdown("**Active preferences:**")
    st.text(f" Diet: {prefs.get('diet','Any')}")
    st.text(f" Allergies / intolerances: {prefs.get('allergies', [])}")
    st.text(f" Prefer sustainable: {prefs.get('sustainability', True)}")
    control_col1, control_col2, control_col3 = st.columns([1,1,2])
    with control_col1:
        st.session_state["planner_max_carbon"] = st.slider("🌍 Max Carbon Emission per Meal (kg CO₂)", 0.1, 20.0, st.session_state.get("planner_max_carbon", 5.0), 0.1)
    with control_col2:
        st.session_state["planner_cuisine"] = st.selectbox("🍴 Preferred Cuisine", ["Any", "Indian", "Italian", "Chinese", "Mexican", "Mediterranean"], index=0)
    with control_col3:
        st.session_state["planner_diet"] = st.selectbox("🥗 Diet Preference", ["Any", "Vegetarian", "Vegan", "Pescatarian", "Keto"], index=0)
    st.markdown("### 🗓️ Your Weekly Plan")
    for day, meals in st.session_state["weekly_plan"].items():
        with st.expander(f"📅 {day}", expanded=False):
            day_total = 0.0
            for meal_type, recipe in meals.items():
                col1, col2 = st.columns([3,1])
                with col1:
                    if recipe:
                        title = recipe.get("title", "Unknown")
                        st.markdown(f"**{meal_type} — {title}**")
                        if recipe.get("image"):
                            st.image(recipe.get("image"), use_container_width=False, width=220)
                        st.markdown("Ingredients:")
                        for ing in recipe.get("ingredients", []):
                            st.write(f"- {ing.get('name')} — {ing.get('amount')}")
                        st.markdown("Instructions:")
                        st.write(recipe.get("instructions", "")[:1000])
                        carbon = recipe.get("carbon", 0.0)
                        st.caption(f"🌍 Carbon: {carbon:.2f} kg CO₂")
                        day_total += carbon or 0.0
                    else:
                        st.write(f"❌ {meal_type} — Not planned")
                with col2:
                    st.button(f"➕ Pick {meal_type}", key=f"pick_{day}_{meal_type}", on_click=open_candidate_picker, args=(day, meal_type))
            st.caption(f"🌍 Total Carbon for {day}: {day_total:.2f} kg CO₂")
    planned_meals = sum(1 for d in st.session_state["weekly_plan"].values() for r in d.values() if r)
    total_carbon = sum((r.get("carbon",0.0) if isinstance(r, dict) else 0.0) for d in st.session_state["weekly_plan"].values() for r in d.values())
    st.markdown("### 📊 Weekly Summary")
    st.success(f"🍽️ Planned Meals: {planned_meals} | 🌍 Weekly Carbon: {total_carbon:.2f} kg CO₂")
    st.markdown("### 🛒 Shopping List (preview)")
    total_ings = sum(len(v) for v in st.session_state.get("shopping_list", {}).values())
    st.write(f"Ingredients ({total_ings})")
    cp = st.session_state.get("__candidate_picker")
    if cp:
        st.markdown("---")
        st.subheader(f"Select a candidate for {cp['day']} — {cp['meal_type']}")
        candidates = cp.get("candidates", [])
        if not candidates:
            st.info("No compatible candidates found for your preferences.")
            if st.button("Close"):
                st.session_state["__candidate_picker"] = None
        else:
            options = [f"{c['title']} — {c.get('carbon', 0.0):.2f} kg CO₂" for c in candidates]
            sel = st.radio("Choose one", options, index=0)
            chosen_idx = options.index(sel)
            chosen = candidates[chosen_idx]
            st.markdown("Preview:")
            st.markdown(f"**Title:** {chosen.get('title')}")
            st.markdown(f"**Carbon (heuristic):** {chosen.get('carbon', 0.0):.2f} kg CO₂")
            st.markdown("**Ingredients:**")
            for ing in chosen.get("ingredients", []):
                st.write(f"- {ing.get('name')} — {ing.get('amount')}")
            st.markdown("**Instructions (snippet):**")
            st.write(chosen.get("instructions", "")[:1000])
            if st.button("✅ Confirm pick"):
                confirm_candidate_pick(chosen.get("id"))
            if st.button("Cancel"):
                st.session_state["__candidate_picker"] = None

# ---------------------------
# Save / Load (sidebar)
# ---------------------------
with st.sidebar.expander("Save / Load Plan", expanded=True):
    st.write(f"Local UID: `{USER_UID}` (bookmark this URL to keep server-saved plan)")
    if st.button("💾 Save plan to server (overwrite)"):
        ok, msg = server_save_plan(USER_UID)
        if ok:
            st.success(f"Plan saved on server: {msg}")
        else:
            st.error(f"Failed to save plan: {msg}")
    if st.button("📥 Load plan from server"):
        ok, msg = server_load_plan(USER_UID)
        if ok:
            st.success(f"Loaded plan: {msg}")
        else:
            st.warning(f"Load failed: {msg}")
    st.markdown("---")
    data = {
        "weekly_plan": st.session_state.get("weekly_plan", {}),
        "shopping_list": st.session_state.get("shopping_list", {}),
        "preferences": st.session_state.get("preferences", {})
    }
    json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
    st.download_button("⬇️ Download plan (JSON)", data=json_bytes, file_name=f"eco_meal_plan_{USER_UID}.json", mime="application/json")
    uploaded = st.file_uploader("🔁 Upload plan JSON", type=["json"])
    if uploaded is not None:
        try:
            payload = json.load(uploaded)
            if "weekly_plan" in payload:
                st.session_state["weekly_plan"] = payload["weekly_plan"]
            if "shopping_list" in payload:
                st.session_state["shopping_list"] = payload["shopping_list"]
            if "preferences" in payload:
                st.session_state["preferences"] = payload["preferences"]
            st.success("Plan loaded from uploaded JSON")
        except Exception as e:
            st.error(f"Failed to load uploaded file: {e}")

# ---------------------------
# Main Navigation
# ---------------------------
st.sidebar.title("🍽 EcoMealAI Navigation")
if "page" not in st.session_state:
    st.session_state["page"] = "Landing"
page = st.sidebar.radio("Go to", ["Landing", "Preferences", "Recipes", "Shopping List", "Weekly Planner"], index=["Landing", "Preferences", "Recipes", "Shopping List", "Weekly Planner"].index(st.session_state["page"]))
if page != st.session_state["page"]:
    st.session_state["page"] = page
if page == "Landing":
    landing_page_ui()
elif page == "Preferences":
    preferences_ui()
elif page == "Recipes":
    recipe_search_ui()
elif page == "Shopping List":
    shopping_list_ui()
elif page == "Weekly Planner":
    weekly_planner_ui()