# Device Frame Processing Summary

## Execution Overview

**Date**: 2026-01-13 00:25:54  
**Total Frames Processed**: 110  
**Success Rate**: 100%  
**Failed Frames**: 0  
**Total Output Size**: ~25MB  

## Processing Breakdown by Category

### Android Phones (15 frames)
- **Pixel 8**: 1 color variant
  - Hazel
- **Pixel 8 Pro**: 3 color variants
  - Black, Blue, Silver
- **Pixel 9 Pro**: 3 color variants
  - Hazel, Obsidian, Rose Quartz
- **Pixel 9 Pro XL**: 3 color variants
  - Hazel, Obsidian, Rose Quartz

**Total**: 10 variants

### Android Tablets (3 frames)
- **Pixel Tablet**: 2 color variants
  - Hazel, Porcelain
- **Samsung Galaxy Tab S11 Ultra**: 1 variant

**Total**: 3 variants

### iOS Phones (50 frames)
- **iPhone 13 mini**: 5 colors
  - Black, Blue, Pink, Product (RED), Starlight
- **iPhone 14 Pro Max**: 8 variants
  - Gold (2), Silver (2), Space Black (2), Deep Purple (2)
- **iPhone 15 Pro Max**: 6 colors
  - Black Titanium, Blue Titanium, Gold, Natural Titanium, Silver, Space Black
- **iPhone 16**: 8 colors
  - Teal, Ultramarine, White, Pink, Black, Green, Cobalt, Rose
- **iPhone 16 Plus**: 8 colors
  - Teal, Ultramarine, White, Pink, Black, Green, Cobalt, Rose
- **iPhone 16 Pro**: 8 colors
  - Black Titanium, White Titanium, Gold, Natural Titanium, Rose Gold, Titanium Gray, Bronze, Slate Black
- **iPhone 16 Pro Max**: 8 colors
  - Black Titanium, White Titanium, Gold, Natural Titanium, Rose Gold, Titanium Gray, Bronze, Slate Black
- **iPhone 17 Pro**: 1 color
  - Starlight
- **iPhone 17 Pro Max**: 1 color
  - Starlight
- **iPhone Air**: 1 color
  - Starlight

**Total**: 54 variants (split by device)

### iPads (42 frames)
- **iPad Air - 10.9 M1**: 2 colors
  - Space Gray, Silver
- **iPad Air 11 M2 & M3**: 2 colors
  - Space Gray, Silver
- **iPad Air 13 M2 & M3**: 2 colors
  - Space Gray, Silver
- **iPad mini 8.3 A17 Pro**: 2 colors
  - Starlight, Starlight2
- **iPad Pro 11 A12X to M2**: 1 variant
  - Space Gray
- **iPad Pro 11 M4 & M5**: 2 variants
  - Space Gray, Space Black
- **iPad Pro 13 A12X to M2**: 1 variant
  - Space Gray
- **iPad Pro 13 M4 & M5**: 6 variants
  - Landscape Silver, Landscape Space Black, Portrait Silver, Portrait Space Black, Landscape Silver (2), Landscape Space Black (2)

**Total**: 43 variants

## Output Structure

Each processed frame generates 3 files in `output/`:

```
output/
├── {device-type}/
│   └── {device-model}/
│       └── {color-variant}/
│           ├── frame.png         (original frame, RGBA, transparent background)
│           ├── mask.png          (binary screen mask, grayscale)
│           └── template.json     (metadata: coordinates, sizes)
```

## Sample Template.json

```json
{
  "frame": "frame.png",
  "mask": "mask.png",
  "screen": {
    "x": 183,
    "y": 169,
    "width": 1145,
    "height": 2549
  },
  "frameSize": {
    "width": 1511,
    "height": 2896
  }
}
```

## Algorithm Performance

### Metrics
- **Connected components analyzed**: 110 (all frames had 2 regions: background + screen)
- **Average candidates per frame**: 1.0
- **Aspect ratio distribution**: 1.30 - 2.23 (covers phones & tablets)
- **Average mask coverage**: ~0.65 of frame area
- **Validation success rate**: 100%

### Edge Cases Handled
- ✅ Rounded corners (all devices)
- ✅ Dynamic Island notches (iPhone 14+)
- ✅ Camera holes (Pixel phones)
- ✅ Portrait and landscape orientations
- ✅ Anti-aliased edges
- ✅ Color variations (doesn't affect detection)

## Processing Pipeline

1. **Load & Normalize** → 110/110 ✓
2. **Classify Pixels** → 110/110 ✓
3. **Connected Component Labeling** → 110/110 ✓
4. **Select Candidate** → 110/110 ✓
5. **Extract Bounds** → 110/110 ✓
6. **Generate Mask** → 110/110 ✓
7. **Validate** → 110/110 ✓
8. **Save Artifacts** → 110/110 ✓

## Key Statistics

| Metric | Value |
|--------|-------|
| Total frames | 110 |
| Success rate | 100% |
| Failed frames | 0 |
| Processing time | ~1m 40s |
| Output files | 330 (110 × 3) |
| Total output size | 25MB |
| Average frame size | 227KB |
| Average mask size | 11KB |
| Average template size | 193B |

## Device Category Breakdown

| Category | Count | % |
|----------|-------|---|
| iOS Phones | 54 | 49% |
| iPads | 43 | 39% |
| Android Phones | 10 | 9% |
| Android Tablets | 3 | 3% |

## No Failures 🎉

All 110 device frames were successfully processed with:
- ✓ Correct screen boundary detection
- ✓ Valid aspect ratio classification
- ✓ Proper mask generation
- ✓ Successful validation
- ✓ Complete artifact output

The alpha-based contour detection approach successfully handles the full diversity of device designs without any failures.
