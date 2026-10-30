"""Render the accepted motivation studies with absolute q0 ROUGE-L anchors."""

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnchoredOffsetbox, DrawingArea, HPacker, TextArea

PAPER = Path(__file__).resolve().parents[1]
ARCHIVE = PAPER.parent / 'FedLLM/exp/_archive_exps'
SWEEP = ARCHIVE / '0928_motivation_q0_8_ranks/report/ni_client_metrics.csv'
PAIRS = (ARCHIVE / '0929_ni16_dir05_round_similarity/local_batch/runs/'
         'ni_10x10_r16_32_64_dir05_q8/cosine/pairs.csv')
RANKS = (16, 32, 64)
COLORS = {16: '#D99259', 32: '#599EC4', 64: '#59B89E'}
MARKERS = {16: 'o', 32: 's', 64: '^'}


def read_rows(path):
    with path.open(newline='') as handle:
        return list(csv.DictReader(handle))


def data():
    rows = [r for r in read_rows(SWEEP)
            if r['rank_group'] == 'r16_32_64' and r['layout'] == 'dir05']
    assert len(rows) == 9 * 16
    by_group = defaultdict(list)
    for row in rows:
        by_group[int(row['q']), int(row['client_rank'])].append(float(row['rougeL']) * 100)
    absolute = {}
    for q in range(9):
        for rank, count in zip(RANKS, (6, 5, 5)):
            assert len(by_group[q, rank]) == count
            absolute[q, rank] = mean(by_group[q, rank])
    bases = {rank: absolute[0, rank] for rank in RANKS}
    deltas = {rank: [absolute[q, rank] - bases[rank] for q in range(9)]
              for rank in RANKS}

    pairs = read_rows(PAIRS)
    assert len(pairs) == 1200
    gaps = defaultdict(list)
    for rnd in range(10):
        current = [r for r in pairs if int(r['round']) == rnd]
        assert len(current) == len({(r['client_i'], r['client_j']) for r in current}) == 120
        for rank in RANKS:
            same_rank = [float(r['upload_effective_delta']) for r in current
                         if int(r['rank_i']) == int(r['rank_j']) == rank
                         and r['same_domain'] == 'False']
            same_domain = [float(r['upload_effective_delta']) for r in current
                           if rank in (int(r['rank_i']), int(r['rank_j']))
                           and r['same_rank'] == 'False' and r['same_domain'] == 'True']
            assert (len(same_rank), len(same_domain)) == {16: (13, 14), 32: (9, 13), 64: (9, 13)}[rank]
            gaps[rank].append(mean(same_rank) - mean(same_domain))
    return bases, deltas, gaps


def baseline_row(ax, bases):
    parts = [TextArea('R-L (%):', textprops={'fontsize': 6.25, 'color': '#555555'})]
    for rank in RANKS:
        marker = DrawingArea(4, 6, 0, 0)
        marker.add_artist(Line2D([2], [3], marker=MARKERS[rank], markersize=2.8,
                                 color=COLORS[rank], linestyle='none'))
        value = TextArea(f'{bases[rank]:.2f}',
                         textprops={'fontsize': 6.25, 'color': '#444444'})
        parts.append(HPacker(children=[marker, value], align='center', pad=0, sep=0.6))
    row = HPacker(children=parts, align='center', pad=0, sep=2.4)
    box = AnchoredOffsetbox(loc='center', child=row, pad=0, borderpad=0,
                           frameon=False, bbox_to_anchor=(.5, 1.08),
                           bbox_transform=ax.transAxes)
    ax.add_artist(box)
    return box


