/**
 * TDD tests for UI markdown rendering
 * Testing that bot messages render markdown as HTML
 */

// Import our markdown renderer
const fs = require('fs');
const path = require('path');

// Read the markdown renderer
const rendererPath = path.join(__dirname, 'assets', 'markdown-renderer.js');
const rendererCode = fs.readFileSync(rendererPath, 'utf8');

// Execute the renderer code to get the function
eval(rendererCode);

// Simple test framework
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

function assertTrue(condition, message) {
    if (!condition) {
        throw new Error(message || 'Expected true but got false');
    }
}

function assertContains(text, substring, message) {
    if (!text.includes(substring)) {
        throw new Error(`${message || 'Expected text to contain substring'}: "${text}" should contain "${substring}"`);
    }
}

// Mock DOM elements for testing
function createMockElement(className) {
    return {
        className: className,
        innerHTML: '',
        textContent: '',
        classList: {
            add: function(cls) { this.className += ' ' + cls; },
            remove: function(cls) { this.className = this.className.replace(cls, '').trim(); }
        }
    };
}

// Simulate the appendMessage function from the UI
function appendMessage(html, isUser = false) {
    const msgDiv = createMockElement(`message ${isUser ? 'user-message' : 'bot-message'}`);

    // This is the key logic from the UI
    if (isUser) {
        msgDiv.textContent = html;
    } else {
        msgDiv.innerHTML = html; // Bot messages should use innerHTML for markdown
    }

    return msgDiv;
}

// Test the actual markdown content that's failing
const failingMarkdown = `Here's my summary of the document: # Piper Morgan 1.0 - Data Model Summary ## File Type/Purpose This appears to be a documentation file describing the data model for a system called "Piper Morgan". It follows a domain-driven design approach. ## Main Content and Structure The document covers: 1. Overview 2. Model Distinctions - Product vs Project - Database vs Domain Models - Relationship Loading 3. Domain Models - Core Entities - Product - Project (extends Product) - ProjectIntegration`;

// Run tests
console.log('Running UI markdown rendering tests...');

test('markdown renderer processes headers correctly', () => {
    const result = renderMarkdown('# Header 1\n## Header 2');
    assertContains(result, '<h1>Header 1</h1>', 'Should render h1');
    assertContains(result, '<h2>Header 2</h2>', 'Should render h2');
});

test('markdown renderer processes lists correctly', () => {
    const result = renderMarkdown('- Item 1\n- Item 2');
    assertContains(result, '<ul>', 'Should have ul tag');
    assertContains(result, '<li>Item 1</li>', 'Should render li items');
});

test('bot message uses innerHTML for markdown', () => {
    const botMessage = appendMessage('# Test Header', false);
    assertEqual(botMessage.innerHTML, '# Test Header', 'Bot message should use innerHTML');
    assertEqual(botMessage.textContent, '', 'Bot message textContent should be empty');
});

test('user message uses textContent for safety', () => {
    const userMessage = appendMessage('# Test Header', true);
    assertEqual(userMessage.textContent, '# Test Header', 'User message should use textContent');
    assertEqual(userMessage.innerHTML, '', 'User message innerHTML should be empty');
});

test('failing markdown gets processed correctly', () => {
    const rendered = renderMarkdown(failingMarkdown);

    assertContains(rendered, '<h1>Piper Morgan 1.0 - Data Model Summary</h1>', 'Should render main header');
    assertContains(rendered, '<h2>File Type/Purpose</h2>', 'Should render subheader');
    assertContains(rendered, '<h2>Main Content and Structure</h2>', 'Should render another subheader');
    assertContains(rendered, '<ul>', 'Should have lists');
    assertContains(rendered, '<li>Overview</li>', 'Should render list items');
});

test('bot message with failing markdown renders as HTML', () => {
    const botMessage = appendMessage(renderMarkdown(failingMarkdown), false);

    assertContains(botMessage.innerHTML, '<h1>', 'Bot message should contain HTML headers');
    assertContains(botMessage.innerHTML, '<h2>', 'Bot message should contain HTML subheaders');
    assertContains(botMessage.innerHTML, '<ul>', 'Bot message should contain HTML lists');
});

test('workflow simulation - API returns markdown, UI renders HTML', () => {
    // Simulate the API response
    const apiResponse = {
        message: failingMarkdown
    };

    // Simulate the UI processing (from the chat form handler)
    const processedHTML = renderMarkdown(apiResponse.message);
    const botMessage = appendMessage(processedHTML, false);

    // The bot message should contain rendered HTML, not raw markdown
    assertContains(botMessage.innerHTML, '<h1>Piper Morgan 1.0 - Data Model Summary</h1>', 'Should render as HTML');
    assertTrue(!botMessage.innerHTML.includes('# Piper Morgan'), 'Should not contain raw markdown');
});

console.log('UI markdown rendering tests completed.');
