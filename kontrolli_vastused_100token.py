import json
import re


def arvuta_täpsus(vastuste_fail, mudeli_vastuste_fail, valede_vastuste_fail):
    # Õigete vastuste laadimine JSON-failist
    with open(vastuste_fail, "r", encoding="utf-8") as fail_õiged:
        õiged_vastused_list = json.load(fail_õiged)

    # Mudeli vastuste laadimine JSON-failist
    with open(mudeli_vastuste_fail, "r", encoding="utf-8") as fail_mudel:
        mudeli_vastused = json.load(fail_mudel)

    # Loome õigete vastuste sõnastiku
    õiged_vastused = {}
    for vastus in õiged_vastused_list:
        küsimused_id = vastus["id"]
        õige_vastus = vastus.get("vastus", "").strip().upper()
        õiged_vastused[küsimused_id] = õige_vastus

    õigeid_kokku = 0
    kokku = 0
    vale_vastuse_id = []

    # Kontrollime mudeli vastuseid
    for vastus in mudeli_vastused:
        küsimused_id = vastus["id"]
        mudeli_vastus_raw = vastus.get("mudeli_vastus", "")

        # Leiame esimese suurtähe
        mudeli_vastus_upper = mudeli_vastus_raw.upper()
        match = re.search(r'[A-Z]', mudeli_vastus_upper)
        if match:
            mudeli_vastus = match.group(0)  # esimene suurtäht
        else:
            mudeli_vastus = ""  # suurtäht puudub

        # Võrdleme õige vastusega
        if küsimused_id in õiged_vastused:
            kokku += 1
            if mudeli_vastus == õiged_vastused[küsimused_id]:
                õigeid_kokku += 1
            else:
                vale_vastuse_id.append(küsimused_id)

    # Salvestame valede vastuste ID-d TXT-faili
    with open(valede_vastuste_fail, "w", encoding="utf-8") as f_out:
        for id_ in vale_vastuse_id:
            f_out.write(f"{id_}\n")

    # Arvutame täpsuse
    if kokku == 0:
        return 0.0
    return õigeid_kokku / kokku


if __name__ == "__main__":
    # JSON-fail õigete vastustega
    vastuste_fail = "küsimused_KOOS_vastustega.json"
    # JSON-fail mudeli vastustega
    mudeli_vastuste_fail = "vastused_gpt-4o-olympiadbench_11032025_100token.json"
    # TXT-fail valede vastuste numbritega
    valede_vastuste_fail = "valed_vastused_gpt-4o-olympiadbench_11032025_100token.txt"

    täpsus = arvuta_täpsus(
        vastuste_fail, mudeli_vastuste_fail, valede_vastuste_fail)
    täpsus_protsent = täpsus * 100
    print(f"Mudeli täpsus: {täpsus_protsent:.2f}%")
