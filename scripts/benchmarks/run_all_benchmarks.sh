#!/bin/bash
# Run all performance benchmarks

echo "Running all performance benchmarks..."
echo ""

cd "$(dirname "$0")/../.."

# Plugin overhead
echo "1. Plugin Overhead Benchmark"
python3 scripts/benchmarks/benchmark_plugin_overhead.py
echo ""

# Startup time
echo "2. Startup Time Benchmark"
python3 scripts/benchmarks/benchmark_startup.py
echo ""

# Memory profile
echo "3. Memory Profile"
python3 scripts/benchmarks/profile_memory.py
echo ""

# Concurrency
echo "4. Concurrency Benchmark"
python3 scripts/benchmarks/benchmark_concurrency.py
echo ""

echo "All benchmarks complete!"
