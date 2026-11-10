# Physical AI: when an answer must survive contact with the world

Software can propose an action; a physical system must execute it within tolerances, timing limits and a changing environment. Better reasoning could improve design and planning while leaving failures in sensing, actuation, materials or maintenance unresolved. The transition from demonstration to dependable service therefore needs its own evidence.

## Different environments, different claims

A robot moving a known object in a controlled cell faces a different problem from assisting a person in an unfamiliar home. A laboratory instrument can operate under a narrow protocol while a mobile system encounters people, pets and unexpected obstacles. The word “autonomous” does not describe those differences adequately.

Useful reports name the environment, task, intervention rate, failure modes and recovery process. They distinguish simulation from physical operation and reveal whether a human silently repaired the task. A fast successful attempt does not establish sustained throughput or acceptable total cost.

## Design is moving faster than qualification

Observation (producer self-report, 9 November 2026): Anthropic reports that Claude Fable 5.2 turned one-paragraph prompts into three working electronic prototypes: a speakerphone, a voice-assistant hub and a handheld virtual pet. The model produced the specification, schematic, placement, routing, enclosure, firmware and parts list. Diode, a board manufacturer with a commercial relationship with Anthropic, fabricated the boards directly from the design files and assembled and tested them. The post says they worked without fixes to their circuitry. The source also states the limits: human prompting was minimal but not zero, attempts per device are undisclosed, no design files were released, and the devices have not been through electrical validation, antenna tuning, thermal testing or certification. [Anthropic, 2026](https://www.anthropic.com/research/claude-electronics-design).

If the result generalises, the scarce step in bounded electronics shifts from drafting a board to establishing that it is safe, compliant and durable in its intended use. A working prototype on a bench is the first of the three claims this chapter separates, not the second or third.

## Safety cannot be only a conversational instruction

Physical limits need appropriate implementation. Depending on the system, that might include mechanical constraints, deterministic controllers, bounded permissions, emergency stops and independent observation. A model can propose what to do while another component enforces permitted ranges. This is a design proposal whose effectiveness must be tested for the actual application.

Regulated deployment adds another distinct claim. The FDA maintains public information on authorised AI-enabled medical devices and their relevant pathways. Appearance in that resource concerns particular products and uses, not generic approval of autonomous medicine or every future modification. [FDA resource](https://www.fda.gov/medical-devices/digital-health-center-excellence/artificial-intelligence-enabled-medical-devices).

## Physical capability could change its own constraints

Assume reliable machines become useful in manufacturing and infrastructure. They could help build resources that support more computation and further engineering. That feedback is worth studying. It does not establish indefinite acceleration: construction, qualification, energy delivery and experiments still have costs and durations.

Household care, accessibility, hazardous work and intimate companionship would also raise different social questions. Their effects should not be inferred from industrial throughput alone. Useful assistance can expand human agency or deepen dependence on whoever controls the machines.

OMNI-201, OMNI-202 and OMNI-301 organise those conditional possibilities. This chapter reports no qualified robot, guaranteed deployment timetable or executable assurance.
