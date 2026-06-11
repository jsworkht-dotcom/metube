# Current UI Manual Review Checklist

## Purpose

This checklist prepares a manual UI review for the local-only MeTube UI after
the quality selector and completed/result table label improvements.

The review focus is the add/download form, video and audio quality selectors,
quality helper popovers, and completed/result table quality display. This is a
review-preparation document only; it does not change UI behavior, backend
behavior, download behavior, or local-only policy.

## Review Status

```text
status: checklist-ready / screenshots-not-yet-captured
```

Screenshots are not captured in this task. This document does not assert visual
pass/fail, layout correctness, or screenshot evidence. A later manual review
should capture screenshots and record findings below.

## Scope

- Add/download form
- Video quality selector
- Audio quality selector
- Quality helper popovers
- Completed/result table
- Result table `品質` column
- Captions / thumbnail quality display
- Mobile/narrow-width readability, if applicable
- Japanese label consistency

## Screenshot Checklist

- [ ] Screenshot: initial add form
- [ ] Screenshot: video quality selector opened
- [ ] Screenshot: video quality helper popover
- [ ] Screenshot: audio quality selector opened
- [ ] Screenshot: audio quality helper popover
- [ ] Screenshot: completed/result table with video row
- [ ] Screenshot: completed/result table with audio row
- [ ] Screenshot: completed/result table with captions/thumbnail row if available
- [ ] Screenshot: narrow-width layout

## Expected UI Wording

Video selector/result labels:

- `最高画質（自動）`
- `4K（2160p）`
- `高画質（1440p）`
- `フルHD（1080p）`
- `標準（720p）`
- `軽量（480p）`
- `低容量（360p）`
- `最小（240p）`

Additional current video option/result fallback observed in the UI code:

- `最低画質（自動）`

Audio selector/result labels:

- `最高音質（自動）`
- `高音質（320kbps）`
- `標準（192kbps）`
- `軽量（128kbps）`

Notes:

- `高音質（320kbps）` is format-dependent and appears for MP3.
- M4A currently offers `最高音質（自動）`, `標準（192kbps）`, and
  `軽量（128kbps）`.
- OPUS, WAV, and FLAC currently offer `最高音質（自動）`.

Other:

- Audio selector label: `音質`
- Result table header: `品質`
- Captions/thumbnail quality value: `-`

Helper popover wording to review:

- Video helper should explain quality targets / upper limits, source-quality
  fallback, auto mode, and file-size tradeoff.
- Audio helper should explain quality/file-size tradeoff, lightweight 128kbps,
  and auto mode.

## Pass/Fail Checklist

- [ ] Labels are readable in Japanese.
- [ ] Numeric values are visible where useful.
- [ ] `画質` is not used for audio quality.
- [ ] `品質` column is understandable in the completed/result table.
- [ ] Popovers do not cover critical controls awkwardly.
- [ ] Higher quality/file-size meaning is understandable.
- [ ] Captions/thumbnails do not show misleading quality.
- [ ] No backend/download behavior is implied to change.
- [ ] No public hosting/ads/update wording appears.
- [ ] Local-only wording remains consistent.

## Findings

### Finding 1

- status:
- screen:
- issue:
- evidence:
- suggested next task:
- risk:

## Next Task Decision

If screenshots show copy/layout issues:

- Create a new High-mid frontend UI copy/layout PR.

If only docs need updating:

- Create a docs-only PR.

If no issues:

- Close as review-complete docs-only.

Safety-gate policy support remains separate and should not be bundled with UI
review.
