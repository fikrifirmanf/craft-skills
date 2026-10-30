# Domain notes

Architecture alone does not make a money system, a booking system or a regulated system correct. When the prompt has one of these signals, add at most three short notes to the intro line above the picker, and copy them into the ADR under Consequences. They are advice about the domain, not extra questions. Write them in the user's language and tie them to the user's words.

| Signal | Notes to add |
|---|---|
| Wallet, balance, payout, payment, invoice | **Ledger, not a balance column:** record every change as balanced entries (debit and credit sum to zero) and derive balances from them. **Money as integer minor units** with a currency; never floats. **Idempotency keys** on every money-moving request, and unique event ids for provider webhooks. **Provider confirms, you record:** credit a top-up only after the provider's signed webhook; hold a withdrawal first, then settle or reverse it. **Lock in a fixed order** when two accounts change in one transaction. |
| Holding or moving other people's money (marketplace payouts, escrow, wallets) | **Licensing:** holding and forwarding third-party funds can need a payments licence in some countries. Suggest using the payment provider's marketplace or disbursement product, and ask the user to confirm with the provider and a lawyer before launch. State it once, without giving legal advice. |
| Audit, compliance, "traceable", regulated records | **Append-only history** that the application database role cannot update or delete, **who and why** on every change, and an **integrity check** (balances reconcile with entries). |
| Booking, scheduling, inventory, tickets | **No double booking:** reserve inside one transaction with a lock or a uniqueness constraint, and release expired reservations. |
| Several sellers, tenants or customers in one system | **Authorization in the query:** filter by owner or tenant id inside the data access, not only in the handler. |
| Webhooks or callbacks from another system | **Verify the signature on the raw body,** deduplicate by event id, and answer quickly, doing slow work in a worker. |
| Personal or health data | **Keep personal data out of immutable logs and events** (store a reference), and log access. |

Do not add a note without a matching signal. If none matches, show no notes.
