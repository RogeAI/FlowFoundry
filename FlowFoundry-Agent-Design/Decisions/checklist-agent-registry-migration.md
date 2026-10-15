# Backlog: Agent Registry Migration

## Context

Currently all agent data (names, roles, descriptions, portraits, states) is hardcoded
as a static array inside `app/page.tsx`. This is prototype-only data.

The decision was made to eventually move this to a proper registry-driven data source
so that ForgeMaster and the UI both read from a single source of truth.

**Do not act on this until explicitly prioritized.**

---

## Checklist

- [ ] Create `data/agents.ts` as the single source of truth for all agent profiles
- [ ] Move hardcoded agent array out of `app/page.tsx` into the registry
- [ ] Define the agent data shape (name, role, description, portrait, state, skills, tools, guardrails)
- [ ] Update UI rendering in `app/page.tsx` to read dynamically from the registry
- [ ] Connect ForgeMaster instructions to reference the registry
- [ ] Validate that all agent states (Available, Busy, Unavailable) still render correctly after migration
- [ ] Update `docs/04-TECHNICAL-HANDOVER.md` to reflect the new data architecture

---

## Related

- [Agent profiles live in FlowFoundry-Agent-Design/Agents/](../Agents/)
- [Shared foundation lives in FlowFoundry-Agent-Design/Foundation/](../Foundation/)
