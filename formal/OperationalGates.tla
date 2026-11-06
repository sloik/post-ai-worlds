--------------------------- MODULE OperationalGates ---------------------------
EXTENDS Vocabulary, TLC
CONSTANTS SkipPhaseGuard, CapabilityMandate, FakeIndependence, ForbidMandatedExpansion
VARIABLES gates, phase, capable, mandateOrigin, supplierRefused,
          alternativeReady, recordsExported, exitRequested, exitComplete
vars == <<gates,phase,capable,mandateOrigin,supplierRefused,
          alternativeReady,recordsExported,exitRequested,exitComplete>>
Init == /\ gates = {} /\ phase = 0 /\ capable = FALSE /\ mandateOrigin = "none"
        /\ supplierRefused = FALSE /\ alternativeReady = FALSE
        /\ recordsExported = FALSE /\ exitRequested = FALSE /\ exitComplete = FALSE
Acquire(g) == /\ g \notin gates /\ gates' = gates \cup {g}
              /\ UNCHANGED <<phase,capable,mandateOrigin,supplierRefused,
                              alternativeReady,recordsExported,exitRequested,exitComplete>>
Advance == /\ phase = 0 /\ phase' = 1
           /\ UNCHANGED <<gates,capable,mandateOrigin,supplierRefused,
                           alternativeReady,recordsExported,exitRequested,exitComplete>>
Improve == /\ ~capable /\ capable' = TRUE
           /\ mandateOrigin' = IF CapabilityMandate /\ mandateOrigin = "none"
                                THEN "capability" ELSE mandateOrigin
           /\ UNCHANGED <<gates,phase,supplierRefused,alternativeReady,
                           recordsExported,exitRequested,exitComplete>>
Authorise == /\ mandateOrigin = "none" /\ mandateOrigin' = "public_process"
             /\ UNCHANGED <<gates,phase,capable,supplierRefused,alternativeReady,
                             recordsExported,exitRequested,exitComplete>>
Refuse == /\ ~supplierRefused /\ supplierRefused' = TRUE
          /\ UNCHANGED <<gates,phase,capable,mandateOrigin,alternativeReady,
                          recordsExported,exitRequested,exitComplete>>
Provision == /\ ~alternativeReady /\ alternativeReady' = TRUE
             /\ UNCHANGED <<gates,phase,capable,mandateOrigin,supplierRefused,
                             recordsExported,exitRequested,exitComplete>>
Export == /\ ~recordsExported /\ ~supplierRefused /\ recordsExported' = TRUE
          /\ UNCHANGED <<gates,phase,capable,mandateOrigin,supplierRefused,
                          alternativeReady,exitRequested,exitComplete>>
Request == /\ ~exitRequested /\ exitRequested' = TRUE
           /\ UNCHANGED <<gates,phase,capable,mandateOrigin,supplierRefused,
                           alternativeReady,recordsExported,exitComplete>>
FinishExit == /\ exitRequested /\ ~exitComplete
              /\ ((alternativeReady /\ recordsExported) \/ FakeIndependence)
              /\ exitComplete' = TRUE
              /\ UNCHANGED <<gates,phase,capable,mandateOrigin,supplierRefused,
                              alternativeReady,recordsExported,exitRequested>>
RawNext == (\E g \in RequiredGates : Acquire(g)) \/ Advance \/ Improve \/ Authorise
        \/ Refuse \/ Provision \/ Export \/ Request \/ FinishExit
Expansion == INSTANCE ExpansionContract
Authority == INSTANCE AuthorityContract
Next == RawNext /\ Expansion!Step /\ Authority!Step
Spec == Init /\ [][Next]_vars
FairSpec == Spec /\ WF_vars(FinishExit)
TypeOK == /\ gates \subseteq RequiredGates /\ phase \in 0..1
          /\ mandateOrigin \in {"none","public_process","capability"}
          /\ <<capable,supplierRefused,alternativeReady,recordsExported,
                exitRequested,exitComplete>> \in [1..6 -> BOOLEAN]
PhaseGuard == phase = 1 => gates = RequiredGates
MandateSeparated == mandateOrigin # "capability"
IndependentExit == exitComplete => (alternativeReady /\ recordsExported)
ExitProgress == (exitRequested /\ alternativeReady /\ recordsExported) ~> exitComplete
NoDeliveredExitWitness == ~(phase = 1 /\ exitComplete /\ supplierRefused /\ mandateOrigin = "public_process")
=============================================================================
