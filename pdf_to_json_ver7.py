import pdfplumber
import json
import re
import os

def aasta_arv(faili_nimi):
    """Extract the year from the filename using a regex."""
    aasta = re.search(r"_(\d{4})_", faili_nimi)
    return aasta.group(1) if aasta else "unknown"

def leia_aste(faili_nimi):
    """Determine the 'aste' value based on filename patterns."""
    if "g" in faili_nimi:
        return "I"
    elif "8_9" in faili_nimi:
        return "II"
    elif "6_7" in faili_nimi:
        return "III"
    else:
        return "unknown"

def eralda_küsimused(faili_nimi):
    aasta = aasta_arv(faili_nimi)
    aste = leia_aste(faili_nimi)

    # 1. Existing question-number patterns like "1.", "2.", "3.", etc.
    question_number_pattern = tuple(f"{i}." for i in range(1, 101))

    # 2. New pattern for lines like "Küsimus 1", "Küsimus 2", etc.
    #    We'll capture the question index if you need it, but here we’ll mostly just trigger a new question.
    question_kusimus_pattern = re.compile(r"^Küsimus\s+(\d+)")

    # 3. Existing answer patterns
    answer_pattern = re.compile(r'^([A-Z])\s?[\.\-–]\s?(.*)')
    answer_pattern_no_punct = re.compile(r'^([A-Z])(\s+.*)?$')

    vormindatud_küsimused = []

    with pdfplumber.open(faili_nimi) as pdf:
        id_küsimus = 1

        küsimus = ""
        valikud = []
        kui_küsimus = False  # Are we reading a question's text lines?
        valik = ""           # Current answer text under construction

        for lehekülg in pdf.pages:
            tekst_leheküljel = lehekülg.extract_text()
            if not tekst_leheküljel:
                continue

            read = tekst_leheküljel.split("\n")

            for rida in read:
                rida = rida.strip()

                # Skip footer lines starting with "EBO"
                if rida.startswith("EBO"):
                    # Finalize the current question if any
                    if küsimus:
                        if valik:
                            valikud.append(" ".join(valik.split()))
                            valik = ""
                        vormindatud_küsimused.append({
                            "id": str(id_küsimus),
                            "küsimus": " ".join(küsimus.split()),
                            "valikud": valikud,
                            "vastus": "X",
                            "punktid": "X",
                            "aasta": aasta,
                            "aste": aste,
                            "teema": "bioloogia"
                        })
                        id_küsimus += 1

                    # Reset everything
                    küsimus = ""
                    valikud = []
                    kui_küsimus = False
                    valik = ""
                    continue

                # --- 1) CHECK FOR A NEW QUESTION (existing pattern "1.", "2.", etc.) ---
                if rida.startswith(question_number_pattern):
                    # Save previous question if it exists
                    if küsimus:
                        if valik:
                            valikud.append(" ".join(valik.split()))
                            valik = ""
                        vormindatud_küsimused.append({
                            "id": str(id_küsimus),
                            "küsimus": " ".join(küsimus.split()),
                            "valikud": valikud,
                            "vastus": "X",
                            "punktid": "X",
                            "aasta": aasta,
                            "aste": aste,
                            "teema": "bioloogia"
                        })
                        id_küsimus += 1

                    # Start a new question: remove "N." prefix (e.g., "3.")
                    küsimus = rida.split(".", 1)[-1].strip()
                    valikud = []
                    valik = ""
                    kui_küsimus = True
                    continue

                # --- 1a) CHECK FOR A NEW QUESTION (new pattern "Küsimus 1", "Küsimus 2", etc.) ---
                match_kusimus = question_kusimus_pattern.match(rida)
                if match_kusimus:
                    # Save previous question if it exists
                    if küsimus:
                        if valik:
                            valikud.append(" ".join(valik.split()))
                            valik = ""
                        vormindatud_küsimused.append({
                            "id": str(id_küsimus),
                            "küsimus": " ".join(küsimus.split()),
                            "valikud": valikud,
                            "vastus": "X",
                            "punktid": "X",
                            "aasta": aasta,
                            "aste": aste,
                            "teema": "bioloogia"
                        })
                        id_küsimus += 1

                    # Start a new question with a blank question text initially.
                    # Next lines (until an answer or next question) will be added to 'küsimus'.
                    küsimus = ""
                    valikud = []
                    valik = ""
                    kui_küsimus = True
                    continue

                # --- 2) CHECK FOR A NEW ANSWER (existing pattern) e.g., "A. text", "B - text", etc. ---
                match_answer = answer_pattern.match(rida)
                if match_answer:
                    # Finalize the previous answer if any
                    if valik:
                        valikud.append(" ".join(valik.split()))
                        valik = ""

                    # Start a new answer
                    kui_küsimus = False
                    valik = match_answer.group(2).strip()
                    continue

                # --- 3) CHECK FOR A NEW ANSWER (new pattern) e.g., "A", "B " or "B some text" ---
                match_answer_no_punct_ = answer_pattern_no_punct.match(rida)
                if match_answer_no_punct_:
                    # If we were building an answer, finalize it
                    if valik:
                        valikud.append(" ".join(valik.split()))
                        valik = ""

                    # Now start a new answer
                    kui_küsimus = False
                    extra_text = match_answer_no_punct_.group(2)
                    if extra_text:
                        valik = extra_text.strip()
                    else:
                        valik = ""
                    continue

                # --- 4) IF WE ARE CURRENTLY BUILDING AN ANSWER, this line is a continuation ---
                if valik:
                    valik += f" {rida}"
                    continue

                # --- 5) IF WE ARE INSIDE A QUESTION BLOCK, this line is a continuation of the question text ---
                if kui_küsimus:
                    küsimus += f" {rida}"
                else:
                    # If not in question mode and not building an answer,
                    # ignore or handle as needed.
                    pass

            # End of page logic — no special handling needed here unless you want to do something.

        # --- 6) After reading all pages, finalize any leftover question ---
        if küsimus:
            if valik:
                valikud.append(" ".join(valik.split()))
                valik = ""
            vormindatud_küsimused.append({
                "id": str(id_küsimus),
                "küsimus": " ".join(küsimus.split()),
                "valikud": valikud,
                "vastus": "X",
                "punktid": "X",
                "aasta": aasta,
                "aste": aste,
                "teema": "bioloogia"
            })
            id_küsimus += 1

    return vormindatud_küsimused

def salvesta_json(andmed, json_faili_nimi):
    with open(json_faili_nimi, "w", encoding="utf-8") as json_file:
        json.dump(andmed, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    faili_nimi = "TK_EBO_PK_PV_vanem_eesti_küsimused_ja_vastused_2023_24.pdf"
    json_faili_nimi = os.path.splitext(faili_nimi)[0] + ".json"

    küsimused = eralda_küsimused(faili_nimi)
    salvesta_json(küsimused, json_faili_nimi)

    print(f"Küsimused salvestatud faili: {json_faili_nimi}.")
