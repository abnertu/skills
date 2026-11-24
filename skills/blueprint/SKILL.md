---
name: blueprint
description: Write a blueprint of a change before you build it, with its behaviors and the evidence that proves each one. Then build the change until all evidence passes. Claude Code and Codex can continue a blueprint in any session. Append the task. Append `codex` to use Codex for reviews and delegated work. Append nothing or `status` to list the open blueprints.
argument-hint: "[codex] [task | status]"
disable-model-invocation: true
---

Take one change from a blueprint to a verified done state. The blueprint fixes the target before the code: the **behaviors** that the change must show and the **evidence** that proves each one. The change is done when all evidence passes. Review finds defects that the evidence misses. Review does not decide when the work is done.

## The blueprint file

Keep each blueprint in `.blueprints/<slug>.md` at the repo root. Add `.blueprints/` to the file that `git rev-parse --git-path info/exclude` names, so that Git ignores the blueprints. Outside a Git repo, ask the user where to keep the blueprint.

Use this structure:

```markdown
# <title>

Status: planning | approved | implementing | verifying | done | cancelled
Base: <commit at approval>
Review: full | light
Parent: <path of the parent blueprint, or none>

## Goal
## Scope
## Out of scope
## Behaviors
- [ ] B1: Given <context>, when <action>, then <observable result>.
  Evidence: <existing | check | test>: <command>. Result: <result>
## Steps
- [ ] <step>. Serves: B1
## Next
## Decisions
## Backlog
## Review log
```

A blueprint is **open** until its status is `done` or `cancelled`. Set `cancelled` when the user drops the blueprint or a split replaces it. Write the reason and the replacing blueprints in **Next**.

The blueprint file is the single source of truth for progress. Update it after each step, review round and verification.

Keep the blueprint ready for a **handoff**. An agent in Claude Code or Codex must continue from the blueprint and Git alone. This applies in a new session and after a compact:

- Write each evidence as a shell command or a file state. Write no tool or subagent of one runtime.
- **Next** holds the next action, work that is not committed and its state, and the gotchas of the current session.
- Runtime state, such as a reviewer thread, does not survive a handoff. Record its results in the blueprint.

## Evidence

Each behavior has one evidence. Choose the first kind that proves the behavior:

1. **existing**: a test, build or lint that the repo already runs covers the behavior. Run it.
2. **check**: a one-off command, script or run of an entry point proves the behavior. Record its output as the result. Keep the check out of the repo.
3. **test**: a permanent test in the repo. Write one only when all of these are true:
   - The behavior is a contract that a later change can break.
   - No existing test covers it.
   - The test fails when the behavior breaks.

A test proves a behavior only when you saw it fail first. Write it before the code, or revert the fix and run it. Test a behavior through its public interface, with one test for each behavior. A test that checks source text, private structure or mock calls does not prove a behavior.

If the repo's rules set a different bar for tests, follow the repo.

## 1. Settle the arguments

Read the text after the skill name.

