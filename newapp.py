# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Exploratory Data Analysis DashBoard")

# Upload data
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file is not None:
    # Load data into a DataFrame
    data = pd.read_csv(uploaded_file)
    
    print(data.info())
    st.sidebar.title("Data Overview")


    st.sidebar.subheader("Data Information")
    if st.sidebar.button("Show Data Information"):
        st.subheader("Data Information")
          
        null_counts = data.isnull().sum()
        data_types = data.dtypes

            
        info_df = pd.DataFrame({
                'Data Type': data_types,
                'Null/NA Count': null_counts,
            })

          
        st.write(info_df)

    
    st.sidebar.subheader("Data Statistics")
    if st.sidebar.button("Show Data Statistics"):
        st.subheader("Data Statistics")
        st.write(data.describe())



    st.sidebar.title("Data Operations")




   
# Groupby operation
    st.sidebar.subheader("Groupby Operation")
    groupby_column = st.sidebar.selectbox("Select Column for Groupby", data.columns)
    agg_function = st.sidebar.selectbox("Select Aggregation Function", ["mean", "sum", "count", "min", "max"])
    if st.sidebar.button("Apply Groupby"):
        try:
            if data[groupby_column].dtype == 'O':  # 'O' represents object data type (non-numeric)
                grouped_data = data.groupby(groupby_column).agg({groupby_column: agg_function}).reset_index()
            else:
                grouped_data = data.groupby(groupby_column).agg(agg_function).reset_index()
            st.subheader(f"Groupby Operation Result - {groupby_column} by {agg_function}")
            st.write(grouped_data)
            st.session_state.groupby_result = grouped_data
        except Exception as e:
            st.warning(f"Error: {e}")




    # Pivot table operation
    st.sidebar.subheader("Pivot Table Operation")
    pivot_index = st.sidebar.selectbox("Select Index for Pivot Table", data.columns)
    pivot_columns = st.sidebar.selectbox("Select Columns for Pivot Table", data.columns)
    pivot_values = st.sidebar.selectbox("Select Values for Pivot Table", data.columns)
    if st.sidebar.button("Apply Pivot Table"):
        pivot_table_data = pd.pivot_table(data, values=pivot_values, index=pivot_index, columns=pivot_columns, aggfunc='mean')
        st.subheader("Pivot Table Operation Result")
        st.write(pivot_table_data)
        st.session_state.groupby_result = pivot_table_data



    st.sidebar.title("Plot Configuration")

    # Select plot type
    plot_types = ["Histogram", "Box Plot", "Scatter Plot", "Pair Plot", "Bar Chart", "Pie Chart", "Line Chart",
                  "Heatmap", "Violin Plot", "Count Plot", "Density Plot", "Q-Q Plot", "Bubble Chart", 
                  "Radar Chart", "Treemap"]
    selected_plot = st.sidebar.selectbox("Select Plot Type", plot_types)

    # Select columns for plotting
    st.sidebar.subheader("Select Columns for Plotting")
    if selected_plot in ["Pair Plot", "Heatmap", "Correlation Matrix Plot"]:
        selected_columns = st.sidebar.multiselect("Select Numerical Columns", data.select_dtypes(include='number').columns)
    else:
        selected_columns = st.sidebar.multiselect("Select Columns", data.columns)

    # Plot based on user selection
    st.subheader(f"{selected_plot}")
    
    if selected_plot == "Histogram":
        for column in selected_columns:
            # st.subheader(f"Histogram - {column}")
            fig = px.histogram(data, x=column, title=f'Histogram - {column}')
            st.plotly_chart(fig)

    elif selected_plot == "Box Plot":
        for column in selected_columns:
            # st.subheader(f"Box Plot - {column}")
            fig = px.box(data, y=column, title=f'Box Plot - {column}')
            st.plotly_chart(fig)

    elif selected_plot == "Scatter Plot":
        if len(selected_columns) >= 2:
            x_column = selected_columns[0]
            y_column = selected_columns[1]
            # st.subheader(f"Scatter Plot - {x_column} vs {y_column}")
            fig = px.scatter(data, x=x_column, y=y_column, title=f'Scatter Plot - {x_column} vs {y_column}')
            st.plotly_chart(fig)

    elif selected_plot == "Pie Chart":
        for column in selected_columns:
            # st.subheader(f"Pie Chart - {column}")
            fig = px.pie(data, names=column, title=f'Pie Chart - {column}')
            st.plotly_chart(fig)

    elif selected_plot == "Line Chart":
        if len(selected_columns) >= 2:
            x_column = selected_columns[0]
            y_column = selected_columns[1]
            # st.subheader(f"Line Chart - {x_column} vs {y_column}")
            fig = px.line(data, x=x_column, y=y_column, title=f'Line Chart - {x_column} vs {y_column}')
            st.plotly_chart(fig)

    elif selected_plot == "Pair Plot":
        if len(selected_columns) >= 2:
            # st.subheader("Pair Plot")
            fig = px.scatter_matrix(data[selected_columns], title="Pair Plot")
            st.plotly_chart(fig)

    elif selected_plot == "Violin Plot":
        if len(selected_columns) >= 2:
            # st.subheader(f"Violin Plot - {', '.join(selected_columns)}")
            for column in selected_columns:
                fig = px.violin(data, y=column, box=True, title=f'Violin Plot - {column}')
                st.plotly_chart(fig)

    elif selected_plot == "Count Plot":
        if len(selected_columns) >= 1:
            # st.subheader(f"Count Plot - {', '.join(selected_columns)}")
            for column in selected_columns:
                fig = px.histogram(data, x=column, color=column, title=f'Count Plot - {column}')
                st.plotly_chart(fig)

    elif selected_plot == "Q-Q Plot":
        if len(selected_columns) >= 1:
            # st.subheader(f"Q-Q Plot - {selected_columns[0]}")
            for column in selected_columns:
                fig = px.scatter(data, x=column, y=column, title=f'Q-Q Plot - {column}')
                st.plotly_chart(fig)

    elif selected_plot == "Bubble Chart":
        if len(selected_columns) == 3:
            # st.subheader(f"Bubble Chart - {', '.join(selected_columns)}")
            fig = px.scatter(data, x=selected_columns[0], y=selected_columns[1], size=selected_columns[2],
                             title=f'Bubble Chart - {selected_columns[0]} vs {selected_columns[1]} (Size: {selected_columns[2]})')
            st.plotly_chart(fig)

    elif selected_plot == "Treemap":
        if len(selected_columns) >= 2:
            st.subheader(f"Treemap - {', '.join(selected_columns)}")
            fig = px.treemap(data, path=selected_columns)
            st.plotly_chart(fig)


    elif selected_plot == "Heatmap":
        if len(selected_columns) >= 2:
            st.subheader(f"Heatmap - {', '.join(selected_columns)}")
            heatmap_data = data[selected_columns]
            
            # Replace NaN values with a default value (e.g., 0)
            heatmap_data = heatmap_data.fillna(0)

            correlation_matrix = heatmap_data.corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            st.pyplot(fig)

