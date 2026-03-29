import { test, expect, afterEach } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";
import { ToolCallBadge } from "../ToolCallBadge";
import type { ToolInvocation } from "ai";

afterEach(() => {
  cleanup();
});

function makeTool(
  toolName: string,
  args: Record<string, unknown>,
  state: "call" | "result" = "result",
  result: unknown = "Success"
): ToolInvocation {
  if (state === "result") {
    return { toolCallId: "test-id", toolName, args, state, result } as ToolInvocation;
  }
  return { toolCallId: "test-id", toolName, args, state: "call" } as ToolInvocation;
}

// str_replace_editor labels
test("shows 'Creating' label for str_replace_editor create command", () => {
  render(<ToolCallBadge toolInvocation={makeTool("str_replace_editor", { command: "create", path: "/App.jsx" })} />);
  expect(screen.getByText("Creating /App.jsx")).toBeDefined();
});

test("shows 'Editing' label for str_replace_editor str_replace command", () => {
  render(<ToolCallBadge toolInvocation={makeTool("str_replace_editor", { command: "str_replace", path: "/App.jsx" })} />);
  expect(screen.getByText("Editing /App.jsx")).toBeDefined();
});

test("shows 'Editing' label for str_replace_editor insert command", () => {
  render(<ToolCallBadge toolInvocation={makeTool("str_replace_editor", { command: "insert", path: "/components/Button.tsx" })} />);
  expect(screen.getByText("Editing /components/Button.tsx")).toBeDefined();
});

test("shows 'Reading' label for str_replace_editor view command", () => {
  render(<ToolCallBadge toolInvocation={makeTool("str_replace_editor", { command: "view", path: "/App.jsx" })} />);
  expect(screen.getByText("Reading /App.jsx")).toBeDefined();
});

test("shows 'Undoing edit' label for str_replace_editor undo_edit command", () => {
  render(<ToolCallBadge toolInvocation={makeTool("str_replace_editor", { command: "undo_edit", path: "/App.jsx" })} />);
  expect(screen.getByText("Undoing edit in /App.jsx")).toBeDefined();
});

test("shows 'Working on' label for str_replace_editor unknown command", () => {
  render(<ToolCallBadge toolInvocation={makeTool("str_replace_editor", { command: "other", path: "/App.jsx" })} />);
  expect(screen.getByText("Working on /App.jsx")).toBeDefined();
});

// file_manager labels
test("shows 'Renaming' label for file_manager rename command", () => {
  render(<ToolCallBadge toolInvocation={makeTool("file_manager", { command: "rename", old_path: "/old.tsx", new_path: "/new.tsx" })} />);
  expect(screen.getByText("Renaming /old.tsx → /new.tsx")).toBeDefined();
});

test("shows 'Deleting' label for file_manager delete command", () => {
  render(<ToolCallBadge toolInvocation={makeTool("file_manager", { command: "delete", path: "/App.jsx" })} />);
  expect(screen.getByText("Deleting /App.jsx")).toBeDefined();
});

test("shows 'Managing files' for file_manager unknown command", () => {
  render(<ToolCallBadge toolInvocation={makeTool("file_manager", { command: "other" })} />);
  expect(screen.getByText("Managing files")).toBeDefined();
});

// Unknown tool
test("shows 'Running' label for unknown tool", () => {
  render(<ToolCallBadge toolInvocation={makeTool("unknown_tool", {})} />);
  expect(screen.getByText("Running unknown_tool")).toBeDefined();
});

// State rendering
test("shows spinner when state is pending (call)", () => {
  const { container } = render(
    <ToolCallBadge toolInvocation={makeTool("str_replace_editor", { command: "create", path: "/App.jsx" }, "call")} />
  );
  // Loader2 renders as an svg with animate-spin class
  expect(container.querySelector(".animate-spin")).toBeDefined();
});

test("shows green dot when state is result with a result value", () => {
  const { container } = render(
    <ToolCallBadge toolInvocation={makeTool("str_replace_editor", { command: "create", path: "/App.jsx" }, "result", "Success")} />
  );
  const dot = container.querySelector(".bg-emerald-500");
  expect(dot).toBeDefined();
});

test("shows amber dot when state is result with no result value", () => {
  const { container } = render(
    <ToolCallBadge toolInvocation={makeTool("str_replace_editor", { command: "create", path: "/App.jsx" }, "result", null)} />
  );
  const dot = container.querySelector(".bg-amber-400");
  expect(dot).toBeDefined();
});
