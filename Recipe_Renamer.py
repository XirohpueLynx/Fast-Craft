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
    "group":       NotRequired[str],
    "pattern":     list[str],
    "key":         dict[str, RecipeKey],
    "unlock":      NotRequired[RecipeUnlockContext | list[RecipeUnlockItem]],
    "result":      RecipeResult|list[RecipeResult],
    "priority":    NotRequired[int]
})

RecipeShapeless = TypedDict("RecipeShapeless", {
    "description": RecipeDescription,
    "tags":        list[str],
    "group":       NotRequired[str],
    "ingredients": list[RecipeKey],
    "unlock":      NotRequired[RecipeUnlockContext | list[RecipeUnlockItem]],
    "result":      RecipeResult|list[RecipeResult],
    "priority":    NotRequired[int]
})

RecipeJSONShaped = TypedDict("RecipeJSONShaped", {
    "format_version": str,
    "minecraft:recipe_shaped": RecipeShaped
    })

RecipeJSONShapeless = TypedDict("RecipeJSONShapeless", {
    "format_version": str,
    "minecraft:recipe_shapeless": RecipeShapeless
    })

type RecipeJSON = RecipeJSONShaped | RecipeJSONShapeless

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

OAK_IS_WOODEN = ["button", "door", "pressure_plate"]
OAK_IS_NOTHING = ["fence_gate", "trapdoor"]

PRE_PATH = "Fast Craft/recipes"

LOG_TYPES = ["oak", "spruce", "birch", "jungle", "acacia", "dark_oak", "mangrove", "cherry", "pale_oak", "poplar"]
STEM_TYPES = ["crimson", "warped"]
# Do bamboo separately since it has differnt ratios

LOG_VARIANTS = ["log", "stripped_log", "wood", "stripped_wood"]
STEM_VARIANTS = ["stem", "stripped_stem", "hyphae", "stripped_hyphae"]

def replace_item_in_json(
    data: RecipeJSON, old: str, new: str, 
    skip_id: bool = False, skip_key: bool = False, skip_result:bool = False,
    skip_unlock: bool = False, exact: bool = True
    ):
    if "minecraft:recipe_shaped" in data:
        recipe = data["minecraft:recipe_shaped"]
        key_ingredients_vals = recipe["key"].values()
    elif "minecraft:recipe_shapeless" in data:
        recipe = data["minecraft:recipe_shapeless"]
        key_ingredients_vals = recipe["ingredients"]
    else: raise ValueError(f"Unknown fields: {data.keys()}")


    # Replace in description/identifier
    if not skip_id:
        recipe["description"]["identifier"] = exact_replace(recipe["description"]["identifier"], old, new, exact)

    # Replace in key
    if not skip_key:
        for value in key_ingredients_vals:
            if "item" in value:
                value["item"] = exact_replace(value["item"], old, new, exact)
            elif "tag" in value:
                value["tag"] = exact_replace(value["tag"], old, new, exact)

    # Replace in result
    result = recipe["result"]
    if skip_result:
        pass
    elif isinstance(result, dict):
        result["item"] = exact_replace(result["item"], old, new, exact)
    elif isinstance(result, list):
        for value in result:
            value["item"] = exact_replace(value["item"], old, new, exact)

    # Replace in unlock
    if "unlock" in recipe and not skip_unlock:
        if isinstance(recipe["unlock"], list):
            for condition in recipe["unlock"]:
                if "item" in condition:
                    condition["item"] = exact_replace(condition["item"], old, new, exact)
                elif "context" in condition:
                    condition["context"] = exact_replace(condition["context"], old, new, exact)
        elif isinstance((condition := recipe["unlock"]), dict):
            if "item" in condition:
                condition["item"] = exact_replace(condition["item"], old, new, exact)
            elif "context" in condition:
                condition["context"] = exact_replace(condition["context"], old, new, exact)

def exact_replace(raw_string: str, old: str, new: str, exact: bool) -> str:
    if exact:
        return re.sub(rf"(?<![^\W_]){old}(?![^\W_])", new, raw_string)
    return raw_string.replace(old, new)

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
            replace_item_in_json(data, "log", log_variant, skip_key=True, skip_result=True, skip_unlock=True)
            replace_item_in_json(data, "birch_log", log_variant_type)
            
            # Write to file
            dump_to_file(data, f"{PRE_PATH}/birch/{log_variant}/birch_{id}_from_{log_variant}.json")

