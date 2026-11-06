-------------------------- MODULE AuthorityContract --------------------------
CONSTANTS CapabilityMandate, ForbidMandatedExpansion
VARIABLES phase, mandateOrigin
Step == /\ (CapabilityMandate \/ mandateOrigin' # "capability")
        /\ (~ForbidMandatedExpansion \/ ~(phase' = 1 /\ mandateOrigin' = "public_process"))
=============================================================================
