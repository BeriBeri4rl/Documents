# Converts parsed nutrition information into an easy-to-understand nutrition score.

# THRESHOLD DATABASE

# Each nutrient contains:

# type: 
# positive or negative

# weight:
# How important this nutrient is compared to others.

# daily_value:
# Thresholds used when a Daily Value percentage exists.

# per_serving:
# Thresholds used when only the nutrient amount exists.

# per_100g:
# Thresholds used for European / Australian labels.


THRESHOLDS = {
    "Dietary Fiber": {
        "type": "positive",
        "weight": 2.2,
        "daily_value": [(8, 1), (18, 2), (30, 3)],
        "per_serving": [(2, 1), (4, 2), (7, 3)],
        "per_100g": [(2.5, 1), (5, 2), (8, 3)],
    },
    "Protein": {
        "type": "positive",
        "weight": 2,
        "daily_value": [(8, 1), (18, 2), (30, 3)],
        "per_serving": [(5, 1), (10, 2), (18, 3)],
        "per_100g": [(5, 1), (10, 2), (18, 3)],
    },
    "Potassium": {
        "type": "positive",
        "weight": 1.5,
        "daily_value": [(8, 1), (18, 2), (30, 3)],
        "per_serving": [(200, 1), (400, 2), (650, 3)],
        "per_100g": [(150, 1), (300, 2), (600, 3)],
    },
    "Iron": {
        "type": "positive",
        "weight": 1.5,
        "daily_value": [(8, 1), (15, 2), (25, 3)],
        "per_serving": [(2, 1), (4, 2), (8, 3)],
        "per_100g": [(2, 1), (4, 2), (8, 3)],
    },
    "Calcium": {
        "type": "positive",
        "weight": 1.4,
        "daily_value": [(8, 1), (18, 2), (30, 3)],
        "per_serving": [(100, 1), (250, 2), (450, 3)],
        "per_100g": [(100, 1), (250, 2), (450, 3)],
    },
    "Vitamin D": {
        "type": "positive",
        "weight": 1.2,
        "daily_value": [(8, 1), (18, 2), (30, 3)],
        "per_serving": [(2, 1), (5, 2), (8, 3)],
        "per_100g": [(2, 1), (5, 2), (8, 3)],
    },
    "Vitamin A": {
        "type": "positive",
        "weight": 1.5,
        "daily_value": [(8, 1), (18, 2), (30, 3)],
        "per_serving": [(75, 1), (150, 2), (300, 3)],
        "per_100g": [(75, 1), (150, 2), (300, 3)],
    },
    "Vitamin C": {
        "type": "positive",
        "weight": 1.5,
        "daily_value": [(8, 1), (18, 2), (35, 3)],
        "per_serving": [(10, 1), (25, 2), (50, 3)],
        "per_100g": [(10, 1), (25, 2), (50, 3)],
    },
    "Vitamin E": {
        "type": "positive",
        "weight": 1.2,
        "daily_value": [(8, 1), (18, 2), (35, 3)],
        "per_serving": [(2, 1), (5, 2), (10, 3)],
        "per_100g": [(2, 1), (5, 2), (10, 3)],
    },
    "Vitamin K": {
            "type": "positive",
            "weight": 2.0,
            "daily_value": [(8, 1), (18, 2), (35, 3)],
            "per_serving": [(2, 1), (5, 2), (10, 3)],
            "per_100g": [(2, 1), (5, 2), (10, 3)],
        },
    "Magnesium": {
        "type": "positive",
        "weight": 1.3,
        "daily_value": [(8, 1), (18, 2), (35, 3)],
        "per_serving": [(40, 1), (80, 2), (160, 3)],
        "per_100g": [(40, 1), (80, 2), (160, 3)],
    },
    "Zinc": {
        "type": "positive",
        "weight": 1.2,
        "daily_value": [(8, 1), (18, 2), (35, 3)],
        "per_serving": [(2, 1), (5, 2), (8, 3)],
        "per_100g": [(2, 1), (5, 2), (8, 3)],
    },
    "Phosphorus": {
        "type": "positive",
        "weight": 1.2,
        "daily_value": [(8, 1), (18, 2), (35, 3)],
        "per_serving": [(100, 1), (250, 2), (500, 3)],
        "per_100g": [(100, 1), (250, 2), (500, 3)],
    },
    "Folate": {
        "type": "positive",
        "weight": 1.8,
        "daily_value": [(8, 1), (18, 2), (35, 3)],
        "per_serving": [(40, 1), (80, 2), (160, 3)],
        "per_100g": [(40, 1), (80, 2), (160, 3)],
    },
    "Added Sugars": {
        "type": "negative",
        "weight": 2,
        "daily_value": [(3, 0.5), (5, -0.5), (10, -2), (20, -3), (25, -4)],
        "per_serving": [(3, 0.5), (5, -0.5), (10, -2), (18, -3), (25, -4)],
        "per_100g": [(3, 0.5), (5, -0.5), (10, -2), (18, -3), (25, -4)],
    },
    "Total Sugars": {
        "type": "negative",
        "weight": 1.6,
        "daily_value": [(10, -1), (20, -2), (35, -3)],
        "per_serving": [(8, -1), (16, -2), (28, -3)],
        "per_100g": [(8, -1), (16, -2), (28, -3)],
    },
    "Saturated Fat": {
        "type": "negative",
        "weight": 2.0,
        "daily_value": [(0.5, 0.5), (5, -1), (10, -2), (20, -3)],
        "per_serving": [(0.5, 0.5), (2, -1), (5, -2), (8, -3)],
        "per_100g": [(0.5, 0.5), (2, -1), (5, -2), (8, -3)],
    },
    "Trans Fat": {
        "type": "negative",
        "weight": 0.9,
        "daily_value": [(0.5, 0.5), (2, -1), (5, -2)],
        "per_serving": [(0.5, 0.5), (1, -1), (3, -2)],
        "per_100g": [(0.5, 0.5), (1, -1), (3, -2)],
    },
    "Sodium": {
        "type": "negative",
        "weight": 1.8,
        "daily_value": [(5, -1), (10, -2), (20, -3)],
        "per_serving": [(120, -1), (350, -2), (700, -3)],
        "per_100g": [(120, -1), (350, -2), (700, -3)],
    },
    "Cholesterol": {
        "type": "negative",
        "weight": 1.2,
        "daily_value": [(5, -1), (10, -2), (20, -3)],
        "per_serving": [(20, -1), (60, -2), (100, -3)],
        "per_100g": [(20, -1), (60, -2), (100, -3)],
    },
    "Total Fat": {
        "type": "negative",
        "weight": 0.8,
        "daily_value": [(8, -1), (18, -2), (30, -3)],
        "per_serving": [(6, -1), (15, -2), (28, -3)],
        "per_100g": [(6, -1), (15, -2), (28, -3)],
    },
}

