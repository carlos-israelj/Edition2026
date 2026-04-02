"""
Day 1: Part-to-Whole Visualization - Minimalist Version
Theme: LLM Usage by Developers (2025)
Inspired by the "1 in 8 women" breast cancer awareness design

This minimalist version focuses on the most striking statistic:
"8 in 10 developers use OpenAI GPT models"
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import os
from pypalettes import load_cmap

# Set style with professional matplotlib best practices
plt.style.use('seaborn-v0_8-white')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# Read data
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'llm_usage_2025.csv')
df = pd.read_csv(data_path)

# Create figure
fig, ax = plt.subplots(figsize=(12, 12), facecolor='white')

# Load color palette
cmap = load_cmap("Acadia")
primary_color = cmap.colors[0]  # OpenAI GPT color
secondary_color = '#E8E8E8'  # Light gray for non-users

# ============================================
# Create 10 human figures arranged in 2 rows
# 8 filled (GPT users), 2 unfilled (non-users)
# ============================================

def draw_human_figure(ax, x, y, size, filled=True):
    """Draw a simple human figure using circles and lines"""
    color = primary_color if filled else secondary_color
    alpha = 1.0 if filled else 0.3

    # Head
    head = Circle((x, y + size * 0.7), size * 0.15,
                  facecolor=color, edgecolor='none', alpha=alpha)
    ax.add_patch(head)

    # Body (rectangle using plot)
    body_width = size * 0.3
    body_height = size * 0.5
    body_x = [x - body_width/2, x + body_width/2, x + body_width/2, x - body_width/2, x - body_width/2]
    body_y = [y + size * 0.5, y + size * 0.5, y, y, y + size * 0.5]
    ax.fill(body_x, body_y, color=color, alpha=alpha, edgecolor='none')

    # Arms
    arm_width = size * 0.4
    ax.plot([x - arm_width/2, x - arm_width], [y + size * 0.35, y + size * 0.2],
            color=color, linewidth=size*8, alpha=alpha, solid_capstyle='round')
    ax.plot([x + arm_width/2, x + arm_width], [y + size * 0.35, y + size * 0.2],
            color=color, linewidth=size*8, alpha=alpha, solid_capstyle='round')

    # Legs
    leg_width = size * 0.15
    ax.plot([x - leg_width, x - leg_width], [y, y - size * 0.4],
            color=color, linewidth=size*8, alpha=alpha, solid_capstyle='round')
    ax.plot([x + leg_width, x + leg_width], [y, y - size * 0.4],
            color=color, linewidth=size*8, alpha=alpha, solid_capstyle='round')

# Arrange 10 figures in 2 rows of 5
figure_size = 0.5
spacing_x = 1.8
spacing_y = 2.0
start_x = 1
start_y = 4

total_developers = 10
gpt_users = 8  # 81% ≈ 8 out of 10

figure_count = 0
for row in range(2):
    for col in range(5):
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        filled = figure_count < gpt_users
        draw_human_figure(ax, x, y, figure_size, filled)
        figure_count += 1

# ============================================
# Add minimalist text
# ============================================

# Main statistic
ax.text(5, 8.5, '8 in 10',
        ha='center', va='center',
        fontsize=72, weight='bold',
        color=primary_color)

ax.text(5, 7.8, 'developers',
        ha='center', va='center',
        fontsize=32, weight='normal',
        color='#2C3E50')

ax.text(5, 7.3, 'use OpenAI GPT models',
        ha='center', va='center',
        fontsize=24, weight='normal',
        color='#34495E')

# Subtext with context
ax.text(5, 0.5,
        'Among 49,000+ developers from 177 countries surveyed in 2025,\n' +
        '81% reported using OpenAI GPT models as their primary AI tool.',
        ha='center', va='center',
        fontsize=11, style='italic',
        color='#7F8C8D')

# Data source
ax.text(5, 0.1,
        'Source: Stack Overflow Developer Survey 2025 | #30DayChartChallenge',
        ha='center', va='center',
        fontsize=9,
        color='#95A5A6')

# ============================================
# Configure axes
# ============================================
ax.set_xlim(0, 10)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_aspect('equal')

# ============================================
# Save in multiple high-quality formats
# ============================================
output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(output_dir, exist_ok=True)

# PNG format
output_png = os.path.join(output_dir, 'day01_minimalist_llm_usage.png')
plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white', format='png')
print(f'✓ PNG saved: {output_png}')

# PDF format
output_pdf = os.path.join(output_dir, 'day01_minimalist_llm_usage.pdf')
plt.savefig(output_pdf, bbox_inches='tight', facecolor='white', format='pdf')
print(f'✓ PDF saved: {output_pdf}')

# SVG format
output_svg = os.path.join(output_dir, 'day01_minimalist_llm_usage.svg')
plt.savefig(output_svg, bbox_inches='tight', facecolor='white', format='svg')
print(f'✓ SVG saved: {output_svg}')

plt.show()
