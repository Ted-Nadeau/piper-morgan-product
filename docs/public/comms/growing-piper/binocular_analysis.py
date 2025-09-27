#!/usr/bin/env python3
"""
Binocular Analysis: Multi-dimensional analysis of Piper Morgan blog posts
Provides complementary perspective to existing spiral analysis
"""

import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

import networkx as nx
import numpy as np


@dataclass
class BlogPost:
    """Represents a single blog post with metadata and content"""

    number: int
    date: str
    title: str
    content: str
    word_count: int
    concepts: List[str]
    emotions: Dict[str, float]
    energy_level: float


class BinocularAnalyzer:
    """Multi-dimensional blog analysis for binocular perspective"""

    def __init__(self, blog_dir: str = "piper-morgan-blogs/raw"):
        self.blog_dir = Path(blog_dir)
        self.posts = []
        self.concept_graph = nx.Graph()
        self.knowledge_graph = nx.DiGraph()

        # Concept patterns for semantic network
        self.concept_patterns = {
            "ai_agents": r"\b(Claude|Gemini|Cursor|agent|AI|LLM)\b",
            "architecture": r"\b(architecture|design|pattern|structure|system)\b",
            "debugging": r"\b(debug|bug|fix|error|issue|problem)\b",
            "learning": r"\b(learn|understand|realize|discover|insight)\b",
            "coordination": r"\b(coordinate|orchestrate|manage|align|sync)\b",
            "testing": r"\b(test|TDD|validate|verify|coverage)\b",
            "performance": r"\b(performance|speed|optimize|efficiency|latency)\b",
            "methodology": r"\b(methodology|process|workflow|approach|strategy)\b",
            "context": r"\b(context|state|memory|history|continuity)\b",
            "abstraction": r"\b(abstract|meta|recursive|pattern|principle)\b",
            "documentation": r"\b(document|docs|ADR|README|write)\b",
            "integration": r"\b(integrate|connect|bridge|link|combine)\b",
            "human_ai": r"\b(human|collaboration|partnership|team|together)\b",
            "pm_concepts": r"\b(product|PM|manager|feature|user|requirement)\b",
            "transformation": r"\b(transform|evolve|change|grow|adapt)\b",
        }

        # Emotional markers for journey mapping
        self.emotion_markers = {
            "frustration": [
                r"frustrat",
                r"stuck",
                r"confused",
                r"why.*not",
                r"annoying",
                r"painful",
            ],
            "breakthrough": [r"aha", r"finally", r"breakthrough", r"eureka", r"got it", r"clicked"],
            "excitement": [r"excit", r"amaz", r"wow", r"incredible", r"fantastic", r"brilliant"],
            "doubt": [r"doubt", r"uncertain", r"maybe", r"perhaps", r"question", r"wonder"],
            "confidence": [
                r"confident",
                r"certain",
                r"clear",
                r"obvious",
                r"definitely",
                r"absolutely",
            ],
            "exhaustion": [r"exhaust", r"tired", r"drain", r"marathon", r"endless", r"fatigue"],
            "satisfaction": [r"satisf", r"accomplish", r"complete", r"done", r"finish", r"achieve"],
            "curiosity": [
                r"curious",
                r"wonder",
                r"what if",
                r"explore",
                r"investigate",
                r"discover",
            ],
        }

        # Reader personas
        self.personas = {
            "technical_pm": {
                "interests": ["architecture", "debugging", "testing", "performance", "integration"],
                "pain_points": ["technical debt", "system design", "scaling"],
                "value_props": ["concrete solutions", "implementation details", "metrics"],
            },
            "strategic_pm": {
                "interests": ["methodology", "abstraction", "transformation", "pm_concepts"],
                "pain_points": ["alignment", "prioritization", "vision"],
                "value_props": ["frameworks", "principles", "long-term thinking"],
            },
            "ux_pm": {
                "interests": ["human_ai", "context", "documentation", "coordination"],
                "pain_points": ["user experience", "communication", "adoption"],
                "value_props": ["user stories", "interaction patterns", "feedback loops"],
            },
            "startup_pm": {
                "interests": ["learning", "methodology", "coordination", "performance"],
                "pain_points": ["speed", "resources", "iteration"],
                "value_props": ["rapid learning", "pragmatic solutions", "efficiency"],
            },
            "enterprise_pm": {
                "interests": ["architecture", "documentation", "testing", "integration"],
                "pain_points": ["scale", "governance", "risk"],
                "value_props": ["robust processes", "proven patterns", "risk mitigation"],
            },
        }

    def load_posts(self) -> None:
        """Load and parse all blog posts"""
        for file_path in sorted(self.blog_dir.glob("*.md")):
            content = file_path.read_text(encoding="utf-8")

            # Extract metadata from filename
            match = re.match(r"(\d+)-(\d{4}-\d{2}-\d{2})-(.*?)\.md", file_path.name)
            if match:
                number = int(match.group(1))
                date = match.group(2)
                title = match.group(3).replace("-", " ")

                # Extract concepts
                concepts = self._extract_concepts(content)

                # Analyze emotions
                emotions = self._analyze_emotions(content)

                # Calculate energy level
                energy = self._calculate_energy(emotions)

                post = BlogPost(
                    number=number,
                    date=date,
                    title=title,
                    content=content,
                    word_count=len(content.split()),
                    concepts=concepts,
                    emotions=emotions,
                    energy_level=energy,
                )
                self.posts.append(post)

        self.posts.sort(key=lambda x: x.date)

    def _extract_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content"""
        found_concepts = []
        content_lower = content.lower()

        for concept, pattern in self.concept_patterns.items():
            if re.search(pattern, content_lower):
                found_concepts.append(concept)

        return found_concepts

    def _analyze_emotions(self, content: str) -> Dict[str, float]:
        """Analyze emotional tone of content"""
        emotions = {}
        content_lower = content.lower()
        word_count = len(content.split())

        for emotion, patterns in self.emotion_markers.items():
            count = sum(len(re.findall(pattern, content_lower)) for pattern in patterns)
            emotions[emotion] = count / word_count * 100  # Normalize by word count

        return emotions

    def _calculate_energy(self, emotions: Dict[str, float]) -> float:
        """Calculate overall energy level from emotions"""
        positive = (
            emotions.get("breakthrough", 0)
            + emotions.get("excitement", 0)
            + emotions.get("satisfaction", 0)
            + emotions.get("confidence", 0)
        )
        negative = (
            emotions.get("frustration", 0)
            + emotions.get("doubt", 0)
            + emotions.get("exhaustion", 0)
        )
        neutral = emotions.get("curiosity", 0)

        return positive - negative + (neutral * 0.5)

    def build_semantic_network(self) -> Dict:
        """Build concept relationship graph"""
        # Create edges between concepts that appear together
        for post in self.posts:
            for i, concept1 in enumerate(post.concepts):
                for concept2 in post.concepts[i + 1 :]:
                    if self.concept_graph.has_edge(concept1, concept2):
                        self.concept_graph[concept1][concept2]["weight"] += 1
                    else:
                        self.concept_graph.add_edge(concept1, concept2, weight=1)

        # Calculate centrality metrics
        if len(self.concept_graph.nodes()) > 0:
            betweenness = nx.betweenness_centrality(self.concept_graph)
            degree = nx.degree_centrality(self.concept_graph)
            closeness = nx.closeness_centrality(self.concept_graph)

            # Find bridge concepts
            bridges = []
            for node in self.concept_graph.nodes():
                temp_graph = self.concept_graph.copy()
                temp_graph.remove_node(node)
                if nx.number_connected_components(temp_graph) > nx.number_connected_components(
                    self.concept_graph
                ):
                    bridges.append(node)

            # Detect concept clusters
            clusters = list(nx.community.greedy_modularity_communities(self.concept_graph))

            return {
                "nodes": list(self.concept_graph.nodes()),
                "edges": [(u, v, d["weight"]) for u, v, d in self.concept_graph.edges(data=True)],
                "centrality": {
                    "betweenness": betweenness,
                    "degree": degree,
                    "closeness": closeness,
                },
                "bridges": bridges,
                "clusters": [list(cluster) for cluster in clusters],
                "most_central": (
                    max(betweenness.items(), key=lambda x: x[1])[0] if betweenness else None
                ),
                "most_connected": max(degree.items(), key=lambda x: x[1])[0] if degree else None,
            }
        return {}

    def map_emotional_journey(self) -> Dict:
        """Map emotional and energy journey over time"""
        journey = {
            "timeline": [],
            "crisis_points": [],
            "breakthroughs": [],
            "plateaus": [],
            "aha_moments": [],
            "energy_trend": [],
        }

        for i, post in enumerate(self.posts):
            entry = {
                "date": post.date,
                "title": post.title,
                "emotions": post.emotions,
                "energy": post.energy_level,
                "dominant_emotion": (
                    max(post.emotions.items(), key=lambda x: x[1])[0] if post.emotions else None
                ),
            }
            journey["timeline"].append(entry)

            # Identify crisis points (high frustration/exhaustion)
            if (
                post.emotions.get("frustration", 0) > 0.5
                or post.emotions.get("exhaustion", 0) > 0.5
            ):
                journey["crisis_points"].append(
                    {
                        "date": post.date,
                        "title": post.title,
                        "trigger": (
                            "frustration"
                            if post.emotions.get("frustration", 0)
                            > post.emotions.get("exhaustion", 0)
                            else "exhaustion"
                        ),
                    }
                )

            # Identify breakthroughs
            if post.emotions.get("breakthrough", 0) > 0.3:
                journey["breakthroughs"].append(
                    {"date": post.date, "title": post.title, "energy_spike": post.energy_level}
                )

            # Identify aha moments
            if (
                "aha" in post.content.lower()
                or "eureka" in post.content.lower()
                or "finally" in post.content.lower()
            ):
                # Extract context around aha moment
                content_lower = post.content.lower()
                for pattern in ["aha", "eureka", "finally"]:
                    if pattern in content_lower:
                        idx = content_lower.find(pattern)
                        context = post.content[
                            max(0, idx - 100) : min(len(post.content), idx + 100)
                        ]
                        journey["aha_moments"].append(
                            {"date": post.date, "title": post.title, "context": context.strip()}
                        )
                        break

            # Track energy trend
            journey["energy_trend"].append(post.energy_level)

        # Identify plateaus (periods of stable energy)
        if len(journey["energy_trend"]) > 3:
            for i in range(1, len(journey["energy_trend"]) - 1):
                if (
                    abs(journey["energy_trend"][i] - journey["energy_trend"][i - 1]) < 0.1
                    and abs(journey["energy_trend"][i] - journey["energy_trend"][i + 1]) < 0.1
                ):
                    journey["plateaus"].append(
                        {
                            "start": self.posts[i - 1].date,
                            "end": self.posts[i + 1].date,
                            "energy_level": journey["energy_trend"][i],
                        }
                    )

        return journey

    def build_knowledge_dependency_graph(self) -> Dict:
        """Build knowledge dependency structure"""
        # Track which concepts build on others
        concept_timeline = defaultdict(list)
        for i, post in enumerate(self.posts):
            for concept in post.concepts:
                concept_timeline[concept].append(i)

        # Build dependency edges
        for post_idx, post in enumerate(self.posts):
            # Look for references to earlier concepts
            for concept in post.concepts:
                first_appearance = min(concept_timeline[concept])
                if first_appearance < post_idx:
                    # This concept was introduced earlier
                    for earlier_idx in range(first_appearance, post_idx):
                        earlier_post = self.posts[earlier_idx]
                        for earlier_concept in earlier_post.concepts:
                            if earlier_concept != concept:
                                self.knowledge_graph.add_edge(earlier_concept, concept)

        # Find critical path
        critical_concepts = []
        if len(self.knowledge_graph.nodes()) > 0:
            # Find nodes with high out-degree (foundational)
            out_degrees = dict(self.knowledge_graph.out_degree())
            if out_degrees:
                foundational = sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
                critical_concepts = [c[0] for c in foundational]

        # Minimum viable learning path
        learning_path = []
        if critical_concepts:
            # Start with most foundational concept
            current = critical_concepts[0]
            visited = {current}
            learning_path.append(current)

            # Follow the path of maximum dependencies
            while True:
                next_concepts = [
                    n for n in self.knowledge_graph.successors(current) if n not in visited
                ]
                if not next_concepts:
                    break
                # Choose concept with most dependencies
                current = max(next_concepts, key=lambda x: self.knowledge_graph.out_degree(x))
                visited.add(current)
                learning_path.append(current)

        return {
            "dependencies": [(u, v) for u, v in self.knowledge_graph.edges()],
            "critical_concepts": critical_concepts,
            "learning_path": learning_path,
            "concept_prerequisites": {
                concept: list(self.knowledge_graph.predecessors(concept))
                for concept in self.knowledge_graph.nodes()
            },
            "unlocked_capabilities": {
                concept: list(self.knowledge_graph.successors(concept))
                for concept in self.knowledge_graph.nodes()
            },
        }

    def analyze_reader_personas(self) -> Dict:
        """Analyze content resonance for different PM personas"""
        persona_analysis = {}

        for persona_name, persona_traits in self.personas.items():
            analysis = {
                "resonant_posts": [],
                "key_insights": [],
                "engagement_score": 0,
                "relevant_concepts": Counter(),
            }

            for post in self.posts:
                # Calculate relevance score
                relevance = 0
                for interest in persona_traits["interests"]:
                    if interest in post.concepts:
                        relevance += 1
                        analysis["relevant_concepts"][interest] += 1

                if relevance > 0:
                    analysis["resonant_posts"].append(
                        {
                            "title": post.title,
                            "date": post.date,
                            "relevance_score": relevance,
                            "matching_interests": [
                                c for c in post.concepts if c in persona_traits["interests"]
                            ],
                        }
                    )

                # Extract insights relevant to pain points
                for pain_point in persona_traits["pain_points"]:
                    if pain_point.replace("_", " ") in post.content.lower():
                        analysis["key_insights"].append(
                            {"post": post.title, "pain_point": pain_point, "date": post.date}
                        )

            # Sort resonant posts by relevance
            analysis["resonant_posts"].sort(key=lambda x: x["relevance_score"], reverse=True)
            analysis["engagement_score"] = sum(
                p["relevance_score"] for p in analysis["resonant_posts"]
            )

            persona_analysis[persona_name] = analysis

        return persona_analysis

    def detect_content_gaps(self) -> Dict:
        """Identify content gaps and unanswered questions"""
        gaps = {
            "unanswered_questions": [],
            "incomplete_spirals": [],
            "implied_principles": [],
            "bridge_content_needed": [],
            "missing_connections": [],
        }

        # Find questions in content
        for post in self.posts:
            questions = re.findall(r"[^.!?]*\?", post.content)
            for question in questions:
                # Check if question appears to be rhetorical or answered
                question_pos = post.content.find(question)
                following_text = post.content[question_pos : question_pos + 500]

                # Simple heuristic: if no definitive statement follows, it's unanswered
                if not re.search(
                    r"\b(answer|solution|because|therefore|thus)\b", following_text.lower()
                ):
                    gaps["unanswered_questions"].append(
                        {"question": question.strip(), "post": post.title, "date": post.date}
                    )

        # Find incomplete spirals (concepts mentioned but not fully explored)
        concept_depth = defaultdict(int)
        for post in self.posts:
            for concept in post.concepts:
                # Rough measure of depth: how much is written about this concept
                pattern = self.concept_patterns[concept]
                matches = len(re.findall(pattern, post.content.lower()))
                concept_depth[concept] += matches

        # Concepts mentioned but not deeply explored
        for concept, depth in concept_depth.items():
            if depth < 5:  # Arbitrary threshold
                gaps["incomplete_spirals"].append(
                    {"concept": concept, "depth": depth, "needs_expansion": True}
                )

        # Find implied but not explicit principles
        principle_patterns = [
            r"always\s+\w+",
            r"never\s+\w+",
            r"rule\s+of\s+thumb",
            r"lesson\s+learned",
            r"key\s+insight",
        ]

        for post in self.posts:
            for pattern in principle_patterns:
                matches = re.findall(pattern, post.content.lower())
                for match in matches:
                    gaps["implied_principles"].append(
                        {"implied": match, "post": post.title, "needs_formalization": True}
                    )

        # Identify where bridge content is needed
        # Look for large jumps in complexity or topic
        for i in range(len(self.posts) - 1):
            current = set(self.posts[i].concepts)
            next_post = set(self.posts[i + 1].concepts)

            # If concepts change dramatically, bridge content might help
            overlap = current.intersection(next_post)
            if len(overlap) < len(current) * 0.3:  # Less than 30% overlap
                gaps["bridge_content_needed"].append(
                    {
                        "between": f"{self.posts[i].title} and {self.posts[i+1].title}",
                        "current_concepts": list(current),
                        "next_concepts": list(next_post),
                        "missing_link": list(current.symmetric_difference(next_post)),
                    }
                )

        return gaps

    def analyze_metacognitive_patterns(self) -> Dict:
        """Analyze how learning and problem-solving evolve"""
        patterns = {
            "learning_evolution": [],
            "problem_solving_approaches": [],
            "debugging_maturity": [],
            "systematic_thinking": [],
        }

        # Track learning evolution
        learning_indicators = {
            "novice": [r"confused", r"stuck", r"don\'t understand", r"why"],
            "developing": [r"starting to", r"beginning to", r"learning", r"figuring out"],
            "competent": [r"understand", r"clear", r"makes sense", r"got it"],
            "expert": [r"obvious", r"trivial", r"simple", r"pattern", r"systematic"],
        }

        for post in self.posts:
            learning_level = {}
            for level, indicators in learning_indicators.items():
                count = sum(len(re.findall(ind, post.content.lower())) for ind in indicators)
                learning_level[level] = count

            dominant_level = (
                max(learning_level.items(), key=lambda x: x[1])[0] if learning_level else "novice"
            )
            patterns["learning_evolution"].append(
                {
                    "date": post.date,
                    "title": post.title,
                    "level": dominant_level,
                    "indicators": learning_level,
                }
            )

        # Track problem-solving approach evolution
        approaches = {
            "trial_and_error": [r"try", r"attempt", r"experiment", r"see what happens"],
            "systematic": [r"systematic", r"methodical", r"process", r"framework"],
            "pattern_matching": [r"pattern", r"similar to", r"like when", r"reminds me"],
            "first_principles": [r"fundamental", r"basic", r"core", r"essence", r"root cause"],
        }

        for post in self.posts:
            approach_scores = {}
            for approach, markers in approaches.items():
                count = sum(len(re.findall(m, post.content.lower())) for m in markers)
                approach_scores[approach] = count

            if approach_scores:
                dominant_approach = max(approach_scores.items(), key=lambda x: x[1])[0]
                patterns["problem_solving_approaches"].append(
                    {
                        "date": post.date,
                        "title": post.title,
                        "approach": dominant_approach,
                        "scores": approach_scores,
                    }
                )

        # Track debugging methodology maturity
        debug_maturity = {
            "reactive": [r"error", r"broken", r"failed", r"crash"],
            "diagnostic": [r"investigate", r"trace", r"debug", r"analyze"],
            "preventive": [r"prevent", r"avoid", r"test first", r"validate", r"verify"],
            "systematic": [r"methodology", r"process", r"checklist", r"protocol"],
        }

        for post in self.posts:
            maturity_scores = {}
            for level, markers in debug_maturity.items():
                count = sum(len(re.findall(m, post.content.lower())) for m in markers)
                maturity_scores[level] = count

            if maturity_scores:
                patterns["debugging_maturity"].append(
                    {
                        "date": post.date,
                        "title": post.title,
                        "maturity": maturity_scores,
                        "dominant": max(maturity_scores.items(), key=lambda x: x[1])[0],
                    }
                )

        # Track emergence of systematic thinking
        systematic_markers = [
            r"framework",
            r"methodology",
            r"systematic",
            r"protocol",
            r"process",
            r"checklist",
            r"standard",
            r"convention",
        ]

        for post in self.posts:
            systematic_count = sum(
                len(re.findall(m, post.content.lower())) for m in systematic_markers
            )
            if systematic_count > 0:
                patterns["systematic_thinking"].append(
                    {
                        "date": post.date,
                        "title": post.title,
                        "systematic_score": systematic_count / post.word_count * 100,
                    }
                )

        return patterns

    def analyze_narrative_arc(self) -> Dict:
        """Analyze the narrative structure and story elements"""
        narrative = {
            "hero_journey": {},
            "crisis_response_cycles": [],
            "character_development": {},
            "supporting_cast": {},
            "narrative_phases": [],
        }

        # Map to hero's journey stages
        journey_stages = {
            "ordinary_world": self.posts[:2] if len(self.posts) > 2 else self.posts,
            "call_to_adventure": [],
            "crossing_threshold": [],
            "tests_and_trials": [],
            "revelation": [],
            "transformation": [],
            "return_with_elixir": [],
        }

        # Identify journey stages based on content
        for post in self.posts:
            content_lower = post.content.lower()

            if "question" in post.title.lower() or "started" in post.title.lower():
                journey_stages["call_to_adventure"].append(post.title)
            elif "battle" in content_lower or "test" in content_lower:
                journey_stages["tests_and_trials"].append(post.title)
            elif "breakthrough" in content_lower or "miracle" in content_lower:
                journey_stages["revelation"].append(post.title)
            elif "transform" in content_lower or "evolve" in content_lower:
                journey_stages["transformation"].append(post.title)

        narrative["hero_journey"] = journey_stages

        # Track crisis-response cycles
        for i, post in enumerate(self.posts):
            if post.emotions.get("frustration", 0) > 0.3:
                # Look for response in next posts
                for j in range(i + 1, min(i + 3, len(self.posts))):
                    if (
                        self.posts[j].emotions.get("breakthrough", 0) > 0.2
                        or self.posts[j].emotions.get("satisfaction", 0) > 0.2
                    ):
                        narrative["crisis_response_cycles"].append(
                            {
                                "crisis": post.title,
                                "crisis_date": post.date,
                                "response": self.posts[j].title,
                                "response_date": self.posts[j].date,
                                "resolution_time": j - i,
                            }
                        )
                        break

        # Track character development (author as protagonist)
        early_posts = self.posts[:5] if len(self.posts) > 5 else self.posts
        late_posts = self.posts[-5:] if len(self.posts) > 5 else self.posts

        early_concepts = set()
        late_concepts = set()
        for post in early_posts:
            early_concepts.update(post.concepts)
        for post in late_posts:
            late_concepts.update(post.concepts)

        narrative["character_development"] = {
            "early_focus": list(early_concepts),
            "late_focus": list(late_concepts),
            "new_capabilities": list(late_concepts - early_concepts),
            "consistent_themes": list(early_concepts.intersection(late_concepts)),
        }

        # Identify supporting cast (AI agents, tools, concepts as characters)
        cast_members = defaultdict(int)
        for post in self.posts:
            # AI agents
            for agent in ["Claude", "Gemini", "Cursor", "Opus", "Sonnet"]:
                if agent.lower() in post.content.lower():
                    cast_members[agent] += 1

            # Tools and systems
            for tool in ["Docker", "Python", "GitHub", "PostgreSQL", "Redis"]:
                if tool.lower() in post.content.lower():
                    cast_members[tool] += 1

        narrative["supporting_cast"] = {
            "main_characters": {k: v for k, v in cast_members.items() if v > 3},
            "recurring_characters": {k: v for k, v in cast_members.items() if v > 1 and v <= 3},
            "cameos": {k: v for k, v in cast_members.items() if v == 1},
        }

        # Identify narrative phases
        phases = []
        phase_size = len(self.posts) // 4 if len(self.posts) >= 4 else 1

        for i in range(0, len(self.posts), phase_size):
            phase_posts = self.posts[i : i + phase_size]
            if phase_posts:
                dominant_emotion = Counter()
                dominant_concepts = Counter()

                for post in phase_posts:
                    if post.emotions:
                        dominant_emotion.update([max(post.emotions.items(), key=lambda x: x[1])[0]])
                    dominant_concepts.update(post.concepts)

                phases.append(
                    {
                        "posts": [p.title for p in phase_posts],
                        "date_range": f"{phase_posts[0].date} to {phase_posts[-1].date}",
                        "dominant_emotion": (
                            dominant_emotion.most_common(1)[0][0] if dominant_emotion else None
                        ),
                        "key_concepts": [c[0] for c in dominant_concepts.most_common(3)],
                    }
                )

        narrative["narrative_phases"] = phases

        return narrative

    def generate_binocular_synthesis(self) -> str:
        """Generate synthesis highlighting unique insights"""
        synthesis = []
        synthesis.append("# Binocular Analysis Synthesis\n")
        synthesis.append("## Unique Insights Not Found in Spiral Analysis\n\n")

        # Semantic Network Insights
        semantic = self.build_semantic_network()
        if semantic:
            synthesis.append("### 1. Conceptual Hub Architecture\n")
            synthesis.append(f"**Most Central Concept**: {semantic.get('most_central', 'N/A')}\n")
            synthesis.append(
                f"**Most Connected Concept**: {semantic.get('most_connected', 'N/A')}\n"
            )
            synthesis.append(f"**Bridge Concepts**: {', '.join(semantic.get('bridges', []))}\n")
            synthesis.append(
                f"**Concept Clusters**: {len(semantic.get('clusters', []))} distinct groups\n\n"
            )

        # Emotional Journey Insights
        journey = self.map_emotional_journey()
        synthesis.append("### 2. Emotional Energy Dynamics\n")
        synthesis.append(f"**Crisis Points**: {len(journey['crisis_points'])} identified\n")
        synthesis.append(f"**Breakthroughs**: {len(journey['breakthroughs'])} moments\n")
        synthesis.append(f"**Aha Moments**: {len(journey['aha_moments'])} discoveries\n")

        if journey["energy_trend"]:
            avg_energy = sum(journey["energy_trend"]) / len(journey["energy_trend"])
            synthesis.append(f"**Average Energy Level**: {avg_energy:.2f}\n")
            synthesis.append(f"**Energy Volatility**: {np.std(journey['energy_trend']):.2f}\n\n")

        # Knowledge Architecture
        knowledge = self.build_knowledge_dependency_graph()
        synthesis.append("### 3. Knowledge Dependency Structure\n")
        if knowledge.get("critical_concepts"):
            synthesis.append(
                f"**Foundational Concepts**: {', '.join(knowledge['critical_concepts'][:3])}\n"
            )
        if knowledge.get("learning_path"):
            synthesis.append(
                f"**Optimal Learning Path**: {' → '.join(knowledge['learning_path'][:5])}\n\n"
            )

        # Persona-Specific Insights
        personas = self.analyze_reader_personas()
        synthesis.append("### 4. Audience Resonance Mapping\n")
        for persona, analysis in personas.items():
            if analysis["engagement_score"] > 0:
                synthesis.append(
                    f"**{persona.replace('_', ' ').title()}**: Engagement Score {analysis['engagement_score']}\n"
                )
                top_posts = analysis["resonant_posts"][:2]
                for post in top_posts:
                    synthesis.append(
                        f"  - {post['title'][:50]}... (relevance: {post['relevance_score']})\n"
                    )
        synthesis.append("\n")

        # Content Gaps
        gaps = self.detect_content_gaps()
        synthesis.append("### 5. Strategic Content Opportunities\n")
        synthesis.append(f"**Unanswered Questions**: {len(gaps['unanswered_questions'])}\n")
        synthesis.append(f"**Incomplete Concept Spirals**: {len(gaps['incomplete_spirals'])}\n")
        synthesis.append(
            f"**Bridge Content Needed**: {len(gaps['bridge_content_needed'])} transitions\n"
        )
        synthesis.append(
            f"**Implied Principles**: {len(gaps['implied_principles'])} to formalize\n\n"
        )

        # Metacognitive Evolution
        meta = self.analyze_metacognitive_patterns()
        synthesis.append("### 6. Learning Process Evolution\n")
        if meta["learning_evolution"]:
            early_level = meta["learning_evolution"][0]["level"]
            late_level = meta["learning_evolution"][-1]["level"]
            synthesis.append(f"**Learning Journey**: {early_level} → {late_level}\n")

        if meta["systematic_thinking"]:
            systematic_growth = (
                meta["systematic_thinking"][-1]["systematic_score"]
                - meta["systematic_thinking"][0]["systematic_score"]
            )
            synthesis.append(
                f"**Systematic Thinking Growth**: {systematic_growth:.1f}% increase\n\n"
            )

        # Narrative Structure
        narrative = self.analyze_narrative_arc()
        synthesis.append("### 7. Story Architecture\n")
        synthesis.append(
            f"**Crisis-Response Cycles**: {len(narrative['crisis_response_cycles'])}\n"
        )
        if narrative["character_development"]:
            synthesis.append(
                f"**New Capabilities Developed**: {len(narrative['character_development']['new_capabilities'])}\n"
            )
            synthesis.append(
                f"**Consistent Themes**: {', '.join(narrative['character_development']['consistent_themes'][:3])}\n"
            )

        # Key Differentiators
        synthesis.append("\n## Key Differentiators from Spiral Analysis\n\n")
        synthesis.append(
            "1. **Emotional Terrain Map**: Shows energy dynamics and breakthrough patterns\n"
        )
        synthesis.append(
            "2. **Knowledge Dependency Graph**: Reveals prerequisite learning structure\n"
        )
        synthesis.append("3. **Persona-Specific Value**: Maps content to reader archetypes\n")
        synthesis.append("4. **Gap Analysis**: Identifies missing content for accessibility\n")
        synthesis.append(
            "5. **Metacognitive Evolution**: Tracks learning-about-learning progression\n"
        )
        synthesis.append("6. **Narrative Structure**: Reveals story elements for engagement\n")
        synthesis.append("7. **Concept Network**: Shows idea relationships and bridges\n\n")

        # Actionable Recommendations
        synthesis.append("## Actionable Transformation Strategy\n\n")
        synthesis.append("### For Technical PMs\n")
        synthesis.append("- Focus on debugging and architecture posts\n")
        synthesis.append("- Highlight performance optimization stories\n")
        synthesis.append("- Emphasize systematic methodology development\n\n")

        synthesis.append("### For Strategic PMs\n")
        synthesis.append("- Extract and formalize the implied principles\n")
        synthesis.append("- Emphasize transformation and evolution themes\n")
        synthesis.append("- Focus on abstraction and pattern recognition\n\n")

        synthesis.append("### For Startup PMs\n")
        synthesis.append("- Highlight rapid learning cycles\n")
        synthesis.append("- Focus on efficiency gains and breakthroughs\n")
        synthesis.append("- Emphasize pragmatic problem-solving\n\n")

        synthesis.append("### Content Development Priorities\n")
        synthesis.append("1. **Bridge Content**: Fill the identified transition gaps\n")
        synthesis.append("2. **Principle Formalization**: Make implied wisdom explicit\n")
        synthesis.append("3. **Emotion-Guided Sequencing**: Use energy map for pacing\n")
        synthesis.append("4. **Persona-Specific Paths**: Create targeted learning journeys\n")
        synthesis.append("5. **Complete Concept Spirals**: Expand incomplete themes\n\n")

        return "".join(synthesis)

    def save_analysis(self, output_dir: str = "analysis") -> None:
        """Save all analysis results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Save semantic network
        with open(output_path / "semantic_network.json", "w") as f:
            json.dump(self.build_semantic_network(), f, indent=2, default=str)

        # Save emotional journey
        with open(output_path / "emotional_journey.json", "w") as f:
            json.dump(self.map_emotional_journey(), f, indent=2, default=str)

        # Save knowledge graph
        with open(output_path / "knowledge_graph.json", "w") as f:
            json.dump(self.build_knowledge_dependency_graph(), f, indent=2, default=str)

        # Save persona analysis
        with open(output_path / "persona_resonance.json", "w") as f:
            json.dump(self.analyze_reader_personas(), f, indent=2, default=str)

        # Save content gaps
        with open(output_path / "content_gaps.json", "w") as f:
            json.dump(self.detect_content_gaps(), f, indent=2, default=str)

        # Save metacognitive analysis
        with open(output_path / "metacognitive_evolution.json", "w") as f:
            json.dump(self.analyze_metacognitive_patterns(), f, indent=2, default=str)

        # Save narrative analysis
        with open(output_path / "narrative_structure.json", "w") as f:
            json.dump(self.analyze_narrative_arc(), f, indent=2, default=str)

        # Save synthesis
        with open(output_path / "binocular_synthesis.md", "w") as f:
            f.write(self.generate_binocular_synthesis())

        print(f"Analysis complete! Results saved to {output_path}/")
        print(f"Total posts analyzed: {len(self.posts)}")
        print(f"Date range: {self.posts[0].date} to {self.posts[-1].date}")
        print(f"Total words: {sum(p.word_count for p in self.posts)}")


if __name__ == "__main__":
    analyzer = BinocularAnalyzer()
    analyzer.load_posts()
    analyzer.save_analysis()