- If it is empty or `status`, run the status report below and stop.
- If it contains `codex`, set up Codex as described in [Codex](#codex). Then remove `codex` from the task text.
- If an open blueprint in `.blueprints/` matches the task, resume it as described in [Resume](#resume). Do not start a second blueprint.

## 2. Write the blueprint

1. Survey the repo before you write the blueprint.
2. Read its `AGENTS.md` or `CLAUDE.md`, the code that the task touches and the related tests.
3. Ask the user about each choice that the files do not settle.

Write the blueprint file:

- **Scope** names what changes. **Out of scope** names the near work that this blueprint leaves alone.
- Each behavior is a result that a user, a caller or a file can observe. A behavior names no implementation.
- Each behavior has an evidence of the first kind in [Evidence](#evidence) that proves it.
- Each step is small enough to commit on its own. It names the files that it changes and the behaviors that it serves.
- **Decisions** records each choice, its reason and who made it.
- **Parent** names the approved blueprint that this blueprint carries out a part of. A child blueprint takes the decisions of its parent.

This step is done when each behavior has an evidence and each step serves a behavior.

## 3. Review the blueprint

Set **Review**. Record the reason in **Decisions**.

- **full**: the blueprint has a decision that only the user can make, changes a public interface, crosses modules or has more than three steps.
- **light**: all other blueprints. A child blueprint is light, unless it changes the scope, the behaviors or the decisions of its parent. Such a change is a change to the parent, as in step 4.

Review the blueprint file. A full blueprint gets one [review](#review). A light blueprint gets one [self-review](#review).

Show the user the reviewed blueprint. After the user approves:

1. Set **Status** to `approved`.
2. Record **Base**.
3. Implement the blueprint.

This is a session boundary.

## 4. Implement

1. Set **Status** to `implementing`.
2. Do the steps in order.
3. Before the code of a step, write each `test` evidence of its behaviors. Run each test and see it fail.
4. Write the code until the evidence of the step's behaviors passes.
5. Commit as the repo's rules say.
6. Check off the step in the blueprint file and update **Next**.

Each step commit is a session boundary.

Use any skill that fits a step, such as a design, test-driven development or debugging skill.

If the work shows that the blueprint is wrong:

1. Stop the step.
2. Fix the blueprint.
3. Review the changed part as in step 3.

A change to the scope or the behaviors needs the user's approval.

## 5. Verify

1. Set **Status** to `verifying`.
2. Run the evidence of each behavior. Record each result and check off each behavior that passes.
3. If an evidence fails, uncheck all behaviors. Then fix the failure and go to item 2.
4. Review the diff from **Base**. A full blueprint gets one [review](#review). A light blueprint gets one [self-review](#review).
5. If the review led to a fix, repeat items 2 and 3 without a second review.

This step is done when one run of all evidence checks off each behavior, and no change follows that run.

## 6. Close

Set **Status** to `done`. Report to the user:

- The blueprint is complete. List each behavior with its evidence and result.
- The commits from **Base**.
- The backlog. Each item is new work for a new blueprint, not open work of this blueprint.

The close is a session boundary.

After you close the blueprint, answer a question about open problems from the blueprint files. A blueprint that is not open has no open work. Report a new finding as a backlog item, and give its concrete failure.

## Review

A review checks one subject: the blueprint file in step 3, or the diff from **Base** in step 5. Each review has a fixed budget.

A **self-review** is one pass by yourself with the full-round instruction below. Sort and fix its findings as in item 2 below. Log it as a round. With `codex`, run one Codex full round in place of each self-review, with no delta round.

A review of a full blueprint runs these rounds:

1. Run one **full round**: a new reviewer with fresh context reviews the whole subject. Use a subagent, or Codex with `codex`.
2. Sort each finding as below. In a diff review, uncheck all behaviors before the first fix. Fix each defect.
3. Run one **delta round** only if a fix changes a behavior, an evidence or a public interface. The reviewer of the full round checks only the fixes.
4. If the delta round finds a defect, show it to the user. Ask whether to fix it and stop, or to split the blueprint.

Continue a reviewer with SendMessage in Claude Code, or with `--resume` for Codex. If the runtime cannot continue a reviewer, run the delta round yourself. If the runtime has no subagent, run each round yourself in a separate pass.

Sort each finding:

- **Defect**: an in-scope problem with a concrete failure. Fix it.
- **Decision**: a choice that only the user can make. Ask the user. Record the answer in **Decisions**.
- **Backlog**: an improvement outside the scope, or a finding with no concrete failure. Add it to **Backlog**. It stays out of this blueprint, unless the user adds it to the scope.

Log each round in **Review log** in one line: the subject, the kind, the reviewer, the count of each tag and the count of defects that led to a fix. These counts show whether the reviews pay off.

Give a full-round reviewer the blueprint file path, the diff range for a diff review, and this instruction:

> 1. Review the subject against the blueprint and the repo.
> 2. Read the files that the blueprint names, and the code and tests that use them.
> 3. Find every defect in this one pass, such as:
>    - Missing or wrong behaviors.
>    - Evidence that passes when its behavior breaks.
>    - Permanent tests that fail the bar of the evidence rules below.
>    - Wrong assumptions about the code.
>    - Unhandled failure cases.
>    - Conflicts with the repo's rules.
> 4. Treat **Decisions** and **Out of scope** as settled. Skip findings that **Backlog** holds.
> 5. Write one line for each finding: its tag (`defect`, `decision` or `backlog`), its location and the concrete failure that it causes.
> 6. Write only these lines.

Append the section [Evidence](#evidence) to the instruction as the evidence rules, because the reviewer does not have this skill.

Give a delta-round reviewer the fixes and this instruction. Give the fixes as a commit range or as a list of the blueprint edits:

> Check these fixes. Find defects in each fix and in the parts of the subject that the fixes affect. Write the findings in the same format.

## Session boundaries

At each session boundary, judge whether the current session should continue. Judge from the work, because the runtime does not show usage limits reliably.

- **New session**: the blueprint is done, or the next work needs none of the current context. Tell the user to start it in either runtime with this skill and the task.
- **Compact**: the next step continues the current work, and the context holds much material that the rest of the blueprint does not need. Examples are long logs and large file reads. Tell the user to compact the context.
- Otherwise, continue without a hint.

1. Update **Next** before you give the hint.
2. Give the hint in one line.
3. End the turn, so that the user can act on it.

## Resume

1. Read the blueprint file. Start from **Status** and **Next**.
2. If **Status** is `planning`, continue at step 2 or step 3. The blueprint has no **Base** yet.
3. Otherwise:
   1. Run `git log --oneline <Base>..HEAD` and `git status`.
   2. Compare them with the checked steps, the checked behaviors and **Next**.
   3. Fix the blueprint file where it differs from Git.
4. Continue from the step that **Status** names.

## Status report

List each open blueprint in `.blueprints/` with its status, its next action, its unchecked behaviors and its backlog size. If no blueprint is open, report that no blueprint is open.

## Codex

The `codex` option needs Claude Code with codex-plugin-cc. In another runtime, tell the user and continue without Codex.

Ask the user in one question which model and which effort Codex uses. Offer the `model` and `model_reasoning_effort` of `~/.codex/config.toml` as the default. The efforts are:

- `none`
- `minimal`
- `low`
- `medium`
- `high`
- `xhigh`

Run Codex through the `codex:codex-rescue` subagent. Pass `--model <model> --effort <effort>` in each request.

- **Review**: ask for a read-only run with the input of the [review](#review). Pass `--fresh` for a full round and `--resume` for a delta round. `--resume` continues the last Codex thread. Fix the findings of a review yourself, so that the review thread stays the last thread.
- **Delegated work**:
  1. Ask for a write run for one blueprint step.
  2. Give the step, the blueprint file path and the files that the step changes.
  3. Check the result against the step and its evidence before you check the step off.
