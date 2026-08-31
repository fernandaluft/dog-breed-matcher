# Import Python packages
import json
import pandas as pd
import re

# Load dataset
df = pd.read_json("data/dog_breeds_raw.json")

print(df.head())
print(df.shape)
print(df.info())

# Check for duplicates
print("Duplicated IDs:", df["id"].duplicated().sum())
print("Duplicated names:", df["name"].duplicated().sum())

duplicates = df[df["name"].duplicated(keep=False)]

print(duplicates[["id", "name", "breed_group", "origin"]])

print(df.isnull().sum())

missing = pd.DataFrame({
    "missing_count": df.isnull().sum(),
    "missing_pct": df.isnull().mean() * 100})

missing = missing.sort_values("missing_pct", ascending=False)

print(missing)
print(df.dtypes)
print(df[["id", "name", "breed_group", "origin"]].nunique())

# Function to parse ranges of weight and height
def parse_range(value, unit="metric"):
    if not isinstance(value, dict):
        return pd.Series([None, None, None])
    metric = value.get(unit)
    if not metric:
        return pd.Series([None, None, None])
    numbers = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", metric)]
    if not numbers:
        return pd.Series([None, None, None])
    min_value = min(numbers)
    max_value = max(numbers)
    midpoint = (min_value + max_value) / 2
    return pd.Series([min_value, max_value, midpoint])


# Parse weight - get min, max and calculate average from metric system
df[["weight_min_kg", "weight_max_kg", "weight_avg_kg"]] = (df["weight"].apply(parse_range))

# Parse height - get min, max and calculate average from metric system
df[["height_min_cm", "height_max_cm", "height_mid_cm"]] = (df["height"].apply(parse_range))

print(df[["weight_min_kg", "weight_max_kg", "height_min_cm", "height_max_cm"]].describe())
duplicates = df[df["name"] == "Caucasian Shepherd Dog"]

print(duplicates.isna().sum(axis=1))

df = df.drop_duplicates(subset="name", keep="first")

print(df["life_span"].dropna().unique())

df[["life_span_min_years", "life_span_max_years"]] = (df["life_span"].str.split("-", expand=True))
df["life_span_min_years"] = pd.to_numeric(df["life_span_min_years"], errors="coerce")
df["life_span_max_years"] = pd.to_numeric(df["life_span_max_years"], errors="coerce")
df["life_span_mid_years"] = (df["life_span_min_years"] + df["life_span_max_years"]) / 2

print("Original nulls:", df["life_span"].isna().sum())
print("Parsed nulls:", df["life_span_min_years"].isna().sum())

# Inspecting temperament
temperaments = (df["temperament"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .str.lower())
print("Unique temperament terms:", temperaments.nunique())
print(temperaments.value_counts())

odd_temp = df[df["temperament"].str.contains(
    "variable depending on ancestry",
    case=False,
    na=False
)]
print(odd_temp[["name", "temperament"]])

term_to_remove = "variable depending on ancestry and individual traits"

df["temperament"] = (
    df["temperament"]
    .apply(lambda x: ", ".join(term.strip() for term in x.split(",") if term.strip().lower() != term_to_remove)
            if pd.notna(x) else x))

temperaments = (df["temperament"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .str.lower())
temperaments = temperaments[temperaments != ""]
print(df[
    df["temperament"]
    .fillna("")
    .str.contains(
        "variable depending on ancestry",
        case=False
    )
])
print("Unique temperament terms:", temperaments.nunique())
# print(temperaments.value_counts())
print(
    temperaments[
        temperaments.str.contains(
            "variable depending on ancestry",
            na=False
        )
    ]
)

print(sorted(temperaments.unique()))