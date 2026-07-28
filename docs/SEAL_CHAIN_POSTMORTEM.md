# Postmortem — a rename broke our cryptographic seal chain for 19 days

| Field | Value |
|---|---|
| **Document** | Engineering postmortem, written for an external audience |
| **Status** | LIVE (roadmap DOC-3) |
| **Date** | 2026-07-28 |
| **Incident window** | 2026-06-30 → 2026-07-19 (19 days) |
| **Severity** | Fail-closed. No incorrect result was produced or published; the sealed pipeline simply could not run. |
| **Primary sources** | [`M4_ERRATUM_2026-07-19.md`](../research/m4_evaluation/M4_ERRATUM_2026-07-19.md) §2.10 · [`decisions/F1_DECISION_RECORD.md`](./decisions/F1_DECISION_RECORD.md) §5a · fix commit `db710aa` |

---

## 1. Context: what the seal chain is for

VESPER is a pre-registered study. Its central anti-tuning guarantee is that thresholds are derived on a calibration set, **sealed**, and then never touched — the test set is read exactly once, against frozen parameters.

"Sealed" is enforced mechanically, not by discipline:

- The derived thresholds live in a JSON manifest (`m3_threshold_manifest_SEALED_CORE.json`).
- The manifest's SHA-256 is recorded as a **literal constant in the loader code** (`seal_loader.SEAL2_SHA256`).
- Every run calls `verify_seal()` first. Digest mismatch → **hard exit**. There is no override flag.
- The values are then handed out through a `@dataclass(frozen=True)`, so no downstream code can reassign a threshold even in memory.

The design is deliberately fail-closed: if anyone edits a sealed value, nothing runs at all. That property is what makes the pre-registration claim checkable by a stranger rather than merely asserted.

## 2. What happened

On **2026-06-30** the project was renamed from `TRINETRA-X` to `VESPER` — the old codename was already in use elsewhere. The rename was executed as a repository-wide string substitution plus file/folder renames, and shipped as public release `v1.0.0`.

The rename was genuinely cosmetic in scientific terms. It changed no algorithm, equation, threshold, result, or figure. `F1_DECISION_RECORD.md` §5a had even **anticipated** that the substitution would alter the recorded digests, and said so explicitly.

What nobody anticipated was the second-order effect. The project name appeared *inside* the sealed manifests — in provenance and description fields. Substituting it changed those files' bytes, and therefore their SHA-256 digests. But the digest literals **in the loader code were not updated to match**.

From that moment:

```
verify_seal()            -> SystemExit: seal drift
verify_v3_manifest()     -> SystemExit: v3 manifest drift
```

Every sealed-pipeline entry point in the repository fail-closed on every invocation, for **19 days**.

## 3. Why it stayed hidden for 19 days

Because nothing exercised it. The single sealed test run (P-5, the one irreversible read) had already been executed on **2026-06-24**, six days *before* the rebrand, using the then-correct digests. The period after the rename was spent on documentation, packaging, and public release — no sealed pipeline invocation occurred.

So the breakage was **latent, not silent-wrong**: the guard never fired because the guard was never called. It was found on 2026-07-19, during a full project audit, when the first post-rebrand attempt to run the sealed machinery hit the wall immediately.

This is the uncomfortable part of the story. A fail-closed guard that is never invoked provides no signal that it is broken. The absence of failures was mistaken for health, when it was actually the absence of tests.

## 4. Root cause

**A rename operation crossed a trust boundary the seal design assumed was immutable.**

More precisely, three decisions combined:

1. **Mutable presentation data was stored inside the sealed artifact.** The manifests carried human-facing project-name strings alongside the scientific parameters. Only the parameters needed sealing; the branding did not. Hashing the whole file made a cosmetic field load-bearing.
2. **The digest was pinned in code as a bare literal**, with no recorded provenance explaining what it pinned or when it was set — so a repo-wide substitution had no reason to consider it, and no automated check tied the two together.
3. **No CI job ever ran `verify_seal()`.** The guard's own correctness was untested. Nothing in the repository would go red if seal verification broke.

Contributing factor: the rebrand was performed by a wide mechanical substitution across all file types. Such an operation is exactly the kind that should be forbidden from touching sealed artifacts, and nothing forbade it.

## 5. The fix (2026-07-19, commit `db710aa`)

