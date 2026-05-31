#!/usr/bin/env python3
"""
Generate remittances visualization for Ecuador Quantificado contest.

Creates a professional, accessible chart showing Ecuador's remittances growth
with Spanish text and two export formats (landscape + social).
Applies data visualization best practices for clarity and accessibility.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

# Professional color palette (colorblind-friendly)
# Using blue-orange pair (accessible for colorblind viewers)
ACCENT_COLOR = "#DD8452"  # Warm orange for the main line
HIGHLIGHT_COLOR = "#FDD9C7"  # Light orange for shaded region
TEXT_COLOR = "#2B2D42"  # Dark blue-gray for text (high contrast)
GRID_COLOR = "#E5E5E5"  # Light gray for gridlines
BACKGROUND_COLOR = "#FFFFFF"  # White background


def load_data(csv_path):
    """Load the remittances dataset."""
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} years of data ({df['anio'].min()}-{df['anio'].max()})")
    return df


def format_millions_spanish(x, pos):
    """
    Format Y-axis labels in Spanish format with thousands separator.
    Uses European notation (period as thousands separator).
    """
    if x >= 1000:
        return f"{int(x):,}".replace(",", ".")
    return f"{int(x)}"


def format_currency_label(val):
    """Format currency values for annotations (e.g., $7.729M)."""
    if abs(val) >= 1000:
        # Use period as decimal separator for Spanish formatting
        return f"${val/1000:.0f}.{int((val % 1000)):03d}M".replace(",", ".")
    return f"${val:,.0f}M"


def create_chart(df, output_path, figsize=(12, 7), social=False):
    """
    Create the remittances visualization with professional styling.

    Args:
        df: DataFrame with remittances data
        output_path: Path to save the chart
        figsize: Figure size tuple
        social: If True, optimize layout for social media (more compact)
    """
    # Set up professional publication-quality style
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.dpi': 150,  # Screen display
        'savefig.dpi': 300,  # Publication quality
        'savefig.bbox': 'tight',  # Avoid clipping
    })

    # Use constrained_layout for automatic spacing (best practice)
    fig, ax = plt.subplots(figsize=figsize, facecolor=BACKGROUND_COLOR,
                           constrained_layout=True)
    ax.set_facecolor(BACKGROUND_COLOR)

    # Plot the main line with markers for accessibility
    ax.plot(
        df["anio"],
        df["remesas_millones_usd"],
        color=ACCENT_COLOR,
        linewidth=3,
        marker='o',
        markersize=4,
        markevery=5,  # Show markers every 5 years for clarity
        zorder=3,
        label='Remesas recibidas'
    )

    # Fill area under the curve for visual weight
    ax.fill_between(
        df["anio"],
        0,
        df["remesas_millones_usd"],
        color=ACCENT_COLOR,
        alpha=0.15,
        zorder=2
    )

    # Highlight the post-2020 surge with pattern for colorblind accessibility
    surge_data = df[df["anio"] >= 2020]
    if not surge_data.empty:
        ax.fill_between(
            surge_data["anio"],
            0,
            surge_data["remesas_millones_usd"],
            color=HIGHLIGHT_COLOR,
            alpha=0.5,
            hatch='///',  # Add pattern for accessibility
            edgecolor=ACCENT_COLOR,
            linewidth=0,
            zorder=1
        )

        # Annotation for the surge - positioned for clarity
        mid_year = 2022.5
        mid_value = df[df["anio"] == 2022]["remesas_millones_usd"].values[0] if 2022 in df["anio"].values else 4500
        ax.annotate(
            "Se duplican\nen 5 años",
            xy=(mid_year, mid_value),
            xytext=(mid_year, mid_value + 1000),
            fontsize=11 if not social else 10,
            color=TEXT_COLOR,
            ha="center",
            va="bottom",
            weight='semibold',
            bbox=dict(boxstyle="round,pad=0.6", facecolor="white",
                     edgecolor=ACCENT_COLOR, linewidth=1.5, alpha=0.95)
        )

    # Direct label for the final data point (2025)
    final_year = df["anio"].max()
    final_value = df[df["anio"] == final_year]["remesas_millones_usd"].values[0]

    # Larger marker for final point
    ax.plot(final_year, final_value, "o", color=ACCENT_COLOR,
            markersize=10, markeredgecolor='white', markeredgewidth=2, zorder=4)

    # Value annotation
    ax.annotate(
        f"${final_value:,.0f}M".replace(",", "."),
        xy=(final_year, final_value),
        xytext=(12, 15),
        textcoords="offset points",
        fontsize=13 if not social else 12,
        fontweight="bold",
        color=ACCENT_COLOR,
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                 edgecolor=ACCENT_COLOR, linewidth=1.5)
    )

    # Context annotation - positioned for maximum clarity
    context_year = 2023
    context_value = final_value * 0.55
    ax.annotate(
        "EE. UU. = 77,8%\nde las remesas (2025)",
        xy=(context_year, context_value),
        fontsize=9.5 if not social else 9,
        color=TEXT_COLOR,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#F8F9FA",
                 edgecolor="#CED4DA", linewidth=1, alpha=0.95)
    )

    # Axis labels with clear units
    ax.set_xlabel("Año", fontsize=12, color=TEXT_COLOR, labelpad=10, weight='semibold')
    ax.set_ylabel("Remesas recibidas (millones de USD)", fontsize=12,
                  color=TEXT_COLOR, labelpad=10, weight='semibold')

    # Format Y-axis with Spanish notation
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_millions_spanish))
    ax.set_ylim(bottom=0, top=final_value * 1.20)

    # Format X-axis to show every 5 years
    ax.set_xlim(left=df["anio"].min() - 1, right=final_year + 1)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(5))

    # Professional grid styling
    ax.grid(axis="y", color=GRID_COLOR, linewidth=0.8, alpha=0.6,
            linestyle='-', zorder=0)
    ax.set_axisbelow(True)

    # Clean spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID_COLOR)
    ax.spines["bottom"].set_color(GRID_COLOR)
    ax.spines["left"].set_linewidth(1.2)
    ax.spines["bottom"].set_linewidth(1.2)

    # Title states the insight, subtitle adds context
    title_fontsize = 17 if not social else 15
    subtitle_fontsize = 12 if not social else 11

    fig.text(
        0.125, 0.96 if not social else 0.94,
        "Récord de remesas: el dinero de la emigración sostiene a Ecuador",
        fontsize=title_fontsize,
        fontweight="bold",
        color=TEXT_COLOR,
        ha="left",
        va="top"
    )

    fig.text(
        0.125, 0.92 if not social else 0.90,
        "Las remesas recibidas se duplicaron entre 2020 y 2025",
        fontsize=subtitle_fontsize,
        color=TEXT_COLOR,
        alpha=0.85,
        ha="left",
        va="top"
    )

    # Source line with verifiable references
    fig.text(
        0.125, 0.02,
        "Fuente: contenido.bce.fin.ec (Balanza de Pagos) y data.worldbank.org (BX.TRF.PWKR.CD.DT)",
        fontsize=7.5,
        color=TEXT_COLOR,
        alpha=0.65,
        ha="left",
        va="bottom",
        style="italic"
    )

    # Save with high quality (constrained_layout handles spacing automatically)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, facecolor=BACKGROUND_COLOR, edgecolor='none')
    print(f"Chart saved to: {output_path}")

    plt.close()


def main():
    """Main execution flow."""
    # Load data
    data_path = os.path.join("data", "remesas_ecuador.csv")
    df = load_data(data_path)

    # Create landscape version
    print("\nGenerating landscape chart...")
    create_chart(
        df,
        output_path=os.path.join("output", "remesas_ecuador.png"),
        figsize=(12, 7),
        social=False
    )

    # Create social media version (more square)
    print("Generating social media chart...")
    create_chart(
        df,
        output_path=os.path.join("output", "remesas_ecuador_social.png"),
        figsize=(10, 10),
        social=True
    )

    print("\n✓ Visualizations generated successfully!")
    print(f"  - Landscape: output/remesas_ecuador.png")
    print(f"  - Social: output/remesas_ecuador_social.png")
    print("\nAccessibility features:")
    print("  ✓ Colorblind-friendly palette")
    print("  ✓ Pattern fills for differentiation")
    print("  ✓ High contrast text")
    print("  ✓ Direct data labels")
    print("  ✓ Verifiable data sources")


if __name__ == "__main__":
    main()
