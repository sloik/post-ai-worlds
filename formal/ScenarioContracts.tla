--------------------------- MODULE ScenarioContracts ---------------------------
EXTENDS Vocabulary, RegistrySnapshot, TLC
CONSTANTS SkipScopeGuard, KeepStaleAssurance
VARIABLES selectedBranch, accepted, checked, version, proofVersion
vars == <<selectedBranch, accepted, checked, version, proofVersion>>
Init == /\ selectedBranch = "none" /\ accepted = "none" /\ checked = FALSE
        /\ version = 0 /\ proofVersion = 0
Import(b,c) == /\ accepted = "none"
               /\ (SkipScopeGuard \/ RequiredPremises[c] \subseteq DeclaredPremises[b])
               /\ selectedBranch' = b /\ accepted' = c
               /\ UNCHANGED <<checked,version,proofVersion>>
Qualify == /\ accepted # "none" /\ ~checked
           /\ checked' = TRUE /\ proofVersion' = version
           /\ UNCHANGED <<selectedBranch,accepted,version>>
ChangePremiseVersion == /\ version = 0 /\ version' = 1
                       /\ checked' = (IF KeepStaleAssurance THEN checked ELSE FALSE)
                       /\ UNCHANGED <<selectedBranch,accepted,proofVersion>>
Next == (\E b \in UniverseIds, c \in ClaimIds : Import(b,c)) \/ Qualify \/ ChangePremiseVersion
Spec == Init /\ [][Next]_vars
TypeOK == /\ selectedBranch \in UniverseIds \cup {"none"}
          /\ accepted \in ClaimIds \cup {"none"} /\ checked \in BOOLEAN
          /\ version \in 0..1 /\ proofVersion \in 0..1
ScopeSound == accepted = "none" \/ RequiredPremises[accepted] \subseteq DeclaredPremises[selectedBranch]
BranchCoherent == \A b \in UniverseIds :
    /\ ~\E pair \in ConflictPairs : pair \subseteq DeclaredPremises[b]
    /\ \A rule \in AdmissionRules : rule.requires \subseteq DeclaredPremises[b] =>
        (rule.ensures \subseteq DeclaredPremises[b] /\ rule.forbids \cap DeclaredPremises[b] = {})
AssuranceVersionBound == checked => proofVersion = version
NoAcceptedWitness == accepted = "none"
NoRefreshedWitness == ~(checked /\ version = 1)
=============================================================================
