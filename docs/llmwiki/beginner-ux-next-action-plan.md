# Beginner UX Next-Action Plan

## Purpose

Y-UX-PLAN-01 defines the next safe beginner UX planning lane after the
artifact-generation decision was placed on hold.

This is docs-only planning. It does not change frontend code, backend code,
runtime behavior, package generation, distribution output, or GitHub settings.

## Y-DIST-08 Result

Y-DIST-08 result:

- artifact generation remains HOLD;
- all artifact categories remain not approved;
- the next safe path is low-risk UX/docs/report/checker planning.

Artifact generation, ZIP/package/installer output, CLEAN folder creation,
metadata generation, checksum generation, real download verification, and
recipient handoff remain blocked until a later explicit human-reviewed lane
approves them.

## Current UX Baseline

- Japanese-localized UI exists.
- Local-only safety posture exists.
- Beginner guide source docs exist.
- Package generation remains blocked.

Current source references:

- `docs/llmwiki/current-ui-manual-review-checklist.md`
- `docs/llmwiki/current-ui-screenshot-review-findings.md`
- `docs/llmwiki/beginner-guide-skeleton.md`
- `docs/llmwiki/beginner-guide-source-plan.md`
- `docs/llmwiki/package-guides/00-first-open.html.source.md`
- `docs/llmwiki/package-guides/03-how-to-use.html.source.md`
- `docs/llmwiki/package-guides/04-troubleshooting.html.source.md`
- `docs/llmwiki/package-guides/05-safe-use.html.source.md`

## UX Principles

- local-only first;
- personal-use only;
- no public hosting;
- no credential/cookie/token guidance;
- no DRM/auth/restriction bypass language;
- beginner-friendly wording;
- stop/quit clarity;
- save-folder clarity;
- error next-action clarity.

Beginner-facing work should keep Japanese wording short, concrete, and
action-oriented. It should favor "what to do next" over technical explanation
and should preserve the existing local-only safety posture.

## Y-UX-COPY-01 Safe-Use Microcopy Review

Y-UX-COPY-01 reviews safe-use microcopy for beginner-facing UX. This section is
docs-only planning. It does not change frontend copy, backend behavior, runtime
behavior, package output, generated folders, or GitHub settings.

The review covers wording for:

- local-only safety;
- personal-use scope;
- allowed-use and not-allowed-use boundaries;
- stop/quit guidance;
- save-folder guidance;
- error next actions;
- help and troubleshooting entry points;
- update-status safety wording.

### Current Copy Baseline

- Japanese-localized UI exists.
- Beginner guide source docs exist.
- Y-UX-PLAN-01 created this beginner UX planning baseline.
- Artifact generation remains HOLD.
- Beginner guide source planning already keeps local-only, personal-use,
  save-folder, stop/quit, troubleshooting, and safe-use boundaries visible.

### Microcopy Principles

- Put local-only scope first.
- Say personal-use only.
- Tell users to use only content they are allowed to save.
- Do not mention or invite cookie/token/secret use.
- Do not describe DRM/auth/restriction bypass.
- Do not normalize public hosting or external-user service use.
- Use short, calm, beginner-friendly Japanese.
- Give the next safe action.
- Avoid blame, pressure, or fear-based copy.

### Recommended Wording Families

Local-only notice:

```text
このツールは、このパソコンの中だけで使うローカル専用ツールです。
```

Allowed-use notice:

```text
自分の動画、許可を得た動画、保存してよい動画だけに使ってください。
```

Not-allowed-use notice:

```text
公開サービス化、広告収益化、制限回避、認証回避のためには使いません。
```

Save-folder guidance:

```text
保存が終わったら「保存先を開く」から確認できます。
```

Stop/quit guidance:

```text
保存中は完了を待ってから終了してください。迷ったら「停止して終了」を使います。
```

Error next-action guidance:

```text
うまくいかない場合は、エラー文を残して、もう一度だけ試してください。
```

Troubleshooting entry guidance:

```text
困ったときは「困ったとき」を開き、今見えているエラー文を残してください。
```

Update-status safety wording:

