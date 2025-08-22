# SewingPattern Figure Control Guide for Jupyter Notebooks

## Problem
When you run `sewing_pattern.draw(show=True)` or `sewing_pattern.draw(show=False)`, the figure always shows up, and you don't know how to save it to a file.

## Solution

### 1. Draw without showing (Recommended)

```python
# Instead of this (which always shows the figure):
data = sewing_pattern.draw(show=True)

# Use this (no figure will appear):
fig, axs = sewing_pattern.draw(show=False)

# Now you can save it:
fig.savefig('my_pattern.png', dpi=300, bbox_inches='tight')
```

### 2. Use the new save_figure method

```python
# Simple one-liner to save:
sewing_pattern.save_figure('my_pattern.png', dpi=300)
```

### 3. Control when to show the figure

```python
# Draw without showing
fig, axs = sewing_pattern.draw(show=False)

# Save it
fig.savefig('my_pattern.png', dpi=300, bbox_inches='tight')

# Show it later if you want
plt.show()
```

## Your Notebook Code - Before and After

### Before (problematic):
```python
GARMENT_IDX = 0
garment_id = scene.garment_id_list[GARMENT_IDX]
sewing_pattern = scene.sewing_pattern_dict[garment_id]
data = sewing_pattern.draw(show=True)  # Always shows figure
```

### After (better):
```python
GARMENT_IDX = 0
garment_id = scene.garment_id_list[GARMENT_IDX]
sewing_pattern = scene.sewing_pattern_dict[garment_id]

# Option 1: Draw and save
fig, axs = sewing_pattern.draw(show=False)
fig.savefig(f'pattern_{garment_id}.png', dpi=300, bbox_inches='tight')

# Option 2: Use save_figure method
sewing_pattern.save_figure(f'pattern_{garment_id}.png', dpi=300)

# Option 3: Show only when you want
fig, axs = sewing_pattern.draw(show=False)
# ... do other things ...
plt.show()  # Show when ready
```

## Common Use Cases

### Save multiple patterns:
```python
for garment_id, sewing_pattern in scene.sewing_pattern_dict.items():
    sewing_pattern.save_figure(f'pattern_{garment_id}.png', dpi=300)
```

### Create a custom layout:
```python
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Draw pattern on first subplot
sewing_pattern.draw_on_axes(axs[0, 0])
axs[0, 0].set_title("Sewing Pattern")

# Add other content
axs[0, 1].plot([1, 2, 3, 4], [1, 4, 2, 3])

# Save the whole layout
fig.savefig('custom_layout.png', dpi=300, bbox_inches='tight')
```

### Save in different formats:
```python
formats = ['png', 'pdf', 'svg']
for fmt in formats:
    sewing_pattern.save_figure(f'pattern.{fmt}', dpi=300)
```

## Key Points

1. **Use `show=False`** to prevent automatic figure display
2. **Use `save_figure()`** for easy saving
3. **Use `plt.show()`** only when you want to display
4. **Use `block=False`** if you want to show without blocking execution

## Jupyter Notebook Tips

- Use `%matplotlib inline` for inline plots
- Use `%matplotlib notebook` for interactive plots
- Use `%matplotlib widget` for advanced interactivity

## Troubleshooting

**Q: The figure still shows up even with `show=False`**
A: This might be due to Jupyter's automatic display. Try:
```python
plt.ioff()  # Turn off interactive mode
fig, axs = sewing_pattern.draw(show=False)
fig.savefig('pattern.png')
plt.ion()   # Turn interactive mode back on
```

**Q: I want to show the figure in the notebook but also save it**
A: Use this pattern:
```python
fig, axs = sewing_pattern.draw(show=False)
fig.savefig('pattern.png', dpi=300, bbox_inches='tight')
plt.show()  # This will display in the notebook
```


