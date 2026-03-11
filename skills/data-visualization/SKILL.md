---
name: data-visualization
description: "Use this skill whenever the user asks to create charts, graphs, plots, dashboards, or any data visualization. This includes: pie charts, bar charts, line charts, scatter plots, heatmaps, treemaps, sunburst charts, histograms, box plots, funnel charts, gauges, geographic maps, candlestick charts, radar charts, sankey diagrams, and any other visual representation of data. Also activate when the user asks to 'visualize', 'plot', 'graph', 'chart', or 'show me a chart of' any data — whether from CSV, Excel, JSON, database results, or inline data in the conversation."
version: 1.0.0
author: ChatableX
category: data
dependencies:
  python:
    - plotly>=5.18
    - pandas>=2.0
    - numpy>=1.24
    - openpyxl
---

# Data Visualization Skill

## Quick Reference

| Task | Approach |
|------|----------|
| Simple chart (pie, bar, line) | `plotly.express` one-liner |
| Complex / multi-trace chart | `plotly.graph_objects` |
| Data from file (CSV/Excel) | `pd.read_csv()` / `pd.read_excel()` → Plotly |
| Data from conversation | Build DataFrame inline → Plotly |
| Dashboard (multiple charts) | Multiple `fig` → combined HTML |

---

## CRITICAL RULES

1. **ALWAYS output HTML** — use `fig.write_html(path)`, NEVER `fig.write_image()` or `fig.savefig()`
2. **NEVER use matplotlib** — always use Plotly (`plotly.express` or `plotly.graph_objects`)
3. **ALWAYS print() the output file path** — this is how the file appears in the chat UI
4. **Use `write_file` + `execute_shell`** workflow — write Python script, then run with `python3`
5. **Chinese labels** — use Chinese for chart titles, axis labels, and legends when user speaks Chinese

---

## Why HTML, not PNG?

- HTML charts are **interactive** — users can hover, zoom, pan, click legends
- No dependency on `kaleido` or system graphics libraries (avoids `ImportError`)
- Flutter client renders `.html` files in an inline WebView automatically
- File size is small and self-contained

---

## Standard Workflow

```
write_file('chart.py', code)  →  execute_shell('python3 chart.py')
```

The script must:
1. Define output dir: `OUTPUT_DIR = '{{output_dir}}'` (auto-injected, do NOT change)
2. Process data (read file or build DataFrame)
3. Create Plotly figure
4. Write to HTML: `fig.write_html(os.path.join(OUTPUT_DIR, 'name.html'))`
5. Print the **absolute path**: `print(output_path)`

---

## Code Templates

### Pie Chart

```python
import os, plotly.express as px, pandas as pd

OUTPUT_DIR = '{{output_dir}}'

data = {'category': ['A类', 'B类', 'C类'], 'value': [30, 50, 20]}
df = pd.DataFrame(data)

fig = px.pie(df, values='value', names='category', title='分类占比',
             color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_traces(textposition='inside', textinfo='percent+label')

output = os.path.join(OUTPUT_DIR, '分类占比.html')
fig.write_html(output)
print(output)
```

### Bar Chart

```python
import os, plotly.express as px, pandas as pd

OUTPUT_DIR = '{{output_dir}}'

df = pd.DataFrame({'month': ['1月','2月','3月'], 'sales': [120, 180, 150]})

fig = px.bar(df, x='month', y='sales', title='月度销售额',
             color='sales', color_continuous_scale='Blues')
fig.update_layout(xaxis_title='月份', yaxis_title='销售额')

output = os.path.join(OUTPUT_DIR, '月度销售额.html')
fig.write_html(output)
print(output)
```

### Line Chart (Time Series)

```python
import os, plotly.express as px, pandas as pd

OUTPUT_DIR = '{{output_dir}}'

df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=12, freq='M'),
    'revenue': [100, 120, 115, 130, 145, 160, 155, 170, 180, 190, 200, 210]
})

fig = px.line(df, x='date', y='revenue', title='月度营收趋势',
              markers=True)
fig.update_layout(xaxis_title='日期', yaxis_title='营收')

output = os.path.join(OUTPUT_DIR, '月度营收趋势.html')
fig.write_html(output)
print(output)
```

### Grouped Bar Chart

```python
import os, plotly.express as px, pandas as pd

OUTPUT_DIR = '{{output_dir}}'

df = pd.DataFrame({
    'quarter': ['Q1','Q1','Q2','Q2','Q3','Q3','Q4','Q4'],
    'product': ['A','B','A','B','A','B','A','B'],
    'sales': [100, 80, 120, 90, 110, 95, 130, 100]
})

fig = px.bar(df, x='quarter', y='sales', color='product', barmode='group',
             title='季度产品销售对比')

output = os.path.join(OUTPUT_DIR, '季度产品销售对比.html')
fig.write_html(output)
print(output)
```

### Scatter Plot

```python
import os, plotly.express as px, pandas as pd

OUTPUT_DIR = '{{output_dir}}'

fig = px.scatter(df, x='price', y='quantity', color='category',
                 size='revenue', hover_data=['name'],
                 title='价格-销量分布')

output = os.path.join(OUTPUT_DIR, '价格销量分布.html')
fig.write_html(output)
print(output)
```

### Heatmap

