-------------------------- MODULE ExpansionContract --------------------------
EXTENDS Vocabulary
CONSTANT SkipPhaseGuard
VARIABLES gates, phase
Step == SkipPhaseGuard \/ (phase' = 1 => gates' = RequiredGates)
=============================================================================
