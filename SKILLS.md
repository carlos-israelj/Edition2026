# Skills y Herramientas - #30DayChartChallenge 2026

Este documento lista todos los skills, herramientas y tecnologías utilizadas en el proyecto #30DayChartChallenge Edition 2026.

## Skills de Claude Code

### 1. **Matplotlib** (`microck/ordinary-claude-skills`)
- **Instalación**: `npx skillfish add microck/ordinary-claude-skills matplotlib`
- **Estrellas**: 81 ⭐
- **Uso**: Visualizaciones estáticas de alta calidad
- **Días aplicados**: Day 1 (Part-to-Whole), Day 2 (Pictogram), Day 3 (Mosaic)
- **Características**:
  - Matplotlib Pattern: Import → plt.subplots() → Fill axes → Customize → Save/Show
  - GridSpec para layouts multi-panel
  - Custom patches (Rectangle) para mosaic plots
  - Export en múltiples formatos (PNG, PDF, SVG)

### 2. **Data Visualization** (`anthropics/knowledge-work-plugins`)
- **Instalación**: `npx skillfish add anthropics/knowledge-work-plugins data-visualization`
- **Estrellas**: 8,000 ⭐
- **Uso**: Análisis y visualización avanzada de datos
- **Días aplicados**: Day 1, Day 2, Day 3
- **Características**:
  - Mejores prácticas para visualización de datos
  - Colorblind-safe palettes
  - Data storytelling techniques
  - Two-dimensional proportion representation (Mosaic plots)

### 3. **Data Viz Plots** (`microck/ordinary-claude-skills`)
- **Instalación**: `npx skillfish add microck/ordinary-claude-skills data-viz-plots`
- **Estrellas**: 81 ⭐
- **Uso**: Tipos específicos de gráficos y visualizaciones
- **Días aplicados**: Day 1, Day 2, Day 3
- **Características**:
  - Treemaps
  - Waffle charts
  - Donut charts
  - Pictogramas
  - Mosaic plots (Marimekko charts)

## Bibliotecas Python

### Core Libraries
```
python
pandas>=2.0.0        # Data manipulation
matplotlib>=3.7.0    # Plotting
numpy>=1.24.0        # Numerical operations
```

### Visualización Avanzada (Day 1)
```python
seaborn>=0.12.0      # Statistical visualization
pypalettes>=0.1.0    # Professional color palettes
```

### Interactive (Usado temporalmente, luego removido)
```python
plotly>=5.14.0       # Interactive plots (removed)
kaleido>=0.2.1       # Static image export (removed)
```

## Paletas de Colores

