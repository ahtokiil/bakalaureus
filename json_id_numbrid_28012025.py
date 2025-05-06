import json

def main():
    # Faili nimi ja esimene id-nr
    json_file = "I_aste_küsimused.json"
    first_id_str = 1
    first_id = int(first_id_str)

    # Uus numeratsioon
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    current_id = first_id
    for obj in data:
        if "id" in obj:
            obj["id"] = str(current_id)
            current_id += 1

    # Salvesta JSON-fail
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f'Uuendatud "id" väärtused failis "{json_file}", alates nr: {first_id}.')

if __name__ == "__main__":
    main()