```text
更新情報は確認用です。更新が必要そうな場合は、案内が出るまで待ってください。
```

### Avoid Wording Families

Avoid these wording families in beginner-facing copy:

- bypass
- unlock
- unrestricted
- hidden
- cookie upload guidance for beginner flow
- token/secret handling
- public access
- share with others
- auto-update now
- force update
- mass download optimization

The intent is not to hide safety limits. The copy should name the safe boundary
plainly, then give one safe next action.

### Review Notes By Surface

First-open and local-only notices should answer "where does this run?" before
any feature detail. Keep the first sentence local and concrete.

Allowed-use copy should be positive and short. Prefer "save only content you
are allowed to save" over legalistic or fearful wording.

Not-allowed-use copy should stay calm and categorical. It should not explain
methods or offer alternate paths.

Save-folder copy should point to the visible "保存先を開く" action and avoid
internal runtime paths.

Stop/quit copy should tell the user what to do while saving is active. The
preferred beginner phrase is "停止して終了" when the app provides that action.

Error copy should preserve the error text and allow one retry. After that, it
should move the user to help/troubleshooting rather than advanced repair steps.

Troubleshooting entry copy should make "困ったとき" the safe next place, not a
developer workflow.

Update-status copy should be readonly. It may say that information is available
for checking, but it should not suggest immediate update execution in the
beginner flow.

### Next Implementation Boundaries

Docs-only review:

- allowed now;
- may update LLMwiki planning, roadmap, and handoff docs;
- may collect candidate copy;
- must not change runtime UI files.

Frontend copy-only implementation:

- later separate lane;
- `ui/**` files must be explicitly scoped;
- no dependency, build, package, generated output, or runtime behavior changes.

Runtime behavior:

- later separate lane;
- not part of Y-UX-COPY-01.

### Explicitly Not Performed

Y-UX-COPY-01 does not perform:

- frontend code changes;
- backend code changes;
- runtime behavior changes;
- artifact generation;
- generated package output;
- CLEAN folder creation;
- metadata or checksum generation;
- real download verification;
- recipient handoff or sharing;
- dependency installation operations;
- container image operations;
- `.github/workflows/` changes;
- GitHub settings mutation;
- `.gitignore` changes;
- credential-bearing file handling;
- secret-like value handling;
- public exposure operations;
- DRM/auth/restriction bypass guidance.

## Y-UI-QUALITY-01 Quality / Label Review

Y-UI-QUALITY-01 reviews beginner-facing quality, format, and label wording as a
docs-only follow-up after Y-UX-COPY-01. This section does not change runtime UI
files, selector behavior, backend behavior, package output, generated folders,
or GitHub settings.

Repo-history note: earlier implementation lanes named `Y-UI-QUALITY-01`,
`Y-UI-QUALITY-02`, and `Y-UI-QUALITY-03` are complete. This review preserves
their runtime behavior and only records the next docs-only label planning
surface.

### Current UI Label Baseline

- Japanese-localized UI exists.
- Video, audio, captions, and thumbnail types exist.
- Quality, format, codec, and captions controls exist.
- Y-UX-COPY-01 created the safe-use wording baseline.
- Artifact generation remains HOLD.
- Existing quality UI work kept option ids, payloads, backend validation, and
  download behavior stable.

### Review Principles

- Use beginner-first labels.
- Use short Japanese labels.
- Keep numeric quality visible where useful.
- Keep advanced codec and format details from dominating the beginner path.
- Do not imply bypass, unrestricted saving, or guaranteed availability.
- Explain that unavailable quality depends on the original source.
- Avoid copy that encourages mass download or restriction bypass.

### Label Families To Review

- `種類`
- `画質`
- `音質`
- `形式`
- `コーデック`
- `字幕の種類`
- `言語`
- `自動開始`
- `取得数の上限`
- `詳細設定`

### Candidate Wording

Video quality:

```text
自動
標準
高画質
最高画質
720p
1080p
```

Audio quality:

```text
自動
標準
高音質
軽量
```

Format:

```text
おまかせ
MP4
音声のみ
字幕
サムネイル
```

Codec:

```text
おまかせ
互換性重視
高効率
上級者向け
```

