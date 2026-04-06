"""
Day 3: Mosaic Visualization
Theme: Blockchain dApps Distribution by Category (2025)
Data Sources: DappRadar, DeFi Llama, State of the DApps
#30DayChartChallenge

Mosaic plot (Marimekko chart) showing:
- Width: Total dApps per blockchain (proportional)
- Height: Category distribution within each blockchain (proportional)
- Color: Category type (monochromatic earth tone palette)

Skills applied:
- matplotlib: Complex mosaic layouts, custom Rectangle patches
- data-visualization: Two-dimensional proportion representation, accessibility principles
- data-viz-plots: Mosaic plots (Marimekko charts)

Design principles applied:
- Colorblind-safe monochromatic palette
- Minimalist typography (bold sans-serif + italic serif)
- Vintage aesthetic with earth tones
- Clear data labels showing percentages
- Proportional layout calculations
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches

# ============================================
# CONFIGURATION CONSTANTS
# ============================================

# Font sizes
TITLE_FONTSIZE = 24
SUBTITLE_FONTSIZE = 14
LABEL_FONTSIZE = 11
CATEGORY_FONTSIZE = 10
PERCENTAGE_FONTSIZE = 9
INSIGHT_FONTSIZE = 11
SOURCE_FONTSIZE = 10

# Figure dimensions
FIGURE_WIDTH = 24
FIGURE_HEIGHT = 12

# Colors - Monochromatic earth tone palette (colorblind-safe, inspired by vintage design)
# Sequential palette from dark to light for ordered categorical data
CATEGORY_COLORS = {
    'DeFi': '#1a1a1a',      # Near black - Darkest (most important category)
    'NFT': '#3a4a2f',       # Dark olive green
    'Gaming': '#5a6a4f',    # Medium olive
    'Social': '#7a8a6f',    # Sage green
    'Other': '#9aaa8f'      # Light sage - Lightest
}

# Background color - Vintage aesthetic
BACKGROUND_COLOR = '#D9D4BA'  # Warm beige/tan for professional vintage look

# Blockchain colors matching vintage earth tone design
BLOCKCHAIN_COLORS = {
    'Ethereum': '#3a4a2f',      # Dark olive green
    'BNB Chain': '#5a6a4f',     # Medium olive
    'Polygon': '#3a4a2f',       # Dark olive green
    'Solana': '#5a6a4f',        # Medium olive
    'Arbitrum': '#3a4a2f',      # Dark olive green
    'Base': '#5a6a4f',          # Medium olive
    'Avalanche': '#3a4a2f',     # Dark olive green
    'Optimism': '#5a6a4f'       # Medium olive
}

# Set style - Professional publication-quality settings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11  # Minimum readable size (accessibility)
plt.rcParams['figure.dpi'] = 100  # Screen display
plt.rcParams['savefig.dpi'] = 300  # Publication quality
plt.rcParams['savefig.bbox'] = 'tight'  # Remove extra whitespace
plt.rcParams['axes.spines.top'] = False  # Reduce chart junk
plt.rcParams['axes.spines.right'] = False

# ============================================
# DATA LOADING AND VALIDATION
# ============================================

def load_and_validate_data(data_path):
    """
    Load and validate the dApps distribution data.

    Args:
        data_path: Path to the CSV file

    Returns:
        DataFrame with validated data

    Raises:
        FileNotFoundError: If data file doesn't exist
        ValueError: If required columns are missing or data is invalid
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")

    df = pd.read_csv(data_path)

    # Validate required columns
    required_columns = ['Blockchain', 'Category', 'Count']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Validate data types
    if not pd.api.types.is_numeric_dtype(df['Count']):
        raise ValueError("Count must be numeric")

    # Check for negative counts
    if (df['Count'] < 0).any():
        raise ValueError("Count cannot be negative")

    return df

# Read data
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'dapps_by_blockchain_2025.csv')

try:
    df = load_and_validate_data(data_path)
except (FileNotFoundError, ValueError) as e:
    print(f"Error loading data: {e}", file=sys.stderr)
    sys.exit(1)

# ============================================
# DATA PREPARATION FOR MOSAIC PLOT
# ============================================

# Calculate totals per blockchain
blockchain_totals = df.groupby('Blockchain')['Count'].sum().sort_values(ascending=False)
total_dapps = blockchain_totals.sum()

# Calculate proportions
df['Proportion'] = df['Count'] / total_dapps

# Order blockchains by total count (for left to right layout)
blockchain_order = blockchain_totals.index.tolist()

# ============================================
# CREATE MOSAIC PLOT
# ============================================

fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), facecolor=BACKGROUND_COLOR)
ax.set_facecolor(BACKGROUND_COLOR)

# Starting position
x_start = 0
mosaic_data = []

# Track category totals for insights
category_totals = df.groupby('Category')['Count'].sum().sort_values(ascending=False)

