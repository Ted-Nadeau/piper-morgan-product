// Test framework
const {
  handleDirectResponse,
  handleWorkflowResponse,
} = require("./bot-message-renderer");

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
    throw new Error(`${message}: expected "${expected}", got "${actual}"`);
  }
}

// Mock DOM elements
const mockElements = {
  direct: { innerHTML: "", classList: { add: () => {}, remove: () => {} } },
  workflow: { innerHTML: "", classList: { add: () => {}, remove: () => {} } },
};

function simulateDirectResponse(message, element) {
  handleDirectResponse({ message }, element);
}

function simulateWorkflowResponse(message, element) {
  handleWorkflowResponse({ message, type: "analyze_file" }, element);
}

test("direct response path uses unified renderer", () => {
  global.marked = { parse: (txt) => `<h1>${txt}</h1>` };
  simulateDirectResponse("# Test Response", mockElements.direct);
  assertEqual(
    mockElements.direct.innerHTML.includes("<h1>"),
    true,
    "Direct path should render markdown"
  );
});

test("workflow response path uses unified renderer", () => {
  global.marked = { parse: (txt) => `<h1>${txt}</h1>` };
  simulateWorkflowResponse("# Test Response", mockElements.workflow);
  assertEqual(
    mockElements.workflow.innerHTML.includes("<h1>"),
    true,
    "Workflow path should render markdown"
  );
});

test("both paths produce identical output", () => {
  global.marked = { parse: (txt) => `<h1>${txt}</h1><strong>Bold</strong>` };
  const message = "# Test\n**Bold** text";
  simulateDirectResponse(message, mockElements.direct);
  simulateWorkflowResponse(message, mockElements.workflow);
  assertEqual(
    mockElements.direct.innerHTML,
    mockElements.workflow.innerHTML,
    "Both paths should produce identical output"
  );
});