Help text:

```text
元の動画にない画質は選べません。
高画質ほどファイルサイズが大きくなることがあります。
迷ったら「自動」または「標準」を選んでください。
```

### Advanced Label Boundary

Beginner-visible labels should stay short and task-focused. Codec families,
container details, extractor-specific labels, batch-count tuning, and advanced
format constraints should stay behind advanced settings unless a later UI lane
explicitly scopes them.

Advanced copy should still avoid promising unavailable quality, unrestricted
saving, or restriction bypass. If a label cannot be made beginner-safe, keep it
outside the beginner path and pair it with a calm help note.

### Next Implementation Boundaries

Docs-only label review:

- allowed now;
- may update LLMwiki planning, roadmap, and handoff docs;
- may collect candidate label copy;
- must not change runtime UI files.

Frontend copy-only implementation:

- later separate lane;
- `ui/**` files must be explicitly scoped;
- no dependency, build, package, generated output, or runtime behavior changes.

Selector behavior changes:

- later separate lane;
- not part of Y-UI-QUALITY-01.

### Explicitly Not Performed

Y-UI-QUALITY-01 does not perform:

- frontend code changes;
- backend code changes;
- runtime behavior changes;
- artifact generation;
- generated package output;
- CLEAN folder creation;
- metadata or checksum generation;
- real download verification;
- recipient handoff or sharing;
- dependency installation operations;
- container image operations;
- `.github/workflows/` changes;
- GitHub settings mutation;
- `.gitignore` changes;
- credential-bearing file handling;
- secret-like value handling;
- public exposure operations;
- DRM/auth/restriction bypass guidance.

## Y-UX-HELP-01 Help / Troubleshooting Entry Review

Y-UX-HELP-01 reviews beginner-facing help and troubleshooting entry points as a
docs-only follow-up after Y-UI-QUALITY-01. This section does not change runtime
UI files, backend behavior, package output, generated folders, or GitHub
settings.

### Current Help Baseline

- Beginner guide source docs exist.
- Troubleshooting source docs exist.
- Y-UX-COPY-01 created the safe-use wording baseline.
- Y-UI-QUALITY-01 created the quality and label review baseline.
- Artifact generation remains HOLD.
- Current guide source planning already includes first-open, usage,
  troubleshooting, and safe-use surfaces.

### Review Principles

- Use beginner-first help entry labels.
- Use short Japanese labels.
- Give one safe next action per error.
- Avoid advanced repair commands in the beginner flow.
- Do not ask for cookies/tokens/secrets.
- Do not suggest public hosting or LAN exposure.
- Do not describe DRM/auth/restriction bypass.
- Prefer "stop and preserve the message" over risky repair steps.
- Help text should reduce confusion, not invite unsafe experimentation.

### Help Entry Families To Review

- `使い方`
- `困ったとき`
- `安全な使い方`
- `保存先を開く`
- `停止して終了`
- `状態を確認`
- `エラー文を残す`
- `もう一度だけ試す`

### Candidate Wording

Help:

```text
使い方を見る
困ったとき
安全な使い方
```

Troubleshooting:

```text
うまくいかない場合は、表示されたエラー文を残してください。
保存中の場合は、完了するまで待ってから操作してください。
保存先が分からない場合は「保存先を開く」を使ってください。
終了に迷った場合は「停止して終了」を使ってください。
何度も失敗する場合は、無理に設定を変えず、エラー文を確認してください。
```

Local-only safety:

```text
このツールはローカル専用です。公開サービスとして使いません。
Cookie、token、secretなどの情報を入力・共有しないでください。
```

### Troubleshooting Priority

1. Preserve the visible error/status message.
2. Check whether a save is currently running.
3. Open the save folder if completion is unclear.
4. Retry once only when safe.
5. Stop and ask for help if the same problem repeats.

### Review Notes By Surface

Help entry labels should map to visible beginner actions. Prefer "使い方を見る",
"困ったとき", and "安全な使い方" over broad technical labels.

Error next-action wording should first preserve the visible message. It should
then offer one safe action, such as waiting for an active save, opening the save
folder, or retrying once only when the action is safe.

