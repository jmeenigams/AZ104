# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**UIGen** is an AI-powered React component generator with live preview. Users describe components in natural language; Claude generates code using tool use, and the result renders in a sandboxed iframe. Supports anonymous and authenticated users, with project persistence via SQLite.

## Commands

```bash
# First-time setup (install deps + Prisma generate + migrate)
npm run setup

# Development server (Turbopack)
npm run dev

# Production build
npm run build

# Run tests
npm run test

# Run a single test file
npx vitest run src/components/chat/__tests__/ChatInterface.test.tsx

# Lint
npm run lint

# Reset database (destructive)
npm run db:reset
```

## Architecture

### Request Flow

1. User types a message → sent to `/api/chat` with serialized VirtualFileSystem snapshot
2. API reconstructs the VirtualFileSystem, calls Claude with tools (`str_replace_editor`, `file_manager`)
3. Claude edits files via tools; changes stream back via `DataStreamResponse`
4. Client-side `FileSystemContext` applies tool results to in-memory state
5. `PreviewFrame` picks up file changes, Babel-transpiles JSX, creates an ESM import map, and renders in a sandboxed iframe (modules resolved via esm.sh CDN)
6. If user is authenticated, the project (messages + file system data) is persisted to SQLite via Prisma on stream completion

### Key Abstractions

- **VirtualFileSystem** (`src/lib/file-system.ts`): In-memory tree, Map-indexed. Serializable for DB storage. No disk writes. All AI file operations target this.
- **AI Tools** (`src/lib/tools/`): `str_replace_editor` for precise edits, `file_manager` for rename/delete. Wired into the chat API route.
- **JSX Transformer** (`src/lib/transform/jsx-transformer.ts`): Babel standalone transpiles TSX/JSX, builds an ESM import map (pointing to esm.sh), and generates blob URLs for iframe execution.
- **System Prompt** (`src/lib/prompts/generation.tsx`): Instructs Claude to always write to `/App.jsx`, use Tailwind CSS (no inline styles), and work within the virtual filesystem.

### Component Tree

```
MainContent
├── FileSystemProvider  ← virtual FS state
│   └── ChatProvider    ← AI chat state (Vercel AI SDK useChat)
│       ├── ChatInterface (left panel)
│       └── Preview / Code panel (right panel)
│           ├── PreviewFrame  ← sandboxed iframe
│           └── FileTree + CodeEditor (Monaco)
```

### Auth

JWT in HTTP-only cookie, 7-day expiry. `src/lib/auth.ts` handles `createSession` / `verifySession`. `src/middleware.ts` protects routes. Passwords hashed with bcrypt.

### Database

Prisma + SQLite (`prisma/dev.db`). Two models: `User` and `Project` (stores messages and file system data as JSON blobs).

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Claude API key; falls back to mock provider if unset |
| `JWT_SECRET` | `development-secret-key` | JWT signing secret |
| `NODE_ENV` | — | Set to `production` for secure cookies |

## Tech Stack

- **Framework**: Next.js 15 (App Router, React Server Components), React 19, TypeScript
- **Styling**: Tailwind CSS v4, Radix UI, Shadcn UI
- **AI**: `@ai-sdk/anthropic` + Vercel AI SDK (`useChat`, `DataStreamResponse`)
- **Editor**: Monaco (`@monaco-editor/react`)
- **ORM**: Prisma (SQLite)
- **Testing**: Vitest + React Testing Library + jsdom
