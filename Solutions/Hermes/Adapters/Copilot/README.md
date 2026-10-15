# Hermes — Copilot Adapter

This adapter configures Hermes for GitHub Copilot.

## What this adapter is

`copilot-adapter.md` is a self-contained instruction file for use with GitHub Copilot. It contains the complete Hermes behavior inline because GitHub Copilot does not support loading multiple files dynamically at runtime.

## What this adapter is not

It is not the canonical agent definition. The canonical source of truth for Hermes is:

```text
Solutions/Hermes/Agent/AGENT.md
Solutions/Hermes/Agent/Instructions/
Solutions/Hermes/Agent/Skills/
```

## How to deploy

1. Open your GitHub repository settings for Copilot.
2. Paste the contents of `copilot-adapter.md` into the custom instructions field, or reference it via `.github/copilot-instructions.md`.
3. Make the skill `.docx` or `.md` files available as knowledge files if your Copilot configuration supports it.

## Keeping the adapter current

When the canonical `Agent/` content changes, update this adapter to reflect those changes. The adapter is a compiled snapshot of the canonical agent, not a live reference.
