--------------------------- MODULE RegistrySnapshot ---------------------------
EXTENDS FiniteSets
\* Actual registry sha256: d376c2aa0a7a7a91abbe424fe99799aab7483a55b42d156e59e65638a3d3e18b
UniverseIds == {"OMNI-000", "OMNI-001", "OMNI-101", "OMNI-102", "OMNI-103", "OMNI-104", "OMNI-201", "OMNI-202", "OMNI-301", "OMNI-401"}
ClaimIds == {"CLM-001", "CLM-002", "CLM-003", "CLM-004", "CLM-005", "CLM-006", "CLM-007", "CLM-008", "CLM-009", "CLM-010", "CLM-011", "CLM-012", "CLM-013", "CLM-014", "CLM-015", "CLM-016", "CLM-017", "CLM-018", "CLM-019", "CLM-020", "CLM-021", "CLM-022", "CLM-023", "CLM-024"}
DeclaredPremises == [id \in UniverseIds |-> CASE id = "OMNI-000" -> {"ASM-001", "ASM-002"}
    [] id = "OMNI-001" -> {"ASM-001", "ASM-002", "ASM-003", "ASM-004", "ASM-016", "ASM-017"}
    [] id = "OMNI-101" -> {"ASM-001", "ASM-002", "ASM-006", "ASM-007", "ASM-008"}
    [] id = "OMNI-102" -> {"ASM-001", "ASM-002", "ASM-009", "ASM-010", "ASM-011"}
    [] id = "OMNI-103" -> {"ASM-001", "ASM-002", "ASM-012"}
    [] id = "OMNI-104" -> {"ASM-001", "ASM-002", "ASM-009", "ASM-013"}
    [] id = "OMNI-201" -> {"ASM-001", "ASM-002", "ASM-003", "ASM-005", "ASM-006", "ASM-007", "ASM-008"}
    [] id = "OMNI-202" -> {"ASM-001", "ASM-002", "ASM-003", "ASM-005", "ASM-009", "ASM-010"}
    [] id = "OMNI-301" -> {"ASM-001", "ASM-002", "ASM-003", "ASM-004", "ASM-014", "ASM-015", "ASM-016"}
    [] id = "OMNI-401" -> {"ASM-001", "ASM-002", "ASM-004", "ASM-016", "ASM-018"}]
RequiredPremises == [id \in ClaimIds |-> CASE id = "CLM-001" -> {"ASM-001"}
    [] id = "CLM-002" -> {"ASM-003"}
    [] id = "CLM-003" -> {"ASM-004"}
    [] id = "CLM-004" -> {"ASM-002"}
    [] id = "CLM-005" -> {"ASM-021"}
    [] id = "CLM-006" -> {"ASM-006"}
    [] id = "CLM-007" -> {}
    [] id = "CLM-008" -> {"ASM-016"}
    [] id = "CLM-009" -> {}
    [] id = "CLM-010" -> {}
    [] id = "CLM-011" -> {}
    [] id = "CLM-012" -> {}
    [] id = "CLM-013" -> {"ASM-020"}
    [] id = "CLM-014" -> {}
    [] id = "CLM-015" -> {}
    [] id = "CLM-016" -> {}
    [] id = "CLM-017" -> {"ASM-023", "ASM-024"}
    [] id = "CLM-018" -> {"ASM-025", "ASM-027"}
    [] id = "CLM-019" -> {"ASM-026"}
    [] id = "CLM-020" -> {"ASM-026", "ASM-027"}
    [] id = "CLM-021" -> {"ASM-028"}
    [] id = "CLM-022" -> {"ASM-029"}
    [] id = "CLM-023" -> {"ASM-029"}
    [] id = "CLM-024" -> {"ASM-029"}]
ConflictPairs == {{"ASM-004", "ASM-005"}, {"ASM-014", "ASM-018"}}
AdmissionRules == {[requires |-> {"ASM-005"}, ensures |-> {"ASM-003"}, forbids |-> {"ASM-004"}],
 [requires |-> {"ASM-014"}, ensures |-> {"ASM-015", "ASM-016"}, forbids |-> {"ASM-018"}],
 [requires |-> {"ASM-017"}, ensures |-> {"ASM-002"}, forbids |-> {}]}
=============================================================================
