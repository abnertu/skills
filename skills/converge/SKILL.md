---
name: converge
description: Plan a change, review the plan until a review finds nothing in scope, then build and verify it to a done state. Append the task. Append `codex` to use Codex for reviews and delegated work. Append nothing or `status` to list the open plans.
argument-hint: "[codex] [task | status]"
disable-model-invocation: true
---

Take one change from plan to a verified done state. A review loop must **converge**: it ends on a **clean pass**, a review round with no in-scope finding.

A loop converges only against a fixed scope and fixed done criteria. A reviewer can always find more to improve. The scope decides which findings count.

## The plan file

Keep each plan in `.plans/<slug>.md` at the repo root. Add `.plans/` to the file that `git rev-parse --git-path info/exclude` names, so that Git ignores the plans. Outside a Git repo, ask the user where to keep the plan.

Use this structure:

```markdown
# <title>

Status: planning | approved | implementing | verifying | done
Base: <commit at approval>
Review: full | light
Parent: <path of the parent plan, or none>

## Goal
## Scope
## Out of scope
## Done criteria
- [ ] <observable result>. Verify: <command or check>. Evidence: <result>
## Steps
- [ ] <step>
## Next
## Decisions
## Backlog
## Review log
```

The plan file is the single source of truth for progress. Update it after each step, review round and verification.

Keep the plan file ready for a **handoff**. A new session must continue from the plan file and Git alone. **Next** holds what the plan does not hold yet:

- The next action.
- Work that is not committed, and its state.
- Gotchas and partial findings of the current session.

## 1. Settle the arguments

Read the text after the skill name.

- If it is empty or `status`, run the status report below and stop.
- If it contains `codex`, set up Codex as described in [Codex](#codex). Then remove `codex` from the task text.
- If an open plan in `.plans/` matches the task, resume that plan as described in [Resume](#resume). Do not start a second plan.

## 2. Plan

Survey the repo before you write the plan. Read its `AGENTS.md` or `CLAUDE.md`, the code that the task touches and the related tests. Ask the user about each choice that the files do not settle.

Write the plan file:

- **Scope** names what changes. **Out of scope** names the near work that this plan leaves alone.
- Each done criterion is an observable result with a check that proves it, such as a command, a test or a file state.
- Each step is small enough to commit on its own and names the files that it changes.
- **Decisions** records each choice, its reason and who made it.
- **Parent** names the approved plan that this plan carries out a part of. A child plan takes the decisions of its parent.

This step is done when each done criterion has a check and each step serves a criterion.

## 3. Review the plan until it converges

Set **Review** before the first round. Record the reason in **Decisions**.

- **full**: the plan has a decision that only the user can make, changes a public interface, crosses modules or has more than three steps.
- **light**: all other plans. A child plan is light, unless it changes the scope, the done criteria or the decisions of its parent. Such a change is a change to the parent plan, as in step 4.

A full review uses a reviewer with fresh context in each round: a subagent, or Codex with `codex`. If the runtime has no subagent, review the plan yourself in a separate pass. A light review is one pass by yourself. If the light pass finds a defect, fix it and set **Review** to `full`.

Give the reviewer the plan file path and this instruction:

> Review this plan against the repo. Find missing steps, wrong assumptions about the code, done criteria that cannot be checked, unhandled failure cases, and conflicts with the repo's rules. For each finding, give the concrete failure that it causes. Tag each finding `defect`, `decision` or `backlog`.

Sort each finding:

- **Defect**: an in-scope problem with a concrete failure. Fix the plan.
- **Decision**: a choice that only the user can make. Ask the user. Record the answer in **Decisions**.
- **Backlog**: an improvement outside the scope, or a finding with no concrete failure. Add it to **Backlog**. It does not start a new round.

Log each round in **Review log** with its finding counts. After you fix the defects, start a new round. The loop converges on a clean pass with no open decision.

If five rounds pass without convergence, stop. Show the user the open defects. A plan that does not converge is usually too large: propose a split into smaller plans.

Show the user the converged plan. Implement it after the user approves. Set **Status** to `approved` and record **Base**. This is a session boundary.

## 4. Implement

Set **Status** to `implementing`. Do the steps in order. Commit as the repo's rules say. Check off each step in the plan file and update **Next**. Each step commit is a session boundary.

Use any skill that fits a step, such as a design, test-driven development or debugging skill.

If the work shows that the plan is wrong, stop the step. Fix the plan and run step 3 again on the changed part. A change to the scope or the done criteria needs the user's approval.

## 5. Verify until it converges

Set **Status** to `verifying`.

1. Run the check of each done criterion. Record the evidence in the plan file. Fix each failure.
2. Review the diff from **Base** against the plan, with a reviewer with fresh context. Use the same tags and the same sorting as in step 3.
3. Fix each defect.
   - A full plan repeats this step until a clean pass with all criteria checked.
   - A light plan runs one review round. After the fixes, run the check of each done criterion again.

## 6. Close

Set **Status** to `done`. Report to the user:

- The plan is complete. List each done criterion with its evidence.
- The commits from **Base**.
- The backlog. Each item is new work for a new plan, not open work of this plan.

The close is a session boundary.

After you close the plan, answer a question about open problems from the plan files. A plan with status `done` has no open work. Report a new finding as a backlog item, and give its concrete failure.

## Session boundaries

At each session boundary, judge whether the current session should continue. Judge from the work, because the runtime does not show usage limits reliably.

- **New session**: the plan is done, or the next work needs none of the current context. Tell the user to start it with this skill and the task.
- **Compact**: the next step continues the current work, and the context holds much material that the rest of the plan does not need. Examples are long logs and large file reads. Tell the user to run `/compact`.
- Otherwise, continue without a hint.

Give the hint in one line. Update **Next** before you give it. Then end the turn, so that the user can act on it.

## Resume

1. Read the plan file. Start from **Status** and **Next**.
2. If **Status** is `planning`, continue at step 2 or step 3. The plan has no **Base** yet.
3. Otherwise, run `git log --oneline <Base>..HEAD` and `git status`. Compare them with the checked steps and **Next**. Fix the plan file where it differs from Git.
4. Continue from the step that **Status** names.

## Status report

List each plan in `.plans/` with its status, its next action, its unchecked done criteria and its backlog size. If no plan is open, report that no planned work is open.

## Codex

The `codex` option needs Claude Code with codex-plugin-cc. In another runtime, tell the user and continue without Codex.

Ask the user in one question which model and which effort Codex uses. Offer the `model` and `model_reasoning_effort` of `~/.codex/config.toml` as the default. The efforts are `none`, `minimal`, `low`, `medium`, `high` and `xhigh`.

Run Codex through the `codex:codex-rescue` subagent. Pass `--model <model> --effort <effort>` in each request.

- **Review**: ask for a read-only run. Give the plan file path, the diff range for a code review, and the reviewer instruction from step 3.
- **Delegated work**: ask for a write run for one plan step. Give the step, the plan file path and the files that the step changes. Check the result against the step before you check the step off.
