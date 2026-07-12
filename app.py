import streamlit as st
import pandas as pd

from api import get_classifications, collect_data
from database import insert_all, run_query
from query import queries

# Page Configuration

st.set_page_config(
    page_title="Harvard Art Museum Explorer",
    page_icon="🏛️",
    layout="wide"
)
# ======================================================
# Sidebar
# ======================================================

st.sidebar.title("🏛 Harvard Art Museum")

st.sidebar.markdown("""
## 📋 Features

- 📥 Collect Data from Harvard API
- 👀 View Extracted Data
- 💾 Insert Data into MySQL
- 📊 Execute SQL Queries
- 📈 Automatic Data Visualization
- 📥 Download Query Results as CSV

---

## 🛠 Technologies Used

- Python
- Streamlit
- MySQL
- Harvard Art Museum API
- Pandas
- Requests

---

Developed by **Amit Yadav**
""")
# ======================================================
# Main Title
# ======================================================

st.title("🏛️ Harvard Art Museum Explorer")

st.write("""
This application allows you to:

✅ Extract artifact data from Harvard Art Museum API

✅ Store data into MySQL

✅ Execute SQL queries

✅ Visualize results

✅ Download query output
""")

# About Project

with st.expander("📖 About This Project"):

    st.write("""
This dashboard extracts museum artifacts using the Harvard Art Museum API,
stores them into MySQL, and allows interactive SQL analysis using Streamlit.

Project covers:

- API Integration
- ETL Pipeline
- MySQL
- SQL Analysis
- Streamlit Dashboard
""")

# Classification

classifications = get_classifications()

selected_classification = st.selectbox(
    "Select Classification",
    classifications
)

# KPI Cards

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Selected Classification",
        selected_classification
    )

with col2:

    if "records" in st.session_state:

        st.metric(
            "Records Loaded",
            len(st.session_state["records"])
        )

    else:

        st.metric(
            "Records Loaded",
            0
        )

with col3:

    st.metric(
        "Target Records",
        2500
    )

# Buttons

st.markdown("## Data Collection")

btn1, btn2, btn3 = st.columns(3)

# ------------------------------------------------------

with btn1:

    if st.button("📥 Collect Data"):

        progress = st.progress(0)

        with st.spinner("Collecting records..."):

            records = collect_data(selected_classification)

            st.session_state["records"] = records

        progress.progress(100)

        st.success(
            f"{len(records)} records collected successfully!"
        )

# ------------------------------------------------------

with btn2:

    if st.button("👀 Show Data"):

        if "records" not in st.session_state:

            st.warning("Please collect data first.")

        else:

            st.info(
                "Showing first 100 records."
            )

            st.dataframe(
                st.session_state["records"][:100],
                use_container_width=True
            )

# ------------------------------------------------------

with btn3:

    if st.button("💾 Insert into SQL"):

        if "records" not in st.session_state:

            st.warning(
                "Please collect data first."
            )

        else:

            with st.spinner("Inserting into MySQL..."):

                insert_all(
                    st.session_state["records"]
                )

            st.success(
                f"{len(st.session_state['records'])} records inserted successfully!"
            )

# SQL Dashboard

st.markdown("---")

st.header("📊 SQL Analysis Dashboard")

st.info(
    "Choose a SQL query and click Run Query."
)

selected_query = st.selectbox(
    "Select SQL Query",
    list(queries.keys())
)

# Run Query

if st.button("▶ Run Query"):

    sql = queries[selected_query]

    df = run_query(sql)

    st.success("Query Executed Successfully!")

    st.metric(
        "Rows Returned",
        len(df)
    )

    with st.expander("📄 View Results", expanded=True):

        st.dataframe(
            df,
            use_container_width=True
        )

    # Download CSV

    csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download CSV",
        csv,
        "query_results.csv",
        "text/csv"
    )

    # Charts

    numeric_columns = df.select_dtypes(include="number").columns

    if len(df.columns) == 2 and len(numeric_columns) > 0:

        st.subheader("📊 Visualization")

        chart = df.set_index(df.columns[0])

        st.bar_chart(chart)
        st.line_chart(chart)

# Footer

st.markdown("---")
st.caption(
    "Developed by Amit Yadav | Harvard Art Museum Explorer"
)