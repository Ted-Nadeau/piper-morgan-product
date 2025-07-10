// Test framework
const { renderBotMessage } = require("./bot-message-renderer");

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

// Test cases
test("renderBotMessage exists", () => {
  assertEqual(
    typeof renderBotMessage,
    "function",
    "renderBotMessage should be a function"
  );
});

test("renders success message with markdown", () => {
  global.marked = { parse: (txt) => `<h1>${txt}</h1><strong>World</strong>` };
  const result = renderBotMessage("# Hello **World**", "success", false);
  assertEqual(result.includes("<h1>"), true, "Should render markdown headers");
  assertEqual(result.includes("<strong>"), true, "Should render markdown bold");
  assertEqual(
    result.includes("result success"),
    true,
    "Should have success CSS class"
  );
});

test("renders error message without markdown", () => {
  const result = renderBotMessage("Error: Something failed", "error", false);
  assertEqual(
    result.includes("<h1>"),
    false,
    "Should not render markdown in errors"
  );
  assertEqual(
    result.includes("result error"),
    true,
    "Should have error CSS class"
  );
});

test("renders thinking message as-is", () => {
  const result = renderBotMessage("Thinking...", "success", true);
  assertEqual(
    result.includes("thinking"),
    true,
    "Should have thinking CSS class"
  );
  assertEqual(
    result,
    '<div class="result success thinking">Thinking...</div>',
    "Should wrap thinking message in correct HTML"
  );
});
