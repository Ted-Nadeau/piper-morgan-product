"""
Piper Morgan Web Interface
Simple FastAPI app for interacting with the main Piper Morgan Platform API
"""
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Configuration - CORRECT PORT
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")

# Create FastAPI app
app = FastAPI(title='Piper Morgan UI', description='Web Interface for the Piper Morgan Platform')

# Mount static files
app.mount("/assets", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "assets")), name="assets")

@app.get('/debug-markdown', response_class=HTMLResponse)
async def debug_markdown(request: Request):
    return HTMLResponse(content='''<!DOCTYPE html>
<html>
<head>
    <title>Markdown Debug Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .test-section { border: 1px solid #ccc; margin: 10px 0; padding: 10px; }
        .raw { background: #f0f0f0; padding: 10px; margin: 5px 0; }
        .rendered { background: #e8f4f8; padding: 10px; margin: 5px 0; }
        h1 { color: #2c3e50; border-bottom: 1px solid #ecf0f1; }
        h2 { color: #34495e; }
        strong { color: #2c3e50; }
    </style>
</head>
<body>
    <h1>Markdown Renderer Debug Test</h1>
    
    <div class="test-section">
        <h3>Test 1: Check if renderMarkdown function exists</h3>
        <div class="rendered" id="test1"></div>
    </div>
    
    <div class="test-section">
        <h3>Test 2: Simple Header</h3>
        <div class="raw">Input: "# Header 1"</div>
        <div class="rendered" id="test2"></div>
    </div>
    
    <div class="test-section">
        <h3>Test 3: Your Failing Example</h3>
        <div class="raw">Input: "Here's my summary... # Header ## Subheader"</div>
        <div class="rendered" id="test3"></div>
    </div>
    
    <script src="/assets/markdown-renderer.js?v=2"></script>
    <script>
        // Test if the function is loaded
        if (typeof renderMarkdown === 'function') {
            document.getElementById('test1').innerHTML = '✅ renderMarkdown function loaded successfully';
            
            // Test 2: Simple header
            document.getElementById('test2').innerHTML = renderMarkdown('# Header 1');
            
            // Test 3: Your failing example
            const failingText = `Here's my summary: # Piper Morgan Summary ## File Type This appears to be documentation.`;
            document.getElementById('test3').innerHTML = renderMarkdown(failingText);
            
        } else {
            document.getElementById('test1').innerHTML = '❌ renderMarkdown function not loaded - check console for errors';
            console.error('renderMarkdown function not found');
        }
    </script>
</body>
</html>''')

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    # Use a different template approach to avoid format/replace issues
    html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Piper Morgan - AI PM Assistant</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #2c3e50; margin: 0; font-size: 2.5em; }
        .header p { color: #7f8c8d; font-size: 1.2em; margin: 10px 0; }
        .chat-form { display: flex; margin-bottom: 20px; }
        .chat-input { flex-grow: 1; padding: 15px; border: 2px solid #ecf0f1; border-radius: 8px; font-size: 16px; margin-right: 10px; }
        .chat-input:focus { outline: none; border-color: #3498db; }
        .submit-btn { background: #3498db; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
        .submit-btn:hover { background: #2980b9; }
        #chat-window {
            height: 400px;
            min-height: 150px;
            max-height: 80vh;
            resize: vertical;
            overflow-y: auto;
            border: 1px solid #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            background: #fdfdfd;
        }
        .message { margin-bottom: 15px; padding: 10px 15px; border-radius: 18px; max-width: 80%; line-height: 1.4; }
        .user-message { background: #3498db; color: white; align-self: flex-end; margin-left: auto; }
        .bot-message { background: #ecf0f1; color: #2c3e50; align-self: flex-start; }
        .bot-message.error { background: #f8d7da; color: #721c24; }
        .bot-message.thinking { color: #7f8c8d; font-style: italic; }
        .message-container { display: flex; flex-direction: column; }
        .result { margin-top: 10px; padding: 10px; border-radius: 8px; border: 1px solid transparent; }
        .success { background: #d4edda; border-color: #c3e6cb; color: #155724; }
        .error { background: #f8d7da; border-color: #f5c6cb; color: #721c24; }
        .workflow-status { margin: 20px 0; padding: 15px; background: #e8f4f8; border-radius: 8px; }
        .upload-section { margin-top: 20px; }
        .upload-toggle { background: #7f8c8d; color: white; border: none; padding: 10px 15px; border-radius: 8px; cursor: pointer; width: 100%; text-align: left; font-size: 16px; }
        .upload-toggle:hover { background: #6c7a89; }
        #upload-form-container { display: none; margin-top: 10px; padding: 15px; border: 1px solid #ecf0f1; border-radius: 8px; }
        #upload-form { display: flex; align-items: center; }
        #upload-form input[type="file"] { flex-grow: 1; }
        .examples { margin-top: 30px; }
        .example { padding: 10px; margin: 5px 0; background: #f8f9fa; border-left: 4px solid #3498db; cursor: pointer; }
        .example:hover { background: #e9ecef; }
        
        /* Markdown styling */
        .message h1, .message h2, .message h3, .message h4, .message h5, .message h6 { margin: 15px 0 10px 0; color: #2c3e50; }
        .message h1 { font-size: 1.5em; border-bottom: 1px solid #ecf0f1; padding-bottom: 5px; }
        .message h2 { font-size: 1.3em; }
        .message h3 { font-size: 1.1em; }
        .message ul, .message ol { margin: 10px 0; padding-left: 20px; }
        .message li { margin: 5px 0; }
        .message code { background: #f8f9fa; padding: 2px 4px; border-radius: 3px; font-family: 'Monaco', 'Menlo', monospace; font-size: 0.9em; }
        .message pre { background: #f8f9fa; padding: 10px; border-radius: 5px; overflow-x: auto; margin: 10px 0; }
        .message pre code { background: none; padding: 0; }
        .message blockquote { border-left: 4px solid #3498db; margin: 10px 0; padding-left: 15px; color: #7f8c8d; }
        .message strong { color: #2c3e50; }
        .message em { color: #34495e; }
        .message table { border-collapse: collapse; width: 100%; margin: 10px 0; }
        .message th, .message td { border: 1px solid #ecf0f1; padding: 8px; text-align: left; }
        .message th { background: #f8f9fa; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><img src="/assets/pm-logo.png" alt="Piper Morgan" style="height: 60px; vertical-align: middle;"> Piper Morgan</h1>
            <p>AI Product Management Assistant</p>
            <p><em>I can create GitHub issues, analyze documents, and more!</em></p>
        </div>
        
        <div id="chat-window">
             <div class="message-container">
                <div class="message bot-message">
                    Hello! How can I help you today?
                </div>
            </div>
        </div>

        <form class="chat-form" id="chatForm">
            <input type="text" name="message" class="chat-input" 
                   placeholder="e.g., Users are complaining about the login page being slow..." 
                   required>
            <button type="submit" class="submit-btn">Send</button>
        </form>
        
        <div class="upload-section">
            <button class="upload-toggle" id="upload-toggle-btn">📄 Upload a document to the knowledge base</button>
            <div id="upload-form-container">
                <form id="upload-form" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <button type="submit" class="submit-btn">Upload</button>
                </form>
            </div>
        </div>
         
        <div class="examples">
            <h3>💡 Try these examples:</h3>
            <div class="example" onclick="setExample(this)">
                Users are complaining that the mobile app crashes when they upload large photos
            </div>
            <div class="example" onclick="setExample(this)">
                The login page is too slow and users are getting frustrated
            </div>
            <div class="example" onclick="setExample(this)">
                We need to add dark mode support to improve user experience
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="/assets/bot-message-renderer.js"></script>
    <script>
        const API_BASE_URL = "API_BASE_URL_PLACEHOLDER";
        const chatWindow = document.getElementById('chat-window');
        let sessionId = null;
        
        // Use DDD bot message renderer for all bot messages
        
        // Wait for DOM and scripts to load
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM loaded, marked.js available:', typeof marked !== 'undefined');
        });

        function appendMessage(html, isUser = false) {
            const msgContainer = document.createElement('div');
            msgContainer.className = 'message-container';
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            
            // If it's a user message, use textContent; if bot message, use innerHTML for markdown
            if (isUser) {
                msgDiv.textContent = html;
            } else {
                msgDiv.innerHTML = html;
            }
            
            msgContainer.appendChild(msgDiv);
            chatWindow.appendChild(msgContainer);
            chatWindow.scrollTop = chatWindow.scrollHeight;
            return msgDiv;
        }

        function setExample(element) {
            document.querySelector('.chat-input').value = element.textContent.trim();
        }
        
        document.getElementById('upload-toggle-btn').addEventListener('click', () => {
            const container = document.getElementById('upload-form-container');
            container.style.display = container.style.display === 'none' ? 'block' : 'none';
        });

        document.getElementById('upload-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const fileInput = form.querySelector('input[type="file"]');
            const file = fileInput.files[0];
            if (!file) return;

            const thinkingDiv = appendMessage(`Uploading ${file.name}...`);
            thinkingDiv.classList.add('thinking');

            const formData = new FormData();
            formData.append('file', file);
            if (sessionId) {
                formData.append('session_id', sessionId);
            }

            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/files/upload`, {
                    method: 'POST',
                    body: formData,
                });
                const result = await response.json();
                let botResponseHTML;

                if (response.ok && result.file_id) {
                     botResponseHTML = `
                        <div class="result success">
                            <strong>✅ Document Uploaded!</strong><br>
                            <strong>File:</strong> ${result.filename}<br>
                            <strong>File ID:</strong> ${result.file_id}
                        </div>`;
                } else {
                    botResponseHTML = `
                        <div class="result error">
                            <strong>❌ Upload Failed</strong><br>
                            ${result.detail || 'An unknown error occurred.'}
                        </div>`;
                }
                thinkingDiv.innerHTML = botResponseHTML;
                thinkingDiv.classList.remove('thinking');

                if (result.session_id) {
                    sessionId = result.session_id;
                }
            } catch (error) {
                thinkingDiv.innerHTML = `
                    <div class="result error">
                        <strong>❌ Network Error</strong><br>
                        Could not connect to API: ${error.message}
                    </div>`;
                thinkingDiv.classList.add('error');
                thinkingDiv.classList.remove('thinking');
            } finally {
                form.reset();
            }
        });
        
        async function pollWorkflowStatus(workflowId, elementToUpdate) {
            let pollCount = 0;
            const maxPolls = 30; // Stop after 60 seconds (2s intervals)
            
            const intervalId = setInterval(async () => {
                pollCount++;
                
                try {
                    const response = await fetch(`${API_BASE_URL}/api/v1/workflows/${workflowId}`);
                    
                    if (!response.ok) {
                        // If 404 and we've seen success before, assume it completed
                        if (response.status === 404 && elementToUpdate.textContent.includes('completed')) {
                            clearInterval(intervalId);
                            return; // Keep the success message
                        }
                        
                        // Otherwise show error and stop
                        elementToUpdate.innerHTML = `<div class="result error">Error checking status.</div>`;
                        clearInterval(intervalId);
                        return;
                    }
                    
                    const data = await response.json();
                    // Use DDD handler for workflow responses
                    if (data.status === 'completed') {
                        elementToUpdate.classList.remove('thinking');
                        elementToUpdate.classList.add('reply');
                        handleWorkflowResponse(data, elementToUpdate);
                        clearInterval(intervalId);
                    } else if (data.status === 'failed') {
                        elementToUpdate.classList.remove('thinking');
                        elementToUpdate.classList.add('error');
                        elementToUpdate.innerHTML = renderBotMessage(`Workflow Failed: ${data.message}`, 'error', false);
                        clearInterval(intervalId);
                    }
                    
                    // Stop polling after max attempts
                    if (pollCount >= maxPolls) {
                        clearInterval(intervalId);
                        elementToUpdate.innerHTML = `<div class="result error">Workflow status check timed out.</div>`;
                    }
                } catch (error) {
                    console.error("Polling error:", error);
                    elementToUpdate.innerHTML = `<div class="result error">Could not connect to API to check status.</div>`;
                    clearInterval(intervalId);
                }
            }, 2000); // Poll every 2 seconds
        }

        document.getElementById('chatForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const input = form.querySelector('.chat-input');
            const message = input.value.trim();
            if (!message) return;

            appendMessage(message, true);
            input.value = '';

            // Show a temporary 'thinking' message
            const thinkingDiv = appendMessage('Thinking...');
            thinkingDiv.classList.add('thinking');

            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/intent`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        message: message,
                        session_id: sessionId 
                    })
                });
                
                const result = await response.json();
                
                if (!response.ok) {
                    throw new Error(result.detail || "An API error occurred");
                }

                // Replace the 'thinking' message with a new bot message (with 'reply' class)
                const botDiv = appendMessage('', false);
                botDiv.classList.add('reply');
                handleDirectResponse(result, botDiv);
                // Remove the old thinking message
                thinkingDiv.remove();

                if (result.workflow_id) {
                    // If a workflow was started, create a new message bubble to poll for its status
                    const statusDiv = appendMessage('Starting workflow...');
                    statusDiv.classList.add('thinking');
                    pollWorkflowStatus(result.workflow_id, statusDiv);
                }
                
                if (result.session_id) {
                    sessionId = result.session_id;
                }
            } catch (error) {
                // Replace the 'thinking' message with a new error message (with 'error' class)
                const errorDiv = appendMessage('', false);
                errorDiv.classList.add('error');
                handleErrorResponse(error, errorDiv);
                thinkingDiv.remove();
            }
        });
    </script>
</body>
</html>"""
    
    # Replace the placeholder with actual API URL
    html_content = html_template.replace("API_BASE_URL_PLACEHOLDER", API_BASE_URL)
    
    return HTMLResponse(content=html_content)