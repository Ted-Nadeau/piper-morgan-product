python scripts/pattern_sweep_enhanced.py \
  --start 2025-11-26 \
  --end 2025-11-30 \
  --verbose \
  --format json \
  --output late-nov-pattern-sweep.json

# Also generate text report
python scripts/pattern_sweep_enhanced.py \
  --start 2025-11-26 \
  --end 2025-11-30 \
  --format text \
  --output late-nov-pattern-sweep.txt
