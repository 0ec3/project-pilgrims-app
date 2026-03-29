# 21 — FEATURE: PLANNER, REMINDERS, WALLET, NOTES, AND BOOKMARKS

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, design lead, Flutter engineers, backend engineers, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for the personal tools feature family, including Planner behavior, local reminders, Wallet artifact storage, Notes, Bookmarks, capture surfaces, itinerary overlays, Supporter enrichments, offline guarantees, export/share behavior, analytics hooks, and release-readiness expectations.
- **Authority level:** This file is the canonical source of truth for the Planner/Reminders/Wallet/Notes/Bookmarks feature family. If implementation, UI, or tests diverge from this file, this file wins unless a higher-level normative contract or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`, `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`, `18-FEATURE-RITUALS-RIC-AND-RELIGIOUS-CONTENT.md`, `19-FEATURE-MAPS-SAVE-MY-GATE-AND-3D-WAYFINDING.md`, `20-FEATURE-GROUP-HUB-CHECKINS-REGROUP-AND-SHARED-COORDINATION.md`
- **Related files:** `22`, `23`, `24`, `25`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because the app’s personal tools are easy to underestimate and easy to fragment.

If left vague, teams and AI coding agents often create several expensive problems:
- Planner turns into a generic productivity app instead of a calm pilgrimage helper,
- reminders quietly depend on network or push infrastructure even though the product promise is local-first,
- Wallet drifts into a payments or identity-wallet concept instead of a simple records folder,
- Notes and Bookmarks become separate mini-products with inconsistent capture flows,
- exports are added without clear privacy posture,
- feature richness grows faster than implementation discipline,
- older entitlement assumptions leak into new code and create downgrade confusion,
- tools become disconnected from Rituals, Maps, Group, and Phrasebook instead of supporting them.

This file prevents those failures by defining:
- what this feature family is for,
- what belongs in Planner versus Wallet versus Notes versus Bookmarks,
- how reminders work on-device,
- how itinerary overlays and RIC handoffs fit into the experience,
- what free users and Supporters can do,
- how export and sharing must behave,
- what must be tested and evidenced before release.

---

# 2. Feature purpose and user value

## 2.1 Feature family purpose
This feature family exists to help pilgrims:
- prepare and remember practical journey tasks,
- preserve useful personal records and proofs,
- quickly save important content or context for later return,
- continue organizing themselves offline,
- recover useful context without needing a cloud account or full productivity workflow.

## 2.2 Main user value statement
A pilgrim should be able to open these personal tools and quickly answer questions like:
- What do I need to do today?
- How do I set a reminder that still works offline?
- Where did I save that ritual, phrase, or map reference?
- How do I keep a record of a remedy receipt or service artifact?
- How do I save and later find my own notes without turning the app into a journaling labyrinth?

## 2.3 Feature-level promise
This feature family must feel:
- calm,
- local-first,
- lightweight,
- private,
- supportive rather than overwhelming,
- reliable under poor connectivity,
- consistent across all capture surfaces.

---

# 3. Scope and boundaries

## 3.1 In scope
This feature family includes:
- Planner list and planner item editing,
- reminder scheduling and reminder settings,
- template-driven day planning,
- smart planner suggestions where entitled,
- read-only itinerary overlays inside the planner context,
- Wallet list, detail, add, and export flows,
- Notes list and note editor,
- Bookmarks list,
- cross-feature capture surfaces for bookmark and note creation,
- local search/filter/sort for notes and bookmarks,
- explicit export/share flows for wallet and notes/bookmarks,
- privacy and downgrade behavior for these personal tools.

## 3.2 Out of scope
This feature family does **not** include:
- cloud sync for planner, notes, or wallet,
- collaborative editing,
- generic calendar sync,
- remote push notifications,
- background health monitoring,
- finance or payment-wallet behavior,
- general document vault behavior,
- passive or hidden data sharing.

## 3.3 Boundary with file `13`
File `13` is the canonical source of truth for device-local persistence categories and hard invariants.
This file may define feature-facing runtime models and required fields, but it must not contradict file `13`.

## 3.4 Boundary with file `14`
The API contract remains intentionally small. This feature family must not assume a sync or notes backend.
The only meaningful online dependency for this family in V1 is read-only supportive context such as itinerary overlays and entitlement snapshots.

## 3.5 Boundary with file `18`
Rituals owns ritual logic and RIC. This feature family only defines how planner suggestions, wallet receipt capture, and note/bookmark capture integrate with ritual flows.

## 3.6 Boundary with file `20`
Group owns itinerary truth and shared coordination semantics. This feature family may display a read-only itinerary overlay inside Planner, but must not redefine group itinerary ownership.

## 3.7 Boundary with file `22`
Phrasebook, Emergency, Safety, and Assistive Tools own their own screens and content. This feature family only defines how notes/bookmarks capture from those surfaces works.

## 3.8 Boundary with file `24`
Account, subscriptions, entitlements, and settings own entitlement truth. This feature family only reacts to entitlement snapshots and user settings.

---

# 4. Product rules that govern this feature family

## 4.1 Local-first rule
Planner, reminders, wallet artifacts, notes, and bookmarks are local-first features.
Core usefulness must not depend on cloud sync, remote push, or always-on network.

## 4.2 Lightweight personal-tools rule
These tools must remain lightweight and pilgrimage-specific.
They are helpers, not a generalized productivity suite.

## 4.3 Wallet is a records folder, not a payment wallet
Wallet exists to store pilgrimage-related proofs and references such as remedy receipts or service artifacts.
It must not drift into payment, identity-wallet, crypto-wallet, or official-document workflow ownership.

## 4.4 Reminders must fail gracefully
If notification permissions, exact timing permissions, or OS delivery conditions are unavailable, the planner item must still exist and remain useful.
The app must never imply a reminder is guaranteed when it could not actually be scheduled.

## 4.5 Notes and bookmarks are private by default
They stay on the device unless the user explicitly exports or shares them.
No hidden sync, background upload, or cross-device propagation is allowed by default.

## 4.6 Capture must be consistent
Bookmark and note capture must look and behave consistently across Rituals, Maps, Planner, Phrasebook, Emergency, and Safety surfaces.

## 4.7 Supporter uplift must stay ethical
Supporter can unlock richer convenience such as smart planner suggestions, markdown, tags, multiple attachments, and export. It must not block baseline user organization or basic reminder usefulness.

## 4.8 Calmness over complexity rule
This feature family should present only the next useful action, not expose unnecessary technical settings or document-management concepts.

---

# 5. Canonical terminology for this feature family

## 5.1 Planner
The feature area for lightweight pilgrimage planning and task organization.

## 5.2 Reminder
A time-based local prompt associated with a planner item.

## 5.3 Wallet
A storage surface for important pilgrimage-related records, especially remedy and service artifacts.

## 5.4 Wallet item
A local record containing artifact metadata and optional linkage to a ritual session.

## 5.5 Bookmark
A saved reference to app content or context for quick return.

## 5.6 Note
User-authored text or structured content saved for later reference.

## 5.7 Attachment
A local file attached to a note or wallet item.

## 5.8 Smart suggestion
A supportive planner recommendation derived from current context and entitlement, shown only where appropriate.

## 5.9 Itinerary overlay
Read-only shared itinerary information rendered inside Planner for convenience.

## 5.10 Quiet hours
The user-configurable reminder-suppression window for non-urgent local notifications.

---

# 6. User stories

## 6.1 Planner and reminders
- **As a pilgrim**, I can apply a simple Umrah or Hajj day template to create a useful plan quickly.
- **As a pilgrim**, I can add my own local items and optional reminders without network.
- **As a pilgrim**, if notifications are denied, I can still keep the item and see why the reminder could not be scheduled.
- **As a Supporter**, I can receive supportive smart suggestions without being interrupted in ritual-critical screens.

## 6.2 Wallet
- **As a pilgrim**, I can attach a remedy receipt or service proof and keep it locally.
- **As a pilgrim**, I can export selected wallet items when I explicitly choose to.
- **As a pilgrim**, I can open a wallet record later and still understand what it refers to.

## 6.3 Notes and bookmarks
- **As a pilgrim**, I can bookmark important ritual, map, phrasebook, planner, or safety content in one or two steps.
- **As a pilgrim**, I can create a note with source context and optional attachments.
- **As a Supporter**, I can use markdown, tags, multiple attachments, and export.
- **As a downgraded user**, I can still read my richer notes even if I can no longer edit all premium fields.

## 6.4 Itinerary overlay
- **As a group member**, I can see the current shared itinerary inside Planner without turning Planner into a collaborative calendar.
- **As a pilgrim**, if that itinerary is stale, I can see that clearly.

---

# 7. Free vs supporter boundaries

## 7.1 Free capability baseline
The following must remain available in the free path:
- Planner list and item creation,
- local reminders subject to OS permission,
- local template application,
- read-only itinerary overlay when available,
- Wallet add and view,
- basic wallet export when product policy allows,
- Bookmarks,
- Notes with plain-text behavior,
- fast capture from supported surfaces,
- offline search/filter for local notes and bookmarks.

## 7.2 Supporter-linked enrichments
Supporter-linked value may include:
- `SMART_PLANNER` suggestions,
- richer pack recommendation prompts in Planner where appropriate,
- extended notes/bookmarks capability through the current entitlement gate,
- markdown note editing,
- tags,
- multiple attachments,
- richer export options,
- smart links back into source screens.

## 7.3 Current entitlement naming rule
The current API contract example uses `NOTES_BOOKMARKS_EXTENDED` for the richer note/bookmark capability.
Older legacy materials may refer to `NOTES_BOOKMARKS`.
Until the entitlement-governance file is normalized, implementation should treat the current API contract as authoritative and preserve compatibility awareness in feature code and tests.

## 7.4 Ethical gating rule
Free users must not be prevented from:
- setting a basic plan,
- keeping a reminder-free item when notifications are unavailable,
- attaching a remedy receipt,
- saving basic notes or bookmarks,
- reading their existing records.

## 7.5 Downgrade rule
When a user loses or lacks the extended notes/bookmarks entitlement:
- existing rich notes remain readable,
- unsupported rich features become read-only,
- new edits must respect free caps and field restrictions,
- the app must explain the limitation clearly without pretending data was lost.

---

# 8. Feature architecture overlay

## 8.1 Runtime responsibilities at the feature level
This feature family is responsible for coordinating:
- planner list state,
- planner item editing state,
- reminder scheduling state,
- quiet-hours settings state,
- wallet list/detail/add/export state,
- notes/bookmarks library state,
- capture sheet state,
- itinerary overlay rendering state,
- entitlement-aware premium enrichments,
- analytics emission for this feature family.

## 8.2 What this feature must not own
This feature must not directly own:
- ritual correctness logic,
- group itinerary authority,
- entitlement authority,
- push notification infrastructure,
- cloud sync architecture,
- purchase validation logic,
- map routing or share-pin generation truth.

## 8.3 Required stable interfaces
Feature implementation should depend on stable roles such as:
- `PlannerRepository`
- `ReminderScheduler`
- `PlannerSuggestionEngine`
- `WalletRepository`
- `WalletExportCoordinator`
- `NotesRepository`
- `BookmarksRepository`
- `CaptureContextAdapter`
- `GroupItineraryOverlayAdapter`

These are representative interface roles, not a locked naming requirement.

---

# 9. Persistence posture and local data contracts

## 9.1 Canonical persistence posture
This feature family is primarily device-local.
Planner, reminder metadata, wallet records, notes, bookmarks, exports, and local settings remain on-device by default.

## 9.2 Planner local entity — PlannerItem
The feature must operate against a local planner-item model aligned with the local-first contract.

### Required fields
- `id`
- `date_key`
- optional `time_local`
- `type`
- `title`
- optional `note`
- `notification_enabled`
- optional `source`
- `created_at`
- `updated_at`

### Rules
- `date_key` uses the local-calendar date key format defined elsewhere,
- `time_local` is stored as local clock time rather than forcing server time semantics,
- item existence must not depend on notification success,
- type values must come from centralized enum definitions rather than ad hoc strings.

## 9.3 Reminder schedule metadata
The runtime may persist reminder-scheduling metadata locally such as:
- scheduled notification identifier,
- next fire time,
- quiet-hours adjustment state,
- delivery capability status,
- last scheduling failure code.

This metadata is operational and may be regenerated when necessary.

## 9.4 Wallet local entity — WalletItem
Until a more detailed canonical table shape is expanded in file `13`, this feature family must use the following local feature contract for wallet runtime behavior.

### Required fields
- `id`
- optional `ritual_session_id`
- `kind`
- `title`
- optional `amount`
- optional `currency`
- `artifact_uri`
- optional `notes`
- `created_at`
- optional `updated_at`

### Rules
- wallet items remain local by default,
- `ritual_session_id` is optional except when created through the ritual remedy flow,
- `artifact_uri` must reference a file inside app-managed local storage until exported explicitly,
- wallet is not a finance ledger and must not depend on amount or currency fields for correctness.

## 9.5 Note local entity — Note
This feature family aligns with the local note model already established in legacy and local-first contracts.

### Required fields
- `id`
- `title`
- `body_md`
- optional `source_kind`
- optional `source_ref`
- `created_at`
- optional `updated_at`
- optional `supporter_features_used`

### Rules
- notes remain local-only by default,
- source references must be stable enough to reopen or at least explain origin later,
- free-mode editing supports plain-text-safe subsets even if rich markdown content exists in read-only form.

## 9.6 NoteAttachment local entity
### Required fields
- `id`
- `note_id`
- `mime`
- `uri`
- `size_bytes`
- `created_at`

### Rules
- attachment URIs stay in app-private storage until export/share,
- attachment size limits must be enforced before final save,
- missing or corrupt attachments should not corrupt the parent note.

## 9.7 Bookmark local entity
### Required fields
- `id`
- `kind`
- `ref`
- `title`
- `created_at`

### Rules
- bookmarks are references, not copies of full content,
- bookmarks may point to source objects by `kind + ref` rather than foreign-key coupling,
- the app should tolerate deleted or changed source content and present a sensible fallback when a bookmark target is no longer directly openable.

## 9.8 Indexing and retention rules
The feature family must respect local indexing guidance and local retention expectations:
- planner items indexed by date,
- notes indexed by creation time,
- bookmarks indexed by `(kind, ref)`,
- data retained until the user deletes it,
- no silent purge of notes/bookmarks/planner items/wallet items except under explicit documented recovery flows.

---

# 10. Planner behavior

## 10.1 Purpose
Planner exists to provide a calm daily plan and lightweight reminders relevant to pilgrimage tasks.

## 10.2 Planner scope rule
Planner is not a full productivity suite.
It focuses on pilgrimage-relevant tasks, reminders, and read-only itinerary context.

## 10.3 Core planner capabilities
Planner must support:
- viewing items by day,
- applying a template,
- adding a custom item,
- editing and deleting items,
- enabling or disabling reminders per item,
- viewing quiet-hours behavior,
- reading shared itinerary overlays where available,
- receiving smart suggestions where entitled.

## 10.4 Source categories for planner items
Planner items may originate from:
- built-in templates,
- user-created custom items,
- smart suggestions,
- itinerary overlays,
- feature handoffs such as ritual-context suggestions.

## 10.5 Merge and dedupe rule
Applying a template or smart suggestion must merge into the current plan without creating confusing duplicate clutter.
The feature should dedupe using stable semantics such as matching type, date, time, and note/title where appropriate.

## 10.6 Day-first presentation rule
Planner should present a clear day-focused view before any multi-day complexity.

## 10.7 Seasonal behavior
Planner must be season-aware.
Off-season Umrah behavior must not leak Hajj-only templates or jamarāt overlays.
If `season=umrah`, Umrah template(s) are the primary default.
If `season=hajj`, Hajj day templates and windows may appear where approved.

---

# 11. Templates and supportive suggestions

## 11.1 Template purpose
Templates help a user build a useful plan quickly without typing many custom items.

## 11.2 Template source posture
Templates are local content assets, versioned with content and gated by season.
They are not user-generated cloud objects.

## 11.3 Umrah template rule
In Umrah-first behavior, Planner must default to Umrah-relevant templates and must not surface Hajj-only cards by default.

## 11.4 Hajj template rule
When Hajj scope is active, Planner may show Hajj-day templates and read-only jamarāt window overlays, but these windows remain informational rather than enforcement logic.

## 11.5 Smart suggestions
Supportive suggestions may consider:
- season,
- ritual mode/progress,
- time of day,
- locale,
- pack state,
- user settings,
- group itinerary context where appropriate.

## 11.6 Smart suggestion boundaries
Suggestions must:
- never interrupt ritual-critical screens,
- remain advisory rather than controlling,
- degrade safely when entitlement or context is missing,
- avoid sounding like medical or operational guarantees.

## 11.7 Example suggestion categories
- hydration reminders,
- shade/rest suggestions,
- review an upcoming item,
- review Ifadah-related planning in Hajj context,
- optional pack preparation prompt where appropriate.

---

# 12. Reminders and local-notification behavior

## 12.1 Purpose
Reminders exist to nudge the user at useful times without requiring a server or push pipeline.

## 12.2 Local-notification rule
Reminders are implemented through platform-local notifications or equivalent OS-scheduled local delivery.
They are not remote push notifications.

## 12.3 Permission request rule
Notification permission should be requested in context when the user enables or meaningfully needs reminders.
The app must explain the value clearly before requesting it.

## 12.4 Denied-permission rule
If notification permission is denied:
- the planner item must still be saved,
- the reminder state must explain that OS delivery is unavailable,
- the user should be able to retry permission or continue without reminder scheduling.

## 12.5 Quiet-hours rule
Quiet hours apply to non-urgent personal reminders by default.
Items that fall inside quiet hours should be delayed or handled according to the documented quiet-hours setting rather than forcibly firing inside the quiet period.

## 12.6 Exact-timing rule
This product must not assume universal exact-alarm capability.
For most reminder types, near-timely local delivery is acceptable.
If an OS requires additional permission for exact timing and that permission is unavailable, the feature must degrade gracefully rather than pretend precision is guaranteed.

## 12.7 Boot/app-update restore rule
Scheduled reminders must be rehydrated or restored as needed after app update, restart, or device reboot according to platform capability.

## 12.8 Reminder actions
Where platform support is appropriate, reminders may expose lightweight actions such as:
- mark done,
- snooze,
- open Planner.

## 12.9 Reminder reliability honesty rule
The UI must distinguish between:
- reminder saved and scheduled,
- reminder saved but not scheduled,
- reminder temporarily unable to schedule,
- reminder stale or needs rehydration.

---

# 13. Wallet behavior

## 13.1 Purpose
Wallet keeps pilgrimage-related records, not payment methods or official-service workflows.

## 13.2 Allowed wallet uses
Wallet may store:
- remedy receipts,
- fidyah/dam evidence records,
- service proofs such as wheelchair hire receipts,
- other pilgrimage-relevant reference artifacts explicitly approved by scope.

## 13.3 Add flow
Wallet items may be created from:
- a Rituals/RIC handoff,
- the Wallet list itself,
- supported file/photo import flows.

## 13.4 Supported artifact sources
Wallet add should support:
- camera capture,
- photo picker,
- PDF or file import where platform allows.

## 13.5 Metadata rule
Wallet metadata should remain simple:
- title required,
- kind required,
- amount/currency optional,
- ritual link optional except when created from ritual remedy flow.

## 13.6 Wallet export rule
Wallet export is explicit and user-initiated.
The app may export selected items as a ZIP with a CSV index and included artifacts.

## 13.7 No automatic sharing rule
The app must never auto-upload or auto-share wallet artifacts.

## 13.8 Large-artifact rule
If storage is low or artifact size exceeds budget, the feature must show a clear resolution path rather than silently failing or purging unrelated user data.

## 13.9 Wallet detail behavior
Wallet detail must make it easy to understand:
- what the artifact is,
- when it was added,
- what kind it belongs to,
- whether it links back to a ritual session,
- what actions are available next.

---

# 14. Notes and bookmarks behavior

## 14.1 Purpose
Notes and Bookmarks help the user preserve useful personal context and return to important content quickly.

## 14.2 Bookmarks versus notes rule
Bookmarks are quick saved references.
Notes are user-authored content.
The product must preserve this distinction in UX and analytics.

## 14.3 Capture surfaces
Bookmark and Add Note actions should be consistently available from supported surfaces such as:
- ritual step detail,
- RIC result,
- map anchor/detail contexts where appropriate,
- phrasebook phrase detail,
- emergency cards where approved,
- planner items,
- safety/advisory surfaces where useful.

## 14.4 Capture speed rule
Basic bookmark capture should take one or two steps.
Note capture should remain lightweight enough for real travel use and must not require a full-page form every time.

## 14.5 Source context rule
When a note or bookmark is created from another feature surface, the feature should preserve enough context to reopen or at least explain the original source later.

## 14.6 Attachment rule
Notes may include attachments subject to entitlement and local storage rules.
Attachment failure must not destroy the note draft.

## 14.7 Markdown rule
Rich markdown is an extended capability, not a requirement for baseline note usefulness.
Where markdown is supported, rendering must stay safe, readable, and compatible with export.

## 14.8 Tag rule
Tags are an extended organization capability and must remain simple, lowercase/token-like, and locally searchable.

## 14.9 Library behavior
The notes/bookmarks library should support:
- all-items view,
- notes-only view,
- bookmarks-only view,
- source filters,
- date filters where helpful,
- attachment filter where helpful,
- tag filtering when entitlement allows,
- local search and sort.

## 14.10 Missing-source fallback
If the source content no longer exists or no longer resolves directly, the note or bookmark must still remain readable and the app should explain that the original source is unavailable.

---

# 15. Capture-sheet contract

## 15.1 Purpose
The capture sheet exists to make note/bookmark creation consistent across the product.

## 15.2 Required capabilities
The capture sheet should support:
- inferred title,
- visible source summary,
- plain text note body,
- optional attachment add,
- optional markdown toggle where entitled,
- optional tags where entitled,
- save action,
- cancel/dismiss behavior that preserves draft safety where appropriate.

## 15.3 Module-specific prefill examples
- Rituals may prefill current step or remedy context,
- Maps may prefill short code or saved-anchor summary,
- Phrasebook may prefill phrase text and locale,
- Planner may prefill planner item summary,
- Safety may prefill advisory copy.

## 15.4 Screenshot and photo rule
Screenshots or photos may be attached where platform and policy allow, but the user must remain in control and platform restrictions must be respected.

## 15.5 Draft preservation rule
If attachment selection fails or the sheet is interrupted, the app should preserve draft text where practical.

---

# 16. Read-only itinerary overlay behavior

## 16.1 Purpose
Planner may display group itinerary context because it is useful to the user’s plan, but it is not the authority for that itinerary.

## 16.2 Ownership rule
Group itinerary remains owned by the Group feature family and its trusted data path.
Planner only reads and renders it as supporting context.

## 16.3 Read-only rule
Members do not edit shared itinerary items from Planner in V1.

## 16.4 Stale-state rule
If the itinerary overlay is cached or stale, Planner must show that honestly and must not present it as guaranteed current.

## 16.5 Merge-boundary rule
Shared itinerary items should not silently turn into fully local planner items unless the user explicitly copies or saves them into their own plan.

---

# 17. Export and share behavior

## 17.1 General export rule
Export and sharing are always explicit, user-initiated actions.

## 17.2 Wallet export
Wallet may export selected items as a ZIP bundle with:
- artifact files,
- a CSV index,
- stable filenames where practical.

## 17.3 Notes/bookmarks export
Extended notes/bookmarks capability may export:
- ZIP archive containing CSVs and attachments,
- or a single note as PDF/plain text when appropriate.

## 17.4 Share-sheet rule
Cross-app sharing should use the platform share sheet or equivalent user-controlled system share UI.

## 17.5 Export destination rule
Exports leave app-private storage only through an explicit save/share step controlled by the user.

## 17.6 Security and readability rule
Exported data should be useful outside the app without silently exposing more than the user chose.

## 17.7 No hidden sync rule
Export must not be used as a disguised background backup mechanism.

---

# 18. Screen and UX contract for this feature family

## 18.1 Relationship to screen inventory
This feature family owns or strongly depends on the following canonical screens:
- `planner_list`
- `planner_item_editor`
- `reminder_editor_settings`
- `wallet_list`
- `wallet_item_detail`
- `notes_list`
- `note_editor`
- `bookmarks_list`

It also depends on entry cards and shortcuts in `tools_root` and other feature surfaces.

## 18.2 Planner List UX contract
### Required content blocks
- date header,
- season context badge where relevant,
- template entry surface,
- my plan list,
- itinerary overlay summary where relevant,
- suggestion card(s) where entitled and appropriate.

### Required states
- empty/no items,
- normal content,
- stale itinerary overlay,
- offline fully local state,
- suggestion unavailable,
- notification permission missing reminder hint where relevant.

### Primary actions
- add item,
- apply template,
- open item editor,
- enable/disable reminder,
- open reminder settings.

### Rule
Planner List should feel like a calm agenda, not a dense task-management dashboard.

## 18.3 Planner Item Editor UX contract
### Required content blocks
- title or item type,
- date/time input,
- note field,
- reminder toggle,
- save action,
- delete action when editing existing item.

### Required states
- create new,
- edit existing,
- reminder available,
- reminder unavailable due to permission,
- invalid input,
- save complete.

### Rule
Item creation should remain short and easy on a phone while traveling.

## 18.4 Reminder Editor / Reminder Settings UX contract
### Required content blocks
- reminder enable state,
- reminder timing summary,
- quiet-hours settings,
- explanation when OS permissions are missing,
- retry/open system settings action where helpful.

### Required states
- permission granted,
- permission denied,
- scheduled,
- unscheduled,
- quiet-hours active.

### Rule
The user must understand the difference between a plan item and a successfully scheduled reminder.

## 18.5 Wallet List UX contract
### Required content blocks
- wallet items list,
- add item action,
- filter or group by type where useful,
- export action,
- empty state explanation.

### Required states
- empty,
- content ready,
- low storage warning,
- export in progress,
- export failure.

### Rule
Wallet List should emphasize simple records management, not finance metaphors.

## 18.6 Wallet Item Detail UX contract
### Required content blocks
- item title,
- kind,
- artifact preview or file summary,
- linked ritual context where relevant,
- export/share action,
- delete action.

### Required states
- content ready,
- missing artifact,
- link to ritual unavailable,
- export failure.

### Rule
Detail must stay readable even when the original source ritual session is no longer active.

## 18.7 Notes List UX contract
### Required content blocks
- notes/bookmarks segmented access or tab behavior,
- search field,
- filters,
- sort control,
- item list,
- add note action.

### Required states
- empty,
- content ready,
- filtered empty,
- offline local state,
- free-cap reached state,
- downgrade read-only state where relevant.

### Rule
Notes List must help retrieval quickly rather than celebrate quantity of saved content.

## 18.8 Note Editor UX contract
### Required content blocks
- title,
- body input,
- source summary,
- attachment controls,
- tags where entitled,
- markdown mode where entitled,
- save action.

### Required states
- create,
- edit,
- attachment add/remove,
- attachment failure,
- cap reached,
- unsupported premium field due to downgrade.

### Rule
Editor must support quick capture first and deeper editing second.

## 18.9 Bookmarks List UX contract
### Required content blocks
- bookmarks list,
- source pill or label,
- open source action,
- sort/filter controls,
- empty state.

### Required states
- empty,
- content ready,
- missing source fallback,
- offline local state.

### Rule
Bookmarks should feel lightweight and navigational, not like full documents.

---

# 19. Copy, localization, RTL, and accessibility rules

## 19.1 Copy tone
Copy for this feature family must be:
- direct,
- calm,
- practical,
- privacy-aware,
- not productivity-jargon heavy.

## 19.2 Planner copy style
Reminders and planner copy should use short supportive prompts such as:
- “Time to drink water.”
- “Find shade and rest.”
- “Review your plan.”

## 19.3 Wallet copy style
Wallet copy should avoid payment language.
Prefer phrases like:
- “Add receipt”
- “Save record”
- “Export selected items”

## 19.4 Notes copy style
Note and bookmark copy should stay lightweight and calm.
Avoid social or cloud-sync implications.

## 19.5 RTL and mixed-content rule
Times, dates, gate codes, short codes, amounts, and mixed-language content must remain bidi-safe and readable in RTL contexts.

## 19.6 Accessibility requirements
This feature family must support:
- large text,
- strong focus order,
- screen-reader labels for reminder toggles and export actions,
- non-color-only state communication for reminder scheduled/unscheduled status,
- readable list density,
- reduced-motion-safe transitions,
- keyboard and assistive-technology friendly note editing where supported.

## 19.7 Attachment accessibility rule
Attachment previews must have meaningful labels and must not be the only place where the user can understand what the record refers to.

---

# 20. Offline behavior and degraded states

## 20.1 Offline tier
This feature family is strongly local-first and should remain highly usable offline.

## 20.2 Offline guarantees
The following must work meaningfully offline:
- Planner item creation and editing,
- local reminder state management,
- template application using installed/local content,
- Wallet add and view for local artifacts,
- Notes and bookmarks CRUD,
- local search/filter over notes/bookmarks,
- viewing previously cached itinerary overlay marked stale when necessary.

## 20.3 Network-independent rule
The absence of internet must never erase or block the user’s local personal-tool data.

## 20.4 Degraded online-support rule
If entitlement refresh, group itinerary fetch, or other supportive online context is unavailable, the feature should continue with last-known safe local state and mark supportive overlays stale when needed.

## 20.5 Storage-pressure rule
When storage pressure threatens attachments or exports, the feature must offer a clear resolution path such as deleting old artifacts or purging packs. It must not silently purge notes, bookmarks, planner items, or wallet records.

---

# 21. Security and privacy rules for this feature family

## 21.1 Local privacy rule
Personal tools data remains local unless the user explicitly exports or shares it.

## 21.2 No background sync rule
The feature must not implement hidden backup, sync, or cross-device propagation.

## 21.3 Minimal permission rule
This feature family should request only relevant permissions, such as notification permission when reminders are enabled and media/file access when the user adds an attachment.
It must not request irrelevant permissions.

## 21.4 Notification honesty rule
The app must not imply notification delivery is guaranteed when OS policies, permission, or device state can prevent it.

## 21.5 File handling rule
Artifact and attachment files should remain in app-managed storage until user-driven export or share occurs.

## 21.6 Sensitive logging rule
Do not log note content, exported payloads, wallet artifact contents, or personal attachment names recklessly in analytics or diagnostics.

---

# 22. Performance and operational rules for this feature family

## 22.1 Performance authority
Global performance budgets are defined normatively in file `17`.
This feature family must obey them.

## 22.2 Feature-level targets
Recommended feature-level operational targets:
- planner day view initial render ≤ **400 ms** on representative mid-tier devices,
- scheduling 10 reminders ≤ **150 ms** on representative mid-tier devices,
- wallet export ZIP for 10 items ≤ **2 s** on representative mid-tier devices,
- notes library open ≤ **400 ms** with 200 items,
- markdown note render ≤ **120 ms** for a moderate note on representative mid-tier devices,
- ZIP export for larger note sets should remain within a few seconds and fail gracefully if resource limits are hit.

## 22.3 Reliability priorities
This feature family must optimize for:
- fast local CRUD,
- clear reminder state,
- stable export behavior,
- offline retrieval speed,
- graceful degradation before failure.

---

# 23. Analytics and observability requirements

## 23.1 Required analytics events
This feature family must emit the canonical events defined in file `17`, including at minimum:
- `planner_item_create`
- `planner_item_complete`
- `planner_item_delete`
- `planner_suggestion_view`
- `wallet_item_create`
- `wallet_item_open`
- `wallet_export_start`
- `notes_item_create`
- `bookmark_create`

## 23.2 Required feature parameters where relevant
- `season`
- `item_type`
- `reminder_enabled`
- `suggestion_kind`
- `wallet_kind`
- `source_kind`
- `has_attachment`
- `extended_features_enabled`
- `network_state`

## 23.3 Privacy-light analytics rule
Do not capture freeform note content, wallet artifact contents, personal attachment filenames, or other private user-authored text as analytics parameters.

## 23.4 Observability priorities
High-signal issues include:
- reminder scheduling failures,
- quiet-hours scheduling regressions,
- wallet export failures,
- attachment import failures,
- free-cap/downgrade logic mismatches,
- local migration failures for planner/notes/bookmarks/wallet data.

---

# 24. Testing and validation requirements

## 24.1 Required automated coverage
Automated tests must cover at minimum:
- planner template merge and dedupe,
- planner item CRUD,
- reminder scheduling state transitions,
- quiet-hours behavior,
- denied-permission fallback,
- wallet add/link/export behavior,
- note and bookmark CRUD,
- source-context capture,
- free-cap and downgrade behavior,
- markdown sanitation/render preparation,
- tag tokenization where entitled,
- export ZIP contents and CSV shape,
- stale itinerary overlay rendering,
- local migration behavior for these models.

## 24.2 Required manual/device validation
Manual or device validation must cover at minimum:
- creating planner items and reminders offline,
- notification permission denied then later granted,
- reminder survival across reboot/app restart where platform permits,
- applying Umrah template off-season,
- Hajj-only cards hidden in Umrah mode,
- RIC-to-Wallet handoff,
- wallet add from camera/photo/file,
- notes capture from Rituals/Maps/Phrasebook/Planner,
- large-text note and planner usability,
- RTL handling for time/date/mixed-content labels,
- downgrade from extended notes/bookmarks entitlement.

## 24.3 Real-world validation requirement
Before release, representative field testing should validate:
- reminder usefulness in normal travel conditions,
- note/bookmark capture speed under stress,
- itinerary overlay clarity,
- wallet proof retrieval speed,
- graceful offline behavior without network.

## 24.4 Fake-success warning
A passing note CRUD test is not enough evidence.
Release confidence requires reminder permission handling, reboot resilience, export correctness, offline use, and downgrade behavior.

---

# 25. Definition of done for this feature family

This feature family is not ready for release unless all of the following are true:
- Planner works meaningfully offline,
- reminders remain useful without assuming remote push,
- denied notification permission does not destroy plan creation,
- Wallet remains a local records tool and export is explicit,
- RIC-to-Wallet handoff works where applicable,
- Notes and bookmarks capture consistently from supported modules,
- free and Supporter boundaries behave ethically and correctly,
- downgrade behavior remains readable and safe,
- itinerary overlays stay read-only and freshness-aware,
- analytics hooks align with file `17`,
- real-device validation confirms the feature family reduces stress rather than adding cognitive load.

---

# 26. Cross-file dependency rules

## 26.1 If planner or reminder local model changes
Update:
- this file,
- file `13`,
- relevant tests/fixtures,
- file `11` where screen state changes.

## 26.2 If wallet artifact/export behavior changes
Update:
- this file,
- file `13` if data shape changes,
- file `17` if analytics or budgets change,
- file `28` if release evidence expectations change.

## 26.3 If notes/bookmarks entitlement behavior changes
Update:
- this file,
- file `24` or entitlement-governance authority,
- file `14` if entitlement response gates change,
- tests and downgrade scenarios.

## 26.4 If capture surfaces change
Update:
- this file,
- the relevant source feature-family file(s),
- file `11` if screen actions change,
- analytics mappings if event semantics change.

## 26.5 If itinerary overlay behavior changes
Update:
- this file,
- file `20`,
- file `14` if read shape or caching semantics change,
- file `13` if persistence strategy changes.

---

# 27. Anti-patterns forbidden by this document

The following are forbidden unless explicitly approved.

## 27.1 Turning Planner into a full productivity suite
Forbidden.

## 27.2 Depending on push infrastructure for baseline reminder usefulness
Forbidden.

## 27.3 Treating Wallet as a payment or identity wallet
Forbidden.

## 27.4 Hidden sync or backup of notes, planner items, wallet artifacts, or bookmarks
Forbidden.

## 27.5 Auto-sharing exported or captured personal data
Forbidden.

## 27.6 Making note and bookmark capture inconsistent across feature surfaces
Forbidden.

## 27.7 Hiding reminder failure behind a fake “scheduled” state
Forbidden.

## 27.8 Using premium prompts in ways that block baseline personal organization or remedy evidence capture
Forbidden.

## 27.9 Silently purging user-private personal-tool data during storage pressure
Forbidden.

## 27.10 Reintroducing Hajj-specific planner surfaces into Umrah-first default behavior without season scope
Forbidden.

---

# 28. Implementation priorities

## 28.1 Phase 1 priorities
Implement first:
- Planner local model and CRUD,
- reminder scheduling with permission-aware fallback,
- Umrah-first template application,
- Wallet add/link/export baseline,
- basic Notes and Bookmarks local model and capture sheet,
- local library/search for notes and bookmarks.

## 28.2 Phase 2 priorities
Then add:
- itinerary overlay rendering,
- richer RIC handoff polish,
- extended notes/bookmarks capability,
- smart planner suggestions,
- richer export options.

## 28.3 Phase 3 priorities
Then refine:
- smarter dedupe and suggestion quality,
- device-specific optimization for export and attachment handling,
- deeper capture-context polish across more surfaces,
- post-downgrade readability and archival polish.

---

# 29. When this file must be updated

This file must be updated whenever any of the following changes:
- planner item behavior,
- reminder scheduling posture,
- quiet-hours rules,
- wallet model or export behavior,
- note/bookmark data or entitlement behavior,
- capture surfaces,
- itinerary overlay behavior,
- local privacy/export posture,
- analytics hooks for these personal tools,
- release-readiness expectations tied to reminders, wallet, notes, or bookmarks.

If these truths change but this file is not updated, implementation and QA will drift quickly.

---

# 30. Summary

This file defines the canonical feature-facing contract for Planner, Reminders, Wallet, Notes, and Bookmarks in Pilgrims Mobile App.

It establishes:
- the purpose and boundaries of the personal-tools family,
- the local-first data and privacy posture,
- planner and reminder behavior,
- wallet record and export behavior,
- notes/bookmarks capture and library behavior,
- itinerary overlay boundaries,
- free versus Supporter enrichment rules,
- screen contracts,
- required analytics, testing, and release-readiness expectations.

Its purpose is to ensure the personal-tools layer becomes:
- calm,
- reliable offline,
- privacy-light,
- ethically monetized,
- and maintainable for long-term AI-assisted implementation.

