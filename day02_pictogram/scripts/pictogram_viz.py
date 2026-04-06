"""
Day 2: Pictogram Visualization
Theme: Blockchain Programming Languages Usage (2025)
Data Sources: Electric Capital Developer Report 2025, Hard Fork Analytics
#30DayChartChallenge

Simple, clean pictogram design.
Each icon represents 5% of blockchain developers.

Skills applied:
- matplotlib: GridSpec layouts, multi-format export
- data-visualization: Colorblind-safe palettes, accessibility
- data-viz-plots: Pictogram best practices
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import cairosvg
from io import BytesIO

# ============================================
# CONFIGURATION CONSTANTS
# ============================================

# Layout constants
ICON_PERCENTAGE = 5.0  # Each icon represents 5% of developers
ROW_HEIGHT = 1.8  # Vertical spacing between languages
LABEL_X_POS = 0.5  # X position for language labels
ICONS_START_X = 1.5  # X position where icons start
ICON_SPACING = 0.9  # Horizontal spacing between icons (increased for high-res icons)
PERCENTAGE_LABEL_OFFSET = 0.35  # Vertical offset for percentage label

# Font sizes
TITLE_FONTSIZE = 22
SUBTITLE_FONTSIZE = 14
LANGUAGE_FONTSIZE = 18
PERCENTAGE_FONTSIZE = 13
ICON_FONTSIZE = 36
INSIGHT_FONTSIZE = 11
SOURCE_FONTSIZE = 10

# Figure dimensions
FIGURE_WIDTH = 18
FIGURE_HEIGHT = 12

# Set style - clean and minimal
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# ============================================
# DATA LOADING AND VALIDATION
# ============================================

def load_and_validate_data(data_path):
    """
    Load and validate the programming languages data.

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
    required_columns = ['Language', 'Usage_Percentage']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Validate data types
    if not pd.api.types.is_numeric_dtype(df['Usage_Percentage']):
        raise ValueError("Usage_Percentage must be numeric")

    # Check for negative percentages
    if (df['Usage_Percentage'] < 0).any():
        raise ValueError("Usage_Percentage cannot be negative")

    # Sort by usage percentage (descending)
    df = df.sort_values('Usage_Percentage', ascending=False)

    return df

# Read data
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'programming_languages_2025.csv')

try:
    df = load_and_validate_data(data_path)
except (FileNotFoundError, ValueError) as e:
    print(f"Error loading data: {e}", file=sys.stderr)
    sys.exit(1)

# ============================================
# LANGUAGE-SPECIFIC COLORS AND ICONS
# ============================================
# Colors selected for accessibility and brand alignment
# Icons chosen to represent each language's characteristics

language_colors = {
    'Solidity': '#363636',    # Solidity dark gray
    'Rust': '#CE422B',        # Rust orange-red
    'JavaScript': '#F7DF1E',  # JavaScript yellow
    'Move': '#4B32C3',        # Move purple
    'Vyper': '#3C3C3D',       # Vyper dark
    'Go': '#00ADD8'           # Go cyan
}

# Default color for unlisted languages (colorblind-safe)
DEFAULT_COLOR = '#7F8C8D'

# Language-specific icon file paths (SVG format)
language_icon_files = {
    'Solidity': 'solidity.svg',
    'Rust': 'rust.svg',
    'JavaScript': 'javascript.svg',
    'Move': 'move.svg',  # Will use fallback if not available
    'Vyper': 'vyper.svg',
    'Go': 'go.svg'
}

# Fallback Unicode symbols if image not available
language_icons_fallback = {
    'Solidity': '⬡',          # Hexagon (Ethereum)
    'Rust': '⚙',              # Gear (systems programming)
    'JavaScript': '{ }',      # Curly braces
    'Move': '➜',              # Arrow (Move semantics)
    'Vyper': '◆',             # Diamond (simple geometric)
    'Go': '▶'                 # Play/Go symbol
}

# Default icon for unlisted languages
DEFAULT_ICON = '</>'

