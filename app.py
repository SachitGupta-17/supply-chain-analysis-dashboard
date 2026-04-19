import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Supply Chain Dashboard",
    page_icon = "📦",
    layout = "wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    df = pd.read_csv("supply_chain_data.csv")
    df['Profit'] = df['Revenue generated'] - (df['Manufacturing costs'] + df['Shipping costs'] + df['Costs'])
    df["Profit margin (%)"] = (df['Profit'] / df["Revenue generated"])*100
    return df

df = load_data()


st.sidebar.title("📊Filters")
st.sidebar.markdown("Use these filters to narrow down the data.")

product_types = st.sidebar.multiselect(
    "Product Type",
    options=df['Product type'].unique(),
    default=df['Product type'].unique()
)

suppliers = st.sidebar.multiselect(
    "Supplier",
    options=df['Supplier name'].unique(),
    default=df['Supplier name'].unique()
)

locations = st.sidebar.multiselect(
    "Location",
    options=df['Location'].unique(),
    default=df['Location'].unique()
)

filtered_df = df[
    (df['Product type'].isin(product_types))&
    (df["Supplier name"].isin(suppliers))&
    (df["Location"].isin(locations))
]

st.title("📦 Supply Chain Analytics Dashboard")
st.markdown("## Data-Driven Insights for Supply Chain Optimization")
st.markdown("_ _ _")



col1 , col2 , col3 , col4 , col5 ,col6 = st.columns(6)

with col1:
    total_revenue = filtered_df['Revenue generated'].sum()
    st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")

with col2:
    total_units = filtered_df['Number of products sold'].sum()
    st.metric("📦 Total Units Sold",f"{total_units:,}")

with col3:
    avg_defect = filtered_df['Defect rates'].mean() * 100
    st.metric("Avg Defect Rate",f"{avg_defect:.2f}%")

with col4:
    avg_shipping_cost = filtered_df['Shipping costs'].mean()
    st.metric("🚚 Avg Shipping Cost",f"${avg_shipping_cost:.2f}")

with col5:
    total_profit=filtered_df['Profit'].sum()
    st.metric("💰 Total Profit",f"${total_profit:,.2f}")

with col6:
    profit_margin = filtered_df['Profit margin (%)'].mean() 
    st.metric("Avg Profit Margin (%)",f"{profit_margin:,.2f}%")

st.markdown("_ _ _")

st.subheader("📈 Product Type Performance")
col1 , col2 , col3= st.columns(3)

with col1:
    revenue_by_product = filtered_df.groupby('Product type')['Revenue generated'].sum().reset_index()
    fig1 = px.bar(
        revenue_by_product,
        x='Product type',
        y='Revenue generated',
        title="Revenue by Product Type",
        color = "Product type",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1,use_container_width=True)

with col2:
    units_by_product = filtered_df.groupby("Product type")["Number of products sold"].sum().reset_index()
    fig2 = px.pie(
        units_by_product,
        values="Number of products sold",
        names="Product type",
        title="Units Sold Distribution"
    )
    st.plotly_chart(fig2,use_container_width=True)

with col3:
    profit_by_product = filtered_df.groupby("Product type")['Profit'].sum().reset_index()
    fig_profit = px.bar(
        profit_by_product,
        x="Product type",
        y="Profit",
        title="Profit by Product Type",
        color="Product type"
    )
    fig_profit.update_layout(showlegend=False)
    st.plotly_chart(fig_profit,use_container_width=True)


st.subheader("🏭 Supplier Performance")
col1 , col2 , col3 = st.columns(3)

with col1:
    supplier_revenue =filtered_df.groupby('Supplier name')['Revenue generated'].sum().reset_index()
    fig3 = px.bar(
        supplier_revenue,
        x="Supplier name",
        y="Revenue generated",
        title="Revenue by Supplier",
        color="Supplier name"
    )
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3,use_container_width=True)

with col2:
    supplier_defect = filtered_df.groupby("Supplier name")['Defect rates'].mean().reset_index()
    supplier_defect['Defect rates'] = supplier_defect['Defect rates']*100
    fig4 = px.bar(
        supplier_defect,
        x="Supplier name",
        y="Defect rates",
        title="Average Defect Rate by Supplier (%)",
        color="Defect rates",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig4,use_container_width=True)

with col3:
    profit_by_supplier = filtered_df.groupby("Supplier name")['Profit'].sum().reset_index()
    fig_supplier_profit = px.bar(
        profit_by_supplier,
        x="Supplier name",
        y="Profit",
        title="Profit by Supplier",
        color="Supplier name"
    )
    fig_supplier_profit.update_layout(showlegend=False)
    st.plotly_chart(fig_supplier_profit,use_container_width=True)

st.subheader("👥 Customer Demographics Analysis")
col1 , col2 = st.columns(2)

with col1:
    revenue_by_demo = filtered_df.groupby("Customer demographics")["Revenue generated"].sum().reset_index()
    fig5 = px.bar(
        revenue_by_demo,
        x="Customer demographics",
        y="Revenue generated",
        title="Revenue by Customer Demographics",
        color="Customer demographics"
    )
    fig5.update_layout(showlegend=False)
    st.plotly_chart(fig5,use_container_width=True)

