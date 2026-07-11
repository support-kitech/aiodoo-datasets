"""Unit tests for factories in Conversation Generator."""

from generators.conversation.factories.message_factory import MessageFactory
from generators.conversation.enums import Role, ConversationType
from generators.conversation.factories.turn_factory import TurnFactory
from generators.conversation.factories.conversation_factory import (
    ConversationFactory,
)


def test_message_factory_determinism() -> None:
    """Test that message IDs are perfectly deterministic based on inputs."""
    # Test identical inputs yield identical IDs
    msg1 = MessageFactory.create(Role.USER, "Hello world", "TRN-1", 0)
    msg2 = MessageFactory.create(Role.USER, "Hello world", "TRN-1", 0)

    # Test role diff yields diff IDs
    msg3 = MessageFactory.create(Role.ASSISTANT, "Hello world", "TRN-1", 0)

    # Test sequence diff yields diff IDs
    msg4 = MessageFactory.create(Role.USER, "Hello world", "TRN-1", 1)

    # Test turn_id diff yields diff IDs
    msg5 = MessageFactory.create(Role.USER, "Hello world", "TRN-2", 0)

    assert msg1.message_id == msg2.message_id
    assert msg1.message_id != msg3.message_id
    assert msg1.message_id != msg4.message_id
    assert msg1.message_id != msg5.message_id

    # Must use MSG- prefix
    assert msg1.message_id.startswith("MSG-")


def test_turn_factory_determinism() -> None:
    """Test that turn IDs are perfectly deterministic."""
    turn_id1 = TurnFactory.generate_id("CONV-1", 0)
    turn_id2 = TurnFactory.generate_id("CONV-1", 0)
    turn_id3 = TurnFactory.generate_id("CONV-1", 1)

    assert turn_id1 == turn_id2
    assert turn_id1 != turn_id3
    assert turn_id1.startswith("TRN-")


def test_conversation_factory_determinism() -> None:
    """Test that conversation IDs are perfectly deterministic."""
    conv_id1 = ConversationFactory.generate_id(ConversationType.PLANNING.value, "source_1")
    conv_id2 = ConversationFactory.generate_id(ConversationType.PLANNING.value, "source_1")
    conv_id3 = ConversationFactory.generate_id(ConversationType.PLANNING.value, "source_2")

    assert conv_id1 == conv_id2
    assert conv_id1 != conv_id3
    assert conv_id1.startswith("CONV-")
