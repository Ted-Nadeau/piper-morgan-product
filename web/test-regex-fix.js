/**
 * Test to demonstrate the regex fix for the markdown formatting issue
 */

// Test the problematic regex vs the fixed regex
console.log("=== TESTING REGEX CHARACTER CLASS ISSUE ===\n");

// The problematic regex from line 63
const problematicRegex = /^[•\-\*\+]\s*/;

// The fixed regex (escape the * instead of the -)
const fixedRegex = /^[•\-*+]\s*/;

// Test strings that should match (normal bullet points)
const normalBullets = [
    "- Normal dash bullet",
    "* Normal asterisk bullet", 
    "+ Normal plus bullet",
    "• Normal Unicode bullet"
];

// Test strings that demonstrate the character range issue
const edgeCases = [
    "– En dash bullet (Unicode 8211)",
    "— Em dash bullet (Unicode 8212)",
    "¡ Inverted exclamation (Unicode 161)",
    "½ Half fraction (Unicode 189)",
    "À A with grave (Unicode 192)",
    "ÿ Y with diaeresis (Unicode 255)"
];

console.log("NORMAL BULLET POINTS:");
normalBullets.forEach(str => {
    const problematicMatch = problematicRegex.test(str);
    const fixedMatch = fixedRegex.test(str);
    console.log(`"${str}"`);
    console.log(`  Problematic: ${problematicMatch}, Fixed: ${fixedMatch}`);
    console.log(`  Should match: ${str.startsWith('-') || str.startsWith('*') || str.startsWith('+') || str.startsWith('•')}`);
    console.log('');
});

console.log("EDGE CASES (should NOT match):");
edgeCases.forEach(str => {
    const problematicMatch = problematicRegex.test(str);
    const fixedMatch = fixedRegex.test(str);
    console.log(`"${str}"`);
    console.log(`  Problematic: ${problematicMatch}, Fixed: ${fixedMatch}`);
    console.log(`  Should match: false`);
    console.log('');
});

// Demonstrate the range issue
console.log("=== CHARACTER RANGE DEMONSTRATION ===\n");

// Show what characters are included in the range [•\-\*\+]
const bulletChar = '•'.charCodeAt(0); // 8226
const backslashChar = '\\'.charCodeAt(0); // 92

console.log(`• character code: ${bulletChar}`);
console.log(`\\ character code: ${backslashChar}`);
console.log(`\\- creates range from ${bulletChar} to ${backslashChar}`);
console.log("This includes many unintended characters!\n");

// Test a few characters in the problematic range
for (let i = 160; i <= 180; i++) {
    const char = String.fromCharCode(i);
    const matches = problematicRegex.test(char + ' text');
    if (matches) {
        console.log(`Character "${char}" (${i}) unexpectedly matches the problematic regex`);
    }
}

// Function to simulate the markdown processing
function simulateMarkdownProcessing(text, useFixedRegex = false) {
    const regex = useFixedRegex ? fixedRegex : problematicRegex;
    const lines = text.split('\n');
    const findings = [];
    
    for (let line of lines) {
        if (line.trim() && line.includes('Key Findings')) {
            continue; // Skip header
        }
        if (line.trim()) {
            // Remove bullet points and add markdown formatting
            const processed = line.replace(regex, '');
            findings.push(`- ${processed}`);
        }
    }
    
    return findings.join('\n');
}

// Test with sample LLM output
const sampleLLMOutput = `## Key Findings
- System performance has improved by 40%
- User satisfaction increased significantly
- À critical bug was found in the payment system
- ½ of users reported mobile issues`;

console.log("\n=== PROCESSING SIMULATION ===\n");
console.log("Original LLM output:");
console.log(sampleLLMOutput);
console.log("\nWith problematic regex:");
console.log(simulateMarkdownProcessing(sampleLLMOutput, false));
console.log("\nWith fixed regex:");
console.log(simulateMarkdownProcessing(sampleLLMOutput, true));

console.log("\n=== CONCLUSION ===");
console.log("The problematic regex [•\\-\\*\\+] creates an unintended character range");
console.log("that matches many characters between Unicode 8226 (•) and 92 (\\).");
console.log("This causes unexpected behavior in markdown processing.");
console.log("The fix is to escape the asterisk instead: [•\\-*+]");