# -------------- Populate all other log types (excluding bamboo) ------------- #
for id in IDS:
    for log_variant in LOG_VARIANTS:
        cur_path = Path(f"{PRE_PATH}/birch/{log_variant}/birch_{id}_from_{log_variant}.json")

        for log_type in LOG_TYPES:
            is_oak = log_type == "oak"

            if log_type == "birch": continue # No need to run again
            with open(file=cur_path, mode="r", encoding="utf-8") as cur_file:

                data = json.load(fp=cur_file)

                # Replace log types
                replace_item_in_json(data, "birch", log_type)

                # Oak edgecases - WHY ARE THEY STILL CALLED WOODEN??!!!
                if is_oak:
                    if id in OAK_IS_WOODEN:
                        replace_item_in_json(data, f"oak_{id}", f"wooden_{id}")
                    elif id in OAK_IS_NOTHING:
                        replace_item_in_json(data, f"oak_{id}", id)

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
            with open(file=cur_path, mode="r", encoding="utf-8") as cur_file:

                data = json.load(fp=cur_file)

                # Replace log types & variants
                replace_item_in_json(data, "birch", stem_type)
                replace_item_in_json(data, base_log_variant, base_stem_variant) # Log to stem

                # Write to file
                dump_to_file(data, f"{PRE_PATH}/{stem_type}/{stem_variant}/{stem_type}_{id}_from_{stem_variant}.json")

# ------------------------- Populate bamboo log types ------------------------ #
for id in IDS:
    is_raft = id == "boat"
    write_id = "raft" if is_raft else id # Bamboo boat is called a raft

    is_sword = id == "hilt_wooden_sword"
    
    for log_variant, block_variant in zip(LOG_VARIANTS[:2], ["block", "stripped_block"]):
        cur_path = Path(f"{PRE_PATH}/birch/{log_variant}/birch_{id}_from_{log_variant}.json")

        base_log_variant = log_variant.split("_")[-1]
        base_block_variant = block_variant.split("_")[-1]

        with open(file=cur_path, mode="r", encoding="utf-8") as cur_file:

            data = json.load(fp=cur_file)

            # Replace log types & variant names
            replace_item_in_json(data, "birch", "bamboo")
            replace_item_in_json(data, id, write_id) # Boat to raft
            replace_item_in_json(data, base_log_variant, base_block_variant) # Log to block

            if "minecraft:recipe_shaped" in data:
                results = data["minecraft:recipe_shaped"]["result"]
            else:
                results = data["minecraft:recipe_shapeless"]["result"]
            if isinstance(results, dict) and "count" in results:
                results["count"] = results["count"]//2
            elif isinstance(results, list):
                if is_sword or is_raft:
                    idxs = [idx for idx, value in enumerate(results) if value["item"] == f"minecraft:{"bamboo_raft" if is_raft else "wooden_sword" if is_sword else ""}"]
                    if len(idxs) % 2 != 0: raise ValueError("Count is odd")
                    count = len(idxs)//2
                    if count == 0: raise ValueError("Count is 0")
                    for i in range(count):
                        results.pop(idxs[i])

                for value in results:
                    if "count" in value:
                        if value["count"] % 2 != 0: raise ValueError("Count is odd")
                        value["count"] = value["count"]//2
                        if value["count"] == 0: raise ValueError("Count is 0")

            # Write to file
            dump_to_file(data, f"{PRE_PATH}/bamboo/{block_variant}/bamboo_{write_id}_from_{block_variant}.json")


# --------------------- Populate Copper Types & Variants --------------------- #
COPPER_TYPES = [
    "copper_block", "exposed_copper", "weathered_copper", "oxidized_copper",
    "waxed_copper", "waxed_exposed_copper", "waxed_weathered_copper", "waxed_oxidized_copper"
]
ARMOUR = ["boots", "chestplate", "helmet", "leggings"]
for cop_type in COPPER_TYPES[1:]:
    for cur_path in Path(f"{PRE_PATH}/copper/block").iterdir():
        is_chain = "chain" in cur_path.name # Chains use ingots, there's no ingot versions
        is_armour = any(i in cur_path.name for i in ARMOUR) # No armour versions

        with open(cur_path, mode="r", encoding="utf-8") as cur_file:

            data = json.load(cur_file)

            # Create ID
            cur_file_name = cur_path.name.removesuffix(".json")
            cur_desc_id = cur_file_name.replace("copper_block", cop_type)

            # Armours and chains only output regular unwaxed stuff
            if not is_armour and not is_chain:
                cur_desc_id = cur_desc_id.replace("copper", cop_type.removesuffix("_block"), count=1)

            # Manually set id
            if "minecraft:recipe_shaped" in data:
                data["minecraft:recipe_shaped"]["description"]["identifier"] = f"minecraft:{cur_desc_id}"
            else:
                data["minecraft:recipe_shapeless"]["description"]["identifier"] = f"minecraft:{cur_desc_id}"

            replace_item_in_json(data, "_block", "", skip_id=True, exact=False)

            replace_item_in_json(data, "copper", cop_type, skip_id=True, skip_unlock=True, skip_result=is_armour or is_chain)
            if is_chain: replace_item_in_json(data, f"{cop_type}_ingot", "copper_ingot", skip_id=True, skip_result=True, skip_unlock=True)

            # Write to file
            dump_to_file(data, rf"{PRE_PATH}/copper/{cop_type}/{cur_desc_id}.json")
