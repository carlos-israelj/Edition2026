"""
Day 1: Part-to-Whole Visualization
Theme: LLM Usage by Developers (2025)
Data Source: Stack Overflow Developer Survey 2025
#30DayChartChallenge

This script demonstrates the Matplotlib Pattern:
1. Import matplotlib.pyplot as plt
2. Create figure and axes with plt.subplots()
3. Fill the axes with plotting methods (ax.pie(), ax.add_patch(), etc.)
4. Customize with ax methods (ax.set_title(), ax.axis(), etc.)
5. Save and show with plt.savefig() and plt.show()
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
import numpy as np
import os
from pypalettes import load_cmap

# Set style with professional matplotlib best practices
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 18

# Read data
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'llm_usage_2025.csv')
df = pd.read_csv(data_path)

# Sort by usage percentage
df = df.sort_values('Usage_Percentage', ascending=False)

# ============================================
# Step 1: Create figure and axes using GridSpec for professional layout
# Following matplotlib best practices for complex multi-panel figures
# Creating 3 subplots: Donut Chart, Treemap, and Waffle Chart
# ============================================
fig = plt.figure(figsize=(24, 8), facecolor='white')
gs = GridSpec(1, 3, figure=fig, wspace=0.25, hspace=0.1)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])

# ============================================
# Load professional color palette using pypalettes
# Using 'Acadia' palette - perfect for qualitative data (showing groups)
# Modified to enhance gray visibility
# ============================================
cmap = load_cmap("Acadia")
colors = list(cmap.colors)

# Replace the light gray with a darker, more visible gray
# Original Acadia has a very light gray that disappears on white background
colors[3] = '#5D6D7E'  # Darker gray with better contrast for "Other LLMs"

# ============================================
# Step 2: Fill ax1 with a Donut Chart (using ax.pie())
# ============================================

wedges, texts, autotexts = ax1.pie(
    df['Usage_Percentage'],
    labels=df['LLM_Model'],
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    pctdistance=0.85,
    explode=[0.05 if i == 0 else 0 for i in range(len(df))],
    textprops={'fontsize': 11, 'weight': 'bold'}
)

# Make percentage text white for better visibility on dark colors
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_weight('bold')

# Create donut effect
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
ax1.add_artist(centre_circle)

# Add center text
ax1.text(0, 0, '49K+\nDevelopers',
         ha='center', va='center',
         fontsize=16, weight='bold',
         color='#2C3E50')

ax1.set_title('LLM Distribution Among Developers',
              fontsize=14, weight='bold', pad=20, color='#2C3E50')

# Add narrative annotation with key insights
insight_text = (
    "OpenAI GPT models dominate the landscape with 81% usage,\n"
    "more than triple the second-place Claude Sonnet (43%).\n"
    "Together, the top 3 commercial models (GPT, Claude, Gemini)\n"
    "account for 159% combined usage - revealing that most\n"
    "developers actively use multiple LLM tools in their workflow."
)
ax1.text(0, -1.5, insight_text,
         ha='center', va='top',
         fontsize=9, style='italic',
         color='#34495E',
         bbox=dict(boxstyle='round,pad=0.8',
                  facecolor='#E8F4F8',
                  alpha=0.9,
                  edgecolor='#3498DB',
                  linewidth=1.5))

# ============================================
# Step 3: Fill ax2 with a Treemap (custom visualization)
# ============================================

def squarify(sizes, x, y, width, height):
    """Create rectangles for treemap"""
    rectangles = []

    if not sizes:
        return rectangles

    if len(sizes) == 1:
        rectangles.append((x, y, width, height))
        return rectangles

    # Normalize sizes
    total = sum(sizes)
    normalized = [s / total for s in sizes]

    # Split based on orientation
    if width >= height:
        # Split vertically
        current_x = x
        for i, norm_size in enumerate(normalized):
            rect_width = width * norm_size
            rectangles.append((current_x, y, rect_width, height))
            current_x += rect_width
    else:
        # Split horizontally
        current_y = y
        for i, norm_size in enumerate(normalized):
            rect_height = height * norm_size
            rectangles.append((x, current_y, width, rect_height))
            current_y += rect_height

    return rectangles

# Create treemap rectangles
rectangles = squarify(df['Usage_Percentage'].tolist(), 0, 0, 10, 10)

# Draw rectangles
for idx, (x, y, w, h) in enumerate(rectangles):
    rect = Rectangle((x, y), w, h,
                     facecolor=colors[idx],
                     edgecolor='white',
                     linewidth=3)
    ax2.add_patch(rect)

    # Add text
    label = df.iloc[idx]['LLM_Model']
    percentage = df.iloc[idx]['Usage_Percentage']

    # Center text in rectangle
    cx = x + w/2
    cy = y + h/2

    # Adjust font size based on rectangle size
    if w > 2.5:  # Large rectangles - show label and percentage
        fontsize = 10
        text_content = f'{label}\n{percentage}%'
    elif w > 1.0:  # Medium rectangles - show only percentage
        fontsize = 9
        text_content = f'{percentage}%'
    else:  # Small rectangles - skip text to avoid overlap
        continue

    ax2.text(cx, cy, text_content,
            ha='center', va='center',
            fontsize=fontsize, weight='bold',
            color='white',
            bbox=dict(boxstyle='round,pad=0.3',
                     facecolor='black',
                     alpha=0.3,
                     edgecolor='none'))

ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('Treemap View of LLM Market Share',
              fontsize=14, weight='bold', pad=20, color='#2C3E50')

# ============================================
# Step 4: Fill ax3 with a Waffle Chart
# Each square represents 1% of developers
# ============================================

def create_waffle_chart(ax, data, colors, cols=10):
    """Create a waffle chart with circular dots where each dot = 1%"""
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-0.5, cols - 0.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Create 100 circles (10x10 grid)
    current_count = 0
    color_idx = 0

    for row in range(cols):
        for col in range(cols):
            # Determine which LLM this circle belongs to
            accumulated = 0
            for idx, percentage in enumerate(data['Usage_Percentage']):
                accumulated += percentage
                if current_count < accumulated:
                    color = colors[idx]
                    label = data.iloc[idx]['LLM_Model']
                    break

            # Draw circle (dot) instead of square
            from matplotlib.patches import Circle
            circle = Circle((col, cols - row - 1), 0.4,
                           facecolor=color,
                           edgecolor='white',
                           linewidth=1.5)
            ax.add_patch(circle)
            current_count += 1

    return ax

create_waffle_chart(ax3, df, colors)
ax3.set_title('Waffle Chart: Each Dot = 1% of Developers',
              fontsize=14, weight='bold', pad=20, color='#2C3E50')

# Add legend for waffle chart
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors[i], edgecolor='white',
                         label=f"{df.iloc[i]['LLM_Model']} ({df.iloc[i]['Usage_Percentage']}%)")
                   for i in range(len(df))]
ax3.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1),
          fontsize=9, frameon=True, fancybox=True, shadow=True)

# ============================================
# Main Title and Footer
# ============================================
fig.suptitle('Developer AI Tool Preferences: LLM Usage Distribution (2025)',
             fontsize=18, weight='bold', y=0.98, color='#2C3E50')

# Add source and challenge info
fig.text(0.5, 0.02,
         'Data Source: Stack Overflow Developer Survey 2025 (49,000+ developers, 177 countries)\n' +
         'URL: https://survey.stackoverflow.co/2025/ | #30DayChartChallenge Day 1: Part-to-Whole',
         ha='center', fontsize=9, style='italic', color='#7F8C8D',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#ECF0F1', alpha=0.8))

# Create output directory if it doesn't exist
output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(output_dir, exist_ok=True)

# ============================================
# Step 4: Save in multiple high-quality formats for publication
# PNG (web/presentation), PDF (print), SVG (vector/editing)
# ============================================

# PNG format - high-resolution for web and presentations
output_png = os.path.join(output_dir, 'day01_part_to_whole_llm_usage.png')
plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white', format='png')
print(f'✓ PNG saved: {output_png}')

# PDF format - publication quality for print
output_pdf = os.path.join(output_dir, 'day01_part_to_whole_llm_usage.pdf')
plt.savefig(output_pdf, bbox_inches='tight', facecolor='white', format='pdf')
print(f'✓ PDF saved: {output_pdf}')

# SVG format - vector graphics for editing
output_svg = os.path.join(output_dir, 'day01_part_to_whole_llm_usage.svg')
plt.savefig(output_svg, bbox_inches='tight', facecolor='white', format='svg')
print(f'✓ SVG saved: {output_svg}')

# Show the plot
plt.show()

print('\n=== Statistics ===')
print(f'Total LLM models analyzed: {len(df)}')
print(f'Most popular LLM: {df.iloc[0]["LLM_Model"]} ({df.iloc[0]["Usage_Percentage"]}%)')
print(f'Combined usage (top 3): {df.head(3)["Usage_Percentage"].sum()}%')
