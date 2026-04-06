"""
Day 3: Mosaic Visualization
Theme: Blockchain dApps Distribution by Category (2025)
Data Sources: DappRadar, DeFi Llama, State of the DApps
#30DayChartChallenge

Mosaic plot (Marimekko chart) showing:
- Width: Total dApps per blockchain
- Height: Category distribution within each blockchain
- Color: Category type

Skills applied:
- matplotlib: Complex mosaic layouts, custom patches
- data-visualization: Two-dimensional proportion representation
- statsmodels: Mosaic plot implementation
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
FIGURE_WIDTH = 20
FIGURE_HEIGHT = 12

# Colors - Accessible palette for categories
CATEGORY_COLORS = {
    'DeFi': '#2E86AB',      # Blue - Financial stability
    'NFT': '#A23B72',       # Purple - Creativity/Art
    'Gaming': '#F18F01',    # Orange - Entertainment
    'Social': '#C73E1D',    # Red - Connection
    'Other': '#6A994E'      # Green - Growth/Other
}

# Blockchain brand colors for labels
BLOCKCHAIN_COLORS = {
    'Ethereum': '#627EEA',
    'BNB Chain': '#F3BA2F',
    'Solana': '#14F195',
    'Polygon': '#8247E5',
    'Arbitrum': '#28A0F0',
    'Base': '#0052FF',
    'Avalanche': '#E84142',
    'Optimism': '#FF0420'
}

# Set style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

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

fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), facecolor='white')
ax.set_facecolor('white')

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
                         edgecolor='white',
                         linewidth=2.5,
                         alpha=0.85)
        ax.add_patch(rect)

        # Add percentage label if rectangle is large enough
        if height > 0.08 and width > 0.06:  # Only label if big enough
            percentage = (count / blockchain_total) * 100
            ax.text(x_start + width/2, y_start + height/2,
                   f'{percentage:.0f}%',
                   ha='center', va='center',
                   fontsize=PERCENTAGE_FONTSIZE,
                   weight='bold',
                   color='white',
                   bbox=dict(boxstyle='round,pad=0.3',
                            facecolor='black',
                            alpha=0.3,
                            edgecolor='none'))

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

    # Add blockchain label at bottom
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
           color='#5D6D7E')

    x_start += width

# ============================================
# TITLES AND ANNOTATIONS
# ============================================

# Main title
fig.text(0.5, 0.96, 'Blockchain dApps Ecosystem Distribution (2025)',
         ha='center', fontsize=TITLE_FONTSIZE, weight='bold', color='#2C3E50')

# Subtitle
fig.text(0.5, 0.93,
         'Mosaic chart showing dApp distribution across blockchains and categories • Width = Total dApps • Height = Category proportion',
         ha='center', fontsize=SUBTITLE_FONTSIZE, style='italic', color='#5D6D7E')

# Legend - Category colors
legend_elements = [mpatches.Patch(facecolor=CATEGORY_COLORS[cat],
                                 edgecolor='white',
                                 label=f'{cat} ({category_totals[cat]:,} dApps)',
                                 linewidth=2)
                  for cat in category_totals.index]

legend = ax.legend(handles=legend_elements,
                  loc='upper left',
                  bbox_to_anchor=(0.02, 0.98),
                  frameon=True,
                  fancybox=True,
                  shadow=True,
                  fontsize=CATEGORY_FONTSIZE,
                  title='Category Distribution',
                  title_fontsize=LABEL_FONTSIZE)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_alpha(0.95)

# Key insights
dominant_blockchain = blockchain_order[0]
dominant_count = blockchain_totals.iloc[0]
dominant_category = category_totals.index[0]

insight_text = (
    f"Key Insights:\n"
    f"• {dominant_blockchain} leads with {dominant_count:,} dApps ({(dominant_count/total_dapps)*100:.1f}% of total ecosystem)\n"
    f"• {dominant_category} dominates across all chains with {category_totals.iloc[0]:,} applications\n"
    f"• Polygon shows highest gaming focus with {df[(df['Blockchain']=='Polygon') & (df['Category']=='Gaming')]['Count'].values[0]} gaming dApps\n"
    f"• Total: {total_dapps:,} dApps tracked across {len(blockchain_order)} major blockchains"
)

fig.text(0.5, 0.12, insight_text,
         ha='center', va='top',
         fontsize=INSIGHT_FONTSIZE,
         color='#34495E',
         bbox=dict(boxstyle='round,pad=0.8',
                  facecolor='#E8F8F5',
                  alpha=0.9,
                  edgecolor='#16A085',
                  linewidth=1.5))

# Data sources
fig.text(0.5, 0.02,
         'Data Sources: DappRadar (www.dappradar.com) | DeFi Llama | State of the DApps\n' +
         '#30DayChartChallenge Day 3: Mosaic',
         ha='center', fontsize=SOURCE_FONTSIZE, style='italic', color='#7F8C8D')

# Configure axes
ax.set_xlim(0, 1)
ax.set_ylim(-0.18, 1)
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
    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white', format='png')
    print(f'✓ PNG saved: {output_png}')

    # PDF format
    output_pdf = os.path.join(output_dir, 'day03_mosaic_blockchain_dapps.pdf')
    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white', format='pdf')
    print(f'✓ PDF saved: {output_pdf}')

    # SVG format
    output_svg = os.path.join(output_dir, 'day03_mosaic_blockchain_dapps.svg')
    plt.savefig(output_svg, bbox_inches='tight', facecolor='white', format='svg')
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