The obvious "fix" — update the literal to the new digest — was rejected. Silently repointing a seal to whatever the file happens to contain now is indistinguishable from tampering, which is precisely what the seal exists to rule out.

Instead:

1. **Each post-rebrand manifest was verified byte-identical to its `phase1-prereg-v3` tag version modulo pure branding strings.** The evidence, not the intent, established that only the name had changed.
2. **Both digests are now accepted**, each annotated with its provenance:

```python
SEAL2_SHA256S = {
    "6292c018...0832692",  # sealed (pre-rebrand)
    "5baf15df...a453d38",  # post-rebrand, content-verified
}
```

3. The same dual-digest treatment was applied to the v3 manifest in `m4_driver.verify_v3_manifest`.
4. The original sealed bytes remain recoverable at tags `phase1-prereg-v2` / `phase1-prereg-v3`, which are untouched. Anyone can re-derive both digests and re-run the branding-normalized comparison independently.

Verified working as of 2026-07-28: `verify_seal()` returns the post-rebrand digest `5baf15df…` and loads the sealed values `z⋆=3.4 · z_mono=5.3 · N_min=2 · T=10.741 · α_FAP=0.01 · B=1000`, matching the sealed record exactly.

## 6. What this cost, and what it did not

**It did not corrupt any result.** The sealed test run predates the rebrand and is preserved verbatim. No threshold changed. No figure changed. The anti-tuning guarantee is intact and independently checkable: `git diff phase1-prereg-v3` over the sealed documents is empty modulo branding strings.

**What it cost** was 19 days of a false sense of security, and the discovery — during an audit rather than from a red build — that the project's single most important safety mechanism had no test.

There is a second, subtler cost worth naming: the incident revealed that "the digests changed, this is expected" had been written down in DR-001 §5a *before* the rebrand, and that writing it down was mistaken for handling it. A documented hazard is not a mitigated hazard.

## 7. Lessons

1. **Do not hash presentation data.** Seal the parameters, not the file that happens to contain them. A sealed artifact should hold nothing a human would ever want to rename. *(Planned: separate scientific payload from provenance metadata, hash only the payload.)*
2. **A fail-closed guard that no test invokes is not a guard.** Its correctness must be asserted by CI on every commit, not discovered on next use. *(Planned: roadmap ENG-1/ENG-6 add a `verify-seals` CI job.)*
3. **Pin digests with provenance, not as bare literals.** Every recorded hash should carry what it pins, when it was set, and under what authority — so a bulk edit has something to trip over. *(Implemented in the dual-digest fix; generalized by roadmap ARCH-2, "frozen-code-as-data".)*
4. **Bulk mechanical edits need an exclusion list.** Sealed artifacts should be write-protected against repo-wide substitutions by policy and, ideally, by tooling.
5. **Documenting a hazard is not mitigating it.** DR-001 §5a correctly predicted the digest change and still the chain broke. Predictions belong in code as assertions, not only in prose.
6. **Fail-closed was the right design.** It is the reason this is a postmortem about downtime rather than about a retracted scientific claim. Given a choice between a system that stops and a system that guesses, the seal stopped — as intended.

## 8. Timeline

| Date | Event |
|---|---|
| 2026-06-15 | Seal #1 (manifest) and Seal #2 (thresholds) created; tag `phase1-prereg-v2` |
| 2026-06-19 | v3 re-registration; tag `phase1-prereg-v3` |
| 2026-06-24 | Single sealed TEST run executed (P-5), seals hash-verified in-run |
| **2026-06-30** | **Rebrand TRINETRA-X → VESPER (`6279a8b`); manifest digests change; loader literals not updated. Seal chain breaks. Public release `v1.0.0` ships.** |
| 2026-06-30 → 07-19 | Latent failure. No sealed pipeline invoked, so nothing surfaces. |
| **2026-07-19** | **Audit attempts a sealed run; immediate fail-closed. Root-caused; dual-digest fix `db710aa`; recorded in erratum §2.10 and DR-001 §5a addendum.** |
| 2026-07-28 | Verified working; this postmortem written (roadmap DOC-3). |

---

*Written as roadmap task DOC-3. The underlying facts are recorded in `M4_ERRATUM_2026-07-19.md` §2.10 and `decisions/F1_DECISION_RECORD.md` §5a, which remain the authoritative sources; this document is the external-audience narrative of them.*
