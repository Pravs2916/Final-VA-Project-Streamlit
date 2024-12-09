import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache_data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

# Load the dataset
file_path = "climate_change_impact_on_agriculture_2024.csv"
data = load_data(file_path)

# App Title
st.title("🌍 Climate Change Impact on Agriculture 🌱")
st.subheader("Analyzing the Effects of Climate Change on Agricultural Production")

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Filters & Visualizations", "Key Insights", "Data Source"])

if data is not None:
    # Home Page
    if menu == "Home":
        st.header("Welcome to the Climate Change Impact on Agriculture!")
        st.write("""
            This interactive app helps to explore how climate change affects agriculture.
            
            Navigate through the pages using the sidebar:
            - Filters & Visualizations: Filter by year and state, and explore dynamic visualizations.
            - Key Insights: Understand critical trends and statistics.
            - Data Source: Information about the data used in this app.
        """)

    # Filters & Visualizations Page
    elif menu == "Filters & Visualizations":
        st.header("Filters & Visualizations")

        # Dropdown filters
        st.subheader("Filters")
        years = sorted(data['Year'].dropna().unique())
        selected_year = st.selectbox("Select Year", options=["All"] + years, index=0)

        states = sorted(data['Region'].dropna().unique())  # Assuming 'Region' contains states
        selected_state = st.selectbox("Select State", options=["All"] + states, index=0)

        # Apply filters
        filtered_data = data.copy()
        if selected_year != "All":
            filtered_data = filtered_data[filtered_data["Year"] == selected_year]
        if selected_state != "All":
            filtered_data = filtered_data[filtered_data["Region"] == selected_state]

        st.write(f"Filtered Dataset: {len(filtered_data)} records")

        # Visualizations
        st.subheader("Visualizations")

        # Visualization 1: CO2 Emissions by Crop Type
        if "Crop_Type" in filtered_data.columns and "CO2_Emissions_MT" in filtered_data.columns:
            emissions_by_crop = filtered_data.groupby("Crop_Type")["CO2_Emissions_MT"].sum().sort_values(ascending=False)
            if not emissions_by_crop.empty:
                st.write("### CO2 Emissions by Crop Type")
                plt.figure(figsize=(10, 6))
                emissions_by_crop.plot(kind="bar", color="skyblue")
                plt.title("CO2 Emissions by Crop Type")
                plt.xlabel("Crop Type")
                plt.ylabel("Total CO2 Emissions (MT)")
                plt.xticks(rotation=45)
                st.pyplot(plt)
            else:
                st.warning("No data available for CO2 Emissions by Crop Type based on selected filters.")

        # Visualization 2: Heat Map for Average Temperature vs Crop Type
        if "Crop_Type" in filtered_data.columns and "Average_Temperature_C" in filtered_data.columns:
            temp_crop_pivot = filtered_data.pivot_table(
                index="Crop_Type", values="Average_Temperature_C", aggfunc="mean"
            )
            if not temp_crop_pivot.empty:
                st.write("### Heat Map: Average Temperature vs Crop Type")
                plt.figure(figsize=(10, 6))
                sns.heatmap(temp_crop_pivot, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Average Temperature (°C)'})
                plt.title("Heat Map: Average Temperature vs Crop Type")
                plt.xlabel("Crop Type")
                plt.ylabel("Average Temperature (°C)")
                st.pyplot(plt)
            else:
                st.warning("No data available for Average Temperature vs Crop Type based on selected filters.")

        # Visualization 3: Crop Yield by Year (Line Graph)
        if "Year" in filtered_data.columns and "Crop_Yield_MT_per_HA" in filtered_data.columns:
            avg_yield_per_year = filtered_data.groupby("Year")["Crop_Yield_MT_per_HA"].mean()
            if not avg_yield_per_year.empty:
                st.write("### Average Crop Yield by Year")
                plt.figure(figsize=(10, 6))
                plt.plot(avg_yield_per_year.index, avg_yield_per_year.values, marker="o", color="green")
                plt.title("Average Crop Yield by Year")
                plt.xlabel("Year")
                plt.ylabel("Crop Yield (MT/HA)")
                plt.xticks(rotation=45)
                st.pyplot(plt)
            else:
                st.warning("No data available for Crop Yield by Year based on selected filters.")

        # Visualization 4: Scatter Plot for Average Temperature by Year
        if "Year" in filtered_data.columns and "Average_Temperature_C" in filtered_data.columns:
            if not filtered_data.empty:
                st.write("### Scatter Plot: Average Temperature by Year")
                plt.figure(figsize=(10, 6))
                plt.scatter(filtered_data["Year"], filtered_data["Average_Temperature_C"], alpha=0.7, color="red")
                plt.title("Scatter Plot: Average Temperature by Year")
                plt.xlabel("Year")
                plt.ylabel("Average Temperature (°C)")
                plt.xticks(rotation=45)
                st.pyplot(plt)
            else:
                st.warning("No data available for Average Temperature by Year based on selected filters.")

    # Key Insights Page
    elif menu == "Key Insights":
        st.header("Key Insights")
        st.write("Here are some insights from the dataset:")
        st.write(f"- Total records: {len(data)}")
        st.write(f"- States covered: {data['Region'].nunique()}")
        st.write(f"- Time range: {data['Year'].min()} - {data['Year'].max()}")
        st.write(f"- Crop types included: {data['Crop_Type'].nunique()}")

        st.subheader("Top 5 States by CO2 Emissions")
        top_states = data.groupby("Region")["CO2_Emissions_MT"].sum().sort_values(ascending=False).head(5)
        st.table(top_states)

        st.subheader("Average Crop Yield by State")
        avg_crop_yield = data.groupby("Region")["Crop_Yield_MT_per_HA"].mean().sort_values(ascending=False)
        st.bar_chart(avg_crop_yield)

    # Data Source Page
    elif menu == "Data Source":
        st.header("Data Source")
        st.write("""
            The dataset used in this application comes from a hypothetical study on the impact of climate change on agriculture.
            
            Columns include:
            - Year: The year of observation.
            - Region: The geographical region/state.
            - Crop_Type: The type of crop studied.
            - Average_Temperature_C: The average temperature recorded in degrees Celsius.
            - CO2_Emissions_MT: The total CO2 emissions in metric tons.
            - Crop_Yield_MT_per_HA: The crop yield measured in metric tons per hectare.
            - Extreme_Weather_Events: The number of extreme weather events recorded.
            
        """)
else:
    st.error("Dataset could not be loaded. Please ensure the file is in the correct directory.")