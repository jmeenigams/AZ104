"use client";

import { ToolInvocation } from "ai";
import { Loader2 } from "lucide-react";

function getLabel(toolInvocation: ToolInvocation): string {
  const { toolName, args } = toolInvocation;

  if (toolName === "str_replace_editor") {
    const path = args?.path ?? "";
    switch (args?.command) {
      case "create":
        return `Creating ${path}`;
      case "str_replace":
      case "insert":
        return `Editing ${path}`;
      case "view":
        return `Reading ${path}`;
      case "undo_edit":
        return `Undoing edit in ${path}`;
      default:
        return `Working on ${path}`;
    }
  }

  if (toolName === "file_manager") {
    switch (args?.command) {
      case "rename":
        return `Renaming ${args?.old_path ?? ""} → ${args?.new_path ?? ""}`;
      case "delete":
        return `Deleting ${args?.path ?? ""}`;
      default:
        return "Managing files";
    }
  }

  return `Running ${toolName}`;
}

interface ToolCallBadgeProps {
  toolInvocation: ToolInvocation;
}

export function ToolCallBadge({ toolInvocation }: ToolCallBadgeProps) {
  const label = getLabel(toolInvocation);
  const isDone = toolInvocation.state === "result";
  const hasResult = isDone && toolInvocation.result != null;

  return (
    <div className="inline-flex items-center gap-2 mt-2 px-3 py-1.5 bg-neutral-50 rounded-lg text-xs font-mono border border-neutral-200">
      {isDone ? (
        <div
          className={`w-2 h-2 rounded-full ${hasResult ? "bg-emerald-500" : "bg-amber-400"}`}
        />
      ) : (
        <Loader2 className="w-3 h-3 animate-spin text-blue-600" />
      )}
      <span className="text-neutral-700">{label}</span>
    </div>
  );
}
