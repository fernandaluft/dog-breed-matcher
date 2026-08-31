# Imports
import streamlit as st
import pandas as pd


# Page configuration MUST come before other Streamlit commands
st.set_page_config(page_title="Dog Breed App", page_icon=":material/pets:", layout="wide")

# Load data
df = pd.read_csv(r"data\dog_breeds_processed.csv")

########### Function recommend dogs ##########

def recommend_dogs(size, children, exercise,grooming, shedding, training, health, temperament):
    dogs = df.copy()

 # Hard filters
    if size != "Any":
        dogs = dogs[dogs["Size"] == size]

    if children == "Yes":
        dogs = dogs[dogs["Good with Children"] == "Yes"]

# Exercise match
    dogs["exercise_match"] = dogs["Exercise Requirements (hrs/day)"].apply(
        lambda x: 1
        if x <= exercise
        else max(0, 1 - (x - exercise)))

# Grooming match
    dogs["grooming_match"] = dogs["grooming_score"].apply(
        lambda x: 1
        if x <= grooming
        else max(0, 1 - (x - grooming) / 3))

# Shedding match
    dogs["shedding_match"] = dogs["shedding_score"].apply(
        lambda x: 1
        if x <= shedding
        else max(0, 1 - (x - shedding) / 3))

# Training match
    dogs["training_match"] = dogs[
        "Training Difficulty (1-10)"].apply(
        lambda x: 1
        if x <= training
        else max(0, 1 - (x - training) / 9))

# Health match
    dogs["health_match"] = dogs["health_risk_score"].apply(
        lambda x: 1
        if x <= health
        else max(0, 1 - (x - health) / 2))

# Temperament
    temperament_map = {
        "Affectionate & Social": "affection_sociability",
        "Energetic": "energy_activity",
        "Playful": "playfulness",
        "Calm": "calm_stability",
        "Protective": "protectiveness",
        "Independent": "independence"}

    temperament_columns = [
        temperament_map[choice]
        for choice in temperament]

    if temperament_columns:
        dogs["temperament_match"] = (
            dogs[temperament_columns].sum(axis=1)
            / len(temperament_columns))
    else:
        dogs["temperament_match"] = 1

# Overall score
    dogs["overall_match"] = dogs[
        ["exercise_match",
            "grooming_match",
            "shedding_match",
            "training_match",
            "health_match",
            "temperament_match"]].mean(axis=1)

    dogs["overall_match_pct"] = (dogs["overall_match"] * 100).round(1)

    dogs = dogs.sort_values("overall_match",ascending=False).reset_index(drop=True)

    return dogs

# Sidebar
st.sidebar.title(":dog: Dog facts no one asked")
st.sidebar.caption("Because apparently comparing 150 dog breeds with Python "
    "is a perfectly reasonable way to spend a weekend.")
st.sidebar.link_button("Auf!", "mailto:fernandaluft@gmail.com")

# Main page
st.title(":material/pets: Find Your Pawfect Match")

st.caption("A highly scientific way to find the dog breed that fits your life. "
    "Okay, mostly data. But also dogs.")

st.header("Meet your new best friend")

# Form

