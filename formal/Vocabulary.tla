------------------------------ MODULE Vocabulary ------------------------------
EXTENDS Naturals, FiniteSets
EpistemicKinds == {"evidence", "empirical_assumption", "conditional_mechanism",
                   "normative_decision", "operational_design", "formalizable_invariant"}
AssuranceStates == {"unchecked", "bounded_checked", "evidence_only", "open", "normative", "empirical_only", "proposed"}
RequiredGates == {"demand", "permission", "capital", "quality"}
=============================================================================
