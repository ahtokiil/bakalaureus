import json

def convert_questions_to_jsonl_custom_format(input_file, output_file):
    """
    Reads a JSON array of questions from `input_file` and writes
    a .jsonl file in the specified custom batch job format.
    """

    # Load the list of question objects from your JSON file
    with open(input_file, "r", encoding="utf-8") as f_in:
        questions = json.load(f_in)  # e.g. [{ "id": ..., "küsimus": ..., "valikud": [...] }, ...]

    with open(output_file, "w", encoding="utf-8") as f_out:
        for i, item in enumerate(questions):
            # Build the user prompt from your data
            # For example, combine "küsimus" and "valikud" into a single text prompt
            question_text = item.get("küsimus", "")
            valikud_list = item.get("valikud", [])
            
            # We'll replicate the example structure. 
            # "system": "Extract the event information." 
            # "user": your question text.
            
            # You might want to do something like:
            # user_prompt = f"{question_text}\nValikud:\n" + "\n".join(valikud_list)
            user_prompt = f"{question_text}\nValikud:\n"
            for choice in valikud_list:
                user_prompt += f"{choice}\n"

            # Now construct the JSON object for this line
            json_line = {
                "custom_id": f"task-{i}",
                "method": "POST",
                "url": "/chat/completions",
                "body": {
                    "model": "gpt-4o-olympiadbench",  # Overwrite with your actual deployment name
                    "messages": [
                        {
                            "role": "system",
                            "content": "Extract the event information."
                        },
                        {
                            "role": "user",
                            "content": user_prompt.strip()  # the question + choices
                        }
                    ],
                    "response_format": {
                        "type": "json_schema",
                        "json_schema": {
                            "name": "CalendarEventResponse",
                            "strict": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "date": {"type": "string"},
                                    "participants": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": ["name", "date", "participants"],
                                "additionalProperties": False
                            }
                        }
                    }
                }
            }

            # Write this object as one line in JSONL
            f_out.write(json.dumps(json_line, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    input_json = "testset_ILMA_vastusteta.json"    # Your input
    output_jsonl = "JSONL_testset_ILMA_vastusteta.jsonl" # Where to write

    convert_questions_to_jsonl_custom_format(input_json, output_jsonl)
    print(f"Converted {input_json} to {output_jsonl} in the custom format.")
