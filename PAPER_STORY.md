# Paper Story — ACL: Allocate–Collaborate

> Current manuscript direction refreshed on 2026-10-14 against the
> [ACL research log](../FedLLM/ACL_Logs/ACL_Logs.md#acl-1003-mainline):
> **ACL-1003 / §39 progressive recipient allocation**, with soft / hard as the
> confirmed implemented research family. The manuscript retains fixed,
> heterogeneous total LoRA ranks, complete training and uploads, and the
> receiver-constrained projection from the soft pipeline.
> On 2026-10-14, by user request, collaboration scoring, strength fitting,
> actual-candidate confirmation, and the dependent allocation rules were
> withdrawn pending a new computable metric and corresponding experiments.
> The workflow, decision rules, method comparison, and conclusion are incomplete
> and marked TODO. The previous soft NI result group is outside the active
> tables; its source records remain in EXPERIMENTS_SOURCES.md and Git history.
> On 2026-10-26, by user request, Fig. 2 and its related text now use the
> accepted 2026-10-23 FLAN eight-client study with two rank budgets, 16 and 64
> (four clients each). The retained baseline tables keep their 2026-10-08
> evidence scope. The current Problem follows the 2026-10-20 definition:
> homogeneous federated LoRA → rank heterogeneity → selective rank sharing
> with a global width → two coupled research challenges.
> DualAda/HIRE is a historical direction. `main.tex` still defines `\sysname`
> as DualAda; that retained macro is not a decision to use the old method.

## Research and evidence entry points

- [Research index](../FedLLM/ACL_Logs/INDEX.md) locates the current method,
  implementation, comparisons, and historical records.
  [ACL research log](../FedLLM/ACL_Logs/ACL_Logs.md#acl-1003-mainline) records the research direction;
  [Current](../FedLLM/ACL_Logs/Current.md) owns live tasks, queues, and blockers.
  This file records manuscript status, not a second experiment queue.
- [§39 mechanism and boundaries](../FedLLM/ACL_Logs/method-39_progressive_recipient_allocation.md),
  the [2026-10-03 design](../FedLLM/exp/_archive_exps/1003_acl_progressive_exchange/design/progressive_allocation_report.md),
  and the [algorithm guide](../FedLLM/docs/algorithms.md#progressive-recipient-allocation-39)
  define the implemented soft pipeline and its limits. They remain sources for
  the retained receiving operator and previous experiments, while the manuscript's
  collaboration metric and decision rules await redesign.
  The old `method_index.md` mapping is now part of
  [INDEX](../FedLLM/ACL_Logs/INDEX.md#acl-1003-implementation).
- [§32 formal challenges](../FedLLM/ACL_Logs/history/method-32_allocate_collaborate.md#formal-challenges)
  and [their original coupling](../FedLLM/ACL_Logs/history/method-32_allocate_collaborate.md#challenge-coupling)
  retain the joint research problem confirmed on 2026-09-10.
  §39 explicitly extends their shared/private supply definition to complete
  uploads with recipient-side protection; historical definitions and results
  retain their original meaning.
- The current
  [Dataset performance](../FedLLM/ACL_Logs/dataset_performance.md) locates the
  accepted ACL-1003 results and matched comparisons.
  [Historical performance](../FedLLM/ACL_Logs/history/dataset_performance.md)
  retains the 1001 baselines, shared-prefix motivation, and older protocols.
  Cite each underlying report and frozen configuration for claims.
- [Baseline reproductions](../FedLLM/ACL_Logs/baseline_reproductions.md) and the
  [historical repaired-baseline report](../FedLLM/exp/_archive_exps/legacy_non_16_32_64/0916_exp_relayout/0913_baseline_repairs/report/README.md)
  define the respective baseline versions and comparison limits.
  [History navigation](../FedLLM/ACL_Logs/history/README.md) owns the old attempts
  and archive mappings, including [DualAda/HIRE](../FedLLM/ACL_Logs/history/dualada/README.md).

## Current problem and writing direction

Client i has a fixed total LoRA budget r_i. The current Problem uses one
common integer shared-prefix width s, with 0 ≤ s ≤ min_i r_i, and a protected
local remainder p_i = r_i − s. Both parts train locally. The server averages
shared B and A factors separately with sample-size weights over all clients,
including self, then broadcasts the prefix; protected remainders stay local.

Allocate asks how to choose the global width under heterogeneous budgets.
Collaborate asks how to adapt external influence under data and rank
heterogeneity. Allocation determines the permitted subspace, and collaboration
determines how external knowledge is applied there, affecting the width's value.
The FLAN motivation illustrates width responses and update geometry; it does
not prescribe a metric, donor rule, strength, or dynamic controller.

The retained §39 Method still uses complete uploads and client-specific
receiving capacity s_i, unlike this global shared-prefix Problem. It awaits
alignment and a new collaboration metric. Do not reinterpret the motivation's
s as §39 reception permission or restore the withdrawn fit/check controller.

[Writing style notes](WRITING_STYLE.md) record the shared techniques inferred
from the local FedMosaic SIGIR 2026 and DarkDistill KDD 2025 reference manuscripts.
Use their problem-to-design reasoning, explicit client/server workflow, and
output-to-input transitions between mechanisms. Each key equation should have
a stated purpose and an explanation of its behavior. Preserve the evidence
limits here when borrowing their presentation structure.

The retained pipeline trains all effective A/B from a personalized state,
freezes complete same-round uploads, and pools all other clients with effective
training-size weights. It projects the full external-minus-full-local BA update
into the receiving prefix's native A subspace, modifying only that prefix's B
columns. All A factors, protected B columns, total rank, scaling, and native
slot identities remain fixed during reception. Zero width or zero strength
retains the local factors exactly. The collaboration metric, strength selection,
capacity comparisons, control conditions, workflow, and associated cost account
are deliberately unwritten until the new design and experimental evidence are
ready. Do not fill these gaps with the former directional fit, repeated check,
or their loss-based controller, and do not invent a replacement metric.
Final test data remain excluded from selection. The motivation plots do not
prove that progressive allocation or a lock is necessary.

The active motivation is the [FLAN eight-client report](../FedLLM/exp/_archive_exps/1023_flan1_motivation/recovery_tail_01/report/flan8c/RESULTS.md)
from the [2026-10-23 frozen protocol](../FedLLM/exp/_archive_exps/1023_flan1_motivation/PROTOCOL.md#additional-authorized-original-eight-client-study).
Its two fixed rank budgets are 16 and 64, with four clients each, using the
original `flan-feddpa1-8c-dir05` split: 300 training and 200 test examples/client.
The eight task categories, client membership, and rank vector
`[16,16,64,16,64,64,16,64]` stay fixed across the width sweep. The model is
Qwen3.5-0.8B, seed615, with ten rounds and ten configured local optimizer
steps/client/round. The existing Dirichlet alpha0.5/IPF allocation matches
local train/test task proportions. No new training or scoring was run for the
2026-10-26 manuscript update.

[Fig. 2](figs/acl_motivation_flan_r16_64.pdf) combines two panels.
Panel (a) compares global widths s=0..8 relative to each rank group's matched
s0 ROUGE-L; its absolute s0 anchors are 64.26% for rank16 and 65.34% for rank64.
At s8, rank16 changes by −0.428953 pp and rank64 by +0.359510 pp.
The overall client mean changes from 64.799145% to 64.764424% (−0.034721 pp).
The observed group peaks at s2 and s3 are descriptive test results, not
confirmed optimal widths or evidence that dynamic allocation is necessary.

Panel (b) uses an independent training-only s8 run, plotting same-rank /
different-domain minus same-domain / different-rank effective-upload-delta
cosine for each rank over R0–R9. R0 is the first completed local round.
Rank16 is positive at R1–R9; rank64 is positive at R1/R9 and negative at
R0/R2–R8. Each group has six same-rank/different-domain pairs and one
same-domain/different-rank pair. Both curves share the sole same-domain
reference, the entailment pair C3/C5; the domain evidence is sparse and the
curves are not independent repeats. All selected cosines are defined.
The diagnostic has 280 raw pair/round records and 20 plotted rank/round values.
It describes geometry, without measuring receiver task benefit or a common
rank-to-domain transition.

The figure uses the requested [archived SVG](../FedLLM/exp/_archive_exps/1023_flan1_motivation/recovery_tail_01/report/flan8c/flan1_motivation_q0_baselines.svg)
and its companion vector PDF, imported without redrawing. DejaVu Serif,
rank16 orange `#D99259`, and rank64 green `#59B89E` are retained.
The Introduction and caption identify FLAN, eight clients, and the two ranks;
the Problem uses their observed responses to motivate global-width selection
and fine-grained collaboration. Full protocol and pair definitions are in
`body/appendix.tex`. The probe uploads/averages only the common prefix and
keeps protected suffixes local; it is not the retained complete-upload Method.
The two panels do not demonstrate allocation-by-collaboration interaction,
causal rank effects, or method superiority. Decision rules belong in Method.
[Motivation evidence and its role](EXPERIMENTS_SOURCES.md#motivation-evidence-and-its-role-in-the-problem)
records raw sources, metric precision, pair denominators, and asset hashes.

Use **ROUGE-L (R-L) as the primary reporting metric** in the narrative, main
figures, and result comparisons; F1, EM, and PPL provide supplementary evidence.
Keep metric names, captions, assets, and values consistent with the source report.
This reporting preference does not change historical validation-selection criteria.

## Implemented method family and manuscript boundaries

| Item | Role and current boundary |
|---|---|
| [§39 / ACL-1003 soft](../FedLLM/ACL_Logs/method-39_progressive_recipient_allocation.md) | Implemented family underlying the retained complete-upload and projected receiving operator. The former fitted/checked strength and loss-based capacity control are withdrawn from the Method pending the new metric. |
| §39 / hard | Same-family reference with only holds or reductions in recipient capacity; it shares the pooled target, strength fitting, and actual-candidate checks. It is not an independent baseline. |
| §39 / `local`, `fixed`, `schedule`, and extensions | Paired controls or our method variants. `repair`, `multi`, `uplink_proxy`, and drop-veto do not belong to the base soft pipeline; costs and frozen versions must be reported separately. |
| §32 / `acl_0909_motivation_rank_sweep` (old `acl`) | Common shared prefix q with FedAvg and a local suffix; a motivation sweep and special case of the joint problem. |
| §32 / `acl_0908_allocate_collaborate` (old `allocate_collaborate`) | Fixed-graph allocation/reception motivation implementation. The later performance tables call this Allocate–Collaborate; that row is not the full joint research problem or a selected final method. |
| [§33 Slot Competition](../FedLLM/ACL_Logs/history/method-33_slot_competition.md) | Historical attempt: external rank-one directions compete with local slots by equal-budget replacement benefit; persistent slot roles and receiver choices couple allocation and collaboration. Includes extra shadow training and validation cost. |
| [§34 Joint Benefit](../FedLLM/ACL_Logs/history/method-34_benefit_joint.md) | Historical attempt: each shared width searches a donor and reception strength, compresses the BA mixture to budget, and compares train-heldout/paired-lookahead benefit with exact self fallback. The implemented search is a finite-grid, single-donor approximation. |
| [§35–38](../FedLLM/ACL_Logs/history/README.md#historical-implementations) | Component cosine, Slot Prefix, Task-metric Residual Exchange, and Budgeted Residual Distillation are historical attempts, not concurrent defaults or independent baselines. |

The historical Slot Competition and Joint Benefit evidence retains its own scope:
gains against LocalOnly are small or layout-dependent, and single-seed results
do not establish a stable or compute-matched advantage. In the dir05 Joint
Benefit pilot, h1 adds optimizer work without improving over h0; use that pilot's
own LocalOnly control rather than the different Slot batch control.
The selected §39 mainline does not turn those earlier runs into evidence for
soft, nor does a decrease in recipient capacity establish capacity graduation.
Complete uploads and local training rank do not decrease with reception capacity.
In the implemented §39 protocol, candidate downloads, calibration gradients,
check forwards, and the feedback round trip remain part of its computation and
communication costs; the pending metric will require its own cost account.

## Evidence available for writing

- Evidence for the implemented §39 family is indexed in
  [§39](../FedLLM/ACL_Logs/method-39_progressive_recipient_allocation.md) and the
  [current performance table](../FedLLM/ACL_Logs/dataset_performance.md).
  The [2026-10-12 repaired-run record](../FedLLM/exp/_archive_exps/1011_acl1003_progressive_rerun_dualhost/completed/README.md)
  and [implementation fixes](../FedLLM/exp/_archive_exps/1011_acl1003_code_fixes/README.md)
  distinguish accepted soft/hard runs from the superseded 2B configurations
  that actually inherited Local settings. Their raw-prompt, validation, model,
  and PPL-sample scopes remain separate from the manuscript's existing NI/GLUE
  tables. These newer results are not imported by the present writing task.
  Single-seed results and self-fallback drops remain exploratory; decreasing
  reception permission alone does not establish that beneficial capacity
  graduated as training matured.

- The active combined motivation figure is
  [acl_motivation_flan_r16_64.pdf](figs/acl_motivation_flan_r16_64.pdf), with the
  [SVG source](figs/acl_motivation_flan_r16_64.svg) preserved in the paper repo.
  The [FLAN eight-client report](../FedLLM/exp/_archive_exps/1023_flan1_motivation/recovery_tail_01/report/flan8c/RESULTS.md),
  [full-precision client metrics](../FedLLM/exp/_archive_exps/1023_flan1_motivation/recovery_tail_01/report/flan8c/metrics.csv),
  [geometry/counts](../FedLLM/exp/_archive_exps/1023_flan1_motivation/recovery_tail_01/report/flan8c/geometry.csv),
  and [summary with raw paths/hashes](../FedLLM/exp/_archive_exps/1023_flan1_motivation/recovery_tail_01/report/flan8c/summary.json)
  trace all 72 client metric rows and 20 cosine points. The paired s0 control
  belongs to this sweep, not to the separate NI/GLUE baselines or §39 method.
  This is single-seed descriptive evidence with a shared one-pair domain reference.
- The [0925 NI16 mixed-layout sweep](../FedLLM/exp/_archive_exps/legacy_non_16_32_64/0925_ni_dir_motivation/README.md)
  uses Qwen3.5-0.8B, fixed ranks 8/32/128, 10 rounds × 10 local steps,
  microbatch2/accum4, full 1000-example training pools, and 200 test examples/client.
  It reuses the original single-layout protocol; q1–8 contain no matched q0.
  Small q2 peaks and different rank-group responses are descriptive. Task mixture,
  capacity, aggregation, and optimization remain intertwined.
- The [E1 original-test review](../FedLLM/ACL_Logs/history/2026-09-26_motivation_review.md#22-e1-原-test-的新-seed-复验)
  reports NI16 dir05 seeds626–628, q0/1/2, with the full training pool and
  the same ACL implementation. Mean q2−q0 R-L is +0.072pp, with unadjusted
  paired-t95% CI [−0.299,+0.442]pp. This previously examined test set is
  descriptive replication, not independent confirmation. This writing task did
  not read the frozen K holdout or E2 intermediate metrics.
- The [fixed-graph motivation report](../FedLLM/exp/_archive_exps/legacy_non_16_32_64/.replaced_0908_allocate_collaborate_motivation_20260914/report/report.md)
  supports allocation-by-reception-strength interaction within its protocol.
  It uses Qwen3.5-2B, NI10, 20 rounds × 10 local steps, and seeds616–618;
  it is distinct from the later Qwen3.5-0.8B NI16 studies. The R-L interaction
  is −0.914pp, with paired-t95% CI [−0.989,−0.839]pp. Configurations were
  frozen using seed615 validation NLL; R-L was a secondary generation endpoint.
  Both confirmed strengths prefer q1; this does not prove an optimal-allocation
  reversal or the necessity of dynamic allocation.
- The [ACL16 sweep](../FedLLM/exp/_archive_exps/legacy_non_16_32_64/0916_exp_relayout/0910_acl_16c_step10/report/README.md) and
  [similarity table](../FedLLM/exp/_archive_exps/legacy_non_16_32_64/0916_exp_relayout/0910_acl_16c_step10/report/identification.csv)
  retain a historical collaboration-signal diagnostic: Qwen3.5-0.8B, four domains, 16 clients,
  ranks 8/32/128, seed615, q1..8, 10 rounds × 10 optimizer steps, full participation;
  q8 uses `q8_recovery`. Cosines use final-round uploads relative to the pre-round
  global state. Generation metrics use final post-aggregation personalized adapters,
  200 test examples/client. Pair means are diagnostics, not measured transfer utility.
  The source report and similarity table retain all four domain/rank pair groups
  and describe the primary ROUGE-L figure and F1 variant.
- Historical attempt evidence is indexed in §33–34 and
  [historical performance](../FedLLM/ACL_Logs/history/dataset_performance.md).
  The [0913 coverage batch](../FedLLM/exp/_archive_exps/legacy_non_16_32_64/0916_exp_relayout/0913_acl_ni4_coverage/README.md) adds
  the fixed-graph Allocate implementation on five layouts, Joint Benefit h1 on
  four, and Slot Competition on 16c-single. It uses Qwen3.5-0.8B, seed615,
  10 rounds × 10 steps, bs1/accum8 and the corresponding client rank layouts.
  Allocate uses fixed q=1, reception strength 0.25, and a near rank-stratified graph.
  Training-pool sizes, external validation data, and selection compute differ
  between protocols despite matching main optimizer budgets and test identities.
  The 16c-single layout now has completed LocalOnly, FlexLoRA, FLoRA, HetLoRA,
  PF²LoRA, pFedLoRA, and FedRoRA controls in the 2026-09-15 summary; these use the
  recorded single-baseline and FedRoRA protocols rather than motivation-sweep runs.
- Historical 0913 FlexLoRA, PF²LoRA, and pFedLoRA comparisons must use the
  [repaired results](../FedLLM/exp/_archive_exps/legacy_non_16_32_64/0916_exp_relayout/0913_baseline_repairs/report/README.md), not the
  superseded scores retained in older reports. That PF²LoRA protocol uses native rank 4+2,
  so it is not capacity-matched to ranks 8/32/128. PF reruns also change paired
  randomness, so old/new differences are not single-bug causal ablations.
  Preserve each report's training membership, validation selection, and precision.
- The [FedRoRA report](../FedLLM/exp/_archive_exps/legacy_non_16_32_64/0918_fedllm_runs_retirement/0914_fedrora/report/README.md) provides an
  independent four-layout baseline under the 936-example train-heldout protocol.
  Its normalized-direction and rank-wise-magnitude implementation is a transfer
  of the published method, with one seed and no test-driven selection.
- The [coverage evaluation recovery](../FedLLM/exp/_archive_exps/legacy_non_16_32_64/0916_exp_relayout/0913_acl_ni4_coverage/eval_acceptance_recovery/README.md)
  retains 78 empty Allocate predictions on Multi-News in the full-sample metrics.
  Archived outputs lack raw tokens/finish reasons, so their termination status
  cannot be inferred. Do not remove empty predictions to improve reported metrics.

## Current manuscript status

Manuscript revisions are maintained in Git history.
The standalone numbered drafts were removed on 2026-10-13; current files are
updated in place without creating separate manuscript backups.

- The current Problem follows the 2026-10-20 global-width definition:
  Preliminaries establish homogeneous LoRA, heterogeneous fixed budgets,
  and selective rank sharing before the two research challenges.
  The 2026-10-26 update replaces the Fig. 2 motivation evidence with the
  completed FLAN eight-client study using ranks16/64, four clients each.
  Introduction, Problem, caption, and setup appendix now match that figure.
  The two challenges and their structural coupling remain global-width
  selection and adaptation of external influence; no decision metric is added.
- Fig. 2 uses `figs/acl_motivation_flan_r16_64.pdf`, with an identical copy of
  the requested SVG at `figs/acl_motivation_flan_r16_64.svg`. Both match their
  archived report assets byte-for-byte. The caption explains the per-group
  s0 reference and the independent s8 cosine diagnostic, and references
  the Appendix's `sec:appendix:motivation-setup` for protocol details.
  The old NI PDF remains an existing asset but is no longer cited by the
  manuscript; its historical plotting script does not generate the FLAN figure.
- On 2026-10-14, by user request, `body/4-method.tex` retains complete local
  training/uploads, the frozen pooled BA target, and the native-subspace receiving
  operator from the earlier §39 soft draft. Strength fitting, actual-candidate
  confirmation, their loss metric, marginal capacity comparisons, EMA/margin
  control conditions, the algorithm box, and the associated cost description
  have been removed. The new computable collaboration metric, strength and
  capacity decisions, and round workflow are marked TODO pending design and
  experimental evidence. The former Soft Allocation Details section and its
  configuration table were removed from the Appendix. `WRITING_STYLE.md` now
  keeps the general writing preferences without prescribing the withdrawn
  fit/check pipeline. Previous text remains accessible through Git history;
  no implementation or experiment in the sibling FedLLM repository was changed.
- The Introduction describes selective rank sharing and the FLAN motivation,
  with the method overview and contribution summary still TODO. The abstract
  remains TODO. Related Work's closing paragraph introduces the two questions.
- On 2026-10-08, by user request, `body/5-exp.tex`'s baseline results were refreshed
  using only Dir(alpha=0.5) and the accepted rank-16/32/64 batches from 2026-10-01.
  The main experiments report NI and GLUE client-macro ROUGE-L in two
  dataset-specific tables, covering eight independent/local baselines including
  Het-CPFLoRA. By subsequent user request, MMLU-Pro's MC accuracy table and its
  evaluation setup are provisionally kept in the Appendix; inclusion in the final
  paper remains undecided.
  Missing baseline/dataset entries remain unfilled. NI and GLUE have 16 clients
  with rank-group counts 6/5/5; MMLU-Pro has 13 clients with counts 5/5/3.
  All entries use Qwen3.5-0.8B, seed615, and checkpoint R9 after 10 rounds.
  The text records the NI 936-versus-1000 training-pool difference, PF²LoRA's
  updated common-4/private-(r_i-4) ranks, and Het-CPFLoRA's shared-3/4 split and
  paper-DWI generation protocol.
  The former separate NI group contained accepted §39 R9 evaluations from
  the 2026-10-08 archive: soft (ours) at 57.1707%, drop-veto (our variant) at
  57.0080%, and the matched LocalOnly control at 57.0806%. On 2026-10-14 these
  rows and their comparison prose were withdrawn along with the collaboration
  metric. Their frozen protocols, source scores, and additional computation
  remain documented in `EXPERIMENTS_SOURCES.md`; they do not evaluate the pending
  metric. The experiment chapter marks the method comparison TODO, while the
  15 baseline cells across NI, GLUE, and the provisional MMLU-Pro appendix retain
  their values and protocols.
  Slot Competition, Slot Prefix, Allocate–Collaborate, and Benefit Joint historical attempts
  remain outside the reported tables.
  [Experiment sources](EXPERIMENTS_SOURCES.md) trace all 18 previously reported
  cells to raw metrics, frozen configurations, and acceptance records, explicitly
  distinguishing the 15 retained baseline cells from the three withdrawn §39 cells.
- The Conclusion retains the receiving-capacity problem and motivation, with
  the method/result summary marked TODO after the 2026-10-14 withdrawal.
  The Appendix contains Motivation Study Setup and the provisional MMLU-Pro
  baselines. The unrelated Main/Assistant sensitivity study remains outside
  the active chapter.
  `main.tex` retains the title, author, and DualAda macro.
