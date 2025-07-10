/**
 * TDD tests for cross-session file resolution
 * Testing the pattern matching for "recently uploaded" queries
 */

// Mock file data
const mockFiles = [
    {
        id: 'file1',
        filename: 'requirements.md',
        created_at: new Date('2025-07-07T10:00:00Z'), // 2 days ago
        session_id: 'old_session'
    },
    {
        id: 'file2', 
        filename: 'spec.md',
        created_at: new Date('2025-07-09T09:00:00Z'), // today
        session_id: 'current_session'
    },
    {
        id: 'file3',
        filename: 'old_requirements.md', 
        created_at: new Date('2025-06-01T10:00:00Z'), // over a month ago
        session_id: 'very_old_session'
    }
];

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

// File resolution logic to test
function detectTemporalReference(message) {
    const temporalPatterns = [
        /\b(recently|a few days ago|yesterday|earlier today|this morning|last week)\b/i,
        /\b(that .+ I uploaded|the .+ I uploaded|file I uploaded)\b/i,
        /\b(uploaded .+ ago|uploaded .+ recently)\b/i
    ];
    
    return temporalPatterns.some(pattern => pattern.test(message));
}

function extractFileReference(message) {
    const filePatterns = [
        /\b(requirements\.md|spec\.md|\.md|\.txt|\.pdf)\b/i,
        /\b(the .+ file|that .+ file|my .+ file)\b/i
    ];
    
    const matches = [];
    filePatterns.forEach(pattern => {
        const match = message.match(pattern);
        if (match) {
            matches.push(match[0]);
        }
    });
    
    return matches;
}

function searchFilesByPattern(query, files, maxDays = 7) {
    const isTemporal = detectTemporalReference(query);
    const fileRefs = extractFileReference(query);
    
    if (!isTemporal && fileRefs.length === 0) {
        return [];
    }
    
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - maxDays);
    
    return files.filter(file => {
        // Check if file is within time range for temporal queries
        if (isTemporal && file.created_at < cutoffDate) {
            return false;
        }
        
        // Check if filename matches any extracted references
        if (fileRefs.length > 0) {
            return fileRefs.some(ref => 
                file.filename.toLowerCase().includes(ref.toLowerCase()) ||
                ref.toLowerCase().includes(file.filename.toLowerCase())
            );
        }
        
        return true;
    });
}

// Run tests
console.log('Running file resolution tests...');

test('detects temporal references', () => {
    assertTrue(detectTemporalReference('Please summarize that requirements.md file I uploaded recently'));
    assertTrue(detectTemporalReference('The file I uploaded a few days ago'));
    assertTrue(detectTemporalReference('That document I uploaded yesterday'));
    assertTrue(!detectTemporalReference('Please summarize requirements.md'));
});

test('extracts file references', () => {
    const refs1 = extractFileReference('Please summarize that requirements.md file I uploaded recently');
    assertTrue(refs1.includes('requirements.md'), 'Should find requirements.md');
    
    const refs2 = extractFileReference('The spec file I uploaded');
    assertTrue(refs2.length > 0, 'Should find file reference');
    
    const refs3 = extractFileReference('Hello world');
    assertEqual(refs3.length, 0, 'Should find no file references');
});

test('finds recently uploaded files', () => {
    const query = 'Please summarize that requirements.md file I uploaded recently';
    const results = searchFilesByPattern(query, mockFiles);
    
    assertTrue(results.length > 0, 'Should find files');
    assertTrue(results.some(f => f.filename === 'requirements.md'), 'Should find requirements.md');
    assertTrue(!results.some(f => f.filename === 'old_requirements.md'), 'Should not find old files');
});

test('finds files without temporal reference', () => {
    const query = 'Please summarize requirements.md';
    const results = searchFilesByPattern(query, mockFiles);
    
    assertTrue(results.some(f => f.filename === 'requirements.md'), 'Should find requirements.md');
});

test('handles no matches', () => {
    const query = 'Hello world';
    const results = searchFilesByPattern(query, mockFiles);
    
    assertEqual(results.length, 0, 'Should find no files');
});

test('respects time cutoff', () => {
    const query = 'Please summarize that file I uploaded recently';
    const results = searchFilesByPattern(query, mockFiles, 1); // Only 1 day back
    
    assertTrue(results.every(f => f.created_at >= new Date('2025-07-08T00:00:00Z')), 'Should only find recent files');
});

console.log('File resolution tests completed.');