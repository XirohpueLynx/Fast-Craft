"""Renames all recipes to new wood type. Uses birch as template"""

__author__ = "XirohpueLynx"

from pathlib import Path
import json
from typing import TypedDict, NotRequired

RecipeDescription = TypedDict("RecipeDescription", {"identifier": str})
RecipeKey = TypedDict("RecipeKey", {
    "item": NotRequired[str],
    "tag": NotRequired[str]
})
RecipeUnlock = TypedDict("RecipeUnlock", {
    "item": NotRequired[str],
    "context": NotRequired[str]
})
RecipeResult = TypedDict("RecipeResult", {"item": str, "count": NotRequired[int]})
RecipeShaped = TypedDict("RecipeShaped", {
    "description": RecipeDescription,
    "tags":        list[str],
    "pattern":     list[str],
    "key":         dict[str, RecipeKey],
    "unlock":      NotRequired[list[RecipeUnlock]],
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
    "stairs",
    "trapdoor",
    "wooden_slab",
    "hilt_wooden_sword"
]

PRE_PATH = "Fast Craft/recipes"

LOG_TYPES = ["oak", "spruce", "birch", "jungle", "acacia", "dark_oak", "mangrove", "cherry", "pale oak", "poplar"]
STEM_TYPES = ["crimson", "warped"]
# Do bamboo separately since it has differnt ratios

LOG_VARIANTS = ["log", "stripped_log", "wood", "stripped_wood"]
STEM_VARIANTS = ["stem", "stripped_stem", "hyphae", "stripped_hyphae"]

# ----------------------- Populate birch variants first ---------------------- #
for id in IDS:
    cur_path = Path(f"{PRE_PATH}/birch/log/birch_{id}_from_log.json")
    for log_variant in LOG_VARIANTS:
        with open(
            file=cur_path, 
            mode="r", 
            encoding="utf-8"
        ) as cur_file:
            if log_variant == "log": continue
            data: RecipeJSON = json.load(fp=cur_file)

            # Replace log variant
            recipe = data["minecraft:recipe_shaped"]
            recipe["description"]["identifier"] = recipe["description"]["identifier"].replace("log", log_variant)
            for value in recipe["key"].values():
                if "item" in value:
                    value["item"] = value["item"].replace("log", log_variant)
                elif "key" in value:
                    value["key"] = value["key"].replace("log", log_variant)
            
            # Write to file
            output_file = Path(f"{PRE_PATH}/birch/{log_variant}/birch_{id}_from_{log_variant}.json")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(file=output_file, mode="w", encoding="utf-8") as fileout:
                json.dump(data, fileout, indent=2)
                fileout.write("\n")

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
            # cur_item = f"{log_type}_{id}" # E.g. oak_boat
                data = json.load(fp=cur_file)

                # Replace log types
                recipe = data["minecraft:recipe_shaped"]
                recipe["description"]["identifier"] = recipe["description"]["identifier"].replace("birch", log_type)
                for value in recipe["key"].values():
                    if "item" in value:
                        value["item"] = value["item"].replace("birch", log_type)
                    elif "key" in value:
                        value["key"] = value["key"].replace("birch", log_type)
                        
                
                result = recipe["result"]
                if isinstance(result, dict):
                    result["item"] = result["item"].replace("birch", log_type)
                elif isinstance(result, list):
                    for value in result:
                        value["item"] = value["item"].replace("birch", log_type)

                # Write to file
                output_file = Path(f"{PRE_PATH}/{log_type}/{log_variant}/{log_type}_{id}_from_{log_variant}.json")
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(file=output_file, mode="w", encoding="utf-8") as fileout:
                    json.dump(data, fileout, indent=2)
                    fileout.write("\n")

# ------------------------- Populate nether log types ------------------------ #
for id in IDS:
    if id == "boat": continue # No Nether boats :'(

    for log_variant, stem_variant in zip(LOG_VARIANTS, STEM_VARIANTS):
        cur_path = Path(f"{PRE_PATH}/birch/{log_variant}/birch_{id}_from_{log_variant}.json")

        for log_type in STEM_TYPES:
            with open(
                file=cur_path, 
                mode="r", 
                encoding="utf-8"
            ) as cur_file:
            # cur_item = f"{log_type}_{id}" # E.g. oak_boat
                data = json.load(fp=cur_file)

                # Replace log types
                recipe = data["minecraft:recipe_shaped"]
                recipe["description"]["identifier"] = recipe["description"]["identifier"].replace("birch", log_type)
                recipe["description"]["identifier"] = recipe["description"]["identifier"].replace("log", stem_variant)
                for value in recipe["key"].values():
                    if "item" in value:
                        value["item"] = value["item"].replace("birch", log_type)
                        value["item"] = value["item"].replace("log", stem_variant)
                    elif "key" in value:
                        value["key"] = value["key"].replace("birch", log_type)
                        value["key"] = value["key"].replace("log", stem_variant)
                        
                
                result = recipe["result"]
                if isinstance(result, dict):
                    result["item"] = result["item"].replace("birch", log_type)
                    result["item"] = result["item"].replace("log", stem_variant)
                elif isinstance(result, list):
                    for value in result:
                        value["item"] = value["item"].replace("birch", log_type)
                        value["item"] = value["item"].replace("log", stem_variant)

                # Write to file
                output_file = Path(f"{PRE_PATH}/{log_type}/{stem_variant}/{log_type}_{id}_from_{stem_variant}.json")
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(file=output_file, mode="w", encoding="utf-8") as fileout:
                    json.dump(data, fileout, indent=2)
                    fileout.write("\n")
