"""M5 (partial): parameter recovery (period/epoch) + FAP calibration — from EXISTING artifacts.

NO new compute, NO TEST re-read: reads the already-produced sealed-test recovery
(data/manifests/m4/test_run/recovery.csv) and the M3 null-pool calibration
(data/manifests/m3/m3_per_star.csv). Produces:
  figures/F5_period_recovery.png   — recovered vs true period (log-log; harmonic aliases)
  figures/F6_fap_calibration.png   — null period-FAP empirical exceedance vs nominal alpha
  M5_TABLES.md  (+ tables/{T5,T4}.csv)

Deferred (need new tooling/compute/data, NOT done here): depth/T14 recovery (not logged),
M6 TOI/EB reality check (T6/F7/F9), gate ablation (T8).

Run: .venv/bin/python research/m4_evaluation/m5_recovery_calibration.py
"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path("research/m4_evaluation"); FIG = HERE / "figures"; TAB = HERE / "tables"
FIG.mkdir(parents=True, exist_ok=True); TAB.mkdir(parents=True, exist_ok=True)
df = pd.read_csv("data/manifests/m4/test_run/recovery.csv")
nul = pd.read_csv("data/manifests/m3/m3_per_star.csv"); nul["tic"] = nul["tic"].astype(str)
# the SEALED calibration uses the CLEANED null pool (146 EB/variable contaminants removed);
# contaminants carry real periodic signals -> low FAP -> inflate the raw exceedance.
exc = set(pd.read_csv("data/manifests/m3/calibration_exclusions.csv")["tic"].astype(str))
ALPHA = 0.01

# ---------- M5 period/epoch recovery (routed injections with a seed) ----------
r = df[df.p_hat.notna()].copy()
matched = r[r.period_match]
t5 = pd.DataFrame([
    {"metric": "routed injections with a period seed", "value": f"{len(r)}"},
    {"metric": "period_match rate (within tolerance)", "value": f"{r.period_match.mean()*100:.1f} %"},
    {"metric": "harmonic among period-matched", "value": f"{matched.harmonic.mean()*100:.1f} %"},
    {"metric": "median |ΔP/P| (all seeded)", "value": f"{r.period_err.abs().median():.4f}"},
    {"metric": "median |ΔP/P| (period-matched)", "value": f"{matched.period_err.abs().median():.4f}"},
    {"metric": "epoch_ok rate (|Δt0| ≤ 0.5 T14)", "value": f"{r.epoch_ok.mean()*100:.1f} %"},
    {"metric": "median epoch offset (T14 units)", "value": f"{r.epoch_err_t14.median():.3f}"},
])
t5.to_csv(TAB / "T5.csv", index=False)

# ---------- T4 null FAP calibration (cleaned pool = sealed basis; raw shown for contrast) ----------
fap_raw = nul["period_fap"].dropna().values
fap = nul[~nul.tic.isin(exc)]["period_fap"].dropna().values   # CLEANED (sealed calibration basis)
emp_at_alpha = float(np.mean(fap <= ALPHA))
emp_raw = float(np.mean(fap_raw <= ALPHA))
t4 = pd.DataFrame([
    {"metric": "cleaned null stars with a period-FAP", "value": f"{len(fap)}"},
    {"metric": f"FAR at nominal α={ALPHA} (cleaned, sealed basis)", "value": f"{emp_at_alpha*100:.2f} %"},
    {"metric": f"FAR at nominal α={ALPHA} (raw, pre-cleaning)", "value": f"{emp_raw*100:.2f} %"},
    {"metric": "nominal α_FAP (sealed)", "value": f"{ALPHA*100:.0f} %"},
    {"metric": "matches sealed M3 (1.08%)", "value": "YES" if abs(emp_at_alpha-0.0108) < 0.001 else "NO"},
    {"metric": "calibration verdict", "value": "well-calibrated" if emp_at_alpha <= 1.5*ALPHA else "check"},
])
t4.to_csv(TAB / "T4.csv", index=False)


def md(d):
    o = ["| " + " | ".join(d.columns) + " |", "|" + "|".join(["---"]*len(d.columns)) + "|"]
    for _, x in d.iterrows():
        o.append("| " + " | ".join(str(v) for v in x) + " |")
    return "\n".join(o)


(HERE / "M5_TABLES.md").write_text(
    "# M5 Tables — parameter recovery + FAP calibration (from existing artifacts)\n\n"
    "> `m5_recovery_calibration.py`; no new compute, no TEST re-read. Period/epoch from the\n"
    "> sealed-test recovery; FAP calibration from the M3 null pool.\n\n"
    "## T5 — Parameter accuracy (period & epoch; depth/T14 deferred — not logged)\n\n" + md(t5) + "\n\n"
    "## T4 — Period-FAP calibration on null stars\n\n" + md(t4) + "\n"
)

# ---------- F5 — recovered vs true period ----------
fig, ax = plt.subplots(figsize=(6.4, 6))
ok = r[r.epoch_ok]; no = r[~r.epoch_ok]
ax.scatter(no.period_days, no.p_hat, s=6, c="#bbb", label="seed, epoch miss", alpha=0.4)
ax.scatter(ok.period_days, ok.p_hat, s=8, c="#2a9d8f", label="seed, epoch ok", alpha=0.6)
lim = [0.4, 40]
ax.plot(lim, lim, "k-", lw=1, label="P̂ = P")
for m, ls in [(2, "--"), (0.5, "--"), (3, ":"), (1/3, ":")]:
    ax.plot(lim, [m*x for x in lim], color="#e76f51", ls=ls, lw=0.8)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(lim); ax.set_ylim(lim)
ax.set_xlabel("true period (days)"); ax.set_ylabel("recovered period P̂ (days)")
ax.set_title("F5 — Period recovery (orange: 2×/½/3×/⅓ harmonics)"); ax.legend(loc="upper left", fontsize=8)
fig.tight_layout(); fig.savefig(FIG / "F5_period_recovery.png", dpi=150, bbox_inches="tight"); plt.close(fig)

# ---------- F6 — FAP calibration (cleaned vs raw; demonstrates the null-cleaning) ----------
grid = np.logspace(-3, 0, 50)
emp = [np.mean(fap <= a) for a in grid]
emp_r = [np.mean(fap_raw <= a) for a in grid]
fig, ax = plt.subplots(figsize=(6.2, 5.6))
ax.plot(grid, grid, "k--", lw=1, label="nominal (ideal)")
ax.plot(grid, emp_r, "-o", ms=3, color="#bbb", label=f"raw null pool (FAR={emp_raw*100:.2f}%)")
ax.plot(grid, emp, "-o", ms=3, color="#264653", label=f"cleaned null pool (FAR={emp_at_alpha*100:.2f}%)")
ax.axvline(ALPHA, color="#e76f51", ls=":", label=f"sealed α={ALPHA}")
ax.scatter([ALPHA], [emp_at_alpha], c="#e76f51", zorder=5)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("nominal α"); ax.set_ylabel("empirical fraction of nulls with FAP ≤ α")
ax.set_title("F6 — Period-FAP calibration on null stars\n(cleaning EB/variable contaminants recovers nominal FAR)")
ax.legend(loc="upper left", fontsize=8)
fig.tight_layout(); fig.savefig(FIG / "F6_fap_calibration.png", dpi=150, bbox_inches="tight"); plt.close(fig)

print("WROTE M5_TABLES.md, figures/F5_period_recovery.png, figures/F6_fap_calibration.png, tables/{T5,T4}.csv")
print(f"T5: period_match={r.period_match.mean()*100:.1f}% epoch_ok={r.epoch_ok.mean()*100:.1f}% "
      f"median|dP/P|={r.period_err.abs().median():.4f}")
print(f"T4: null FAR at α={ALPHA} = {emp_at_alpha*100:.2f}% (n={len(fap)})")
