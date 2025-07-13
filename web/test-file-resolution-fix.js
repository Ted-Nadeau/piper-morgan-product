/**
 * TDD test for the specific failing query
 */

// Test the exact user query that's failing
const failingQuery = "Please summarize that requirements.md file I uploaded recently.";

// Expected temporal patterns that should match
const temporalPatterns = [
    /\b(few days ago|days ago|yesterday|last week|earlier|previously|before)\b/i,
    /\b(uploaded.*ago|uploaded.*earlier|uploaded.*before)\b/i,
    /\b(recently|a few days ago|yesterday|earlier today|this morning|last week)\b/i, // Missing pattern
    /\b(uploaded.*recently|uploaded.*a few days ago)\b/i  // Missing pattern
];

function test(name, fn) {
    try {
        fn();
        console.log(`✅ ${name}`);
    } catch (error) {
        console.error(`❌ ${name}: ${error.message}`);
    }
}

function assertTrue(condition, message) {
    if (!condition) {
        throw new Error(message || 'Expected true but got false');
    }
}

function detectTemporalReference(message) {
    return temporalPatterns.some(pattern => pattern.test(message));
}

// Run tests
console.log('Testing temporal pattern detection for failing query...');

test('original patterns miss "recently"', () => {
    const originalPatterns = [
        /\b(few days ago|days ago|yesterday|last week|earlier|previously|before)\b/i,
        /\b(uploaded.*ago|uploaded.*earlier|uploaded.*before)\b/i
    ];

    const isMatch = originalPatterns.some(pattern => pattern.test(failingQuery));
    assertTrue(!isMatch, 'Original patterns should not match "recently"');
});

test('updated patterns detect "recently"', () => {
    const isMatch = detectTemporalReference(failingQuery);
    assertTrue(isMatch, 'Updated patterns should detect "recently"');
});

test('detects various temporal references', () => {
    const testCases = [
        "Please summarize that requirements.md file I uploaded recently.",
        "Show me the document I uploaded a few days ago",
        "Find the file I uploaded yesterday",
        "The requirements.md file I uploaded last week",
        "That document I uploaded earlier today",
        "The file I uploaded this morning"
    ];

    testCases.forEach(testCase => {
        const isMatch = detectTemporalReference(testCase);
        assertTrue(isMatch, `Should detect temporal reference in: "${testCase}"`);
    });
});

console.log('Temporal pattern detection tests completed.');
