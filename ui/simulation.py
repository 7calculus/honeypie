"""Animated simulation: how an algorithm chooses honeypot spots, then how
simulated attackers traverse the network and get intercepted.

Pure presentation. Placements, traces and histories come from the backend
(run_experiment); coverage sets come from src.coverage.covered_ids.
The animation is a Plotly frame animation rendered client-side, so replaying
or scrubbing never triggers a Streamlit rerun.
"""
from __future__ import annotations
import streamlit.components.v1 as components
import plotly.graph_objects as go

from src.coverage import covered_ids
from ui import data, netviz
from ui.theme import ALGO_COLORS, HONEYPOT, PATH_HILITE, ROLE_COLORS

MAX_SA_FRAMES = 60
MAX_TRAVERSE_PATHS = 12
CYAN, GREEN, RED = "#22d3ee", "#34d399", "#fb7185"


def _xy(pos, edges):
    xs, ys = [], []
    for u, v in edges:
        xs += [pos[u][0], pos[v][0], None]
        ys += [pos[u][1], pos[v][1], None]
    return xs, ys


def _path_edges(paths, ids):
    out = set()
    for pid in ids:
        p = paths[pid]
        out |= set(zip(p[:-1], p[1:]))
    return out


# ------------------------------------------------------------ phase A
def selection_steps(r, algo):
    """[(honeypot_set, caption)] describing how `algo` arrives at its answer."""
    n, res = r["n_paths"], data.algos(r)[algo]
    if res is None:
        return []
    steps = [(set(), f"<b>{algo}</b> — no honeypots placed yet")]
    if algo == "Greedy":
        chosen = set()
        for t in r["greedy_trace"]:
            chosen = chosen | {t["node"]}
            steps.append((set(chosen), f"Greedy step {t['step']}: pick <b>{t['node']}</b> "
                          f"(+{t['gain']} new paths → {t['cumulative']}/{n} covered)"))
    elif algo == "Betweenness":
        bc = r["bc_values"]
        ranked = sorted(bc, key=lambda x: (-bc[x], str(x)))[:len(res.nodes)]
        chosen = set()
        for i, node in enumerate(ranked, 1):
            chosen = chosen | {node}
            steps.append((set(chosen), f"Betweenness rank #{i}: <b>{node}</b> "
                          f"(score {bc[node]:.4f}) → {data.covered_by_set(r, chosen)}/{n} covered"))
    elif algo == "Exhaustive":
        chosen = set()
        for node in sorted(res.nodes, key=str):
            chosen = chosen | {node}
            steps.append((set(chosen), f"Optimal combination reveals <b>{node}</b> "
                          f"(checked {res.iterations:,} combinations)"))
    else:  # SA
        hist = r["sa_history"]
        if hist and "nodes" not in hist[0]:      # stale cached run from before src/annealing.py was updated
            hist = []
        init = set(r["greedy"].nodes)
        steps = [(init, f"SA starts from the greedy solution ({r['greedy'].covered}/{n} covered)")]
        if not hist:
            steps.append((set(res.nodes), "SA made no moves — " + (data.sa_skip_reason(r) or
                          "walk details unavailable (restart Streamlit and re-run to record them)")))
        else:
            keep, best_prev = {0, len(hist) - 1}, -1
            for i, h in enumerate(hist):
                if h["best"] > best_prev:
                    keep.add(i)
                best_prev = max(best_prev, h["best"])
            stride = max(1, len(hist) // max(1, MAX_SA_FRAMES - len(keep)))
            keep |= set(range(0, len(hist), stride))
            for i in sorted(keep)[:MAX_SA_FRAMES]:
                h = hist[i]
                mark = "accepted" if h["accepted"] else "rejected"
                steps.append((set(h["nodes"]), f"SA iter {h['iter']:,} · T={h['T']:.3f} · swap {mark} · "
                              f"current {h['current']}/{n} · best {h['best']}/{n}"))
            steps.append((set(res.nodes), f"SA returns its best-so-far: {res.covered}/{n} covered"))
    last_set = steps[-1][0]
    if set(res.nodes) != last_set:
        steps.append((set(res.nodes), f"Final {algo} placement: {res.covered}/{n} covered"))
    return steps


def _traverse_ids(r, honeypots):
    cov = covered_ids(honeypots, r["index"])
    all_ids = list(range(r["n_paths"]))
    if len(all_ids) <= MAX_TRAVERSE_PATHS:
        return all_ids
    unc = [i for i in all_ids if i not in cov][:4]
    rest = [i for i in all_ids if i not in unc]
    need = MAX_TRAVERSE_PATHS - len(unc)
    step = len(rest) / need
    pick = [rest[int(j * step)] for j in range(need)]
    return sorted(set(unc + pick))


# ------------------------------------------------------------ figure
def build_figure(r, algo, layout=netviz.LAYOUTS[0], speed=450, height=580):
    G, s, t = r["G"], r["s"], r["t"]
    paths = r["paths"]
    pos = netviz.compute_layout(r, layout)
    labels = netviz.short_label(G.nodes)
    acol = ALGO_COLORS[algo]
    res = data.algos(r)[algo]
    final_hp = set(res.nodes)
    all_edges = list(G.edges())
    eligible = set(r["eligible"])

    def role(n):
        return "Source" if n == s else "Target" if n == t else \
            "Eligible" if n in eligible else "Ineligible"

    # ---- frame plan: list of dicts
    plan = []
    for hp, cap in selection_steps(r, algo):
        cov_edges = _path_edges(paths, covered_ids(hp, r["index"]))
        plan.append(dict(hp=hp, cap=cap, cov=cov_edges, trail=[], trav=None, trail_col=CYAN, hit=None))

    caught = escaped = 0
    cov_final = _path_edges(paths, covered_ids(final_hp, r["index"]))
    ids = _traverse_ids(r, final_hp)
    plan.append(dict(hp=final_hp, cap=f"<b>Attack simulation</b> — {len(ids)} candidate paths "
                     f"(of {r['n_paths']}) are traversed by simulated attackers",
                     cov=set(), trail=[], trav=None, trail_col=CYAN, hit=None))
    for pid in ids:
        path = paths[pid]
        hit_at = next((i for i, n in enumerate(path) if i > 0 and n in final_hp), None)
        end = hit_at if hit_at is not None else len(path) - 1
        for i in range(end + 1):
            trail = list(zip(path[:i], path[1:i + 1]))
            last = i == end
            col = (RED if hit_at is not None else GREEN) if last and i > 0 else CYAN
            if last and hit_at is not None:
                cap = (f"p{pid + 1} <b>intercepted</b> at honeypot <b>{path[i]}</b> "
                       f"(caught {caught + 1} · escaped {escaped})")
            elif last:
                cap = f"p{pid + 1} reached the target <b>undetected</b> (caught {caught} · escaped {escaped + 1})"
            else:
                cap = f"Attacker on p{pid + 1} → <b>{path[i]}</b> (hop {i}/{len(path) - 1})"
            plan.append(dict(hp=final_hp, cap=cap, cov=set(), trail=trail, trav=path[i],
                             trail_col=col, hit=path[i] if (last and hit_at is not None) else None))
        if hit_at is not None:
            caught += 1
        else:
            escaped += 1
    plan.append(dict(hp=final_hp, cov=cov_final, trail=[], trav=None, trail_col=CYAN, hit=None,
                     cap=f"<b>Done.</b> Simulated attackers: {caught} intercepted · {escaped} escaped "
                         f"— backend coverage {res.covered}/{r['n_paths']} "
                         f"({data.pct(res.covered, r['n_paths']):.1f}%)"))

    # ---- traces (index: purpose)
    bx, by = _xy(pos, all_edges)
    nodes = list(G.nodes)
    traces = [
        go.Scatter(x=bx, y=by, mode="lines", line=dict(color="#334155", width=1.4), hoverinfo="skip",
                   showlegend=False),                                               # 0 base edges
        go.Scatter(x=[], y=[], mode="lines", line=dict(color=acol, width=9), opacity=0.22,
                   hoverinfo="skip", showlegend=False),                             # 1 covered glow
        go.Scatter(x=[], y=[], mode="lines", line=dict(color=acol, width=2.6),
                   hoverinfo="skip", showlegend=False),                             # 2 covered core
        go.Scatter(x=[], y=[], mode="lines", line=dict(color=CYAN, width=11), opacity=0.25,
                   hoverinfo="skip", showlegend=False),                             # 3 trail glow
        go.Scatter(x=[], y=[], mode="lines", line=dict(color=CYAN, width=3.4),
                   hoverinfo="skip", showlegend=False),                             # 4 trail core
        go.Scatter(x=[pos[n][0] for n in nodes], y=[pos[n][1] for n in nodes], mode="markers",
                   marker=dict(size=42, color=[ROLE_COLORS[role(n)] for n in nodes], opacity=0.2),
                   hoverinfo="skip", showlegend=False),                             # 5 node halo
        go.Scatter(x=[pos[n][0] for n in nodes], y=[pos[n][1] for n in nodes], mode="markers+text",
                   text=[labels[n] for n in nodes],
                   textposition=["top center" if pos[n][1] >= 0 else "bottom center" for n in nodes],
                   textfont=dict(size=10, color="#e2e8f0"),
                   marker=dict(size=[30 if n in (s, t) else 22 for n in nodes],
                               color=[ROLE_COLORS[role(n)] for n in nodes],
                               line=dict(color="#0b1220", width=2)),
                   hovertext=[netviz.node_hover(r, n) for n in nodes], hoverinfo="text",
                   showlegend=False),                                               # 6 nodes
        go.Scatter(x=[], y=[], mode="markers", marker=dict(size=60, color=HONEYPOT, opacity=0.25),
                   hoverinfo="skip", showlegend=False),                             # 7 honeypot halo
        go.Scatter(x=[], y=[], mode="markers", marker=dict(symbol="star", size=34, color=HONEYPOT,
                   line=dict(color=acol, width=2.5)), hoverinfo="skip", showlegend=False),  # 8 stars
        go.Scatter(x=[], y=[], mode="markers", marker=dict(size=40, color=CYAN, opacity=0.3),
                   hoverinfo="skip", showlegend=False),                             # 9 attacker halo
        go.Scatter(x=[], y=[], mode="markers", marker=dict(symbol="diamond", size=16, color="#ffffff",
                   line=dict(color=CYAN, width=3)), hoverinfo="skip", showlegend=False),    # 10 attacker
    ]
    for name, col, sym in (("Source", ROLE_COLORS["Source"], "circle"), ("Target", ROLE_COLORS["Target"], "circle"),
                           ("Eligible", ROLE_COLORS["Eligible"], "circle"),
                           ("Ineligible", ROLE_COLORS["Ineligible"], "circle"),
                           ("Honeypot", HONEYPOT, "star"), ("Attacker", "#ffffff", "diamond")):
        traces.append(go.Scatter(x=[None], y=[None], mode="markers", name=name,
                                 marker=dict(color=col, size=12, symbol=sym)))
    dyn = [1, 2, 3, 4, 7, 8, 9, 10]

    def frame_data(f):
        cx, cy = _xy(pos, f["cov"])
        tx, ty = _xy(pos, f["trail"])
        hp = [n for n in nodes if n in f["hp"]]
        hx, hy = [pos[n][0] for n in hp], [pos[n][1] for n in hp]
        tv = [pos[f["trav"]]] if f["trav"] is not None else []
        tcol = f["trail_col"]
        out = [
            go.Scatter(x=cx, y=cy), go.Scatter(x=cx, y=cy),
            go.Scatter(x=tx, y=ty, line=dict(color=tcol, width=11)),
            go.Scatter(x=tx, y=ty, line=dict(color=tcol, width=3.4)),
            go.Scatter(x=hx, y=hy), go.Scatter(x=hx, y=hy),
            go.Scatter(x=[p[0] for p in tv], y=[p[1] for p in tv],
                       marker=dict(size=64 if f["hit"] else 40, color=RED if f["hit"] else tcol, opacity=0.35)),
            go.Scatter(x=[p[0] for p in tv], y=[p[1] for p in tv],
                       marker=dict(symbol="x" if f["hit"] else "diamond", size=18, color="#ffffff",
                                   line=dict(color=RED if f["hit"] else tcol, width=3))),
        ]
        return out

    def caption(txt):
        return [dict(text=txt, xref="paper", yref="paper", x=0.5, y=1.0, yanchor="bottom",
                     showarrow=False, font=dict(size=14, color="#e2e8f0"),
                     bgcolor="rgba(15,23,42,0.85)", bordercolor=acol, borderwidth=1, borderpad=6)]

    frames = [go.Frame(name=str(i), data=frame_data(f), traces=dyn, layout=dict(annotations=caption(f["cap"])))
              for i, f in enumerate(plan)]
    fig = go.Figure(data=traces, frames=frames)
    f0 = frame_data(plan[0])
    for tr_i, d in zip(dyn, f0):
        fig.data[tr_i].update(d)

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    padx = max(0.6, (max(xs) - min(xs)) * 0.05)
    pady = max(0.9, (max(ys) - min(ys)) * 0.14)
    anim = dict(frame=dict(duration=speed, redraw=True), transition=dict(duration=0),
                fromcurrent=True, mode="immediate")
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=height, margin=dict(l=0, r=0, t=70, b=70), annotations=caption(plan[0]["cap"]),
        font=dict(color="#cbd5e1"), legend=dict(orientation="h", y=-0.02, x=0.5, xanchor="center",
                                                bgcolor="rgba(15,23,42,0.6)"),
        xaxis=dict(visible=False, range=[min(xs) - padx, max(xs) + padx]),
        yaxis=dict(visible=False, range=[min(ys) - pady, max(ys) + pady]),
        updatemenus=[dict(type="buttons", direction="left", x=0.0, y=-0.1, xanchor="left", yanchor="top",
                          bgcolor="#1e293b", bordercolor=acol, font=dict(color="#e2e8f0"),
                          buttons=[dict(label="▶ Play / Replay", method="animate", args=[None, anim]),
                                   dict(label="❚❚ Pause", method="animate",
                                        args=[[None], dict(frame=dict(duration=0, redraw=False),
                                                           mode="immediate", transition=dict(duration=0))])])],
        sliders=[dict(active=0, x=0.28, y=-0.1, len=0.72, xanchor="left", yanchor="top",
                      currentvalue=dict(visible=False), pad=dict(t=0, b=0),
                      bgcolor="#1e293b", activebgcolor=acol, bordercolor="#334155",
                      tickcolor="rgba(0,0,0,0)", font=dict(color="rgba(0,0,0,0)"),
                      steps=[dict(method="animate", label="", args=[[str(i)], dict(
                          mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))])
                          for i in range(len(plan))])],
    )
    return fig, anim, len(plan)


def render(r, algo, layout, speed=450, autoplay=True):
    fig, anim, n = build_figure(r, algo, layout, speed)
    html = fig.to_html(full_html=True, include_plotlyjs=True, auto_play=autoplay,
                       animation_opts=anim, default_height="580px", default_width="100%",
                       config={"displaylogo": False, "displayModeBar": False})
    html = html.replace("<head>", "<head><style>html,body{background:transparent;margin:0;overflow:hidden}</style>", 1)
    components.html(html, height=600)
    return n