### **Acadia Palette** (pypalettes)
- **Día 1 y 2**: Palette colorblind-safe
- **Modificaciones**: Gris oscuro (#5D6D7E) para mejor contraste
- **Uso**: Lenguajes de programación, categorías múltiples

### **Custom Blockchain Palette** (Day 2)
```python
{
    'Solidity': '#363636',    # Dark gray
    'Rust': '#CE422B',        # Orange-red
    'JavaScript': '#F7DF1E',  # Yellow
    'Move': '#4B32C3',        # Purple
    'Vyper': '#3C3C3D',       # Dark
    'Go': '#00ADD8'           # Cyan
}
```

### **Vintage Earth Tone Palette** (Day 3)
```python
# Monochromatic earth tone palette
{
    'DeFi': '#1a1a1a',      # Near black
    'NFT': '#3a4a2f',       # Dark olive green
    'Gaming': '#5a6a4f',    # Medium olive
    'Social': '#7a8a6f',    # Sage green
    'Other': '#9aaa8f'      # Light sage
}
# Background: '#D9D4BA' (Warm beige)
```

## Fuentes de Datos

### Day 1: Part-to-Whole
- **Stack Overflow Developer Survey 2025**
- URL: https://survey.stackoverflow.co/2025/
- Press: https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/
- Datos: LLM Usage por 49K+ desarrolladores, 177 países

### Day 2: Pictogram
- **Electric Capital Developer Report 2025**
- URL: https://www.developerreport.com
- **Hard Fork Analytics**
- Datos: Blockchain programming languages usage statistics

### Day 3: Mosaic
- **DappRadar**
- URL: https://www.dappradar.com
- **DeFi Llama**
- **State of the DApps**
- Datos: 12,520 dApps across 8 blockchains, 5 categories (2025)

## Técnicas de Visualización

### Day 1: Part-to-Whole
1. **Donut Chart**: Distribución proporcional con centro vacío
2. **Treemap**: Rectangles proporcionales jerárquicos
3. **Waffle Chart**: Grid con puntos circulares (cada uno = 1%)
4. **Minimalist Version**: "8 in 10" human figures

### Day 2: Pictogram
1. **Icon-based comparison**: Cada símbolo = 5% developers
2. **Language-specific icons**:
   - Solidity: ⬡ (Hexagon - Ethereum)
   - Rust: ⚙ (Gear - systems)
   - JavaScript: { } (Curly braces)
   - Move: ➜ (Arrow - Move semantics)
   - Vyper: ◆ (Diamond)
   - Go: ▶ (Play symbol)

### Day 3: Mosaic
1. **Mosaic Plot (Marimekko Chart)**: Two-dimensional proportional visualization
2. **Design elements**:
   - Width: Proportional to total dApps per blockchain
   - Height: Category distribution within each blockchain
   - Color: Monochromatic gradient for categories
   - Vintage aesthetic: Earth tones, warm beige background
3. **Techniques applied**:
   - Custom Rectangle patches
   - Proportional layout calculations
   - Dynamic label positioning
   - Minimalist typography (bold sans-serif + italic serif)

## Git Workflow

### Commits sin mencionar Claude
```bash
git commit -m "Add Day X visualization: [description]

- Feature 1
- Feature 2
- Data source: [source]"
```

### Push a GitHub
```bash
git push origin main
```

## Formato de Exportación

Cada día genera 3 formatos:
1. **PNG**: 300 DPI - web/presentaciones
2. **PDF**: Vector - publicación/impresión
3. **SVG**: Vector - edición posterior

## Best Practices Aplicadas

1. ✅ **Datos referenciales**: Todas las visualizaciones usan fuentes verificables
2. ✅ **Colorblind-safe**: Paletas diseñadas para accesibilidad
3. ✅ **Multiple formats**: PNG, PDF, SVG para diferentes usos
4. ✅ **Clean design**: Inspirado en ejemplos profesionales
5. ✅ **Narrative insights**: Cada visualización cuenta una historia
6. ✅ **Proper attribution**: Fuentes de datos claramente citadas

## Estructura del Proyecto

```
30Days/Edition2026/
├── day01_part_to_whole/
│   ├── data/
│   │   └── llm_usage_2025.csv
│   ├── scripts/
│   │   ├── part_to_whole_viz.py
│   │   └── minimalist_viz.py
│   ├── output/
│   │   ├── day01_part_to_whole_llm_usage.png/pdf/svg
│   │   └── day01_minimalist_llm_usage.png/pdf/svg
│   ├── requirements.txt
│   └── README.md
├── day02_pictogram/
│   ├── data/
│   │   └── programming_languages_2025.csv
│   ├── scripts/
│   │   └── pictogram_viz.py
│   ├── output/
│   │   └── day02_pictogram_programming_languages.png/pdf/svg
│   ├── requirements.txt
│   └── venv/
├── day03_mosaic/
│   ├── data/
│   │   └── dapps_by_blockchain_2025.csv
│   ├── scripts/
│   │   └── mosaic_viz.py
│   ├── output/
│   │   └── day03_mosaic_blockchain_dapps.png/pdf/svg
│   ├── requirements.txt
│   └── venv/
└── SKILLS.md (este archivo)
```

## Comandos Útiles

### Setup Environment
```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### Run Visualization
```bash
./venv/bin/python scripts/[script_name].py
```

### Install Skills
```bash
npx skillfish add microck/ordinary-claude-skills matplotlib
npx skillfish add anthropics/knowledge-work-plugins data-visualization
npx skillfish add microck/ordinary-claude-skills data-viz-plots
```

---

**Proyecto**: #30DayChartChallenge Edition 2026
**Usuario**: carlos-israelj
**Repositorio**: https://github.com/carlos-israelj/Edition2026