Save-folder help should point to "保存先を開く" and avoid internal runtime paths.

Stop/quit help should point to "停止して終了" when the user is unsure. It should
not frame quitting as a risky technical operation.

Local-only safety help should state the boundary plainly. It should not invite
credential-bearing file handling, public exposure operations, or bypass
guidance.

Beginner-safe escalation should tell the user to stop, preserve the message,
and ask for help when the same problem repeats.

### Next Implementation Boundaries

Docs-only help review:

- allowed now;
- may update LLMwiki planning, roadmap, and handoff docs;
- may collect candidate help and troubleshooting copy;
- must not change runtime UI files.

Frontend copy-only implementation:

- later separate lane;
- `ui/**` files must be explicitly scoped;
- no dependency, build, package, generated output, or runtime behavior changes.

Runtime behavior:

- later separate lane;
- not part of Y-UX-HELP-01.

### Explicitly Not Performed

Y-UX-HELP-01 does not perform:

- frontend code changes;
- backend code changes;
- runtime behavior changes;
- artifact generation;
- generated package output;
- CLEAN folder creation;
- metadata or checksum generation;
- real download verification;
- recipient handoff or sharing;
- dependency installation operations;
- container image operations;
- `.github/workflows/` changes;
- GitHub settings mutation;
- `.gitignore` changes;
- credential-bearing file handling;
- secret-like value handling;
- public exposure operations;
- DRM/auth/restriction bypass guidance.

## Next UX Candidates

- `Y-UX-STATE-01 status / progress / completion clarity review`
- `Y-UX-STOP-01 stop/quit user-flow design`

Repo-history note: earlier `Y-UI-QUALITY-01`, `Y-UI-QUALITY-02`, and
`Y-UI-QUALITY-03` lanes are already complete. If a new implementation PR starts
from the quality selector / label review candidate, use a non-colliding follow-up
lane name while keeping the candidate intent.

## Recommended First Next Lane

Recommended first next lane:

- `Y-UX-STATE-01 status / progress / completion clarity review` docs-only; or
- frontend copy-only implementation if explicitly scoped later.

Repo-history note: because historical `Y-UI-QUALITY-01` is already complete in
this fork, prefer a fresh quality selector / label review follow-up lane name
if implementation starts.

Prefer frontend copy-only implementation only if the next task explicitly scopes
UI files and accepts the human-reviewed frontend lane.

## Risk Boundaries

Docs-only UX planning:

- allowed via fast safe flow;
- may update LLMwiki planning, roadmap, and handoff docs;
- must not generate artifacts or change runtime behavior.

Frontend copy-only implementation:

- later separate lane;
- requires UI files explicitly scoped;
- no package/build/dependency changes.

Runtime behavior changes:

- later separate lane;
- not part of Y-UX-PLAN-01.

## Explicitly Not Performed

Y-UX-PLAN-01 does not perform:

- frontend code changes;
- backend code changes;
- runtime behavior changes;
- artifact generation;
- `動画保存ツール_ローカル専用/` creation;
- generated package output;
- metadata generation;
- checksum generation;
- real download verification;
- recipient handoff or sharing;
- dependency installation operations;
- container image operations;
- `.github/workflows/` changes;
- GitHub settings, branch protection, ruleset, required-check, or CODEOWNERS
  mutation;
- `.gitignore` changes;
- cookie/token/secret/credential handling;
- public exposure operations or non-loopback exposure;
- DRM/auth/restriction bypass guidance.

## Handoff Sync

PR #105 completed Y-DIST-08 no-generation hold. PR #106 completed
Y-UX-PLAN-01. PR #107 completed Y-UX-COPY-01. PR #108 completed
Y-UI-QUALITY-01. Y-UX-HELP-01 reviews help and troubleshooting entry wording as
the next docs-only planning step:

- artifact generation remains blocked;
- fast safe flow is the default for low-risk docs/report/checker lanes;
- beginner UX work should start with safe planning before any UI implementation;
- future UI copy-only work remains a separate human-reviewed lane unless later
  safety-gate policy explicitly changes.
