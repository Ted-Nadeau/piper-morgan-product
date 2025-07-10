/**
 * Improved markdown renderer for inline and multi-line markdown
 * @param {string} text - The markdown text to render
 * @returns {string} - The rendered HTML
 */
function renderMarkdown(text) {
    if (!text) return '';
    
    // Step 1: Split by headers to handle inline markdown properly
    let html = text;
    
    // Replace headers with placeholders to avoid conflicts
    const headerReplacements = [];
    let counter = 0;
    
    // Handle h3 first (most specific)
    html = html.replace(/###\s([^#\n]+?)(?=\s##|\s#|$)/g, (match, content) => {
        const placeholder = `__H3_${counter++}__`;
        headerReplacements.push([placeholder, `<h3>${content.trim()}</h3>`]);
        return placeholder;
    });
    
    // Handle h2
    html = html.replace(/##\s([^#\n]+?)(?=\s##|\s#|$)/g, (match, content) => {
        const placeholder = `__H2_${counter++}__`;
        headerReplacements.push([placeholder, `<h2>${content.trim()}</h2>`]);
        return placeholder;
    });
    
    // Handle h1
    html = html.replace(/#\s([^#\n]+?)(?=\s##|\s#|$)/g, (match, content) => {
        const placeholder = `__H1_${counter++}__`;
        headerReplacements.push([placeholder, `<h1>${content.trim()}</h1>`]);
        return placeholder;
    });
    
    // Step 2: Handle other markdown elements
    html = html
        // Bold
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        // Italic
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        // Code
        .replace(/`(.+?)`/g, '<code>$1</code>');
    
    // Step 3: Handle lists
    const lines = html.split('\n');
    const processedLines = [];
    let inList = false;
    
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        
        // Check if this is a list item
        const listMatch = line.match(/^[\s]*[-*+]\s(.+)$/);
        if (listMatch) {
            if (!inList) {
                processedLines.push('<ul>');
                inList = true;
            }
            processedLines.push(`<li>${listMatch[1]}</li>`);
        } else {
            // Not a list item
            if (inList) {
                processedLines.push('</ul>');
                inList = false;
            }
            processedLines.push(line);
        }
    }
    
    // Close any open list
    if (inList) {
        processedLines.push('</ul>');
    }
    
    html = processedLines.join('\n');
    
    // Step 4: Restore headers
    headerReplacements.forEach(([placeholder, replacement]) => {
        html = html.replace(new RegExp(placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), replacement);
    });
    
    // Step 5: Handle line breaks
    html = html.replace(/\n\n/g, '<br><br>');
    html = html.replace(/\n/g, '<br>');
    
    // Clean up <br> tags around headers and lists
    html = html.replace(/<br>(<h[1-6]>)/g, '$1');
    html = html.replace(/(<\/h[1-6]>)<br>/g, '$1');
    html = html.replace(/<ul><br>/g, '<ul>');
    html = html.replace(/<br><\/ul>/g, '</ul>');
    html = html.replace(/<\/li><br>/g, '</li>');
    
    return html;
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { renderMarkdown };
}