```python
import os, plotly.express as px, pandas as pd, numpy as np

OUTPUT_DIR = '{{output_dir}}'

matrix = pd.DataFrame(np.random.rand(5, 5),
                      columns=['Mon','Tue','Wed','Thu','Fri'],
                      index=['9am','10am','11am','12pm','1pm'])

fig = px.imshow(matrix, text_auto='.2f', title='热力图',
                color_continuous_scale='RdYlGn')

output = os.path.join(OUTPUT_DIR, '热力图.html')
fig.write_html(output)
print(output)
```

### Treemap

```python
import os, plotly.express as px

OUTPUT_DIR = '{{output_dir}}'

fig = px.treemap(df, path=['category', 'subcategory'], values='amount',
                 title='分类结构', color='amount',
                 color_continuous_scale='Blues')

output = os.path.join(OUTPUT_DIR, '分类结构.html')
fig.write_html(output)
print(output)
```

### Multi-chart Dashboard

```python
import os, plotly.graph_objects as go
from plotly.subplots import make_subplots

OUTPUT_DIR = '{{output_dir}}'

fig = make_subplots(rows=1, cols=2,
                    subplot_titles=('销售额', '利润率'))

fig.add_trace(go.Bar(x=months, y=sales, name='销售额'), row=1, col=1)
fig.add_trace(go.Scatter(x=months, y=profit_rate, name='利润率',
                         mode='lines+markers'), row=1, col=2)

fig.update_layout(title_text='业务概览', showlegend=True)

output = os.path.join(OUTPUT_DIR, '业务概览.html')
fig.write_html(output)
print(output)
```

---

## Reading Data from Files

```python
import pandas as pd

# CSV
df = pd.read_csv('/path/to/data.csv')

# Excel
df = pd.read_excel('/path/to/data.xlsx', sheet_name='Sheet1')

# JSON
df = pd.read_json('/path/to/data.json')

# Preview data before charting
print(df.head())
print(df.columns.tolist())
print(df.dtypes)
```

When working with user-provided files:
- Always check column names first with `df.columns.tolist()`
- Handle encoding: `pd.read_csv(path, encoding='utf-8')` or `encoding='gbk'` for Chinese files
- Handle missing values: `df.dropna()` or `df.fillna(0)` as appropriate

---

## Styling Best Practices

### Color Palettes

Use Plotly's built-in palettes for consistency:

| Palette | Best for |
|---------|----------|
| `px.colors.qualitative.Set2` | Categorical data (pie, bar) |
| `px.colors.qualitative.Plotly` | Default, good contrast |
| `px.colors.sequential.Blues` | Sequential data (heatmaps) |
| `px.colors.diverging.RdYlGn` | Diverging data (positive/negative) |
| `px.colors.sequential.Viridis` | Scientific data |

### Layout Tuning

```python
fig.update_layout(
    title=dict(text='标题', font=dict(size=20)),
    font=dict(family='Microsoft YaHei, SimHei, sans-serif', size=14),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(orientation='h', yanchor='bottom', y=1.02),
    margin=dict(l=60, r=30, t=80, b=60),
)
```

### Avoid

- **Don't use write_image()** — it requires kaleido, which often fails to install
- **Don't use matplotlib** — it produces static images and requires GUI backends
- **Don't create overly complex charts** — if data has 50+ categories, consider top-N or grouping
- **Don't skip axis labels** — always label axes with meaningful Chinese names
- **Don't use default gray background** — set `plot_bgcolor='white'` for clean look

---

## Output Path (CRITICAL — Must follow exactly!)

The chat UI **only** displays files that are detected and registered by the backend.
Detection chain: `print(absolute_path)` → shell_tool scans stdout → FileManager registers → client renders inline.

**`{{output_dir}}` is auto-injected** by the system, pointing to:
`~/.ChatableX/workspace/outputs/data-visualization/`

The directory is pre-created, no need for `os.makedirs()`.

**Three iron rules:**
1. Use `OUTPUT_DIR = '{{output_dir}}'` — do NOT hardcode paths
2. `print()` the **absolute path** as the **only content on its own line**
3. File extension must be `.html`

**Standard pattern (all templates above follow this):**

```python
import os

OUTPUT_DIR = '{{output_dir}}'
output = os.path.join(OUTPUT_DIR, '订单金额分布.html')
fig.write_html(output)
print(output)  # ← MUST be alone on its own line
```

**Why this matters:**
- `execute_shell` scans stdout for file paths matching known extensions (`.html` is included)
- Matched paths are registered with FileManager → assigned a `file_id`
- Client receives `file_id` → detects `.html` → renders **inline interactive chart** via WebView
- If `print()` is missing or path is relative → file won't be detected → won't appear in chat

**DON'T do this:**
```python
# ❌ Relative path — won't be detected
fig.write_html('chart.html')

# ❌ Path mixed with other text — regex can't extract it
print(f"Chart saved to {output}, done!")

# ❌ No print at all — file is invisible to the chat UI
fig.write_html(output)

# ❌ Hardcoded path — wrong convention
OUTPUT_DIR = os.path.expanduser('~/.ChatableX/workspace/outputs')
```

**DO this:**
```python
# ✅ Use injected output_dir, print absolute path alone
OUTPUT_DIR = '{{output_dir}}'
output = os.path.join(OUTPUT_DIR, 'chart.html')
fig.write_html(output)
print(output)
```

If the user explicitly specifies a path (e.g., "保存到桌面"), respect their request:
```python
output = os.path.expanduser('~/Desktop/chart.html')
fig.write_html(output)
print(output)
```