def main():
    bases, deltas, gaps = data()
    plt.rcParams.update({
        'font.family': 'DejaVu Serif', 'mathtext.fontset': 'dejavuserif',
        'font.size': 7.5, 'axes.labelsize': 7.5, 'axes.titlesize': 7.5,
        'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5, 'legend.fontsize': 7.5,
        'axes.linewidth': .55, 'lines.linewidth': 1.0,
        'axes.spines.top': False, 'axes.spines.right': False,
        'pdf.fonttype': 42, 'ps.fonttype': 42,
    })
    plot_width = 295.2
    width = plot_width + 54
    height = 116.32
    fig = plt.figure(figsize=(width / 72, height / 72), dpi=72)
    axes = [fig.add_axes([left / width, 24.6 / height,
                         98.0244274809 / width, 60.48 / height])
            for left in (33.948, 192.7475725191)]
    handles = []
    for rank in RANKS:
        line, = axes[0].plot(range(9), deltas[rank], color=COLORS[rank],
                             marker=MARKERS[rank], markersize=2.4,
                             markeredgewidth=.4, label=f'rank {rank}')
        handles.append(line)
        axes[1].plot(range(10), gaps[rank], color=COLORS[rank],
                     marker=MARKERS[rank], markersize=2.4, markeredgewidth=.4)
    for ax in axes:
        ax.axhline(0, color='#777777', lw=.65, ls=(0, (3, 2)), zorder=0)
        ax.grid(axis='y', color='#e5e5e5', lw=.45, zorder=0)
        ax.tick_params(width=.55, length=2, pad=2)
    # Historical source keys use q; panel (a) follows the manuscript's s notation.
    axes[0].set(xticks=range(9), xlim=(-.15, 8.15), ylim=(-1.15, 1.05),
                yticks=[-1, -.5, 0, .5, 1], xlabel='Shared rank $s$',
                ylabel=r'$\Delta$ ROUGE-L (pp)')
    axes[1].set(xticks=range(10), xlim=(-.15, 9.15), ylim=(-.18, .35),
                yticks=[-.15, 0, .15, .30], xlabel='Training round', ylabel='Cosine gap')
    for ax in axes:
        ax.xaxis.labelpad = 3
        ax.yaxis.labelpad = -.25
    subtitles = []
    for ax, title, subtitle in zip(axes,
                                  ('(a) Shared width', '(b) Similarity ($q=8$)'),
                                  ('relative to $s=0$', 'same rank − same domain')):
        ax.text(.5, 1.415, title, ha='center', va='center', transform=ax.transAxes)
        subtitles.append(ax.text(.5, 1.25, subtitle, ha='center', va='center',
                                 color='#555555', transform=ax.transAxes))
    baseline = baseline_row(axes[0], bases)
    legend = fig.legend(handles=handles, loc='center left',
                        bbox_to_anchor=((plot_width + 5) / width,
                                        (24.6 + 60.48 / 2) / height),
                        ncol=1, frameon=False, handlelength=1.1,
                        handletextpad=.3, labelspacing=.7, borderaxespad=0)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    baseline_bbox = baseline.get_window_extent(renderer)
    # Align the right description with the center of the two-line left block.
    subtitle_bbox = subtitles[0].get_window_extent(renderer)
    description_center_y = (subtitle_bbox.y1 + baseline_bbox.y0) / 2
    subtitle_y = axes[1].transAxes.inverted().transform((0, description_center_y))[1]
    subtitles[1].set_y(subtitle_y)
    assert baseline_bbox.width < axes[0].get_window_extent(renderer).width + 10
    legend_bbox = legend.get_window_extent(renderer)
    assert legend_bbox.x0 > axes[1].get_window_extent(renderer).x1
    assert legend_bbox.x1 <= fig.bbox.x1 + .1
    assert legend_bbox.y0 >= fig.bbox.y0 - .1
    assert legend_bbox.y1 <= fig.bbox.y1 + .1
    for text in [*fig.texts, *axes[0].texts, *axes[1].texts,
                 *(ax.xaxis.label for ax in axes), *(ax.yaxis.label for ax in axes)]:
        bbox = text.get_window_extent(renderer)
        assert bbox.x0 >= -.5 and bbox.x1 <= fig.bbox.width + .5, (text.get_text(), bbox)
        assert bbox.y0 >= -.5 and bbox.y1 <= fig.bbox.height + .5, (text.get_text(), bbox)
    output = PAPER / 'figs/acl_motivation_0928_r16_32_64'
    fig.savefig(output.with_suffix('.pdf'), metadata={
        'Creator': Path(__file__).name, 'CreationDate': None,
        'Title': 'Motivation: shared-width responses and update similarity',
        'Subject': 'Dir(alpha=0.5), ranks 16/32/64; q0 client-macro ROUGE-L baselines (%)',
    })
    fig.savefig(output.with_suffix('.png'), dpi=360)
    plt.close(fig)
    output.with_suffix('.json').write_text(json.dumps({
        'sources': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (SWEEP, PAIRS)},
        'q0_rouge_l_percent': bases, 'delta_rouge_l_pp': deltas, 'cosine_gaps': gaps,
    }, indent=2) + '\n')
    print(output.with_suffix('.png'))
    print('Baseline strip:', {rank: f'{bases[rank]:.2f}' for rank in RANKS})


if __name__ == '__main__':
    main()
