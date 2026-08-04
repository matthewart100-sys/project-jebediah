import json
import urllib.request


MEMORY_URL = "http://jebediah-memory:8000/memory/store"


VBA_EVIDENCE = [
    {
        "id": "VBA-PUB-001",
        "title": "Official VBA Website",
        "content": "Virginia B. Andes Volunteer Community Clinic official public website information.",
    },
    {
        "id": "VBA-PUB-002",
        "title": "Organizational Identity Information",
        "content": "Virginia B. Andes Volunteer Community Clinic is a nonprofit healthcare organization providing free healthcare services to qualifying community members.",
    },
    {
        "id": "VBA-PUB-003",
        "title": "Community Impact Information",
        "content": "Public information describing VBA community healthcare impact and service mission.",
    },
    {
        "id": "VBA-PUB-004",
        "title": "Financial Transparency Information",
        "content": "Publicly available financial transparency information related to Virginia B. Andes Volunteer Community Clinic.",
    },
    {
        "id": "VBA-PUB-005",
        "title": "Public Policies Information",
        "content": "Public organizational policies and publicly available operational guidelines.",
    },
    {
        "id": "VBA-PUB-006",
        "title": "Patient Services and Public Forms Information",
        "content": "Public patient eligibility information and service access documentation.",
    },
    {
        "id": "VBA-PUB-007",
        "title": "Public Communications Information",
        "content": "Public organizational communications and announcements.",
    },
]


def post_memory(payload):
    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        MEMORY_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


for evidence in VBA_EVIDENCE:
    payload = {
        "source_identity": evidence["id"],
        "content": evidence["content"],
        "memory_type": "fact",
        "importance": 0.9,
        "source": "public_organizational_evidence",
        "creator": "Project Jebediah VBA Pilot",
        "creation_context": evidence["title"],
        "supporting_evidence": [
            evidence["id"],
        ],
    }

    print(evidence["id"])
    print(post_memory(payload))
    print("-" * 60)