with col2:
    units_by_demo = filtered_df.groupby("Customer demographics")["Number of products sold"].sum().reset_index()
    fig6=px.pie(
        units_by_demo,
        values="Number of products sold",
        names="Customer demographics",
        title="Sales Distribution by Demographics"
    )
    st.plotly_chart(fig6,use_container_width=True)



st.subheader("🚛 Logistics & Shipping Analysis")
col1,col2 = st.columns(2)

with col1:
    carrier_cost = filtered_df.groupby("Shipping carriers")["Shipping costs"].mean().reset_index()
    fig7 = px.bar(
        carrier_cost,
        x="Shipping carriers",
        y="Shipping costs",
        title="Average Shipping Cost by Carrier",
        color="Shipping carriers"
    )
    fig7.update_layout(showlegend=False)
    st.plotly_chart(fig7,use_container_width=True)

with col2:
    carrier_time = filtered_df.groupby("Shipping carriers")["Shipping times"].mean().reset_index()
    fig8 = px.bar(
        carrier_time,
        x="Shipping carriers",
        y="Shipping times",
        title="Average Shipping Time by Carrier (in Days)",
        color="Shipping carriers"
    )
    fig8.update_layout(showlegend=False)
    st.plotly_chart(fig8,use_container_width=True)



st.subheader("Transportation Mode Analysis")
col1 , col2 = st.columns(2)

with col1:
    transport_cost = filtered_df.groupby("Transportation modes")["Costs"].mean().reset_index()
    fig9 = px.bar(
        transport_cost,
        x='Transportation modes',
        y='Costs',
        title="Average Transportation Cost by Mode",
        color='Transportation modes'
    )
    fig9.update_layout(showlegend=False)
    st.plotly_chart(fig9,use_container_width=True)
    
with col2:
    transport_count = filtered_df['Transportation modes'].value_counts().reset_index()
    transport_count.columns = ['Transportation modes','Count']
    fig10 = px.pie(
        transport_count,
        values='Count',
        names='Transportation modes',
        title='Transportation Mode Distribution'
    )
    st.plotly_chart(fig10,use_container_width=True)


st.subheader("📍 Location Wise Analysis")
col1,col2 = st.columns(2)

with col1:
    location_cost = filtered_df.groupby('Location')['Manufacturing costs'].mean().reset_index()
    fig11 = px.bar(
        location_cost,
        x='Location',
        y='Manufacturing costs',
        title='Average Manufacturing Cost by Location',
        color='Location'
    )
    fig11.update_layout(showlegend=False)
    st.plotly_chart(fig11,use_container_width=True)

with col2:
    location_revenue = filtered_df.groupby('Location')['Revenue generated'].sum().reset_index()
    fig12 = px.bar(
        location_revenue,
        x="Location",
        y='Revenue generated',
        title = 'Revenue by Location',
        color='Location'
    )
    fig12.update_layout(showlegend=False)
    st.plotly_chart(fig12,use_container_width=True)


st.subheader("✅ Quality Control Analysis")
col1 , col2 = st.columns(2)

with col1:
    inspection_counts = filtered_df['Inspection results'].value_counts().reset_index()
    inspection_counts.columns = ['Inspection results','Count']
    fig13 = px.pie(
        inspection_counts,
        values='Count',
        names='Inspection results',
        title='Inspection results Distribution',
        color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12']
    )
    st.plotly_chart(fig13,use_container_width=True)

with col2:
    defect_by_inspection = filtered_df.groupby('Inspection results')['Defect rates'].mean().reset_index()
    defect_by_inspection['Defect rates'] = defect_by_inspection['Defect rates']*100
    fig14 = px.bar(
        defect_by_inspection,
        x='Inspection results',
        y='Defect rates',
        title='Average Defect Rate by Inspection Result (%)',
        color='Inspection results'
    )
    fig14.update_layout(showlegend=False)
    st.plotly_chart(fig14,use_container_width=True)



st.subheader("Correlation Analysis")
col1 , col2 = st.columns(2)

with col1:
    fig15 = px.scatter(
        filtered_df,
        x='Lead times',
        y='Defect rates',
        title='Lead Time vs Defect Rate',
        color='Product type',
        size='Number of products sold',
        hover_data=['SKU'],
        labels={'Defect rates':'Defect Rate (%)','Lead times':'Lead Time (Days)'}
    )
    fig15.update_layout(height=500)
    st.plotly_chart(fig15,use_container_width=True)

with col2:
    fig16 = px.scatter(
        filtered_df,
        x='Price',
        y='Revenue generated',
        title='Price vs Revenue',
        color='Product type',
        size='Number of products sold',
        hover_data=['SKU']
    )
    fig16.update_layout(height=500)
    st.plotly_chart(fig16,use_container_width=True)


st.markdown("_ _ _")
st.markdown("### Key Insights Summary")
st.markdown("""
- **Top Performing Product Types:** Chech revenue and sold charts.
- **Best SUpplier:** Compare revenue vs defect rate; high revenue with low defect rate is ideal.
- **Logistics Optimization:** Carrier with lowest shipping time and cost should be priotized.
- **Quality Focus:** High defect rate products need attention; inspect supplier quality.
- **Loaction Strategy:** Manufacturing cost vs revenue generated helps decide where to produce.
""")



with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered_df)

st.markdown("_ _ _")
st.markdown("Supply Chain Dashboard By SACHIT GUPTA")