for blockchain in blockchain_order:
    # Get data for this blockchain
    blockchain_df = df[df['Blockchain'] == blockchain].copy()
    blockchain_total = blockchain_df['Count'].sum()

    # Width proportional to total dApps count
    width = blockchain_total / total_dapps

    # Sort categories by count (top to bottom: highest to lowest)
    blockchain_df = blockchain_df.sort_values('Count', ascending=False)

    # Draw rectangles for each category
    y_start = 0
    for idx, row in blockchain_df.iterrows():
        category = row['Category']
        count = row['Count']
        height = count / blockchain_total  # Height proportional to category within blockchain

        # Create rectangle
        rect = Rectangle((x_start, y_start), width, height,
                         facecolor=CATEGORY_COLORS[category],
                         edgecolor=BACKGROUND_COLOR,
                         linewidth=2.5,
                         alpha=1.0)
        ax.add_patch(rect)

        # Add percentage label if rectangle is large enough
        if height > 0.08 and width > 0.06:  # Only label if big enough
            percentage = (count / blockchain_total) * 100
            ax.text(x_start + width/2, y_start + height/2,
                   f'{percentage:.1f}%',
                   ha='center', va='center',
                   fontsize=PERCENTAGE_FONTSIZE + 2,
                   weight='bold',
                   color='white')

        mosaic_data.append({
            'blockchain': blockchain,
            'category': category,
            'x': x_start,
            'y': y_start,
            'width': width,
            'height': height,
            'count': count,
            'blockchain_total': blockchain_total
        })

        y_start += height

    # Add blockchain label at bottom (all horizontal, same font size)
    ax.text(x_start + width/2, -0.08,
           blockchain,
           ha='center', va='top',
           fontsize=LABEL_FONTSIZE,
           weight='bold',
           color=BLOCKCHAIN_COLORS.get(blockchain, '#2C3E50'),
           rotation=0)

    # Add total count below blockchain name
    ax.text(x_start + width/2, -0.14,
           f'{blockchain_total:,} dApps',
           ha='center', va='top',
           fontsize=CATEGORY_FONTSIZE,
           style='italic',
           color='#5D6D7E',
           rotation=0)

    x_start += width

# ============================================
# TITLES AND ANNOTATIONS
# ============================================

# Main title - Bold sans-serif (states the content)
fig.text(0.5, 0.96, 'BLOCKCHAIN dAPPS',
         ha='center', fontsize=TITLE_FONTSIZE + 8, weight='heavy', color='#1a1a1a',
         family='sans-serif')

# Subtitle - Italic script-style (vintage aesthetic)
fig.text(0.5, 0.925, 'by category',
         ha='center', fontsize=SUBTITLE_FONTSIZE + 8, style='italic', color='#2C3E50',
         family='serif')

# Description - Clear context about the visualization
fig.text(0.5, 0.89,
         'Where different blockchains distribute their dApps in 2025',
         ha='center', fontsize=SUBTITLE_FONTSIZE, color='#4a4a4a')

# Legend - Category colors (simplified, matching reference style)
# Order categories from darkest to lightest (sequential palette)
# Accessibility: Legend provides alternative to color-only encoding
category_order = ['DeFi', 'NFT', 'Gaming', 'Social', 'Other']
legend_elements = [mpatches.Patch(facecolor=CATEGORY_COLORS[cat],
                                 edgecolor='none',
                                 label=cat)
                  for cat in category_order if cat in category_totals.index]

legend = ax.legend(handles=legend_elements,
                  loc='center right',
                  bbox_to_anchor=(1.08, 0.5),
                  frameon=False,
                  fontsize=CATEGORY_FONTSIZE + 1,
                  title='Categories')
legend.get_frame().set_facecolor(BACKGROUND_COLOR)
legend.get_frame().set_alpha(1.0)

# Removed key insights box to match cleaner reference design

# Data sources and attribution
fig.text(0.5, 0.02,
         'Data source: DappRadar, DeFi Llama, State of the DApps (2024) | Visualization: Your Name | #30DayChartChallenge 2026',
         ha='center', fontsize=SOURCE_FONTSIZE, style='italic', color='#6a6a6a')

# Configure axes
ax.set_xlim(0, 1)
ax.set_ylim(-0.16, 1)
ax.axis('off')

# ============================================
# SAVE OUTPUTS
# ============================================
output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(output_dir, exist_ok=True)

print('\n=== Saving visualizations ===')

try:
    # PNG format
    output_png = os.path.join(output_dir, 'day03_mosaic_blockchain_dapps.png')
    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor=BACKGROUND_COLOR, format='png')
    print(f'✓ PNG saved: {output_png}')

    # PDF format
    output_pdf = os.path.join(output_dir, 'day03_mosaic_blockchain_dapps.pdf')
    plt.savefig(output_pdf, bbox_inches='tight', facecolor=BACKGROUND_COLOR, format='pdf')
    print(f'✓ PDF saved: {output_pdf}')

    # SVG format
    output_svg = os.path.join(output_dir, 'day03_mosaic_blockchain_dapps.svg')
    plt.savefig(output_svg, bbox_inches='tight', facecolor=BACKGROUND_COLOR, format='svg')
    print(f'✓ SVG saved: {output_svg}')

except Exception as e:
    print(f'Error saving files: {e}', file=sys.stderr)
    sys.exit(1)

plt.show()

# ============================================
# STATISTICS AND SUMMARY
# ============================================
print('\n=== Visualization Statistics ===')
print(f'Total dApps analyzed: {total_dapps:,}')
print(f'Number of blockchains: {len(blockchain_order)}')
print(f'Number of categories: {len(category_totals)}')
print(f'\nTop 3 Blockchains:')
for i, (blockchain, count) in enumerate(blockchain_totals.head(3).items(), 1):
    print(f'{i}. {blockchain}: {count:,} dApps ({(count/total_dapps)*100:.1f}%)')

print(f'\nCategory Distribution:')
for category, count in category_totals.items():
    print(f'  - {category}: {count:,} dApps ({(count/total_dapps)*100:.1f}%)')

print(f'\nMosaic rectangles created: {len(mosaic_data)}')
