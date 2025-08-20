import json
import os
from typing import List, Dict, Optional


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def pick_demods(tree: dict, device_id: str, keep_indices=("1", "3")) -> Dict:
    dev_block = tree.get(device_id, {})
    demods = dev_block.get("demods", {})

    # 兼容键为 int 的情况（转成字符串）
    demods_strkey = {str(k): v for k, v in demods.items()}

    picked = {k: demods_strkey[k] for k in keep_indices if k in demods_strkey}
    return {"demods": picked}


def merge_demods_from_files(
    paths: List[str],
    device_id: str = "dev1657",
    keep_indices=("1", "3"),
    name_map: Optional[Dict[str, str]] = None,
) -> Dict[str, Dict]:
    out = {}
    for p in paths:
        data = load_json(p)
        name = (
            name_map[p]
            if name_map and p in name_map
            else os.path.splitext(os.path.basename(p))[0]
        )
        out[name] = pick_demods(data, device_id=device_id, keep_indices=keep_indices)
    return out


def save_json(obj: dict, out_path: str):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":

    files = [
        "./results/2508191850_amp1_1_amp2_0.01/alldatas_2508191850.json",
        "./results/2508191850_amp1_1_amp2_0.01/alldatas_2508191850.json",
    ]
    name_map = None

    merged = merge_demods_from_files(
        files,
        device_id="dev1657",
        keep_indices=("1", "3"),
    )
    save_json(merged, "./results/merged_demods.json")
