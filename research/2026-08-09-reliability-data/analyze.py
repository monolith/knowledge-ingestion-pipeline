"""Reliability analysis for the 2x2(+1) taxonomy experiment.

Primary metric is inter-rater agreement (Krippendorff's alpha, nominal), NOT
agreement with the author's key. The question is whether the scheme is
reproducible; the key was written by the same person who designed the scheme, so
scoring against it measures self-consistency, not reliability. The key appears
only as a clearly-labeled secondary.
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter, defaultdict

sys.path.insert(0, "/home/anatoly/knowledge-ingestion-plugin/src")
from kip.taxonomy import FAMILY_OF, LEGACY_MAP, TYPE_TESTS, TYPES, UNCLASSIFIED, derive_type


# --- Agreement statistics -----------------------------------------------------


def krippendorff_alpha(ratings: dict[str, list[str]]) -> float | None:
    """Nominal Krippendorff's alpha over {item: [rater labels]}.

    alpha = 1 - Do/De. Chance-corrected, which is what makes a 20-label arm
    comparable to a 6-label arm at all: raw percent agreement would flatter the
    smaller label set purely because random collisions are likelier.
    """
    units = {u: [v for v in vs if v is not None] for u, vs in ratings.items()}
    units = {u: vs for u, vs in units.items() if len(vs) >= 2}
    if not units:
        return None

    n_total = sum(len(vs) for vs in units.values())
    observed = 0.0
    for vs in units.values():
        counts = Counter(vs)
        m_u = len(vs)
        pairs = sum(a * b for a, b in itertools.permutations(counts.values(), 2))
        observed += pairs / (m_u - 1)
    Do = observed / n_total

    totals = Counter(v for vs in units.values() for v in vs)
    De_pairs = sum(a * b for a, b in itertools.permutations(totals.values(), 2))
    De = De_pairs / (n_total * (n_total - 1))
    if De == 0:
        return 1.0
    return 1.0 - Do / De


def fleiss_kappa(ratings: dict[str, list[str]]) -> float | None:
    units = {u: vs for u, vs in ratings.items() if all(v is not None for v in vs)}
    if not units:
        return None
    m = len(next(iter(units.values())))
    if any(len(vs) != m for vs in units.values()) or m < 2:
        return None
    cats = sorted({v for vs in units.values() for v in vs})
    n = len(units)
    P_i = []
    col = Counter()
    for vs in units.values():
        counts = Counter(vs)
        col.update(vs)
        P_i.append((sum(c * c for c in counts.values()) - m) / (m * (m - 1)))
    P_bar = sum(P_i) / n
    P_e = sum((col[c] / (n * m)) ** 2 for c in cats)
    if P_e == 1:
        return 1.0
    return (P_bar - P_e) / (1 - P_e)


def unanimity(ratings: dict[str, list[str]]) -> float:
    full = [vs for vs in ratings.values() if all(v is not None for v in vs)]
    if not full:
        return 0.0
    return sum(1 for vs in full if len(set(vs)) == 1) / len(full)


def pairwise_percent(ratings: dict[str, list[str]]) -> float:
    agree = total = 0
    for vs in ratings.values():
        clean = [v for v in vs if v is not None]
        for a, b in itertools.combinations(clean, 2):
            total += 1
            agree += a == b
    return agree / total if total else 0.0


# --- Label projection ---------------------------------------------------------


def legacy_to_six(label: str) -> str:
    """Project a 20-label answer onto the six types via the shipped LEGACY_MAP.

    This is the apples-to-apples comparison: whichever vocabulary the rater was
    given, where did they land? It answers the question the raw per-arm alphas
    cannot -- is the six-type destination reached more reliably through six
    labels or through twenty?
    """
    if label in LEGACY_MAP:
        mapped = LEGACY_MAP[label][0]
        return mapped if mapped else "question"
    return UNCLASSIFIED


def to_family(label: str) -> str:
    return FAMILY_OF.get(label, UNCLASSIFIED)


# --- Main ---------------------------------------------------------------------


def main(raw_path: str) -> None:
    payload = json.load(open(raw_path))
    raters = payload["raters"]
    items = {i["id"]: i for i in json.load(open("/tmp/eval/items.json"))["items"]}
    author_key = json.load(open("/tmp/eval/items.json"))["author_key"]

    # arm -> item -> [label per rater]
    by_arm: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    gate_rows: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))

    for r in raters:
        arm, mode = r["arm"], r["mode"]
        seen = {}
        for row in r["labels"] or []:
            iid = row.get("id")
            if iid not in items:
                continue
            if mode == "gates":
                tests = {t: bool(row.get(t)) for t in TYPE_TESTS}
                seen[iid] = derive_type(tests)
                gate_rows[arm][iid] = gate_rows[arm].get(iid, []) + [tests]
            else:
                seen[iid] = (row.get("label") or "").strip().lower()
        for iid in items:
            by_arm[arm][iid].append(seen.get(iid))

    report: dict = {"arms": {}, "comparisons": {}, "n_items": len(items)}

    for arm in sorted(by_arm):
        ratings = dict(by_arm[arm])
        legacy_arm = arm.startswith(("A_", "B_"))

        proj = {u: [legacy_to_six(v) if (legacy_arm and v) else v for v in vs]
                for u, vs in ratings.items()}
        fam = {u: [to_family(v) if v else None for v in vs] for u, vs in proj.items()}

        def subset(d, stratum):
            return {u: v for u, v in d.items() if items[u]["stratum"] == stratum}

        entry = {
            "coverage": sum(1 for vs in ratings.values() if all(vs)) / len(items),
            "native_alpha": krippendorff_alpha(ratings),
            "native_fleiss": fleiss_kappa(ratings),
            "native_unanimity": unanimity(ratings),
            "native_pairwise": pairwise_percent(ratings),
            "projected_six_alpha": krippendorff_alpha(proj),
            "projected_six_unanimity": unanimity(proj),
            "family_alpha": krippendorff_alpha(fam),
            "family_unanimity": unanimity(fam),
            "alpha_boundary": krippendorff_alpha(subset(proj, "boundary")),
            "alpha_routine": krippendorff_alpha(subset(proj, "routine")),
            "label_distribution": dict(Counter(
                v for vs in proj.values() for v in vs if v).most_common()),
        }

        # Secondary, and labelled as such: agreement with the author's key.
        hits = tot = 0
        for u, vs in proj.items():
            if u not in author_key:
                continue
            for v in vs:
                if v is None:
                    continue
                tot += 1
                hits += v == author_key[u]["primary"]
        entry["author_key_agreement_SECONDARY"] = (hits / tot) if tot else None

        if arm in gate_rows:
            fires = [sum(1 for t in TYPE_TESTS if row[t])
                     for rows in gate_rows[arm].values() for row in rows]
            entry["gates"] = {
                "mean_gates_fired": sum(fires) / len(fires) if fires else None,
                "multi_fire_rate": sum(1 for f in fires if f >= 2) / len(fires) if fires else None,
                "abstain_rate": sum(1 for f in fires if f == 0) / len(fires) if fires else None,
            }
        report["arms"][arm] = entry

    a = report["arms"]

    def alpha(arm, field="projected_six_alpha"):
        return a.get(arm, {}).get(field)

    report["comparisons"] = {
        "definitions_effect_20_labels (B - A)":
            _delta(alpha("B_legacy20_taught"), alpha("A_legacy20_bare")),
        "definitions_effect_6_labels (D - C)":
            _delta(alpha("D_six_taught"), alpha("C_six_bare")),
        "count_effect_taught (D - B)":
            _delta(alpha("D_six_taught"), alpha("B_legacy20_taught")),
        "count_effect_bare (C - A)":
            _delta(alpha("C_six_bare"), alpha("A_legacy20_bare")),
        "gates_vs_sixway_taught (E - D)":
            _delta(alpha("E_six_gates_taught"), alpha("D_six_taught")),
        "family_tier_gain_over_type (D)":
            _delta(alpha("D_six_taught", "family_alpha"), alpha("D_six_taught")),
        "family_tier_gain_over_type (E)":
            _delta(alpha("E_six_gates_taught", "family_alpha"), alpha("E_six_gates_taught")),
    }
    json.dump(report, open("/tmp/eval/report.json", "w"), indent=2)
    _print(report)


def _delta(x, y):
    if x is None or y is None:
        return None
    return round(x - y, 4)


def _print(report):
    print(f"\n{'='*78}\nRELIABILITY — inter-rater agreement, 3 blind raters/arm, "
          f"{report['n_items']} items\n{'='*78}")
    hdr = f"{'arm':<22}{'α native':>10}{'α→6':>8}{'α family':>10}{'unanim':>9}{'cover':>8}"
    print(hdr); print("-" * len(hdr))
    for arm, e in report["arms"].items():
        def f(x, w=10, p=3):
            return f"{x:>{w}.{p}f}" if isinstance(x, float) else f"{'n/a':>{w}}"
        print(f"{arm:<22}{f(e['native_alpha'])}{f(e['projected_six_alpha'],8)}"
              f"{f(e['family_alpha'])}{f(e['projected_six_unanimity'],9,2)}"
              f"{f(e['coverage'],8,2)}")
    print(f"\n{'by stratum (projected to six types)':<40}{'boundary':>12}{'routine':>12}")
    for arm, e in report["arms"].items():
        def f(x):
            return f"{x:>12.3f}" if isinstance(x, float) else f"{'n/a':>12}"
        print(f"{arm:<40}{f(e['alpha_boundary'])}{f(e['alpha_routine'])}")
    print("\nCOMPARISONS (Δ Krippendorff α, projected to six types)")
    for k, v in report["comparisons"].items():
        print(f"  {k:<42}{v if v is not None else 'n/a':>+8}" if isinstance(v, float)
              else f"  {k:<42}{'n/a':>8}")
    for arm, e in report["arms"].items():
        if "gates" in e:
            g = e["gates"]
            print(f"\nGATE BEHAVIOR ({arm})")
            for k, v in g.items():
                print(f"  {k:<24}{v:.3f}" if isinstance(v, float) else f"  {k:<24}n/a")
    print("\nSECONDARY — agreement with the author's key (boundary items only;")
    print("the key's author designed the scheme, so this is self-consistency)")
    for arm, e in report["arms"].items():
        v = e["author_key_agreement_SECONDARY"]
        print(f"  {arm:<24}{v:.3f}" if isinstance(v, float) else f"  {arm:<24}n/a")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/eval/raw.json")
