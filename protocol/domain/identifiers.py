"""Protocol Identifier Domain Model."""

from dataclasses import dataclass
import hashlib


@dataclass(frozen=True, slots=True)
class ProtocolIdentifier:
    """
    A globally unique, deterministic identifier for protocol objects.
    Constructed via SHA-256 hashing of composite deterministic keys.
    Never uses randomness or UUIDs.
    """
    
    hash_value: str
    
    @classmethod
    def generate(cls, *components: str) -> "ProtocolIdentifier":
        """
        Generate a deterministic identifier from multiple string components.
        
        Args:
            *components: The string components to hash together.
            
        Returns:
            A new ProtocolIdentifier containing the SHA-256 hash.
        """
        sha256 = hashlib.sha256()
        for comp in components:
            sha256.update(comp.encode('utf-8'))
            # Add a separator to prevent hash collisions like ("ab", "c") vs ("a", "bc")
            sha256.update(b"\x00")
            
        return cls(hash_value=sha256.hexdigest())
    
    def __str__(self) -> str:
        return self.hash_value
