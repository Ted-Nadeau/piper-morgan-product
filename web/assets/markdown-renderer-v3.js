/**
 * Simple but effective markdown renderer
 * @param {string} text - The markdown text to render
 * @returns {string} - The rendered HTML
 */
function renderMarkdown(text) {
    if (!text) return '';

    let html = text;

    // Step 1: Handle headers by splitting and processing
    const headerParts = [];
    let currentText = html;

    // Split by headers and process each part
    const headerRegex = /(#{1,3})\s+([^#\n]+?)(?=\s+#{1,3}\s|$)/g;
    let match;
    let lastIndex = 0;

    while ((match = headerRegex.exec(html)) !== null) {
        // Add text before the header
        if (match.index > lastIndex) {
            headerParts.push(html.slice(lastIndex, match.index));
        }

        // Add the header
        const level = match[1].length;
        const headerText = match[2].trim();
        headerParts.push(`<h${level}>${headerText}</h${level}>`);

        lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < html.length) {
        headerParts.push(html.slice(lastIndex));
    }

    html = headerParts.join('');

    // Step 2: Handle other formatting
    html = html
        // Bold
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        // Italic (but not inside strong tags)
        .replace(/(?<!<strong>.*)\*([^*]+?)\*(?!.*<\/strong>)/g, '<em>$1</em>')
        // Code
        .replace(/`(.+?)`/g, '<code>$1</code>');

    // Step 3: Handle lists if we have actual newlines
    if (html.includes('\n')) {
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

        // Step 4: Handle line breaks
        html = html.replace(/\n\n/g, '<br><br>');
        html = html.replace(/\n/g, '<br>');

        // Clean up <br> tags around headers and lists
        html = html.replace(/<br>(<h[1-6]>)/g, '$1');
        html = html.replace(/(<\/h[1-6]>)<br>/g, '$1');
        html = html.replace(/<ul><br>/g, '<ul>');
        html = html.replace(/<br><\/ul>/g, '</ul>');
        html = html.replace(/<\/li><br>/g, '</li>');
    }

    return html;
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { renderMarkdown };
}