# FRIENDLY USER MESSAGES

MESSAGES = {
    "Dietary Fiber": "High dietary fiber content supports healthy digestion.",
    "Protein": "Good protein content helps with muscle growth and repair.",
    "Potassium": "Good potassium content supports normal muscle and nerve function.",
    "Iron": "Good iron content helps transport oxygen around the body.",
    "Calcium": "Good calcium content supports healthy bones and teeth.",
    "Vitamin D": "Good vitamin D content helps calcium absorption.",
    "Added Sugars": "High added sugar content may negatively affect health.",
    "Total Sugars": "High sugar content should be consumed in moderation.",
    "Saturated Fat": "High saturated fat intake should be limited.",
    "Sodium": "High sodium intake may contribute to high blood pressure.",
    "Cholesterol": "High cholesterol intake should be monitored.",
    "Total Fat": "High total fat content may increase calorie intake.",
}

# HELPER FUNCTIONS

# Convert a nutrient value into points.
# The thresholds are searched from lowest to highest.
# The highest matching threshold becomes the final score.


def get_points(value, thresholds):

    points = 0

    for limit, score in thresholds:

        if value >= limit:

            points = score

    return points


# Apply the nutrient weighting.
# Example:
# 3 points
# ×
# weight 2
# =
# 6 weighted points


def apply_weight(points, weight):

    return points * weight


# Convert a raw score into a 0–10 display score.
# These limits were calibrated using real nutrition labels rather than theoretical maximum values.


def normalise_score(raw_score):

    MIN_RAW = -12

    MAX_RAW = 16

    score = ((raw_score - MIN_RAW) / (MAX_RAW - MIN_RAW)) * 10

    return max(0, min(10, score))


# MAIN SCORING FUNCTION

# Calculates the final nutrition score.
# Every nutrient decides its own scoring method:
# Daily Value
# Per Serving
# Per 100g


def calculate_score(nutrition):

    nutrients = nutrition["nutrients"]

    raw_score = 0

    contributions = []

    # Maximum possible score.
    # Used only for debugging and future tuning.

    max_positive = 0

    max_negative = 0

    # Score every nutrient independently.

    for nutrient, values in nutrients.items():

        if nutrient not in THRESHOLDS:

            continue

        threshold_info = THRESHOLDS[nutrient]

        score_mode = values["score_mode"]

        # Skip nutrients that could not be parsed.

        if score_mode is None:

            continue

        # Decide which value should be used.

        if score_mode == "daily_value":

            value = values["dv"]

        else:

            value = values["amount"]

        if value is None:

            continue

        # Select the correct threshold table.

        thresholds = threshold_info[score_mode]

        # Calculate base points.

        points = get_points(value, thresholds)

        # Apply nutrient weighting.

        weighted_points = apply_weight(points, threshold_info["weight"])

        raw_score += weighted_points

        # Save contribution.

        contributions.append(
            {
                "nutrient": nutrient,
                "message": MESSAGES.get(
                    nutrient, f"{nutrient} contributes to the nutrition score."
                ),
                "mode": score_mode,
                "points": round(weighted_points, 2),
            }
        )

    # Convert to display score.

    display_score = normalise_score(raw_score)

    # Determine rating.

    if display_score >= 9:

        rating = "Excellent"

    elif display_score >= 7:

        rating = "Good"

    elif display_score >= 5:

        rating = "Average"

    elif display_score >= 3:

        rating = "Poor"

    else:

        rating = "Very Poor"

    # Sort biggest impacts first.

    contributions.sort(key=lambda item: abs(item["points"]), reverse=True)

    top_three = contributions[:3]

    # Build final result.

    return {
        "raw_score": round(raw_score, 2),
        "display_score": round(display_score, 1),
        "rating": rating,
        "top_three": top_three,
    }
