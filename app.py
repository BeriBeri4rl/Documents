import streamlit as st
from PIL import Image
import easyocr
import numpy as np

from parser import parse_ocr
from scoring_model import calculate_score


def main():
    # Load EasyOCR and other modules
    reader = easyocr.Reader(["en"])

    # Configure page
    st.set_page_config(page_title="Nutri Scan", page_icon="🥗")

    # Title

    st.title("🥗 Nutri Scan")

    st.subheader("Nutrition Label Analyzer")

    st.write("Welcome to my IB Personal Project!")

    st.write(
        "This app analyzes nutrition labels using OCR and calculates a health score."
    )

    # Upload image

    uploaded_file = st.file_uploader(
        "Choose a nutrition label image", type=["png", "jpg", "jpeg"]
    )

    # Run only after an image has been uploaded

    if uploaded_file is not None:
        # Open image
        image = Image.open(uploaded_file).convert("RGB")

        # Display image
        st.image(image, caption="Uploaded Nutrition Label", width="stretch")

        st.success("Image uploaded successfully!")

        # Convert image for OCR

        image_array = np.array(image)

        # OCR

        results = reader.readtext(image_array)

        # Parse OCR

        nutrition = parse_ocr(results)

        # Calculate score

        score = calculate_score(nutrition)

        if not score["top_three"]:
            st.warning("No nutritional info detected.")

            with st.expander("Detected OCR Text (Technical Information)"):
                for result in results:
                    st.write(result[1])

            return

        # Nutrition Score

        st.divider()

        st.header("⭐ Nutrition Score")

        left, right = st.columns([1, 2])

        with left:

            st.metric(label="Health Score", value=f"{score['display_score']:.1f}/10")

        with right:

            st.subheader(score["rating"])

        # Rating explanation

        if score["rating"] == "Excellent":

            st.success(
                "This product is nutritionally well balanced and contains many beneficial nutrients."
            )

        elif score["rating"] == "Good":

            st.info(
                "This product contains more healthy than unhealthy nutritional qualities."
            )

        elif score["rating"] == "Average":

            st.warning(
                "This product has a mixture of healthy and unhealthy nutritional qualities."
            )

        elif score["rating"] == "Poor":

            st.warning(
                "This product should be eaten in moderation due to its nutritional profile."
            )

        else:

            st.error(
                "This product contains high amounts of less healthy nutrients and should be consumed sparingly."
            )

        # Top Contributors

        st.subheader("Top Factors Affecting This Score")

        for item in score["top_three"]:

            if item["points"] >= 0:

                st.success(f"🟢 {item['message']} (+{item['points']} points)")

            else:

                st.error(f"🔴 {item['message']} ({item['points']} points)")

        # Parsed Nutrition

        st.divider()

        st.subheader("Parsed Nutrition")

        table_data = []

        for nutrient, info in nutrition["nutrients"].items():

            amount = info["amount"]
            unit = info["unit"]
            dv = info["dv"]

            table_data.append(
                {
                    "Nutrient": nutrient,
                    "Amount": ("Not Found" if amount is None else amount),
                    "Unit": ("-" if unit is None else unit),
                    "%DV": ("-" if dv is None else f"{dv}%"),
                }
            )

        st.table(table_data)

        # OCR Output

        with st.expander("Detected OCR Text (Technical Information)"):

            for result in results:

                st.write(result[1])

    else:

        st.info("Upload a nutrition label image to begin analysis.")

    with st.expander("Developer Information"):

        if "score" in locals():
            st.write("Raw Score:", score["raw_score"])
        else:
            st.write("No analysis yet.")

    st.write(
        "This score is generated using Optical Character Recognition (OCR). While the app aims to read nutrition labels accurately, some labels may contain unusual layouts, poor image quality, or OCR errors. The nutrition score should be used as an estimate rather than a definitive nutritional assessment."
    )

    # Run with:
    # python3 -m streamlit run ./app.py


if __name__ == "__main__":
    main()
# using main was a suggestion from a friend
