"""
Unit Tests for Token Counter Service

Tests token counting, metrics collection, and baseline reporting functionality.

Issue #306: CONV-MCP-MEASURE
"""

import json
from unittest.mock import AsyncMock

import pytest

from services.integrations.mcp.token_counter import TokenCounter, TokenMetrics


class TestTokenCounter:
    """Test TokenCounter functionality"""

    @pytest.fixture
    def token_counter(self):
        """Create TokenCounter instance for testing"""
        return TokenCounter()

    @pytest.mark.smoke
    def test_estimate_tokens_empty_string(self, token_counter):
        """Test token estimation with empty string"""
        assert token_counter.estimate_tokens("") == 0

    @pytest.mark.smoke
    def test_estimate_tokens_short_text(self, token_counter):
        """Test token estimation with short text"""
        # 4 chars = 1 token
        result = token_counter.estimate_tokens("test")
        assert result == 1

    @pytest.mark.smoke
    def test_estimate_tokens_exact_multiple(self, token_counter):
        """Test token estimation with exact multiple of 4"""
        # 16 chars = 4 tokens
        result = token_counter.estimate_tokens("0123456789abcdef")
        assert result == 4

    @pytest.mark.smoke
    def test_estimate_tokens_partial(self, token_counter):
        """Test token estimation with partial token"""
        # 5 chars = 1 token (uses max() to avoid 0)
        result = token_counter.estimate_tokens("12345")
        assert result == 1

    @pytest.mark.smoke
    def test_estimate_tokens_large_text(self, token_counter):
        """Test token estimation with large text"""
        # 1000 chars = ~250 tokens
        large_text = "a" * 1000
        result = token_counter.estimate_tokens(large_text)
        assert result == 250

    @pytest.mark.smoke
    def test_estimate_tokens_converts_to_string(self, token_counter):
        """Test token estimation converts non-string input to string"""
        result = token_counter.estimate_tokens({"key": "value"})
        assert result > 0

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_wrap_mcp_call_basic(self, token_counter):
        """Test wrapping MCP call with token counting"""

        async def sample_operation():
            return {"result": "success"}

        result = await token_counter.wrap_mcp_call(
            "test_operation",
            sample_operation(),
            input_data="input_data",
        )

        assert result == {"result": "success"}
        assert len(token_counter.metrics) == 1

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_wrap_mcp_call_records_metrics(self, token_counter):
        """Test that wrap_mcp_call records metrics correctly"""

        async def sample_operation():
            return "output_data"

        await token_counter.wrap_mcp_call(
            "test_op",
            sample_operation(),
            input_data="test_input",
        )

        metrics = token_counter.metrics[0]
        assert metrics.operation == "test_op"
        assert metrics.input_tokens > 0
        assert metrics.output_tokens > 0
        assert metrics.total_tokens == metrics.input_tokens + metrics.output_tokens
        assert metrics.execution_time_ms >= 0

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_wrap_mcp_call_exception_handling(self, token_counter):
        """Test exception handling in wrap_mcp_call"""

        async def failing_operation():
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            await token_counter.wrap_mcp_call(
                "failing_op",
                failing_operation(),
                input_data="",
            )

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_wrap_mcp_call_counts_operations(self, token_counter):
        """Test that operation counts are tracked"""

        async def op1():
            return "result1"

        async def op2():
            return "result2"

        await token_counter.wrap_mcp_call("op_a", op1(), input_data="")
        await token_counter.wrap_mcp_call("op_a", op1(), input_data="")
        await token_counter.wrap_mcp_call("op_b", op2(), input_data="")

        assert len(token_counter.metrics) == 3
        assert token_counter._operation_counts["op_a"] == 2
        assert token_counter._operation_counts["op_b"] == 1

    @pytest.mark.smoke
    def test_get_baseline_metrics_empty(self, token_counter):
        """Test baseline metrics with no data"""
        baseline = token_counter.get_baseline_metrics()
        assert baseline["status"] == "no_data"
        assert baseline["total_operations"] == 0
        assert baseline["total_tokens_consumed"] == 0

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_baseline_metrics_populated(self, token_counter):
        """Test baseline metrics with data"""

        async def op1():
            return "a" * 100

        async def op2():
            return "b" * 200

        await token_counter.wrap_mcp_call("list_databases", op1(), input_data="a" * 50)
        await token_counter.wrap_mcp_call("list_databases", op1(), input_data="a" * 50)
        await token_counter.wrap_mcp_call("query_database", op2(), input_data="b" * 75)

        baseline = token_counter.get_baseline_metrics()

        assert baseline["status"] == "complete"
        assert baseline["total_operations"] == 3
        assert baseline["total_tokens_consumed"] > 0
        assert "top_5_operations" in baseline
        assert len(baseline["top_5_operations"]) <= 5
        assert "operation_frequency" in baseline
        assert baseline["operation_frequency"]["list_databases"] == 2
        assert baseline["operation_frequency"]["query_database"] == 1

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_top_5_operations_ranking(self, token_counter):
        """Test that top 5 operations are correctly ranked by tokens"""

        # Create operations with different token costs
        async def expensive_op():
            return "x" * 1000  # ~250 tokens output

        async def cheap_op():
            return "y" * 100  # ~25 tokens output

        # Add expensive operations
        for i in range(3):
            await token_counter.wrap_mcp_call(
                "expensive_op",
                expensive_op(),
                input_data="input" * 50,
            )

        # Add cheap operations
        for i in range(2):
            await token_counter.wrap_mcp_call(
                "cheap_op",
                cheap_op(),
                input_data="input",
            )

        baseline = token_counter.get_baseline_metrics()
        top_5 = baseline["top_5_operations"]

        # Expensive should be ranked first
        assert top_5[0]["operation"] == "expensive_op"
        assert top_5[1]["operation"] == "cheap_op"

    @pytest.mark.smoke
    def test_export_metrics_json(self, token_counter):
        """Test exporting metrics as JSON"""
        token_counter.metrics = [
            TokenMetrics(
                operation="test_op",
                input_tokens=10,
                output_tokens=20,
                total_tokens=30,
                execution_time_ms=5.5,
            ),
        ]

        json_str = token_counter.export_metrics_json()
        data = json.loads(json_str)

        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["operation"] == "test_op"
        assert data[0]["total_tokens"] == 30

    @pytest.mark.smoke
    def test_clear_metrics(self, token_counter):
        """Test clearing metrics"""
        token_counter.metrics = [
            TokenMetrics(
                operation="test",
                input_tokens=1,
                output_tokens=2,
                total_tokens=3,
                execution_time_ms=1.0,
            ),
        ]
        token_counter._operation_counts = {"test": 1}

        token_counter.clear_metrics()

        assert len(token_counter.metrics) == 0
        assert len(token_counter._operation_counts) == 0

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_metrics_summary_output(self, token_counter):
        """Test human-readable metrics summary"""

        async def op():
            return "result" * 50

        await token_counter.wrap_mcp_call("op1", op(), input_data="input")
        await token_counter.wrap_mcp_call("op2", op(), input_data="input")

        summary = token_counter.get_metrics_summary()

        assert "Token Baseline Metrics Report" in summary
        assert "Total Operations: 2" in summary
        assert "Total Tokens Consumed:" in summary
        assert "Top 5 Most Expensive Operations:" in summary

    @pytest.mark.smoke
    def test_token_metrics_to_dict(self):
        """Test TokenMetrics conversion to dict"""
        metrics = TokenMetrics(
            operation="test_op",
            input_tokens=10,
            output_tokens=20,
            total_tokens=30,
            execution_time_ms=5.5,
        )

        result = metrics.to_dict()

        assert result["operation"] == "test_op"
        assert result["input_tokens"] == 10
        assert result["output_tokens"] == 20
        assert result["total_tokens"] == 30
        assert result["execution_time_ms"] == 5.5
        assert "timestamp" in result

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_no_performance_impact(self, token_counter):
        """Test that token counting has minimal performance impact"""
        import time

        async def quick_op():
            await AsyncMock(return_value="result")()
            return "result"

        # Measure overhead
        start = time.perf_counter()
        await token_counter.wrap_mcp_call("perf_test", quick_op(), input_data="")
        overhead_ms = (time.perf_counter() - start) * 1000

        # Overhead should be <10ms (per issue requirement)
        assert overhead_ms < 10, f"Token counting overhead: {overhead_ms:.2f}ms (target <10ms)"
