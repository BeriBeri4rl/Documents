import re

# Nutrient database
# Stores every nutrient that the parser should search for.
# Each nutrient has a default unit in case OCR cannot detect one.

NUTRIENTS = {
    "Calories": {"default_unit": "kcal"},
    "Total Fat": {"default_unit": "g"},
    "Saturated Fat": {"default_unit": "g"},
    "Trans Fat": {"default_unit": "g"},
    "Cholesterol": {"default_unit": "mg"},
    "Sodium": {"default_unit": "mg"},
    "Total Carbohydrate": {"default_unit": "g"},
    "Dietary Fiber": {"default_unit": "g"},
    "Total Sugars": {"default_unit": "g"},
    "Added Sugars": {"default_unit": "g"},
    "Protein": {"default_unit": "g"},
    "Vitamin D": {"default_unit": "mcg"},
    "Calcium": {"default_unit": "mg"},
    "Iron": {"default_unit": "mg"},
    "Potassium": {"default_unit": "mg"},
    "Vitamin A": {"default_unit": "mcg"},
    "Vitamin C": {"default_unit": "mg"},
    "Vitamin E": {"default_unit": "mg"},
    "Vitamin K": {"default_unit": "mcg"},
    "Magnesium": {"default_unit": "mg"},
    "Zinc": {"default_unit": "mg"},
    "Phosphorus": {"default_unit": "mg"},
    "Folate": {"default_unit": "mcg"},
}


# Unit database
# OCR may read units in different ways.
# Everything is converted into one standard format.

UNITS = {
    "mcg": "mcg",
    "μg": "mcg",
    "ug": "mcg",
    "mg": "mg",
    "milligram": "mg",
    "milligrams": "mg",
    "g": "g",
    "gram": "g",
    "grams": "g",
    "ml": "ml",
    "milliliter": "ml",
    "milliliters": "ml",
    "kcal": "kcal",
    "cal": "kcal",
    "kj": "kJ",
    "%": "%",
}


# Clean OCR mistakes
# EasyOCR commonly mistakes:
# O -> 0
# | -> 1


def clean_ocr_text(text):

    text = text.replace("Og", "0g")
    text = text.replace("Omg", "0mg")
    text = text.replace("Omcg", "0mcg")

    text = text.replace("oG", "0g")
    text = text.replace("OMG", "0mg")

    text = text.replace("|", "1")

    return text


# Extract complete nutrient information from one OCR line
#
# Examples:
#
# 17g
# amount = 17
# unit = g
#
# 250mg
# amount = 250
# unit = mg
#
# 18%
# dv = 18
#
# This prevents % values being mistaken as grams.


def extract_information(text):

    information = {"amount": None, "unit": None, "dv": None}

    lower = text.lower()

    # Remove commas OCR sometimes inserts into numbers.

    lower = lower.replace(",", "")

    # Extract Daily Value percentage

    dv_match = re.search(r"(\d+)\s*%", lower)

    if dv_match:

        information["dv"] = int(dv_match.group(1))

    # Extract nutrient amount with units
    # Order matters:
    # Longer units must come before shorter units.

    amount_match = re.search(
        r"(\d+(?:,\d{3})*\.?\d*)\s*(mcg|μg|ug|mg|g|ml|kcal|kj)", lower
    )

    if amount_match:

        number = amount_match.group(1)

        unit = amount_match.group(2)

        if "." in number:

            information["amount"] = float(number)

        else:

            information["amount"] = int(number)

        information["unit"] = UNITS.get(unit, unit)

    return information


# Detect whether a label contains per 100g information
#
# This is no longer used as a global scoring mode.
# It only helps identify labels where per 100g values may exist.


def detect_per_100(lines):

    joined = " ".join(lines).lower()

    labels = ["per 100g", "per 100 g", "per 100ml", "per 100 ml", "100g", "100 g"]

    for label in labels:

        if label in joined:

            return True

    return False


# Decide how each individual nutrient should be scored.
#
# Priority:
#
# 1. Per 100g if detected
# 2. Daily Value if available
# 3. Amount based scoring


def choose_score_mode(data, has_per_100):

    if has_per_100 and data["amount"] is not None:

        return "per_100g"

    if data["dv"] is not None:

        return "daily_value"

    if data["amount"] is not None:

        return "per_serving"

    return None


# Create an empty nutrition dictionary
# Every nutrient always has the same structure.


def create_nutrition_template():

    nutrition = {}

    for nutrient in NUTRIENTS:

        nutrition[nutrient] = {
            "amount": None,
            "unit": NUTRIENTS[nutrient]["default_unit"],
            "dv": None,
            "score_mode": None,
        }

    return nutrition


# Find which nutrient appears in a line
#
# This is separated so nutrient detection
# is independent from value extraction.


def find_nutrient(line):

    lower = line.lower()

    # Longer names first prevents:
    # "Total Fat" being confused with "Fat"

    nutrient_names = sorted(NUTRIENTS.keys(), key=len, reverse=True)

    for nutrient in nutrient_names:

        if nutrient.lower() in lower:

            return nutrient

    return None


# Main OCR parser
# Converts EasyOCR output into a structured nutrition dictionary.
#
# Each nutrient decides its own scoring method.


def parse_ocr(results):

    # Extract and clean OCR text

    lines = []

    for result in results:

        text = clean_ocr_text(result[1])

        lines.append(text)

    # Check if this label contains per 100g data

    has_per_100 = detect_per_100(lines)

    # Create nutrition storage

    nutrients = create_nutrition_template()

    # Search every OCR line

    for index, line in enumerate(lines):

        nutrient = find_nutrient(line)

        if nutrient is None:

            continue

        # Extract information from current line

        information = extract_information(line)

        # Search the next few OCR lines.
        # OCR often splits one nutrient across multiple lines.
        # Keep filling in missing information until everything is found
        # or another nutrient is reached.

        for offset in range(1, 4):

            if index + offset >= len(lines):

                break

            # Stop searching if another nutrient begins.

            if find_nutrient(lines[index + offset]) is not None:

                break

            next_information = extract_information(lines[index + offset])

            for key, value in next_information.items():

                if information[key] is None and value is not None:

                    information[key] = value

            # Stop early if both amount and Daily Value are found.

            if information["amount"] is not None and information["dv"] is not None:

                break

        # Save extracted information

        nutrients[nutrient]["amount"] = information["amount"]

        nutrients[nutrient]["dv"] = information["dv"]

        if information["unit"] is not None:

            nutrients[nutrient]["unit"] = information["unit"]

        # Decide scoring method for this nutrient

        nutrients[nutrient]["score_mode"] = choose_score_mode(
            nutrients[nutrient], has_per_100
        )

    # Final parser output

    nutrition = {"nutrients": nutrients, "contains_per_100": has_per_100}

    return nutrition
