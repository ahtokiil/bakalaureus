import json

def merge_json_files_and_reset_ids(file1, file2, file3, output_file):
    """
    Simply merges the lists of objects from three JSON files into one list
    and then resets the 'id' values to start from 1 (no duplicate checking).
    """

    combined_list = []

    # Helper to load each file and append its items
    def load_and_append(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            combined_list.extend(data)

    # 1) Load all three files
    load_and_append(file1)
    load_and_append(file2)
    load_and_append(file3)

    # 2) Renumber the items' 'id' fields from 1 onward
    for i, item in enumerate(combined_list, start=1):
        item["id"] = str(i)

    # 3) Write the merged list to the output file
    with open(output_file, "w", encoding="utf-8") as f_out:
        json.dump(combined_list, f_out, ensure_ascii=False, indent=4)

    print(f"Merged {len(combined_list)} items into {output_file}, IDs reset from 1 to {len(combined_list)}.")

if __name__ == "__main__":
    f1 = "I_aste_küsimused.json"
    f2 = "II_aste_küsimused.json"
    f3 = "III_aste_küsimused.json"
    out = "küsimused_KOOS_vastustega.json"

    merge_json_files_and_reset_ids(f1, f2, f3, out)
