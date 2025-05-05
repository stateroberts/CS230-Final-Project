"""
Name:       Skylar Roberts, Kyle Marvin, Michael Doria, Isaiah Timas
CS230:      Section 7
Data:       NY Housing Market
URL:        https://cs230-final-project-cw58snrfetwozbstsjazqs.streamlit.app/

Description:
This program allows users to filter their housing search based on a number of characteristics
like broker, price, and number of bedrooms or bathrooms. Users can also view a table and map
with their filtered search, as well as several graphs that analyze the entire dataset.

"""

import streamlit as st
import pandas as pd

# Load the data
df = pd.read_csv("NY-House-Dataset.csv")

# Set title
st.title("New York City House Listings")

#===================================================================================================
# Create tabs
# Chat GPT prompt: how can I make tabs to separate the filters from the table and map?
# [ST4]
tab0,tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home Page","🔎 Filters", "🏙 Listings","🗺 Map","📊 Statistics and Graphs"]) # I think these tabs are very cool!
with tab0:
    st.subheader("CS 230-7 Final Project")
    st.write("Use the tabs above to explore data. Go to the filter page to filter the listings you'd like to see.")

    # Chat GPT prompt: how can I display an image?
    from PIL import Image

    image = Image.open("NYC2.jpg")  # load local image
    st.image(image, use_container_width=True)

with tab1:
    # [DA4] [DA5]
    st.header("Filter Houses")

    # Bedrooms filter with a slider
    # [ST1]
    st.subheader("Filter by Bedrooms")
    min_beds = int(df["BEDS"].min())
    max_beds = int(df["BEDS"].max())

    beds_range = st.slider(
        "Select bedroom range:",
        min_value=min_beds,
        max_value=max_beds,
        value=(min_beds, max_beds),
        step=1
    )

    # Bathrooms filter with a slider
    # [ST1]
    st.subheader("Filter by Bathrooms")
    min_baths = int(df["BATH"].min())
    max_baths = int(df["BATH"].max())

    baths_range = st.slider(
        "Select bathroom range:",
        min_value=min_baths,
        max_value=max_baths,
        value=(min_baths, max_baths),
        step=1
    )

    filtered_df = df[
        (df["BEDS"] >= beds_range[0]) & (df["BEDS"] <= beds_range[1]) &
        (df["BATH"] >= baths_range[0]) & (df["BATH"] <= baths_range[1])
    ]
#===================================================================================================

    # Add way to filter by price range
    # Chat GPT prompt: How can I ask for users to input on max and min price with text boxes in streamlit?
    # [ST2]

    st.subheader("Filter by Price")

    # Get min and max from dataset
    min_price = int(df["PRICE"].min())
    max_price = int(df["PRICE"].max())

    user_min = st.number_input("Enter minimum price:", min_value=min_price, max_value=max_price, value=min_price, step=10000)
    user_max = st.number_input("Enter maximum price:", min_value=min_price, max_value=max_price, value=max_price, step=10000)

    # Validation: user_min should not exceed user_max
    if user_min > user_max:
        st.error("Minimum price cannot be greater than maximum price.")
        filtered_df = filtered_df[0:0]  # Empty DataFrame to avoid crash
    else:
        filtered_df = filtered_df[(filtered_df["PRICE"] >= user_min) & (filtered_df["PRICE"] <= user_max)]

    #===================================================================================================

    # Dictionary mapping simplified city names to actual sublocality strings in the data
    # [PY4] [ST3]
    borough_dict = {
        "Manhattan": "Manhattan",
        "Brooklyn": "Brooklyn",
        "Queens": "Queens",
        "Staten Island": "Staten Island",
        "Bronx": "Bronx"
    }
    st.subheader("Filter by Borough")

    # Let users choose one or more boroughs
    selected_boroughs = st.multiselect(
        "Select borough/boroughs:",
        options=list(borough_dict.keys()),
        default=list(borough_dict.keys())  # or leave empty if you want no default
    )

    # Apply city filter using the dictionary values
    if selected_boroughs:
        mapped_boroughs = [borough_dict[borough] for borough in selected_boroughs]
        filtered_df = filtered_df[filtered_df["SUBLOCALITY"].isin(mapped_boroughs)]

    #===================================================================================================

    # Broker filter with multiselect (empty default, no pre-selection)
    # Chat GPT prompt: How can I add a multiselect for user to choose brokers, but make it so the default is empty?
    # [ST3]
    st.subheader("Filter by Broker")

    broker_options = sorted(df["BROKERTITLE"].dropna().unique())
    selected_brokers = st.multiselect(
        "Select one or more brokers to filter (leave empty to show all):",
        options=broker_options,
        default=[] # [PY3]
    )

    # Apply broker filter only if the user selects any
    if selected_brokers:
        filtered_df = filtered_df[filtered_df["BROKERTITLE"].isin(selected_brokers)]

