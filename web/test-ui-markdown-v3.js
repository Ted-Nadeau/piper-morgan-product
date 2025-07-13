/**
 * TDD tests for final markdown renderer
 */

// Import the final markdown renderer
const { renderMarkdown } = require('./assets/markdown-renderer-v3.js');

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
console.log('Running final UI markdown rendering tests...');

test('renders basic headers correctly', () => {
    const result = renderMarkdown('# Header 1');
    assertContains(result, '<h1>Header 1</h1>', 'Should render h1');
});

test('renders inline headers correctly', () => {
    const result = renderMarkdown('Text # Header 1 ## Header 2 more text');
    console.log('Inline result:', result);
    assertContains(result, '<h1>Header 1</h1>', 'Should render h1');
    assertContains(result, '<h2>Header 2 more text</h2>', 'Should render h2 with remaining text');
    assertContains(result, 'Text', 'Should preserve other text');
});

test('failing markdown gets processed correctly', () => {
    const rendered = renderMarkdown(failingMarkdown);
    console.log('Failing markdown result:', rendered);

    assertContains(rendered, '<h1>Piper Morgan 1.0 - Data Model Summary</h1>', 'Should render main header');
    assertContains(rendered, '<h2>File Type/Purpose', 'Should render subheader start');
    assertContains(rendered, '<h2>Main Content and Structure', 'Should render another subheader start');
    assertNotContains(rendered, '# Piper Morgan', 'Should not contain raw markdown');
    assertNotContains(rendered, '## File Type', 'Should not contain raw markdown');
});

test('handles mixed content correctly', () => {
    const mixed = 'Start # Header some **bold** text ## Another header end';
    const result = renderMarkdown(mixed);
    console.log('Mixed result:', result);

    assertContains(result, '<h1>Header some <strong>bold</strong> text</h1>', 'Should render h1 with content');
    assertContains(result, '<h2>Another header end</h2>', 'Should render h2 with remaining text');
    assertContains(result, 'Start', 'Should preserve start text');
});

test('handles headers with spaces correctly', () => {
    const result = renderMarkdown('Text # Header 1 ## Another header with spaces text');
    console.log('Spaces result:', result);
    assertContains(result, '<h1>Header 1</h1>', 'Should render h1');
    assertContains(result, '<h2>Another header with spaces text</h2>', 'Should render h2 with remaining text');
});

console.log('Final UI markdown rendering tests completed.');
