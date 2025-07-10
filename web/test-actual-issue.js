/**
 * Test to identify the actual issue with "all italics" formatting
 * This simulates what might be happening when the LLM returns text that gets processed
 */

console.log("=== TESTING ACTUAL ITALIC ISSUE ===\n");

// Simulate what might be causing the "all italics" issue
// The issue could be that the regex is not matching properly, leaving asterisks that get interpreted as italics

const problematicRegex = /^[•\-\*\+]\s*/;
const fixedRegex = /^[•\-*+]\s*/;

// Test cases that might cause the issue
const testCases = [
    "• This is a bullet point with *emphasis*",
    "- This is a bullet point with **bold**",
    "* This entire line might become italic",
    "+ This is a plus bullet point",
    "• **Important**: This has bold text",
    "- *Note*: This has italic text",
];

console.log("TESTING REGEX PROCESSING:");
testCases.forEach((testCase, index) => {
    console.log(`\nTest Case ${index + 1}: "${testCase}"`);
    
    // Test with problematic regex
    const problematicMatch = testCase.match(problematicRegex);
    const problematicResult = testCase.replace(problematicRegex, '');
    
    // Test with fixed regex
    const fixedMatch = testCase.match(fixedRegex);
    const fixedResult = testCase.replace(fixedRegex, '');
    
    console.log(`  Problematic match: ${problematicMatch}`);
    console.log(`  Problematic result: "${problematicResult}"`);
    console.log(`  Fixed match: ${fixedMatch}`);
    console.log(`  Fixed result: "${fixedResult}"`);
    
    // Check if result would cause markdown italic formatting
    const hasUnpairedAsterisk = (problematicResult.match(/\*/g) || []).length % 2 === 1;
    console.log(`  Would cause italic formatting: ${hasUnpairedAsterisk}`);
});

// Test the specific issue that might be happening
console.log("\n=== TESTING SPECIFIC ITALIC ISSUE ===\n");

// What if the LLM is returning something like:
const llmOutput = `## Key Findings

* System performance improved by 40%
* User experience enhanced significantly  
* Database queries optimized
* Security vulnerabilities addressed
* Mobile responsiveness improved`;

console.log("Simulated LLM output:");
console.log(llmOutput);

// Process it through the format_key_findings_as_markdown function simulation
function simulateKeyFindingsProcessing(text) {
    const lines = text.split('\n');
    const findings = [];
    
    let inKeyFindings = false;
    
    for (let line of lines) {
        if (line.includes('Key Findings')) {
            inKeyFindings = true;
            continue;
        }
        
        if (inKeyFindings && line.trim()) {
            console.log(`\nProcessing line: "${line}"`);
            
            // Apply the problematic regex
            const problematicProcessed = line.replace(problematicRegex, '');
            console.log(`After problematic regex: "${problematicProcessed}"`);
            
            // Apply the fixed regex
            const fixedProcessed = line.replace(fixedRegex, '');
            console.log(`After fixed regex: "${fixedProcessed}"`);
            
            // Add markdown bullet point
            findings.push(`- ${problematicProcessed}`);
        }
    }
    
    return findings.join('\n');
}

const processedFindings = simulateKeyFindingsProcessing(llmOutput);

console.log("\nFinal processed findings:");
console.log(processedFindings);

// Test what happens when this gets rendered as markdown
console.log("\n=== MARKDOWN RENDERING SIMULATION ===\n");

// Simple markdown italic pattern
const italicRegex = /\*([^*]+)\*/g;
const boldRegex = /\*\*([^*]+)\*\*/g;

function simulateMarkdownRendering(text) {
    console.log(`Input: "${text}"`);
    
    // First apply bold (should be done first)
    let processed = text.replace(boldRegex, '<strong>$1</strong>');
    console.log(`After bold: "${processed}"`);
    
    // Then apply italic
    processed = processed.replace(italicRegex, '<em>$1</em>');
    console.log(`After italic: "${processed}"`);
    
    return processed;
}

const lines = processedFindings.split('\n');
lines.forEach(line => {
    if (line.trim()) {
        console.log('\n---');
        simulateMarkdownRendering(line);
    }
});

// Test the hypothesis about the character range
console.log("\n=== TESTING CHARACTER RANGE HYPOTHESIS ===\n");

const bulletChar = '•';
const backslashChar = '\\';
const asteriskChar = '*';

console.log(`Unicode values:`);
console.log(`• (bullet): ${bulletChar.charCodeAt(0)}`);
console.log(`\\ (backslash): ${backslashChar.charCodeAt(0)}`);
console.log(`* (asterisk): ${asteriskChar.charCodeAt(0)}`);

// Test if the regex actually creates the range issue
const testString = "* This starts with asterisk";
console.log(`\nTesting "${testString}":`);
console.log(`Problematic regex matches: ${problematicRegex.test(testString)}`);
console.log(`Fixed regex matches: ${fixedRegex.test(testString)}`);

// The issue might be that the asterisk at the start of "* This starts with asterisk" 
// is not being removed properly, leaving the entire line to be processed as italic