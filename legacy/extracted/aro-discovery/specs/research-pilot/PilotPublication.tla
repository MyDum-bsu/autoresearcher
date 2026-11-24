-------------------------- MODULE PilotPublication --------------------------
EXTENDS Naturals, Sequences

CONSTANTS Workers, Judge, MaxAttempts, AllowStaleSubmission, AllowGateBypass
ASSUME /\ Workers # {}
       /\ Judge \notin Workers
       /\ "none" \notin Workers \cup {Judge}
       /\ MaxAttempts \in Nat \ {0}
       /\ AllowStaleSubmission \in BOOLEAN
       /\ AllowGateBypass \in BOOLEAN

\* One immutable question version. An attempt number abstracts a lease fence
\* and a non-refundable unit of the attempt budget.
VARIABLES phase, attempt, worker, submission, verifiedBy, gateOpen,
          log, projection

vars == <<phase, attempt, worker, submission, verifiedBy, gateOpen,
          log, projection>>

Empty == [by |-> "none", fence |-> 0, admissible |-> FALSE]
Terminal == {"committed", "canceled", "deferred"}

Init ==
    /\ phase = "ready"
    /\ attempt = 0
    /\ worker = "none"
    /\ submission = Empty
    /\ verifiedBy = "none"
    /\ gateOpen = FALSE
    /\ log = <<>>
    /\ projection = 0

Claim(w) ==
    /\ phase = "ready"
    /\ attempt < MaxAttempts
    /\ phase' = "leased"
    /\ attempt' = attempt + 1
    /\ worker' = w
    /\ UNCHANGED <<submission, verifiedBy, gateOpen, log, projection>>

Expire ==
    /\ phase = "leased"
    /\ phase' = "ready"
    /\ worker' = "none"
    /\ UNCHANGED <<attempt, submission, verifiedBy, gateOpen, log, projection>>

Submit(w, fence, admissible) ==
    /\ phase = "leased"
    /\ w = worker
    /\ AllowStaleSubmission \/ fence = attempt
    /\ phase' = "submitted"
    /\ submission' = [by |-> w, fence |-> fence, admissible |-> admissible]
    /\ UNCHANGED <<attempt, worker, verifiedBy, gateOpen, log, projection>>

Verify(actor) ==
    /\ phase = "submitted"
    /\ actor = Judge
    /\ phase' = IF submission.admissible THEN "validated" ELSE "rejected"
    /\ verifiedBy' = IF submission.admissible THEN actor ELSE "none"
    /\ UNCHANGED <<attempt, worker, submission, gateOpen, log, projection>>

Requeue ==
    /\ phase = "rejected"
    /\ phase' = "ready"
    /\ worker' = "none"
    /\ submission' = Empty
    /\ UNCHANGED <<attempt, verifiedBy, gateOpen, log, projection>>

SetGate ==
    /\ phase \notin Terminal
    /\ gateOpen' = ~gateOpen
    /\ UNCHANGED <<phase, attempt, worker, submission, verifiedBy, log, projection>>

Cancel ==
    /\ phase \notin Terminal
    /\ phase' = "canceled"
    /\ UNCHANGED <<attempt, worker, submission, verifiedBy, gateOpen, log, projection>>

Exhaust ==
    /\ phase = "ready"
    /\ attempt = MaxAttempts
    /\ phase' = "deferred"
    /\ UNCHANGED <<attempt, worker, submission, verifiedBy, gateOpen, log, projection>>

\* The durable append is the commit point. A duplicate request can only
\* read the existing result. A later cancellation cannot erase this event.
Commit ==
    /\ phase = "validated"
    /\ gateOpen \/ AllowGateBypass
    /\ log = <<>>
    /\ log' = <<[fence |-> submission.fence, by |-> submission.by,
                  judge |-> verifiedBy, admissible |-> submission.admissible,
                  gate |-> gateOpen]>>
    /\ phase' = "committed"
    /\ UNCHANGED <<attempt, worker, submission, verifiedBy, gateOpen, projection>>

\* A crash can discard a projection, but never the durable commit.
LoseProjection ==
    /\ projection > 0
    /\ projection' = 0
    /\ UNCHANGED <<phase, attempt, worker, submission, verifiedBy, gateOpen, log>>

Replay ==
    /\ projection < Len(log)
    /\ projection' = Len(log)
    /\ UNCHANGED <<phase, attempt, worker, submission, verifiedBy, gateOpen, log>>

Next ==
    \/ \E w \in Workers : Claim(w)
    \/ Expire
    \/ \E w \in Workers, fence \in 1..attempt, admissible \in BOOLEAN :
         Submit(w, fence, admissible)
    \/ \E actor \in Workers \cup {Judge} : Verify(actor)
    \/ Requeue
    \/ SetGate
    \/ Cancel
    \/ Exhaust
    \/ Commit
    \/ LoseProjection
    \/ Replay

Spec == Init /\ [][Next]_vars /\ WF_vars(Replay)

AttemptBudget == attempt \in 0..MaxAttempts

SingleCurrentWriter ==
    phase \in {"submitted", "validated", "rejected", "committed"} =>
        /\ worker \in Workers
        /\ submission.by = worker
        /\ submission.fence = attempt

OneAuthoritativeCommit ==
    /\ Len(log) <= 1
    /\ (phase = "committed") <=> (Len(log) = 1)

AuthorizedCommit ==
    \A n \in 1..Len(log) :
        /\ log[n].judge = Judge
        /\ log[n].admissible
        /\ log[n].gate
        /\ log[n].fence = attempt
        /\ log[n].by = worker

ProjectionNeverLeads == projection \in 0..Len(log)

EventuallyVisible == (Len(log) = 1) ~> (projection = 1)
=============================================================================
