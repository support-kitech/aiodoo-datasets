"""Integration tests for pipeline in Conversation Generator."""

from pathlib import Path
from tempfile import TemporaryDirectory
from aiodoo_datasets.generators.conversation.pipeline_context import PipelineContext
from aiodoo_datasets.generators.conversation.builders.metadata_builder import MetadataBuilder
from aiodoo_datasets.generators.conversation.enums import ConversationType
from aiodoo_datasets.generators.conversation.pipeline import ConversationPipeline

def test_pipeline_generate():
    """Test complete pipeline execution."""
    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        output_path = tmp_path / "conversation_dataset.jsonl"
        manifest_path = tmp_path / "dataset_manifest.json"
        
        metadata = MetadataBuilder.build(
            conversation_type=ConversationType.PLANNING,
            source_module="test_module"
        )
        
        # Fake planner protocol
        input_protocols = {
            "planner_protocol": {
                "tasks": [{"task_id": "T1", "description": "A task"}]
            }
        }
        
        context = PipelineContext(
            input_protocols=input_protocols,
            metadata=metadata,
            output_dir=str(tmp_path),
            source_identifier="test_review_1"
        )
        
        result = ConversationPipeline.generate(context)
        
        assert result.success is True
        assert len(result.diagnostics) == 0
        
        # Verify file output
        assert output_path.exists()
        assert manifest_path.exists()
        
        # Should have created 1 conversation
        assert result.statistics.conversations_generated == 1
        assert result.statistics.turns_generated == 1
        assert result.statistics.messages_generated == 2 # 1 user, 1 assistant