# Icon size in the visualization
ICON_SIZE = 0.05  # Zoom factor for images (reduced to prevent overlap)
ICON_RESOLUTION = 800  # Higher resolution for crisp icons (px)

# ============================================
# LOAD ICON IMAGES
# ============================================

def load_icon_image(language):
    """
    Load the icon image for a given language.
    Converts SVG to high-resolution PNG using cairosvg for crisp display.

    Args:
        language: The programming language name

    Returns:
        PIL.Image object or None if not available
    """
    icons_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icons')
    icon_file = language_icon_files.get(language)

    if icon_file:
        icon_path = os.path.join(icons_dir, icon_file)
        if os.path.exists(icon_path):
            try:
                if icon_path.endswith('.svg'):
                    # Convert SVG to high-res PNG in memory using cairosvg
                    # Using high resolution for crisp rendering at 300 DPI
                    png_data = cairosvg.svg2png(
                        url=icon_path,
                        output_width=ICON_RESOLUTION,
                        output_height=ICON_RESOLUTION
                    )
                    img = Image.open(BytesIO(png_data))
                    # Convert to RGBA if needed for transparency
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    return img
                else:
                    return Image.open(icon_path)
            except Exception as e:
                print(f"Warning: Could not load icon for {language}: {e}")
                return None
    return None

# ============================================
# MATPLOTLIB PATTERN: Create figure
# ============================================
fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), facecolor='white')
ax.set_facecolor('white')

# ============================================
# DRAW PICTOGRAM
# Each icon represents 5% of blockchain developers
# ============================================

def calculate_num_icons(usage_percentage):
    """
    Calculate number of icons to display based on usage percentage.

    Uses floor division to ensure consistent representation:
    - 90% → 18 icons (18 * 5% = 90%)
    - 35% → 7 icons (7 * 5% = 35%)
    - 28% → 5 icons (5 * 5% = 25%, closer than 6*5=30%)

    Args:
        usage_percentage: The usage percentage value

    Returns:
        Number of icons to display (minimum 0)
    """
    # Use round for better visual representation of the data
    num_icons = int(np.round(usage_percentage / ICON_PERCENTAGE))
    return max(0, num_icons)  # Ensure non-negative

y_start = len(df) * ROW_HEIGHT
current_y = y_start

for idx, row in df.iterrows():
    language = row['Language']
    usage = row['Usage_Percentage']
    color = language_colors.get(language, DEFAULT_COLOR)

    # Calculate number of icons
    num_icons = calculate_num_icons(usage)

    # Draw language name
    ax.text(LABEL_X_POS, current_y, language,
            fontsize=LANGUAGE_FONTSIZE, weight='bold', va='center', ha='right',
            color='#2C3E50')

    # Draw usage percentage
    ax.text(LABEL_X_POS, current_y - PERCENTAGE_LABEL_OFFSET, f'{usage}%',
            fontsize=PERCENTAGE_FONTSIZE, va='center', ha='right',
            color='#5D6D7E', style='italic')

    # Draw language-specific icons
    if num_icons > 0:
        icon_image = load_icon_image(language)

        for i in range(num_icons):
            x_pos = ICONS_START_X + (i * ICON_SPACING)

            if icon_image:
                # Use image icon
                try:
                    imagebox = OffsetImage(icon_image, zoom=ICON_SIZE)
                    ab = AnnotationBbox(imagebox, (x_pos, current_y),
                                      frameon=False,
                                      box_alignment=(0.5, 0.5))
                    ax.add_artist(ab)
                except Exception as e:
                    # Fallback to Unicode symbol
                    icon = language_icons_fallback.get(language, DEFAULT_ICON)
                    ax.text(x_pos, current_y, icon,
                            fontsize=ICON_FONTSIZE, weight='bold', va='center', ha='center',
                            color=color)
            else:
                # Fallback to Unicode symbol if image not available
                icon = language_icons_fallback.get(language, DEFAULT_ICON)
                ax.text(x_pos, current_y, icon,
                        fontsize=ICON_FONTSIZE, weight='bold', va='center', ha='center',
                        color=color)
    else:
        # For languages with < 5%, show a small indicator
        ax.text(ICONS_START_X, current_y, f"({usage}%)",
                fontsize=PERCENTAGE_FONTSIZE - 2, va='center', ha='left',
                color='#95A5A6', style='italic')

    # Move to next language
    current_y -= ROW_HEIGHT

