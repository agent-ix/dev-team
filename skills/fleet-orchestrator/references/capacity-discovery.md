# Capacity discovery

Each host's sustainable lane count is unknown until measured. Discovery ramps lanes only. Build slots are computed by the build scheduler from live headroom and read from `ix_build_slots_sustainable`; the orchestrator does not change them. Discovery state and the capacity history are produced by `ix-board fleet capacity` (SWM-216, SWM-252), which is not on main; until it is installed, state that no capacity record exists and start no run, because a run that cannot be recorded would breach ORCH-R19 (Interim mode). ORCH-R16 to ORCH-R24, ORCH-R28 and ORCH-R29 are `n.a.` meanwhile.

## Procedure, per host

1. **Start.** A host with no recorded level starts a run when the ready-buffer deficit is zero and the capacity history is available to record the run (ORCH-R20). A host runs at most 2 discovery runs a day, first runs and re-discoveries counted together (ORCH-R24). `fleet tick` suppresses `add_lane` for a host while its run is active.
2. **Step.** Add one lane per step (ORCH-R16). A run takes at most 8 steps; a run that reaches the bound ends with reason `step_bound` and records the last valid level (ORCH-R21).
3. **Hold.** Keep each level for the measurement window, default 2 hours, and hold each step for it (ORCH-R16). The first 30 minutes after a lane is added are ramp-up and are excluded from the measurement.
4. **Demand gate.** Judge a step only on a window in which `ix_fleet_ready_buffer_deficit` was zero throughout. Any other window is inconclusive and is repeated (ORCH-R17). After 2 inconclusive windows in a row the run ends with reason `inconclusive_no_demand`, and the host returns to the last level measured on a valid window (ORCH-R28). The deficit is sent to the planners (ORCH-R14).
5. **Measure.** Per level, host output is tickets closed plus pull requests merged per hour, summed over the host's lanes. When a window has fewer than 5 of those combined, use commits pushed per hour for that comparison. Also read throttled time (`ix_build_pause_seconds_total`, `ix_build_admission_blocked_seconds_total`), memory and thermal headroom (`ix_build_probe_value`), and build slots busy against sustainable (`ix_build_slots_busy`, `ix_build_slots_sustainable`).
6. **Knee.** A valid step is past the knee when the gain in total host output over the previous level is below 50% of the previous level's mean per-lane output, or the throttled share exceeds 5% of the window. Stop at the first knee signal (ORCH-R18).
7. **Hold at the knee.** Step back one lane and keep the host at that level (ORCH-R18).
8. **Build-slot saturation.** When build slots busy equal sustainable slots for a whole valid window, the run ends with reason `build_slots_saturated` at the current level, records it, and does not raise the host further. This is not a knee (ORCH-R29).
9. **Record.** Record the found level and the reason the run ended (`knee`, `build_slots_saturated`, `step_bound`, `inconclusive_no_demand`) with the window, host output, throttled share, headroom and slot use it was measured at (ORCH-R19).

## Step-down, cool-off and drain

- **Overload.** When memory headroom falls below the profile reserve, or the scheduler aborts a build for a thermal limit, mark one lane draining in the same cycle and send it no new assignment (ORCH-R25).
- **Throttle.** A host throttled above 5% for an hour at its recorded level steps down one lane and is re-discovered when the daily cap allows (ORCH-R22, ORCH-R24).
- **Cool-off.** After a step-down, do not raise the host above the stepped-down level before the cool-off ends, default 6 hours (ORCH-R23).
- **Drain.** A draining lane finishes its current ticket to a commit or pull request and is never removed during a build (ORCH-R26). A drain still open after the drain cap, default 4 hours, is escalated to the lane's code lead by the minder's `escalate_drain` send (ORCH-R30, MIND-R20). An `escalate_drain` addressed to the orchestrator is acted on under ORCH-R10, citing the ledger action row (ORCH-R30).
- **Evidence for any reduction.** Lower a lane count for a thermal or memory reason only with scheduler evidence at that time (ORCH-R12). Knee, throttle and overload step-downs are the recorded exceptions.
