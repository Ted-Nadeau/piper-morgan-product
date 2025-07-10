/**
 * Debug script to trace markdown formatting flow
 * This simulates the exact flow of data through the system
 */

// Simulate the raw LLM output (what we expect from the LLM)
const rawLLMOutput = `This is a comprehensive analysis of the document.

## Document Type
This appears to be a technical specification.

## Key Findings
- The document outlines system requirements
- Security considerations are mentioned
- Performance metrics are defined
- User experience guidelines are provided
- Integration points are specified`;

// Simulate the regex processing from format_key_findings_as_markdown
function simulateKeyFindingsProcessing(text) {
    console.log("=== RAW LLM OUTPUT ===");
    console.log(text);
    console.log("\n=== PROCESSING KEY FINDINGS ===");
    
    // Split by lines like the real code does
    const lines = text.split('\n');
    console.log("Lines after split:", lines);
    
    // Find the key findings section
    let inKeyFindings = false;
    let findings = [];
    
    for (let line of lines) {
        if (line.includes('Key Findings')) {
            inKeyFindings = true;
            console.log("Found Key Findings section");
            continue;
        }
        
        if (inKeyFindings && line.trim()) {
            // This is where the problem regex is applied
            console.log("Original line:", JSON.stringify(line));
            
            // The problematic regex: r'^[•\-\*\+]\s*'
            // In JavaScript, this would be: /^[•\-\*\+]\s*/
            // But the \- creates a range from • to \
            const problematicRegex = /^[•\-\*\+]\s*/;
            const fixedRegex = /^[•\-*+]\s*/;
            
            console.log("Problematic regex match:", line.match(problematicRegex));
            console.log("Fixed regex match:", line.match(fixedRegex));
            
            // Apply the problematic regex like the real code
            const processed = line.replace(problematicRegex, '');
            console.log("After problematic regex:", JSON.stringify(processed));
            
            findings.push(`- ${processed}`);
        }
    }
    
    console.log("\n=== FORMATTED FINDINGS ===");
    console.log(findings.join('\n'));
    
    return findings.join('\n');
}

// Test with the simulated output
const processedText = simulateKeyFindingsProcessing(rawLLMOutput);

console.log("\n=== FINAL RESULT ===");
console.log(processedText);

// Test the character class issue specifically
console.log("\n=== REGEX CHARACTER CLASS TESTING ===");
const testStrings = [
    "- Normal bullet point",
    "* Asterisk bullet point", 
    "+ Plus bullet point",
    "• Unicode bullet point",
    "– En dash bullet point",
    "— Em dash bullet point"
];

const problematicRegex = /^[•\-\*\+]\s*/;
const fixedRegex = /^[•\-*+]\s*/;

testStrings.forEach(str => {
    console.log(`String: "${str}"`);
    console.log(`  Problematic regex matches: ${problematicRegex.test(str)}`);
    console.log(`  Fixed regex matches: ${fixedRegex.test(str)}`);
    console.log(`  Character codes: ${str.split('').map(c => c.charCodeAt(0)).join(', ')}`);
    console.log('---');
});