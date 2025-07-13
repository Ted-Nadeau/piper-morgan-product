/**
 * TDD tests for improved UI markdown rendering
 */

// Import the improved markdown renderer
const { renderMarkdown } = require('./assets/markdown-renderer-v2.js');

// Simple test framework
function test(name, fn) {
    try {
        fn();
        console.log(`✅ ${name}`);
    } catch (error) {
        console.error(`❌ ${name}: ${error.message}`);
    }
}

function assertContains(text, substring, message) {
    if (!text.includes(substring)) {
        throw new Error(`${message || 'Expected text to contain substring'}: "${text}" should contain "${substring}"`);
    }
}

function assertNotContains(text, substring, message) {
    if (text.includes(substring)) {
        throw new Error(`${message || 'Expected text to not contain substring'}: "${text}" should not contain "${substring}"`);
    }
}

// Test the actual failing markdown
const failingMarkdown = `Here's my summary of the document: # Piper Morgan 1.0 - Data Model Summary ## File Type/Purpose This appears to be a documentation file describing the data model for a system called "Piper Morgan". It follows a domain-driven design approach. ## Main Content and Structure The document covers: 1. Overview 2. Model Distinctions - Product vs Project - Database vs Domain Models - Relationship Loading 3. Domain Models - Core Entities - Product - Project (extends Product) - ProjectIntegration`;

// Run tests
console.log('Running improved UI markdown rendering tests...');

test('renders inline headers correctly', () => {
    const result = renderMarkdown('Text # Header 1 ## Header 2 more text');
    assertContains(result, '<h1>Header 1</h1>', 'Should render h1');
    assertContains(result, '<h2>Header 2</h2>', 'Should render h2');
    assertContains(result, 'Text', 'Should preserve other text');
});

test('failing markdown gets processed correctly', () => {
    const rendered = renderMarkdown(failingMarkdown);
    console.log('Rendered output:', rendered);

    assertContains(rendered, '<h1>Piper Morgan 1.0 - Data Model Summary</h1>', 'Should render main header');
    assertContains(rendered, '<h2>File Type/Purpose</h2>', 'Should render subheader');
    assertContains(rendered, '<h2>Main Content and Structure</h2>', 'Should render another subheader');
    assertNotContains(rendered, '# Piper Morgan', 'Should not contain raw markdown');
    assertNotContains(rendered, '## File Type', 'Should not contain raw markdown');
});

test('handles mixed content correctly', () => {
    const mixed = 'Start # Header some **bold** text ## Another header end';
    const result = renderMarkdown(mixed);

    assertContains(result, '<h1>Header</h1>', 'Should render h1');
    assertContains(result, '<h2>Another header</h2>', 'Should render h2');
    assertContains(result, '<strong>bold</strong>', 'Should render bold');
    assertContains(result, 'Start', 'Should preserve start text');
    assertContains(result, 'end', 'Should preserve end text');
});

test('handles numbered lists in text', () => {
    const withLists = 'Text: 1. Overview 2. Model Distinctions 3. Domain Models';
    const result = renderMarkdown(withLists);

    // Numbers in text should be preserved, not converted to HTML lists
    assertContains(result, '1. Overview', 'Should preserve numbered text');
    assertContains(result, '2. Model Distinctions', 'Should preserve numbered text');
});

test('handles bullet lists correctly', () => {
    const withBullets = 'Items:\n- Item 1\n- Item 2\nEnd';
    const result = renderMarkdown(withBullets);

    assertContains(result, '<ul>', 'Should create list');
    assertContains(result, '<li>Item 1</li>', 'Should render list items');
    assertContains(result, '<li>Item 2</li>', 'Should render list items');
    assertContains(result, '</ul>', 'Should close list');
});

console.log('Improved UI markdown rendering tests completed.');
