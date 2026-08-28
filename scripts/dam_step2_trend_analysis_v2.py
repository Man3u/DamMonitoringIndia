import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

DATA_DIR = os.path.expanduser("~/Desktop/DamMonitoringIndia/data")
OUT_DIR = os.path.expanduser("~/Desktop/DamMonitoringIndia/output")
os.makedirs(OUT_DIR, exist_ok=True)

DAMS = {
    "NagarjunaSagar": "water_area_coverage_NagarjunaSagar.csv",
    "Srisailam": "water_area_coverage_Srisailam.csv",
}

MIN_COVERAGE_PCT = 70

annual_series = {}

for name, filename in DAMS.items():
    df = pd.read_csv(os.path.join(DATA_DIR, filename))
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m")
    df["year"] = df["date"].dt.year
    df = df.dropna(subset=["water_area_ha", "pct_valid_coverage"])

    total_months = df.shape[0]
    reliable = df[df["pct_valid_coverage"] >= MIN_COVERAGE_PCT]
    dropped = total_months - reliable.shape[0]
    print(f"\n{name}: {total_months} months total, {reliable.shape[0]} kept (>= {MIN_COVERAGE_PCT}% coverage), {dropped} dropped as unreliable")
    print(f"  Water area range (reliable months only): {reliable['water_area_ha'].min():.0f} - {reliable['water_area_ha'].max():.0f} ha")

    annual = reliable.groupby("year")["water_area_ha"].mean().reset_index()
    months_per_year = reliable.groupby("year").size()
    reliable_years = months_per_year[months_per_year >= 6].index
    annual = annual[annual["year"].isin(reliable_years)]
    annual_series[name] = annual

    slope, intercept, r_value, p_value, std_err = stats.linregress(annual["year"], annual["water_area_ha"])
    print(f"  Trend: {slope:.1f} ha/year (p={p_value:.4f}, R2={r_value**2:.3f})")

    mean_area = annual["water_area_ha"].mean()
    std_area = annual["water_area_ha"].std()
    drought_years = annual[annual["water_area_ha"] < mean_area - std_area]["year"].tolist()
    print(f"  Long-term average: {mean_area:.0f} ha, std dev: {std_area:.0f} ha")
    print(f"  Drought years (>1 std dev below average, coverage-filtered): {drought_years}")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(reliable["date"], reliable["water_area_ha"], alpha=0.4, linewidth=0.8, label="Monthly (reliable coverage only)")
    ax.plot(
        pd.to_datetime(annual["year"], format="%Y"),
        annual["water_area_ha"],
        color="darkred", linewidth=2, marker="o", markersize=3, label="Annual mean",
    )
    trend_line = intercept + slope * annual["year"]
    ax.plot(pd.to_datetime(annual["year"], format="%Y"), trend_line, "--", color="black", label=f"Trend ({slope:.1f} ha/yr)")
    for y in drought_years:
        ax.axvspan(pd.Timestamp(f"{y}-01-01"), pd.Timestamp(f"{y}-12-31"), color="orange", alpha=0.15)
    ax.set_title(f"{name}: Reservoir Water Surface Area, coverage-filtered (>= {MIN_COVERAGE_PCT}% observed)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Water surface area (hectares)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig_path = os.path.join(OUT_DIR, f"trend_{name}_v2.png")
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {fig_path}")

    annual.to_csv(os.path.join(OUT_DIR, f"annual_water_area_{name}_v2.csv"), index=False)

merged = pd.merge(
    annual_series["NagarjunaSagar"], annual_series["Srisailam"],
    on="year", suffixes=("_NagarjunaSagar", "_Srisailam"),
)
corr = merged["water_area_ha_NagarjunaSagar"].corr(merged["water_area_ha_Srisailam"])
print(f"\nCorrelation between the two dams' annual water area (coverage-filtered): {corr:.3f}")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(merged["year"], merged["water_area_ha_NagarjunaSagar"], marker="o", label="Nagarjuna Sagar")
ax.plot(merged["year"], merged["water_area_ha_Srisailam"], marker="o", label="Srisailam")
ax.set_title(f"Nagarjuna Sagar vs Srisailam: Annual Water Surface Area, coverage-filtered (correlation = {corr:.2f})")
ax.set_xlabel("Year")
ax.set_ylabel("Water surface area (hectares)")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
comparison_path = os.path.join(OUT_DIR, "dam_comparison_v2.png")
fig.savefig(comparison_path, dpi=150)
print(f"Saved: {comparison_path}")

merged.to_csv(os.path.join(OUT_DIR, "dam_comparison_annual_v2.csv"), index=False)
print("\nDone.")
