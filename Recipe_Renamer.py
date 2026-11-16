"""Renames all recipes to new wood type. Uses birch as template"""

__author__ = "XirohpueLynx"

from pathlib import Path
import json
from typing import TypedDict, NotRequired
import re

RecipeDescription = TypedDict("RecipeDescription", {"identifier": str})
RecipeKey = TypedDict("RecipeKey", {
    "item": NotRequired[str],
    "tag": NotRequired[str]
})
RecipeUnlockItem = TypedDict("RecipeUnlockItem", {
    "item": str,
})

RecipeUnlockContext = TypedDict("RecipeUnlockContext", {
    "context": str
})

RecipeResult = TypedDict("RecipeResult", {"item": str, "count": NotRequired[int]})
RecipeShaped = TypedDict("RecipeShaped", {
    "description": RecipeDescription,
    "tags":        list[str],
    "pattern":     list[str],
    "key":         dict[str, RecipeKey],
    "unlock":      NotRequired[list[RecipeUnlockItem | RecipeUnlockContext]],
    "result":      RecipeResult|list[RecipeResult],
    "priority":    NotRequired[int]
})

RecipeJSON = TypedDict("RecipeJSON", {
    "format_version": str,
    "minecraft:recipe_shaped": RecipeShaped
    })

# List of all the files
IDS = [
    "boat",
    "button",
    "door",
    "fence",
    "fence_gate",
    "pressure_plate",
    "sign",
    "slab",
    "stairs",
    "trapdoor",
    "hilt_wooden_sword"
]

PRE_PATH = "Fast Craft/recipes"

LOG_TYPES = ["oak", "spruce", "birch", "jungle", "acacia", "dark_oak", "mangrove", "cherry", "pale_oak", "poplar"]
STEM_TYPES = ["crimson", "warped"]
# Do bamboo separately since it has differnt ratios

LOG_VARIANTS = ["log", "stripped_log", "wood", "stripped_wood"]
STEM_VARIANTS = ["stem", "stripped_stem", "hyphae", "stripped_hyphae"]

def replace_item_in_json(data: RecipeJSON, old: str, new: str, id_only: bool = False):
    recipe = data["minecraft:recipe_shaped"]

    # Replace in description/identifier
    recipe["description"]["identifier"] = exact_replace(recipe["description"]["identifier"], old, new)

    if id_only: return

    # Replace in key
    for value in recipe["key"].values():
        if "item" in value:
            value["item"] = exact_replace(value["item"], old, new)
        elif "tag" in value:
            value["tag"] = exact_replace(value["tag"], old, new)

    # Replace in result
    result = recipe["result"]
    if isinstance(result, dict):
        result["item"] = exact_replace(result["item"], old, new)
    elif isinstance(result, list):
        for value in result:
            value["item"] = exact_replace(value["item"], old, new)

    # Replace in unlock
    if "unlock" in recipe:
        for condition in recipe["unlock"]:
            if "item" in condition:
                condition["item"] = exact_replace(condition["item"], old, new)
            elif "context" in condition:
                condition["context"] = exact_replace(condition["context"], old, new)

def exact_replace(raw_string: str, old: str, new: str) -> str:
    return re.sub(rf"(?<![^\W_]){old}(?![^\W_])", new, raw_string)

def dump_to_file(data: RecipeJSON, str_path: str):
    output_file = Path(str_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(file=output_file, mode="w", encoding="utf-8") as fileout:
        json.dump(data, fileout, indent=2)
        fileout.write("\n")

def variant_and_type(log_variant: str, log_type: str) -> str:
    log_variant_and_type = log_variant.split("_")
    log_variant_and_type.insert(-1, log_type)
    return "_".join(log_variant_and_type)

# ----------------------- Populate birch variants first ---------------------- #
for id in IDS:
    cur_path = Path(f"{PRE_PATH}/birch/log/birch_{id}_from_log.json")
    for log_variant in LOG_VARIANTS:
        log_variant_type = variant_and_type(log_variant, "birch")
        
        if log_variant == "log": continue
        with open(
            file=cur_path, 
            mode="r", 
            encoding="utf-8"
        ) as cur_file:

            data: RecipeJSON = json.load(fp=cur_file)

            # Replace log variants
            replace_item_in_json(data, "log", log_variant, id_only=True)
            replace_item_in_json(data, "birch_log", log_variant_type)
            
            # Write to file
            dump_to_file(data, f"{PRE_PATH}/birch/{log_variant}/birch_{id}_from_{log_variant}.json")

# -------------- Populate all other log types (excluding bamboo) ------------- #
for id in IDS:
    for log_variant in LOG_VARIANTS:
        cur_path = Path(f"{PRE_PATH}/birch/{log_variant}/birch_{id}_from_{log_variant}.json")

        for log_type in LOG_TYPES:
            if log_type == "birch": continue # No need to run again
            with open(
                file=cur_path, 
                mode="r", 
                encoding="utf-8"
            ) as cur_file:

                data = json.load(fp=cur_file)

                # Replace log types
                replace_item_in_json(data, "birch", log_type)

                # Write to file
                dump_to_file(data, f"{PRE_PATH}/{log_type}/{log_variant}/{log_type}_{id}_from_{log_variant}.json")

# ------------------------- Populate nether log types ------------------------ #
for id in IDS:
    if id == "boat": continue # No Nether boats :'(

    for log_variant, stem_variant in zip(LOG_VARIANTS, STEM_VARIANTS):
        cur_path = Path(f"{PRE_PATH}/birch/{log_variant}/birch_{id}_from_{log_variant}.json")

        base_log_variant = log_variant.split("_")[-1]
        base_stem_variant = stem_variant.split("_")[-1]

        for stem_type in STEM_TYPES:
            with open(
                file=cur_path, 
                mode="r", 
                encoding="utf-8"
            ) as cur_file:

                data = json.load(fp=cur_file)

                # Replace log types & variants
                replace_item_in_json(data, "birch", stem_type)
                replace_item_in_json(data, base_log_variant, base_stem_variant) # Log to stem

                # Write to file
                dump_to_file(data, f"{PRE_PATH}/{stem_type}/{stem_variant}/{stem_type}_{id}_from_{stem_variant}.json")

# ------------------------- Populate bamboo log types ------------------------ #
for id in IDS:
    write_id = "raft" if id == "boat" else id # Bamboo boat is called a raft
    
    for log_variant, block_variant in zip(LOG_VARIANTS[:2], ["block", "stripped_block"]):
        cur_path = Path(f"{PRE_PATH}/birch/{log_variant}/birch_{id}_from_{log_variant}.json")

        base_log_variant = log_variant.split("_")[-1]
        base_block_variant = block_variant.split("_")[-1]

        with open(
            file=cur_path, 
            mode="r", 
            encoding="utf-8"
        ) as cur_file:

            data = json.load(fp=cur_file)

            # Replace log types & variant names
            replace_item_in_json(data, "birch", "bamboo")
            replace_item_in_json(data, id, write_id) # Boat to raft
            replace_item_in_json(data, base_log_variant, base_block_variant) # Log to block

            results = data["minecraft:recipe_shaped"]["result"]
            if isinstance(results, dict) and "count" in results:
                results["count"] = results["count"]//2
            elif isinstance(results, list):
                for value in results:
                    if "count" in value:
                        if value["count"] % 2 != 0: raise ValueError("Count is odd")
                        value["count"] = value["count"]//2
                        if value["count"] == 0: raise ValueError("Count is 0")

            # Write to file
            dump_to_file(data, f"{PRE_PATH}/bamboo/{block_variant}/bamboo_{write_id}_from_{block_variant}.json")
