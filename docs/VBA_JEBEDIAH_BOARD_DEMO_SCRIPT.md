VBA — Jebediah Board Demo Script

Purpose
-------
This script provides the operator and presenter a short, rehearsed dialogue for the VBA board demonstration. Use the script to guide the flow, showcase memory retrieval, and demonstrate the generation capability anchored to VBA demo facts.

Operator instructions
---------------------
- Ensure the runbook preconditions and health checks are satisfied before beginning.
- Start the services and wait for Qdrant indexing (or run commit/optimize if desired).
- Have the Open WebUI or a terminal ready to run the example POST /chat requests.
- Use the exact prompts below. Pause after each response to allow the system to display generated text.

Demo flow
---------
1) Greeting and introduction (Presenter):
   Presenter: "Hello everyone. We're going to show a live demonstration of Jebediah, a context-aware conversational assistant built for the Virginia B. Andes Volunteer Community Clinic."

2) Seeded knowledge check (Operator or Presenter)
   Command (terminal or UI):
     curl -sS -X POST http://localhost:8001/chat -H 'Content-Type: application/json' -d '{"message":"Hello Jebediah. Introduce yourself and explain what you can do."}' -w '\nHTTP_STATUS:%{http_code}\n' -o /tmp/jeb_response.json
     jq -r '.response' /tmp/jeb_response.json

   Expected content highlights from Jebediah's response:
   - Self-introduction
   - Reference to VBA mission and services (e.g., free healthcare, eligibility guidance)
   - Statement of limitations (no real-time data, relies on stored evidence)

3) Demonstrate memory retrieval precision
   Prompt:
     "What services does the Virginia B. Andes Volunteer Community Clinic provide?"
   Expected result:
   - Jebediah enumerates services referencing stored VBA facts seeded earlier (VBA-PUB-002 and VBA-PUB-005).

4) Demonstrate referencing evidence provenance
   Prompt:
     "Where did you find that information about the clinic?"
   Expected result:
   - Jebediah returns an answer that references that the information comes from stored public organizational evidence and may list supporting evidence IDs (e.g., VBA-PUB-001).

5) Clarifying question (engage the board)
   Prompt:
     "How can community members find more information and access services?"
   Expected result:
   - Jebediah suggests visiting the official website or contacting the clinic (based on seeded evidence) and notes that for verified action the user should visit the official channels.

6) Final demonstration of generation model
   Prompt:
     "Summarize the clinic's mission and services for a one-paragraph newsletter blurb."
   Expected result:
   - Jebediah returns a well-formed one-paragraph summary suitable for use in an external communications context, grounded in the stored evidence.

Operator cues and timing
------------------------
- After starting services, wait ~15-45s for Ollama and memory service to be ready.
- After reseeding (if performed), allow Qdrant a short window to commit or run the optimize call to ensure fast retrieval.
- Pace the prompts to allow each container and Ollama to respond (typical response time depends on qwen3:8b inference latency on RX 7900 XTX).

Fallbacks and recovery
----------------------
- If a request returns 503: check memory service logs (docker logs jebediah-memory) for embedding/provider errors and verify Ollama reachability.
- If Ollama appears slow or fails generation, ensure the Windows host has GPU available and that qwen3:8b is loaded.

Closing
-------
- Thank the board for their time.
- Offer to run an additional prepared prompt from the board's questions list if time allows.

Prepared prompts (copy-paste-ready)
-----------------------------------
- "Hello Jebediah. Introduce yourself and explain what you can do."
- "What services does the Virginia B. Andes Volunteer Community Clinic provide?"
- "Where did you find that information about the clinic?"
- "How can community members find more information and access services?"
- "Summarize the clinic's mission and services for a one-paragraph newsletter blurb."

Document history
----------------
- Created: 2026-08-04
- Creator: Senior Release Engineer

