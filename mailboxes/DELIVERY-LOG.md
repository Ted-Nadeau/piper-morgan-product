# Mail Delivery Log

Each `/deliver-mail` run appends an entry below. The timestamp of the last entry is used to determine "since last delivery."

---

## 2026-03-21 22:50

- **Ingested**: 6 memos from dev/active/ (reply wave from CIO memo deliveries + HOSR Agent 360 follow-ups)
- **Routed to inboxes**: cio (4), cxo (2), ppm (2), exec (1), lead (1)
- **Web delivery**: 9 delivered, 0 skipped, 0 deferred
- **Code delivery**: 1 (lead inbox, self-serve)
- **Senders**: arch (1), cxo (1), hosr (3), ppm (1)
- **Stale inboxes**: none
- **Errors**: none

---

## 2026-03-21 21:55

- **Ingested**: 0 memos from incoming/
- **Web delivery**: 5 delivered, 0 skipped, 0 deferred
- **Breakdown**: arch (1 CIO memo), cxo (1 CIO memo + 1 PPM reroute), ppm (1 CIO memo), exec (1 docs response)
- **Routing fix**: PPM failure gap memo was in spec inbox, addressed To: CXO CC: Lead/PM/Arch. Moved to cxo/read/, copied to lead/inbox and arch/inbox. PM confirmed CXO had already read it on Mar 16.
- **Stale inboxes**: lead has 1 new item (PPM failure gap, CC copy); arch has 1 new item (same)
- **Errors**: 1 misrouted memo (spec→cxo, corrected)

---

## 2026-03-19 15:53

- **Ingested**: 1 memo from incoming/ (memo-cos-to-docs-infrastructure-2026-03-19.md, routed as from:exec to:docs)
- **Routed to inboxes**: docs
- **Web delivery**: 21 delivered, 0 skipped, 0 deferred
- **Breakdown**: hosr (4), comms (1), cxo (5), cio (5), ppm (6)
- **Notes**: First v3 run. 16 items were pre-v3 deliveries confirmed by PM. 5 were new 360 questionnaire deliveries.
- **Stale inboxes**: none
- **Errors**: 1 legacy filename (cos→exec slug correction per PM)
