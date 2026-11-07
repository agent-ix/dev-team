#!/bin/sh
# Tests for scripts/team-gate. Run: sh skills/code-lead/tests/team-gate-test.sh
set -u
here=$(cd "$(dirname "$0")" && pwd -P)
gate=$here/../scripts/team-gate
root=$(mktemp -d "${TMPDIR:-/tmp}/team-gate-test.XXXXXX") || exit 2
trap 'rm -rf "$root"' EXIT
fail=0
ok() { echo "ok   $1"; }
bad() { echo "FAIL $1"; fail=1; }
expect() { # name expected actual
  if [ "$2" = "$3" ]; then ok "$1"; else bad "$1 (expected $2, got $3)"; fi
}
export TEAM=t TEAM_RETRO_HOME=$root/state
unset TEAM_GATE_LOG TEAM_GATE_LOCK
log=$root/state/t/gate.jsonl

"$gate" gate --pr 7 -- sh -c 'exit 37'; expect "exit status passes through" 37 $?
expect "one gate line" 1 "$(wc -l < "$log" | tr -d ' ')"
grep -q '"pr":7,"kind":"gate"' "$log"; expect "gate line has pr and kind" 0 $?
grep -Eq '[0-9a-f]{40}' "$log"; expect "no commit hash in log" 1 $?

out=$("$gate" gate --pr 8 -- printf '%s|' 'a b' "c'd" '' 2>&1); expect "arguments with spaces and quotes survive" "a b|c'd||" "$out"

"$gate" repin --pr 8; expect "repin exits 0" 0 $?
tail -1 "$log" | grep -q '"kind":"repin"'; expect "repin line written" 0 $?

"$gate" gate --pr x -- true 2>/dev/null; expect "non-numeric pr rejected" 2 $?

# lock wait is recorded
TEAM_GATE_LOCK="/usr/bin/lockf $root/l.lock" "$gate" gate --pr 1 -- sleep 3 &
sleep 1
TEAM_GATE_LOCK="/usr/bin/lockf $root/l.lock" "$gate" gate --pr 2 -- true
wait
line=$(grep '"pr":2,"kind":"gate"' "$log" | tail -1)
req=$(echo "$line" | sed 's/.*"requested_lock_at":"\([^"]*\)".*/\1/')
acq=$(echo "$line" | sed 's/.*"acquired_lock_at":"\([^"]*\)".*/\1/')
[ "$req" != "$acq" ]
expect "lock wait recorded" 0 $?

# git work tree refusal: directory, nested new directory, symlinked directory, symlinked file
mkdir -p "$root/repo" && git init -q "$root/repo"
TEAM_GATE_LOG=$root/repo/g.jsonl "$gate" repin --pr 1 2>/dev/null; expect "log inside work tree refused" 2 $?
TEAM_GATE_LOG=$root/repo/newdir/g.jsonl "$gate" repin --pr 1 2>/dev/null; expect "nested path in work tree refused" 2 $?
[ ! -e "$root/repo/newdir" ]; expect "no directory created in work tree" 0 $?
ln -s "$root/repo" "$root/linkdir"
TEAM_GATE_LOG=$root/linkdir/g.jsonl "$gate" repin --pr 1 2>/dev/null; expect "symlinked directory refused" 2 $?
mkdir -p "$root/outside" && ln -s "$root/repo/f.jsonl" "$root/outside/g.jsonl"
TEAM_GATE_LOG=$root/outside/g.jsonl "$gate" repin --pr 1 2>/dev/null; expect "symlinked log file refused" 2 $?
[ ! -e "$root/repo/f.jsonl" ]; expect "nothing written through the symlink" 0 $?

# bad TMPDIR does not stop the gate
TMPDIR=$root/missing "$gate" gate --pr 9 -- true; expect "missing TMPDIR falls back" 0 $?

# lock command that fails before the gate starts logs nothing
before=$(wc -l < "$log" | tr -d ' ')
TEAM_GATE_LOCK="false" "$gate" gate --pr 10 -- true 2>/dev/null; expect "failed lock command exit status" 1 $?
expect "failed lock command logs nothing" "$before" "$(wc -l < "$log" | tr -d ' ')"

# TERM reaches the gate command
"$gate" gate --pr 11 -- sleep 30 &
p=$!
sleep 1
kill -TERM "$p"
wait "$p"; rc=$?
[ "$rc" -ne 0 ]; expect "TERM stops the gate and returns non-zero" 0 $?

# concurrent appends stay whole lines
for i in 1 2 3 4 5 6 7 8 9 10; do "$gate" repin --pr $i & done; wait
bad_lines=$(grep -vc '^{.*}$' "$log")
expect "concurrent appends are whole lines" 0 "$bad_lines"

exit $fail
