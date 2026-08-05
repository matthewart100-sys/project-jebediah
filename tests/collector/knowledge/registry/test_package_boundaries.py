import ast
from pathlib import Path
import sys

import collector.knowledge
import collector.knowledge.registry as registry
import collector.memory


REPOSITORY_ROOT = Path(__file__).parents[4]
SOURCE_ROOT = REPOSITORY_ROOT / "src" / "collector"
KNOWLEDGE_ROOT = SOURCE_ROOT / "knowledge"


def parse_imports(path: Path):
    return ast.walk(
        ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    )


def test_registry_uses_only_standard_library_and_local_imports():
    for path in KNOWLEDGE_ROOT.rglob("*.py"):
        for node in parse_imports(path):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root_module = alias.name.partition(".")[0]
                    assert root_module in sys.stdlib_module_names
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    assert node.level == 1
                else:
                    root_module = (node.module or "").partition(".")[0]
                    assert root_module in sys.stdlib_module_names


def test_existing_source_does_not_import_registry():
    for path in SOURCE_ROOT.rglob("*.py"):
        if path.is_relative_to(KNOWLEDGE_ROOT):
            continue

        for node in parse_imports(path):
            if isinstance(node, ast.Import):
                assert all(
                    not alias.name.startswith(
                        "collector.knowledge"
                    )
                    for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert not module.startswith("collector.knowledge")
                assert not (
                    node.level
                    and module.partition(".")[0] == "knowledge"
                )


def test_knowledge_root_does_not_reexport_registry_api():
    assert not hasattr(
        collector.knowledge,
        "KnowledgeRegistryRecord",
    )


def test_memory_package_does_not_reexport_registry_api():
    assert not hasattr(
        collector.memory,
        "KnowledgeRegistryRecord",
    )


def test_registry_public_api_excludes_reference_adapter():
    assert set(registry.__all__) == {
        "EvidenceReference",
        "FreshnessState",
        "GovernanceScope",
        "HumanReview",
        "HumanReviewState",
        "KnowledgeLifecycle",
        "KnowledgeLifecycleState",
        "KnowledgeProvenance",
        "KnowledgeRegistryConflict",
        "KnowledgeRegistryRecord",
        "KnowledgeRegistryRepository",
        "SourceReference",
        "TemporalContext",
        "TransformationReference",
        "UncertaintyAssessment",
        "UncertaintyState",
    }
    assert not hasattr(
        registry,
        "InMemoryKnowledgeRegistryRepository",
    )