#===================================================================================================

with tab2:
    st.header("Filtered Listings")
    # Show how many listings match
    # [CHART 1] [DA2]
    st.markdown(f"**Listings found: {len(filtered_df)} (Bedrooms: {beds_range[0]}–{beds_range[1]}, Bathrooms: {baths_range[0]}–{baths_range[1]}, Price: ${user_min:,}–${user_max:,})**")

    # Show results
    st.subheader(f"Houses found:")
    st.dataframe(filtered_df[["TYPE", "PRICE", "BEDS", "BATH", "ADDRESS", "STATE"]])

    # Show top 5 values in table
    # [CHART 2] [DA 3]
    st.subheader("View Top 5 Listings by a Column")

    # Let user select which column to sort
    sort_column = st.selectbox(
        "Select a column to sort by:",
        options=["PRICE", "BEDS", "BATH", "PROPERTYSQFT"]
    )

    # Let user select largest or smallest
    sort_order = st.selectbox(
        "View Top 5:",
        options=["Largest", "Smallest"]
    )

    # Sort and select Top 5
    if sort_order == "Largest":
        top5_df = filtered_df.sort_values(by=sort_column, ascending=False).head(5)
    else:
        top5_df = filtered_df.sort_values(by=sort_column, ascending=True).head(5)

    st.dataframe(top5_df[["TYPE", "PRICE", "BEDS", "BATH", "PROPERTYSQFT", "ADDRESS", "STATE"]])

    # [CHART 3] [DA9]
    st.subheader("Custom Formula Calculator")

    user_formula = st.text_input(
        "Enter a formula using column names (e.g., PRICE / BEDS):"
    )

    if user_formula:
        try:
            result_series = filtered_df.eval(user_formula)
            st.dataframe(result_series)
        except Exception as e:
            st.error(f"Error in formula: {e}")

#===================================================================================================

with tab3:
    st.header("Filtered Map of Listings")
    # Map that allows you to hover over listings for more details
    # Chat GPT prompt: is it possible to make a map that shows you the address, broker, and price when you hover over a dot?
    # [MAP]
    st.markdown("Hover over listings for more details.")
    import pydeck as pdk

    # Rename lat/lon for pydeck
    filtered_df = filtered_df.rename(columns={"LATITUDE": "lat", "LONGITUDE": "lon"})

    # Make sure data types are compatible
    filtered_df["PRICE"] = filtered_df["PRICE"].astype(int)

    # Define the map layer with tooltips
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_df,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 160]',
        get_radius=700,
        pickable=True,
    )

    # Define the view state (centered on New York area)
    view_state = pdk.ViewState(
        latitude=filtered_df["lat"].mean(),
        longitude=filtered_df["lon"].mean(),
        zoom=8,
        pitch=0
    )

    # Tooltip fields
    tooltip = {
        "html": """
            <b>Address:</b> {ADDRESS}<br/>
            <b>Broker:</b> {BROKERTITLE}<br/>
            <b>Price:</b> ${PRICE}
        """,
        "style": {
            "backgroundColor": "white",
            "color": "black"
        }
    }

    # Create and render the map
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    ))

#===================================================================================================