# ============================================
# TITLES, ANNOTATIONS, AND INSIGHTS
# ============================================

# Main title
fig.text(0.5, 0.96, 'Blockchain Programming Languages Usage (2025)',
         ha='center', fontsize=TITLE_FONTSIZE, weight='bold', color='#2C3E50')

# Subtitle with icon explanation
fig.text(0.5, 0.93,
         f'Each icon represents {ICON_PERCENTAGE:.0f}% of blockchain developers • Percentages reflect adoption overlap',
         ha='center', fontsize=SUBTITLE_FONTSIZE, style='italic', color='#5D6D7E')

# Key insight - data storytelling
insight_text = (
    "Solidity dominates with 90% of smart contracts built on Ethereum.\n"
    "Rust (35%) is gaining traction in Solana and Polkadot ecosystems.\n"
    "Move language shows 120% growth in 2025 driven by Aptos and Sui adoption.\n"
    "Note: Totals exceed 100% as developers often work with multiple languages."
)
fig.text(0.5, 0.14, insight_text,
         ha='center', va='top',
         fontsize=INSIGHT_FONTSIZE, style='italic',
         color='#34495E',
         bbox=dict(boxstyle='round,pad=0.8',
                  facecolor='#E8F4F8',
                  alpha=0.9,
                  edgecolor='#3498DB',
                  linewidth=1.5))

# Data source and attribution (moved down to avoid overlap)
fig.text(0.5, 0.02,
         'Data Sources: Electric Capital Developer Report 2025 (www.developerreport.com) | Hard Fork Analytics\n' +
         '#30DayChartChallenge Day 2: Pictogram',
         ha='center', fontsize=SOURCE_FONTSIZE, style='italic', color='#7F8C8D')

# Configure axes
ax.set_xlim(0, 20)
ax.set_ylim(-2, y_start + 1)
ax.axis('off')

# ============================================
# MATPLOTLIB PATTERN: Save outputs in multiple formats
# ============================================
output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(output_dir, exist_ok=True)

print('\n=== Saving visualizations ===')

try:
    # PNG format - high resolution for web/presentations
    output_png = os.path.join(output_dir, 'day02_pictogram_programming_languages.png')
    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white', format='png')
    print(f'✓ PNG saved: {output_png}')

    # PDF format - vector for publication/printing
    output_pdf = os.path.join(output_dir, 'day02_pictogram_programming_languages.pdf')
    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white', format='pdf')
    print(f'✓ PDF saved: {output_pdf}')

    # SVG format - vector for editing
    output_svg = os.path.join(output_dir, 'day02_pictogram_programming_languages.svg')
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
print(f'Total languages analyzed: {len(df)}')
print(f'Most popular: {df.iloc[0]["Language"]} ({df.iloc[0]["Usage_Percentage"]}% usage)')
print(f'Least popular: {df.iloc[-1]["Language"]} ({df.iloc[-1]["Usage_Percentage"]}% usage)')
print(f'Total usage (exceeds 100% due to overlap): {df["Usage_Percentage"].sum():.1f}%')
print(f'Each icon represents: {ICON_PERCENTAGE}% of blockchain developers')
print(f'Total icons displayed: {sum(calculate_num_icons(row["Usage_Percentage"]) for _, row in df.iterrows())}')

# Check for languages below threshold
below_threshold = df[df['Usage_Percentage'] < ICON_PERCENTAGE]
if not below_threshold.empty:
    print(f'\nLanguages below {ICON_PERCENTAGE}% threshold (shown with percentage only):')
    for _, row in below_threshold.iterrows():
        print(f'  - {row["Language"]}: {row["Usage_Percentage"]}%')
