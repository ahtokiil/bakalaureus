import openai
import json

# 1) Your API key
openai.api_key = ""

# 2) Load the questions (which contain no answers yet)
input_file = "küsimused_ILMA_vastusteta.json"
with open(input_file, "r", encoding="utf-8") as f_in:
    questions = json.load(f_in)

# 3) We'll store the question objects + the model's answers in this list
answered_questions = []
kys_nr = 1

for item in questions:
    question_text = item["küsimus"]
    valikud_list = item["valikud"]

    # Build a simple text to show the question and possible answers,
    # instruct the model to respond with a single capital letter only.
    user_prompt = f"Küsimus:\n{question_text}\n\nValikud:\n"
    for choice in valikud_list:
        user_prompt += f"{choice}\n"
    user_prompt += "\nPalun anna vastus AINULT ühe suurtähega (ilma selgituseta):"

    # 4) Send the prompt to the OpenAI API with ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",
                "content": "Sa oled bioloogiaolümpiaadil osalev õpilane Eestis."},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1,        # we only want 1 token for the letter
        temperature=0,       # reduce randomness for a 'best guess'
        top_p=1,
        n=1
    )

    # 5) Extract the model's answer (just the single letter).
    model_answer = response["choices"][0]["message"]["content"].strip()

    # 6) Save the answer back into the item, e.g. under "model_vastus"
    item["model_vastus"] = model_answer
    print(f"Küsimus nr {kys_nr}. Vastus: {model_answer}")
    kys_nr += 1

    # Add to the results list
    answered_questions.append(item)

# 7) Write out a new JSON with the model's answers
output_file = "vastused_gpt-4_15022025.json"
with open(output_file, "w", encoding="utf-8") as f_out:
    json.dump(answered_questions, f_out, indent=4, ensure_ascii=False)

print(f"Done! Answers saved to {output_file}")
