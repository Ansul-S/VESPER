"""Generate Phase-I paper tables (T2/T3/T7) + figures (F3/F8) from the M4 TEST artifacts.

Pure analysis/visualization of the single-read result — NO TEST re-read, NO sealed value
touched. Reads data/manifests/m4/test_run/{summary.json,recovery.csv,e1_per_cell.csv,
timing_ledger.csv} and writes:
  research/m4_evaluation/figures/{F3_completeness_maps.png,F8_runtime.png}
  research/m4_evaluation/M4_TABLES.md   (T2 headline, T3 recall-by-population, T7 compute ledger)
  research/m4_evaluation/tables/{T2,T3,T7}.csv

Run: .venv/bin/python research/m4_evaluation/make_paper_artifacts.py
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUN = Path("data/manifests/m4/test_run")
HERE = Path("research/m4_evaluation")
FIG = HERE / "figures"; TAB = HERE / "tables"
FIG.mkdir(parents=True, exist_ok=True); TAB.mkdir(parents=True, exist_ok=True)

summary = json.loads((RUN / "summary.json").read_text())
df = pd.read_csv(RUN / "recovery.csv")
pc = pd.read_csv(RUN / "e1_per_cell.csv")
led = pd.read_csv(RUN / "timing_ledger.csv")

E1, E2 = summary["E1"], summary["E2"]
W = pc["w_c"].sum()
wR_tls = float((pc["w_c"] * pc["R_tls"]).sum() / W)
wR_comb = float((pc["w_c"] * pc["R_comb"]).sum() / W)


def md_table(dframe, floatfmt="%.3f"):
    cols = list(dframe.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in dframe.iterrows():
        cells = [(floatfmt % v if isinstance(v, (float, np.floating)) else str(v)) for v in r]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


# ---------- T2 — headline ----------
t2 = pd.DataFrame([
    {"quantity": "Recall — full TLS (occ-weighted)", "value": f"{wR_tls:.3f}"},
    {"quantity": "Recall — combined (occ-weighted)", "value": f"{wR_comb:.3f}"},
    {"quantity": "ΔR̄ (occ-weighted)", "value": f"{E1['delta_R_bar']*100:+.2f} pp"},
    {"quantity": "ΔR̄ one-sided 95% lower bound", "value": f"{E1['ci95_one_sided_lower']*100:+.2f} pp"},
    {"quantity": "E1 margin", "value": f"{E1['margin']*100:.0f} pp"},
    {"quantity": "E1 — recall non-inferiority", "value": "PASS" if E1["pass"] else "FAIL"},
    {"quantity": "Compute ratio (combined/full)", "value": f"{E2['compute_ratio']:.3f}"},
    {"quantity": "Compute reduction (scoped)", "value": f"{E2['reduction']*100:.1f} %"},
    {"quantity": "ρ_d (routing entry tax)", "value": f"{E2['rho_d']*100:.1f} %"},
    {"quantity": "Reduction target", "value": f"{E2['reduction_target']*100:.0f} %"},
    {"quantity": "E2 — scoped compute", "value": "PASS" if E2["pass"] else "FAIL"},
    {"quantity": "Routing fraction", "value": f"{summary['routed_frac']:.3f}"},
    {"quantity": "Injections", "value": f"{summary['n_injections']}"},
    {"quantity": "VERDICT (pre-committed, VAL §7a)", "value": summary["verdict_pre_committed"]},
])
t2.to_csv(TAB / "T2.csv", index=False)


# ---------- T3 — recall by population ----------
def by(col):
    g = df.groupby(col).agg(n=("rec_tls", "size"), R_tls=("rec_tls", "mean"),
                            R_comb=("rec_comb", "mean")).reset_index()
    g["dR_pp"] = (g["R_comb"] - g["R_tls"]) * 100
    return g

t3_rp = by("radius_rearth").rename(columns={"radius_rearth": "Rp (R_earth)"})
t3_p = by("period_days").rename(columns={"period_days": "P (days)"})
# monotransit cut (n_transits == 1) vs multi
df["regime"] = np.where(df["n_transits"] == 1, "monotransit (n_tr=1)", "multi (n_tr≥2)")
t3_mt = df.groupby("regime").agg(n=("rec_tls", "size"), R_tls=("rec_tls", "mean"),
                                 R_comb=("rec_comb", "mean")).reset_index()
t3_mt["dR_pp"] = (t3_mt["R_comb"] - t3_mt["R_tls"]) * 100
for t, name in [(t3_rp, "T3_by_radius"), (t3_p, "T3_by_period"), (t3_mt, "T3_by_regime")]:
    t.to_csv(TAB / f"{name}.csv", index=False)


# ---------- T7 — compute ledger ----------
st = E2["per_stage_means_s"]
t7 = pd.DataFrame([
    {"item": "n eligible stars timed", "value": f"{E2['n_eligible']}"},
    {"item": "mean full-TLS cost / star (s)", "value": f"{st['full_tls']:.1f}"},
    {"item": "mean detector cost / star (s)", "value": f"{st['detector']:.2f}"},
    {"item": "mean combined-TLS cost / star (s)", "value": f"{st['tls_comb']:.1f}"},
    {"item": "C_full total (s)", "value": f"{E2['C_full_s']:.1f}"},
    {"item": "C_comb total (s)", "value": f"{E2['C_comb_s']:.1f}"},
    {"item": "compute ratio", "value": f"{E2['compute_ratio']:.3f}"},
    {"item": "reduction", "value": f"{E2['reduction']*100:.1f} %"},
    {"item": "ρ_d (entry tax)", "value": f"{E2['rho_d']*100:.1f} %"},
    {"item": "π* break-even occurrence", "value": f"{E2['pi_star_breakeven']:.3f}"},
    {"item": "fast-path confirmed (of timed)", "value": f"{int(led['confirmed_cheap'].sum())}/{len(led)}"},
])
t7.to_csv(TAB / "T7.csv", index=False)

# ---------- M4_TABLES.md ----------
(HERE / "M4_TABLES.md").write_text(
    "# M4 Phase-I Tables (generated from the sealed-TEST artifacts)\n\n"
    "> Auto-generated by `make_paper_artifacts.py` from `data/manifests/m4/test_run/`. "
    "Analysis of the single-read result; no TEST re-read, no sealed value changed.\n\n"
    "## T2 — Headline result\n\n" + md_table(t2) + "\n\n"
    "## T3 — Recall by population\n\n"
    "### by planet radius\n\n" + md_table(t3_rp) + "\n\n"
    "### by orbital period\n\n" + md_table(t3_p) + "\n\n"
    "### by transit regime (monotransit reported separately; excluded from headline)\n\n" + md_table(t3_mt) + "\n\n"
    "## T7 — Compute ledger\n\n" + md_table(t7) + "\n\n"
    "*ΔR̄ headline is occurrence-weighted (K&M-2020 prior); the per-population ΔR above are "
    "unweighted within each class, so they expose the structure the weighting averages over.*\n"
)

# ---------- F3 — completeness maps ----------
P_order = sorted(df["period_days"].unique())
R_order = sorted(df["radius_rearth"].unique())
piv = {k: pc.pivot(index="Rp", columns="P", values=k).reindex(index=R_order, columns=P_order)
       for k in ["R_tls", "R_comb"]}
piv["dR"] = piv["R_comb"] - piv["R_tls"]
fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
specs = [("R_tls", "Full TLS recall", "viridis", 0, 1),
         ("R_comb", "Combined recall", "viridis", 0, 1),
         ("dR", "Δ recall (combined − full)", "RdBu", -0.4, 0.4)]
for ax, (k, title, cmap, vmin, vmax) in zip(axes, specs):
    M = piv[k].values
    im = ax.imshow(M, origin="lower", aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_xticks(range(len(P_order))); ax.set_xticklabels([f"{p:g}" for p in P_order])
    ax.set_yticks(range(len(R_order))); ax.set_yticklabels([f"{r:g}" for r in R_order])
    ax.set_xlabel("Period (days)"); ax.set_ylabel("Radius (R⊕)"); ax.set_title(title)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if np.isfinite(M[i, j]):
                ax.text(j, i, f"{M[i,j]:.2f}", ha="center", va="center", fontsize=7,
                        color="black" if (k != "dR" and M[i, j] > 0.5) else "white" if k != "dR" else "black")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
fig.suptitle("F3 — Completeness maps (sealed TEST; 30 cells × 500 injections)", y=1.02)
fig.tight_layout(); fig.savefig(FIG / "F3_completeness_maps.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------- F8 — runtime ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.6))
x = np.arange(len(led))
a1.bar(x - 0.2, led["cost_full"], 0.4, label="full TLS (Arm A)", color="#444")
a1.bar(x + 0.2, led["cost_comb"], 0.4, label="combined (Arm B)", color="#2a9d8f")
a1.set_xlabel("fast-path-eligible star (timed subset)"); a1.set_ylabel("cost (s)")
a1.set_title("Per-star cost: full TLS vs combined"); a1.legend()
# stacked stage breakdown for combined
a2.bar(x, led["cost_detector"], 0.6, label="detector+FAP (entry tax ρ_d)", color="#e76f51")
a2.bar(x, led["cost_tls"], 0.6, bottom=led["cost_detector"], label="confirm / TLS fallback", color="#264653")
a2.set_xlabel("fast-path-eligible star (timed subset)"); a2.set_ylabel("cost (s)")
a2.set_title("Combined-arm stage breakdown"); a2.legend()
fig.suptitle(f"F8 — Runtime per star (reduction {E2['reduction']*100:.1f}%, ρ_d {E2['rho_d']*100:.1f}%)", y=1.02)
fig.tight_layout(); fig.savefig(FIG / "F8_runtime.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("WROTE:")
print(" ", HERE / "M4_TABLES.md")
print(" ", FIG / "F3_completeness_maps.png")
print(" ", FIG / "F8_runtime.png")
print("  tables/{T2,T3_by_*,T7}.csv")
print(f"\nT2 sanity: wR_tls={wR_tls:.3f} wR_comb={wR_comb:.3f} dRbar={E1['delta_R_bar']*100:+.2f}pp "
      f"(check={(wR_comb-wR_tls)*100:+.2f}pp) | E2 reduction={E2['reduction']*100:.1f}%")
