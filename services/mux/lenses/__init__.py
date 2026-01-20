# mux.lenses module - Perceptual lenses for 8D spatial perception

from .base import Lens, Target
from .causal import CausalLens
from .collaborative import CollaborativeLens
from .contextual import ContextualLens
from .flow import FlowLens
from .hierarchy import HierarchyLens
from .lens_set import LensSet
from .priority import PriorityLens
from .quantitative import QuantitativeLens
from .temporal import TemporalLens

__all__ = [
    # Base
    "Lens",
    "Target",
    "LensSet",
    # Individual lenses (8 total, mapping to 8D spatial dimensions)
    "TemporalLens",
    "HierarchyLens",
    "PriorityLens",
    "CollaborativeLens",
    "FlowLens",
    "QuantitativeLens",
    "CausalLens",
    "ContextualLens",
]
