import os
import json


def update_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        amplifier = data.get("Other", {}).get("settings", {}).get("amplifier", [])

        # "1e^5" -> "1e^4"
        updated = False
        for i, val in enumerate(amplifier):
            if val == "1e^5":
                amplifier[i] = "1e^4"
                updated = True

        if updated:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✔ Updated: {file_path}")
        else:
            print(f"Skipped (no match): {file_path}")

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")


def traverse_and_update(root_dir="./results"):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith("settings_") and filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                update_json_file(file_path)


if __name__ == "__main__":
    traverse_and_update("./results")
