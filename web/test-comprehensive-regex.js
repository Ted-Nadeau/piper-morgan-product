/**
 * Comprehensive test to find the exact regex issue causing markdown problems
 */

console.log("=== COMPREHENSIVE REGEX TESTING ===\n");

// The problematic regex from line 63
const problematicRegex = /^[•\-\*\+]\s*/;

// Test different interpretations of the fix
const fixedRegex1 = /^[•\-*+]\s*/;  // Escape asterisk instead of dash
const fixedRegex2 = /^[•\\\-*+]\s*/; // Escape both dash and asterisk
const fixedRegex3 = /^[•\-\*\+]\s*/; // Original (for comparison)

console.log("Regex patterns:");
console.log("Problematic: /^[•\\-\\*\\+]\\s*/");
console.log("Fixed 1:     /^[•\\-*+]\\s*/");
console.log("Fixed 2:     /^[•\\\\-*+]\\s*/");
console.log("Fixed 3:     /^[•\\-\\*\\+]\\s*/ (original)");
console.log();

// Test more edge cases to find the difference
const testCases = [
    "- Normal dash",
    "* Normal asterisk",
    "+ Normal plus",
    "• Normal bullet",
    "– En dash (8211)",
    "— Em dash (8212)",
    "※ Reference mark (8251)",
    "‣ Triangular bullet (8227)",
    "⁃ Hyphen bullet (8259)",
    "∗ Asterisk operator (8727)",
    "＋ Fullwidth plus (65291)"
];

console.log("COMPREHENSIVE TEST CASES:");
testCases.forEach(testCase => {
    const p = problematicRegex.test(testCase);
    const f1 = fixedRegex1.test(testCase);
    const f2 = fixedRegex2.test(testCase);
    const f3 = fixedRegex3.test(testCase);

    console.log(`"${testCase}"`);
    console.log(`  Problematic: ${p}, Fixed1: ${f1}, Fixed2: ${f2}, Fixed3: ${f3}`);
    console.log(`  Unicode: ${testCase.charCodeAt(0)}`);
    console.log();
});

// Test the actual character range issue
console.log("=== CHARACTER RANGE ANALYSIS ===\n");

// In [•\-\*\+], the \- might not be creating a range as expected
// Let's test what the actual range is
function testCharacterInRange(char, regex) {
    return regex.test(char + ' ');
}

// Test characters around the expected range
const problematicMatches = [];
const fixedMatches = [];

// Test ASCII range first (around \ which is 92)
for (let i = 40; i < 100; i++) {
    const char = String.fromCharCode(i);
    if (testCharacterInRange(char, problematicRegex)) {
        problematicMatches.push(`${char} (${i})`);
    }
    if (testCharacterInRange(char, fixedRegex1)) {
        fixedMatches.push(`${char} (${i})`);
    }
}

console.log("ASCII characters matched by problematic regex:");
console.log(problematicMatches.join(', '));
console.log("\nASCII characters matched by fixed regex:");
console.log(fixedMatches.join(', '));

// Test specific problematic characters that might cause "all italics"
console.log("\n=== ITALIC-CAUSING CHARACTERS ===\n");

const italicCausingChars = [
    '*', // Asterisk - causes italics in markdown
    '_', // Underscore - causes italics in markdown
    '`', // Backtick - causes code formatting
    '~', // Tilde - causes strikethrough
    '\\', // Backslash - escape character
];

italicCausingChars.forEach(char => {
    const testStr = char + ' some text';
    const problematicMatch = problematicRegex.test(testStr);
    const fixedMatch = fixedRegex1.test(testStr);

    console.log(`Character "${char}" (${char.charCodeAt(0)}):`);
    console.log(`  Problematic matches: ${problematicMatch}`);
    console.log(`  Fixed matches: ${fixedMatch}`);
    console.log(`  Could cause markdown issues: ${['*', '_', '`', '~', '\\'].includes(char)}`);
    console.log();
});

// Test the actual markdown processing simulation
function simulateFullProcessing(text) {
    console.log(`Original: "${text}"`);

    // Simulate the problematic regex replacement
    const problematicResult = text.replace(problematicRegex, '');
    console.log(`After problematic regex: "${problematicResult}"`);

    // Simulate the fixed regex replacement
    const fixedResult = text.replace(fixedRegex1, '');
    console.log(`After fixed regex: "${fixedResult}"`);

    console.log();
}

console.log("=== PROCESSING SIMULATION ===\n");

// Test cases that might reveal the issue
const processingTests = [
    "- Normal bullet point",
    "* This might cause italics",
    "_ This underscore might cause issues",
    "` This backtick might cause code formatting",
    "~ This tilde might cause strikethrough"
];

processingTests.forEach(simulateFullProcessing);

// Test the specific case that might be causing the issue
console.log("=== SPECIFIC MARKDOWN BREAKING TEST ===\n");

const markdownBreakingTest = "• This is a bullet point with *emphasis* and **bold** text";
console.log("Testing markdown-breaking case:");
simulateFullProcessing(markdownBreakingTest);
