import json
import time
import openai

# OpenAi teek  Azure jaoks
openai.api_type = "azure"
openai.api_base = "https://tu-openai-api-management.azure-api.net/ltat-tartunlp"
openai.api_version = "2024-08-01-preview"
openai.api_key = ""

# Testküsimuste andmestik
kysimused = "küsimused_ILMA_vastusteta.json"
with open(kysimused, "r", encoding="utf-8") as fail_sisse:
    questions = json.load(fail_sisse)

# Vastuste järjend; küsimuse number kuvamiseks
mudeli_vastused = []
kys_nr = 1

# Küsimuse viip mudeli jaoks
for item in questions:
    küsimuse_tekst = item["küsimus"]
    valikute_nimekiri = item["valikud"]

    viip = f"Küsimus:\n{küsimuse_tekst}\n\nValikud:\n"
    for valik in valikute_nimekiri:
        viip += f"{valik}\n"
    viip += "\nPalun anna lõplik vastus ühe suurtähega:"

    # Päringu esitamine mudelile
    vastus = openai.ChatCompletion.create(
        engine="gpt-4o-mini-olympiadbench",
        messages=[
            {"role": "system",
                "content": "Sa oled bioloogiaolümpiaadil osalev õpilane Eestis."},
            {"role": "user", "content": viip}
        ],
        temperature=0,
        top_p=1,
        max_tokens=800
    )

    # Vastuse eraldamine
    mudeli_vastus = vastus["choices"][0]["message"]["content"].strip()

    # 7) Save the answer back into the item, e.g. under "model_vastus"
    item["model_vastus"] = mudeli_vastus
    print(f"Küsimus nr {kys_nr}. Vastus: {mudeli_vastus}")
    kys_nr += 1
    time.sleep(1)  # Viivitus, et mitte ületada lubatud pöördumiste arvu

    # Add to the results list
    mudeli_vastused.append(item)

# Mudeli vastuste salvestamine JSON-faili
vastuste_fail = "vastused_gpt-4o-mini-olympiadbench_16022025.json"
with open(vastuste_fail, "w", encoding="utf-8") as fail_välja:
    json.dump(mudeli_vastused, fail_välja, indent=4, ensure_ascii=False)

print(f"Vastused on salvestatud faili: {vastuste_fail}.")