with tab4:
    st.header("Statistics and Graphs")
    # Bedroom histogram
    # Chat GPT prompt: How can I add a histogram using seaborn and change the color to pink?
    # [CHART 4] [SEA 1]
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Only plot if filtered_df is not empty
    if not filtered_df.empty:
        st.subheader("Distribution of Number of Bedrooms")

        fig, ax = plt.subplots()

        # Pink-themed histogram
        sns.histplot(
            filtered_df["BEDS"].dropna(),
            bins=range(int(filtered_df["BEDS"].min()), int(filtered_df["BEDS"].max()) + 2),
            discrete=True,
            ax=ax,
            color="#ff69b4"  # Hot pink
        )

        ax.set_xlabel("Number of Bedrooms")
        ax.set_ylabel("Number of Houses")
        ax.set_title("Histogram of Bedrooms", fontsize=14, color="#d63384")  # Optional: pink title

        st.pyplot(fig)
    else:
        st.info("No listings available to show a bedroom histogram.")

#===================================================================================================

    # Bathroom histogram
    # [CHART 5] [SEA 2]
    if not filtered_df.empty:
        st.subheader("Distribution of Number of Bathrooms")

        fig, ax = plt.subplots()

        sns.histplot(
            filtered_df["BATH"].dropna(),
            bins=range(int(filtered_df["BATH"].min()), int(filtered_df["BATH"].max()) + 2),
            discrete=True,
            ax=ax,
            color="#8a2be2"  # Purple (BlueViolet)
        )

        ax.set_xlabel("Number of Bathrooms")
        ax.set_ylabel("Number of Houses")
        ax.set_title("Histogram of Bathrooms", fontsize=14, color="#6f42c1")

        st.pyplot(fig)
    else:
        st.info("No listings available to show a bathroom histogram.")

#===================================================================================================
    # Scatterplot showing price by the number of bedrooms with a regression line
    # Chat GPT prompt: How can I make a graph that shows number of bedrooms by price with a regression line, excluding outliers?
    # [CHART 6] [SEA 3]
    if not df.empty:
        st.subheader("Price vs. Number of Bedrooms (with Regression Line, Excluding Outliers)")

        # Exclude outliers based on Price
        Q1 = df["PRICE"].quantile(0.25)
        Q3 = df["PRICE"].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        filtered_no_outliers = df[
            (df["PRICE"] >= lower_bound) &
            (df["PRICE"] <= upper_bound)
        ]

        fig, ax = plt.subplots()

        sns.regplot(
            data=filtered_no_outliers,
            x="BEDS",
            y="PRICE",
            scatter=True,
            scatter_kws={"color": "#ff69b4"},  # pink dots
            line_kws={"color": "#800080", "linewidth": 2},  # purple line
            truncate=True,
            ax=ax
        )

        ax.set_xlabel("Number of Bedrooms")
        ax.set_ylabel("Price ($)")
        ax.set_title("Price vs. Bedrooms (Outliers Removed)")

        st.pyplot(fig)

    else:
        st.info("No data available to plot regression.")

#===================================================================================================

    # [PY1, PY2]
    def calculate_price_ratios(df, min_beds, max_price):
        """
        Returns average price per bedroom and bathroom as a dictionary.
        Filters by minimum number of beds and maximum price.
        """
        filtered = df[(df["BEDS"] >= min_beds) & (df["PRICE"] <= max_price)]

        if filtered.empty:
            return {"avg_price_per_bedroom": None, "avg_price_per_bathroom": None}, len(filtered)

        avg_price_per_bed = filtered["PRICE"].sum() / filtered["BEDS"].sum()
        avg_price_per_bath = filtered["PRICE"].sum() / filtered["BATH"].sum()

        result = {
            "avg_price_per_bedroom": round(avg_price_per_bed, 2),
            "avg_price_per_bathroom": round(avg_price_per_bath, 2)
        }

        return result, len(filtered)

    st.subheader("🔍 Custom Price Ratio Calculator")

    min_beds_input = st.number_input("Enter minimum number of bedrooms:", min_value=0, value=2)
    max_price_input = st.number_input("Enter maximum price ($):", min_value=0, value=500000)

    if st.button("Calculate Ratios"):
        ratios, count = calculate_price_ratios(filtered_df, min_beds_input, max_price_input)

        if count == 0:
            st.warning("No listings found with those filters.")
        else:
            st.success(f"Listings matched: {count}")
            st.write("### Results:")
            st.write(f"💰 Avg Price per Bedroom: ${ratios['avg_price_per_bedroom']:,.2f}")
            st.write(f"🛁 Avg Price per Bathroom: ${ratios['avg_price_per_bathroom']:,.2f}")