with st.form("dog_match_form"):
    st.subheader("Your lifestyle")
    size_map = {
        "Small — lap-sized": "Small",
        "Medium — best of both worlds": "Medium",
        "Large — more dog to love": "Large",
        "Surprise me": "Any"}

    size = st.pills(
        "🏠 What size dog suits your home?",
        list(size_map.keys()),
        selection_mode="single")

    size_value = (
        size_map[size]
        if size is not None
        else None)

    children_map = {
        "Yes — tiny humans included": "Yes",
        "No — adults-only household": "No"}

    children = st.pills(
        "👶 Will the dog be around children?",
        list(children_map.keys()),
        selection_mode="single")

    children_value = (
        children_map[children]
        if children is not None
        else None)

    st.subheader("The practical stuff")

    shedding = st.selectbox(
        "🧹 How much dog hair are you prepared to find on your clothes?",
        options=(
            "Almost none, please",
            "A little is fine",
            "I can live with it",
            "Hair everywhere. I've accepted my fate"),index=None)

    grooming = st.selectbox(
        "✂ How committed are you to grooming?",
        options=(
            "Low maintenance only",
            "A little brushing is fine",
            "Regular grooming is okay",
            "I don't mind having a canine beauty routine"), index=None)

    health_options = {
        "I'd prefer a breed with fewer health concerns": 1,
        "Some health risks are okay": 2,
        "Not a deciding factor for me": 3}

    health_label = st.selectbox(
        "🩺 How important is lower health risk to you?",
        options=list(health_options.keys()),
        index=None)

    health = (
        health_options[health_label]
        if health_label is not None
        else None)

    st.subheader("🐾 Life together")

    training = st.selectbox(
        "🎓 How much of a training challenge are you up for?",
        options=(
            "Please make it easy",
            "I can handle a little stubbornness",
            "I enjoy a challenge",
            "Challenge accepted"),index=None)

    exercise_options = {
        "About 1 hour — civilized walks": 1.0,
        "Around 1.5 hours — reasonably active": 1.5,
        "Around 2 hours — I like being outside": 2.0,
        "Around 2.5 hours — very active": 2.5,
        "3 hours — my dog may become my personal trainer": 3.0}

    exercise_label = st.radio(
        "🚶 How much exercise can you realistically provide?",
        options=list(exercise_options.keys()),
        index=None)

    exercise_hours = (
        exercise_options[exercise_label]
        if exercise_label is not None
        else None)

    shedding_map = {
        "Almost none, please": 1,
        "A little is fine": 2,
        "I can live with it": 3,
        "Hair everywhere. I've accepted my fate": 4}

    grooming_map = {
        "Low maintenance only": 1,
        "A little brushing is fine": 2,
        "Regular grooming is okay": 3,
        "I don't mind having a canine beauty routine": 4}

    training_map = {
        "Please make it easy": 3,
        "I can handle a little stubbornness": 5,
        "I enjoy a challenge": 7,
        "Challenge accepted": 10}

    shedding_value = (
        shedding_map[shedding]
        if shedding is not None
        else None)

    grooming_value = (
        grooming_map[grooming]
        if grooming is not None
        else None)

    training_value = (
        training_map[training]
        if training is not None
        else None)

    st.subheader("✨ Personality matters")
    st.caption("Choose as many as you like. Dogs contain multitudes.")

    user_temperament = st.pills(
        "What personality do you prefer?",
        [   "Affectionate & Social",
            "Energetic",
            "Playful",
            "Calm",
            "Protective",
            "Independent"], selection_mode="multi")

    find_match = st.form_submit_button("🐾 Find my dog match",
        type="primary", use_container_width=True)

# Results
if find_match:
    required_values = [
        size_value,
        children_value,
        exercise_hours,
        grooming_value,
        shedding_value,
        training_value,
        health]

    if any(value is None for value in required_values):
        st.warning("Please answer all the questions before "
            "I start sniffing through the data 🐕")
    else:
        with st.spinner("Sniffing through the data..."):
            result = recommend_dogs(size_value, children_value, exercise_hours,
                grooming_value,shedding_value,training_value,health, user_temperament)

        if result.empty:
            st.warning("No matches found with these choices. "
                "Try relaxing one of your preferences.")
        else:
            st.success("We found some very good dogs for you. "
                "This was inevitable.")

            winner = result.iloc[0]
            st.markdown("### 🥇 Your #1 match")
            st.write(winner["Name"])
            if pd.notna(winner["image_url"]):
                st.image(winner["image_url"], width=400)
            st.write("A little bit of history: ", result["history"].iloc[0])
            st.write("They are ", result["temperament"].iloc[0], ".")

            st.dataframe(
                result[["Name",
                        "overall_match_pct",
                        "exercise_match",
                        "grooming_match",
                        "shedding_match",
                        "training_match",
                        "health_match",
                        "temperament_match"]].head(5), hide_index=True)