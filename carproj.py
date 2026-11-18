import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cars Market | Executive View", page_icon="🚗", layout="wide")

DATA_FILE = "Cars Data1.csv"
ORIGIN_COLORS = {"USA": "#2563eb", "Asia": "#10b981", "Europe": "#f59e0b"}
PALETTE = ["#2563eb", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899"]
T = "plotly_white"

st.markdown("""
<style>
.block-container {padding-top: 1.5rem;}
div[data-testid="stMetric"] {
    background:#fff; border:1px solid #e5e7eb; border-left:5px solid #2563eb;
    padding:14px 18px; border-radius:12px; box-shadow:0 1px 4px rgba(0,0,0,.06);
}
div[data-testid="stMetric"] label {color:#6b7280; font-weight:600;}
.insight {background:#f0f6ff; border-radius:10px; padding:12px 16px; margin-bottom:8px; color:#1e3a8a;}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
    except UnicodeDecodeError:
        df = pd.read_csv(DATA_FILE, encoding="latin-1")
    df = df.dropna(how="all").drop_duplicates()
    for col in ["MSRP", "Invoice"]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(r"[$,\s]", "", regex=True), errors="coerce")
    df = df.dropna(subset=["Make", "MSRP", "Invoice"])  # NaN kept elsewhere (no fake zeros)
    df["Name"] = df["Make"] + " " + df["Model"]
    df["Dealer Margin $"] = df["MSRP"] - df["Invoice"]
    df["Dealer Margin %"] = df["Dealer Margin $"] / df["MSRP"] * 100
    df["MPG Combined"] = 0.55 * df["MPG_City"] + 0.45 * df["MPG_Highway"]
    df["HP per Ton (lb)"] = df["Horsepower"] / df["Weight"] * 1000
    df["HP per Liter"] = df["Horsepower"] / df["EngineSize"]
    df["HP per $1k"] = df["Horsepower"] / (df["MSRP"] / 1000)
    return df


df = load_data()

# ---------------- Sidebar ----------------
st.sidebar.header("🎛️ Filters")
origins = st.sidebar.multiselect("Origin", sorted(df["Origin"].unique()), default=sorted(df["Origin"].unique()))
types = st.sidebar.multiselect("Body type", sorted(df["Type"].unique()), default=sorted(df["Type"].unique()))
drives = st.sidebar.multiselect("Drivetrain", sorted(df["DriveTrain"].unique()), default=sorted(df["DriveTrain"].unique()))
makes = st.sidebar.multiselect("Brand (optional)", sorted(df["Make"].unique()))
pmin, pmax = int(df["MSRP"].min()), int(df["MSRP"].max())
price = st.sidebar.slider("MSRP range ($)", pmin, pmax, (pmin, pmax), step=1000)

f = df[df["Origin"].isin(origins) & df["Type"].isin(types) & df["DriveTrain"].isin(drives)
       & df["MSRP"].between(*price)]
if makes:
    f = f[f["Make"].isin(makes)]
if f.empty:
    st.warning("No vehicles match the selected filters.")
    st.stop()

# ---------------- Header & KPIs ----------------
st.title("🚗 Cars Market — Executive Summary")
st.caption(f"{len(f):,} models • {f['Make'].nunique()} brands • all figures reflect the filters on the left")

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Models", f"{len(f):,}")
c2.metric("Avg. MSRP", f"${f['MSRP'].mean():,.0f}")
c3.metric("Median MSRP", f"${f['MSRP'].median():,.0f}")
c4.metric("Avg. Dealer Margin", f"{f['Dealer Margin %'].mean():.1f}%")
c5.metric("Avg. Horsepower", f"{f['Horsepower'].mean():.0f} hp")
c6.metric("Avg. MPG (comb.)", f"{f['MPG Combined'].mean():.1f}")

# ---------------- Insights ----------------
by_make = f.groupby("Make").agg(Models=("Model", "count"), AvgMSRP=("MSRP", "mean"))
origin_price = f.groupby("Origin")["MSRP"].mean()
best_value = f.loc[f["HP per $1k"].idxmax()]
most_eff = f.loc[f["MPG Combined"].idxmax()]
priciest = f.loc[f["MSRP"].idxmax()]
margin_make = f.groupby("Make")["Dealer Margin %"].mean()

insights = [
    f"🏷️ Widest range: **{by_make['Models'].idxmax()}** ({by_make['Models'].max()} models). "
    f"Most expensive on average: **{by_make['AvgMSRP'].idxmax()}** (${by_make['AvgMSRP'].max():,.0f}).",
    f"🌍 **{origin_price.idxmax()}** vehicles carry the highest average price (${origin_price.max():,.0f}).",
    f"💪 Best performance per dollar: **{best_value['Name']}** ({best_value['Horsepower']:.0f} hp at ${best_value['MSRP']:,.0f}).",
    f"⛽ Most fuel-efficient: **{most_eff['Name']}** ({most_eff['MPG Combined']:.0f} MPG combined).",
    f"💰 Highest dealer margin: **{margin_make.idxmax()}** (avg {margin_make.max():.1f}% between MSRP and invoice).",
]
st.markdown("### 🔎 Key Takeaways")
for i in insights:
    st.markdown(f'<div class="insight">{i}</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["🌍 Market", "💲 Price & Margin", "⚡ Performance", "⛽ Efficiency", "🏢 Brands", "🗂️ Data"])

# ---------------- Market ----------------
with tab1:
    a, b = st.columns(2)
    o = f["Origin"].value_counts().reset_index()
    o.columns = ["Origin", "Models"]
    a.plotly_chart(px.pie(o, names="Origin", values="Models", hole=.55, color="Origin",
                          color_discrete_map=ORIGIN_COLORS, title="Model Share by Origin")
                   .update_layout(height=400), use_container_width=True)
    t = f.groupby(["Type", "Origin"]).size().reset_index(name="Models")
    b.plotly_chart(px.bar(t, x="Type", y="Models", color="Origin", color_discrete_map=ORIGIN_COLORS,
                          title="Body Types by Origin").update_layout(template=T, height=400),
                   use_container_width=True)
    d = f.groupby(["DriveTrain", "Origin"]).size().reset_index(name="Models")
    st.plotly_chart(px.bar(d, x="DriveTrain", y="Models", color="Origin", barmode="group",
                           color_discrete_map=ORIGIN_COLORS, title="Drivetrain Mix")
                    .update_layout(template=T, height=350), use_container_width=True)

# ---------------- Price & Margin ----------------
with tab2:
    a, b = st.columns(2)
    a.plotly_chart(px.box(f, x="Origin", y="MSRP", color="Origin", color_discrete_map=ORIGIN_COLORS,
                          points="outliers", hover_name="Name", title="MSRP Distribution by Origin")
                   .update_layout(template=T, showlegend=False, height=420), use_container_width=True)
    b.plotly_chart(px.box(f, x="Type", y="MSRP", color="Type", color_discrete_sequence=PALETTE,
                          hover_name="Name", title="MSRP Distribution by Body Type")
                   .update_layout(template=T, showlegend=False, height=420), use_container_width=True)
    mm = f.groupby("Make")["Dealer Margin %"].mean().sort_values().tail(12).reset_index()
    st.plotly_chart(px.bar(mm, x="Dealer Margin %", y="Make", orientation="h", text_auto=".1f",
                           title="Top 12 Brands by Avg. Dealer Margin (%)", color_discrete_sequence=[PALETTE[0]])
                    .update_layout(template=T, height=450), use_container_width=True)

# ---------------- Performance ----------------
with tab3:
    st.plotly_chart(px.scatter(f, x="MSRP", y="Horsepower", color="Origin", size="EngineSize",
                               hover_name="Name", color_discrete_map=ORIGIN_COLORS, opacity=.7,
                               title="Does More Money Buy More Power? (bubble = engine size)")
                    .update_layout(template=T, height=450), use_container_width=True)
    a, b = st.columns(2)
    top_pw = f.nlargest(10, "HP per Ton (lb)").sort_values("HP per Ton (lb)")
    a.plotly_chart(px.bar(top_pw, x="HP per Ton (lb)", y="Name", orientation="h", color="Origin",
                          color_discrete_map=ORIGIN_COLORS, title="Top 10 Power-to-Weight (hp per 1,000 lb)")
                   .update_layout(template=T, height=450, yaxis_title=""), use_container_width=True)
    top_val = f.nlargest(10, "HP per $1k").sort_values("HP per $1k")
    b.plotly_chart(px.bar(top_val, x="HP per $1k", y="Name", orientation="h", color="Origin",
                          color_discrete_map=ORIGIN_COLORS, title="Top 10 Value (hp per $1,000 MSRP)")
                   .update_layout(template=T, height=450, yaxis_title=""), use_container_width=True)

# ---------------- Efficiency ----------------
with tab4:
    a, b = st.columns(2)
    a.plotly_chart(px.scatter(f, x="Weight", y="MPG Combined", color="Type", hover_name="Name",
                              trendline="ols" if len(f) > 10 else None, color_discrete_sequence=PALETTE,
                              title="Heavier = Thirstier: Weight vs. Fuel Economy")
                   .update_layout(template=T, height=420), use_container_width=True)
    b.plotly_chart(px.box(f, x="Type", y="MPG Combined", color="Type", color_discrete_sequence=PALETTE,
                          hover_name="Name", title="Fuel Economy by Body Type")
                   .update_layout(template=T, showlegend=False, height=420), use_container_width=True)
    top_eff = f.nlargest(10, "MPG Combined").sort_values("MPG Combined")
    st.plotly_chart(px.bar(top_eff, x="MPG Combined", y="Name", orientation="h", color="Type",
                           color_discrete_sequence=PALETTE, title="Top 10 Most Fuel-Efficient Models")
                    .update_layout(template=T, height=420, yaxis_title=""), use_container_width=True)

# ---------------- Brands ----------------
with tab5:
    sc = f.groupby(["Make", "Origin"]).agg(
        Models=("Model", "count"), AvgMSRP=("MSRP", "mean"), AvgHP=("Horsepower", "mean"),
        AvgMPG=("MPG Combined", "mean"), Margin=("Dealer Margin %", "mean")).reset_index()
    st.plotly_chart(px.scatter(sc, x="AvgMSRP", y="AvgHP", size="Models", color="Origin", text="Make",
                               color_discrete_map=ORIGIN_COLORS, size_max=45,
                               title="Brand Positioning: Price vs. Power (bubble = number of models)")
                    .update_traces(textposition="top center").update_layout(template=T, height=520),
                    use_container_width=True)
    st.markdown("#### Brand Scorecard")
    st.dataframe(
        sc.sort_values("AvgMSRP", ascending=False).rename(columns={
            "AvgMSRP": "Avg MSRP ($)", "AvgHP": "Avg HP", "AvgMPG": "Avg MPG", "Margin": "Dealer Margin %"})
        .style.format({"Avg MSRP ($)": "{:,.0f}", "Avg HP": "{:.0f}", "Avg MPG": "{:.1f}", "Dealer Margin %": "{:.1f}"}),
        use_container_width=True, hide_index=True)

# ---------------- Data ----------------
with tab6:
    st.dataframe(f.drop(columns=["Name"]), use_container_width=True)
    st.download_button("⬇️ Download filtered data (CSV)", f.to_csv(index=False).encode(), "filtered_cars.csv")
