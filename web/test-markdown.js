/**
 * Unit tests for markdown renderer
 */

const { renderMarkdown } = require('./assets/markdown-renderer.js');

// Test framework
function test(name, fn) {
    try {
        fn();
        console.log(`✅ ${name}`);
    } catch (error) {
        console.error(`❌ ${name}: ${error.message}`);
    }
}

function assertEqual(actual, expected, message) {
    if (actual !== expected) {
        throw new Error(`${message || 'Assertion failed'}: expected "${expected}", got "${actual}"`);
    }
}

// Tests
test('renders headers correctly', () => {
    assertEqual(renderMarkdown('# Header 1'), '<h1>Header 1</h1>');
    assertEqual(renderMarkdown('## Header 2'), '<h2>Header 2</h2>');
    assertEqual(renderMarkdown('### Header 3'), '<h3>Header 3</h3>');
});

test('renders bold text correctly', () => {
    assertEqual(renderMarkdown('**bold**'), '<strong>bold</strong>');
    assertEqual(renderMarkdown('This is **bold** text'), 'This is <strong>bold</strong> text');
});

test('renders italic text correctly', () => {
    assertEqual(renderMarkdown('*italic*'), '<em>italic</em>');
    assertEqual(renderMarkdown('This is *italic* text'), 'This is <em>italic</em> text');
});

test('renders code correctly', () => {
    assertEqual(renderMarkdown('`code`'), '<code>code</code>');
    assertEqual(renderMarkdown('This is `code` text'), 'This is <code>code</code> text');
});

test('renders bullet lists correctly', () => {
    const input = '- Item 1\n- Item 2';
    const expected = '<ul><li>Item 1</li><li>Item 2</li></ul>';
    assertEqual(renderMarkdown(input), expected);
});

test('handles line breaks correctly', () => {
    assertEqual(renderMarkdown('Line 1\nLine 2'), 'Line 1<br>Line 2');
    assertEqual(renderMarkdown('Para 1\n\nPara 2'), 'Para 1<br><br>Para 2');
});

test('handles complex markdown', () => {
    const input = `# Summary

## Key Points
- **Important**: This is bold
- *Emphasis*: This is italic
- Code: \`example\`

### Details
Normal text here.`;

    const result = renderMarkdown(input);
    console.log('Complex markdown result:', result);

    // Should contain all elements
    if (!result.includes('<h1>Summary</h1>')) throw new Error('Missing h1');
    if (!result.includes('<h2>Key Points</h2>')) throw new Error('Missing h2');
    if (!result.includes('<strong>Important</strong>')) throw new Error('Missing bold');
    if (!result.includes('<em>Emphasis</em>')) throw new Error('Missing italic');
    if (!result.includes('<code>example</code>')) throw new Error('Missing code');
});

test('handles empty input', () => {
    assertEqual(renderMarkdown(''), '');
    assertEqual(renderMarkdown(null), '');
    assertEqual(renderMarkdown(undefined), '');
});

console.log('Running markdown renderer tests...');
