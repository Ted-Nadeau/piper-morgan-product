#!/usr/bin/env python3
"""
Blog Spiral Learning Analysis
Analyzes blog posts for thematic patterns, evolution over time, and spiral learning
"""

import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import structlog

logger = structlog.get_logger()


class BlogSpiralAnalyzer:
    """Analyzes blog posts for spiral learning patterns and thematic evolution"""

    def __init__(self, blog_dir: str = "piper-morgan-blogs/raw"):
        self.blog_dir = Path(blog_dir)
        self.posts = {}
        self.themes = defaultdict(list)
        self.timeline = []
        self.spiral_patterns = []

    def load_all_posts(self) -> Dict[str, Dict]:
        """Load and parse all blog posts"""
        logger.info("Loading blog posts", directory=str(self.blog_dir))

        for file_path in self.blog_dir.glob("*.md"):
            if file_path.name.startswith("."):
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
                post_data = self._parse_post(file_path.name, content)
                if post_data:
                    self.posts[file_path.name] = post_data
                    self.timeline.append(post_data)
            except Exception as e:
                logger.error("Failed to load post", file=file_path.name, error=str(e))

        # Sort timeline by date
        self.timeline.sort(key=lambda x: x["date"])
        logger.info("Loaded posts", count=len(self.posts))
        return self.posts

    def _parse_post(self, filename: str, content: str) -> Dict[str, Any]:
        """Parse individual blog post"""
        # Extract metadata from filename
        match = re.match(r"(\d{3})-(\d{4}-\d{2}-\d{2})-(.+)\.md", filename)
        if not match:
            return None

        post_num = int(match.group(1))
        date_str = match.group(2)
        title = match.group(3).replace("-", " ").title()

        # Try to extract actual date from content
        date_match = re.search(r"(\w+ \d{1,2},? \d{4})", content)
        actual_date = date_match.group(1) if date_match else date_str

        # Extract key insights and themes
        insights = self._extract_insights(content)

        return {
            "filename": filename,
            "post_number": post_num,
            "date": actual_date,
            "date_sort": date_str,
            "title": title,
            "content": content,
            "word_count": len(content.split()),
            "insights": insights,
            "themes": self._identify_themes(content),
            "technical_depth": self._assess_technical_depth(content),
            "universal_principles": self._extract_universal_principles(content),
        }

    def _extract_insights(self, content: str) -> List[str]:
        """Extract key insights from post content"""
        insights = []

        # Look for key phrases that indicate insights
        insight_patterns = [
            r"What I actually learned[:\s]+(.+?)(?=\n\n|\n[A-Z]|$)",
            r"The payoff[:\s]+(.+?)(?=\n\n|\n[A-Z]|$)",
            r"What this taught me[:\s]+(.+?)(?=\n\n|\n[A-Z]|$)",
            r"Key takeaway[:\s]+(.+?)(?=\n\n|\n[A-Z]|$)",
            r"Lesson learned[:\s]+(.+?)(?=\n\n|\n[A-Z]|$)",
            r"This revealed[:\s]+(.+?)(?=\n\n|\n[A-Z]|$)",
            r"What I discovered[:\s]+(.+?)(?=\n\n|\n[A-Z]|$)",
        ]

        for pattern in insight_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            insights.extend([m.strip() for m in matches if m.strip()])

        return insights

    def _identify_themes(self, content: str) -> List[str]:
        """Identify recurring themes in the post"""
        theme_keywords = {
            "Architecture": ["architecture", "design", "structure", "system design", "patterns"],
            "Testing": ["test", "testing", "validation", "debug", "debugging", "qa"],
            "AI/ML": ["ai", "machine learning", "llm", "claude", "gpt", "model", "training"],
            "Product Management": ["product", "pm", "user", "customer", "feature", "roadmap"],
            "Development Process": ["agile", "sprint", "iteration", "workflow", "process"],
            "Technical Debt": ["technical debt", "refactor", "legacy", "maintenance", "cleanup"],
            "Team Coordination": [
                "team",
                "collaboration",
                "communication",
                "coordination",
                "handoff",
            ],
            "Learning": ["learn", "learning", "discovery", "insight", "understanding"],
            "Problem Solving": ["problem", "challenge", "issue", "bug", "fix", "solution"],
            "Infrastructure": [
                "infrastructure",
                "deployment",
                "scaling",
                "performance",
                "monitoring",
            ],
        }

        identified_themes = []
        content_lower = content.lower()

        for theme, keywords in theme_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                identified_themes.append(theme)

        return identified_themes

    def _assess_technical_depth(self, content: str) -> str:
        """Assess the technical depth of the post"""
        technical_indicators = [
            "import",
            "class",
            "function",
            "api",
            "database",
            "sql",
            "python",
            "javascript",
            "git",
            "docker",
            "deployment",
            "infrastructure",
            "architecture",
            "patterns",
            "testing",
            "debugging",
            "performance",
            "scaling",
            "monitoring",
        ]

        content_lower = content.lower()
        technical_count = sum(1 for indicator in technical_indicators if indicator in content_lower)

        if technical_count > 10:
            return "High"
        elif technical_count > 5:
            return "Medium"
        else:
            return "Low"

    def _extract_universal_principles(self, content: str) -> List[str]:
        """Extract universal principles that apply beyond technical context"""
        universal_patterns = [
            r"This applies to any (.+?)(?=\n|\.)",
            r"Universal principle[:\s]+(.+?)(?=\n|\.)",
            r"This is true for (.+?)(?=\n|\.)",
            r"Key insight for (.+?)(?=\n|\.)",
            r"What this teaches us about (.+?)(?=\n|\.)",
        ]

        principles = []
        for pattern in universal_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            principles.extend([m.strip() for m in matches if m.strip()])

        return principles

    def analyze_spiral_learning(self) -> Dict[str, Any]:
        """Analyze for spiral learning patterns"""
        logger.info("Analyzing spiral learning patterns")

        # Group posts by theme
        theme_evolution = defaultdict(list)
        for post in self.timeline:
            for theme in post["themes"]:
                theme_evolution[theme].append(
                    {
                        "date": post["date"],
                        "post_number": post["post_number"],
                        "title": post["title"],
                        "insights": post["insights"],
                        "technical_depth": post["technical_depth"],
                    }
                )

        # Detect spiral patterns (themes that recur with increasing abstraction)
        spiral_patterns = []
        for theme, posts in theme_evolution.items():
            if len(posts) > 1:
                # Sort by post number to see evolution
                posts.sort(key=lambda x: x["post_number"])

                # Check for increasing abstraction/complexity
                abstraction_levels = []
                for i, post in enumerate(posts):
                    level = self._calculate_abstraction_level(post, i)
                    abstraction_levels.append(level)

                # Detect if abstraction increases over time (spiral pattern)
                if len(abstraction_levels) > 1 and abstraction_levels[-1] > abstraction_levels[0]:
                    spiral_patterns.append(
                        {
                            "theme": theme,
                            "posts": posts,
                            "abstraction_progression": abstraction_levels,
                            "spiral_strength": abstraction_levels[-1] - abstraction_levels[0],
                        }
                    )

        return {
            "theme_evolution": dict(theme_evolution),
            "spiral_patterns": spiral_patterns,
            "total_themes": len(theme_evolution),
            "spiral_themes": len(spiral_patterns),
        }

    def _calculate_abstraction_level(self, post: Dict, position: int) -> float:
        """Calculate abstraction level of a post"""
        base_level = position * 0.5  # Later posts get higher base abstraction

        # Technical depth contributes to abstraction
        depth_multiplier = {"High": 1.5, "Medium": 1.0, "Low": 0.5}

        # Insight count contributes to abstraction
        insight_bonus = len(post["insights"]) * 0.2

        return base_level * depth_multiplier.get(post["technical_depth"], 1.0) + insight_bonus

    def generate_content_transformation_guide(self) -> Dict[str, Any]:
        """Generate guide for transforming technical posts into accessible content"""
        logger.info("Generating content transformation guide")

        # Identify universal principles across all posts
        all_principles = []
        for post in self.timeline:
            all_principles.extend(post["universal_principles"])

        principle_frequency = Counter(all_principles)

        # Group insights by accessibility level
        accessible_insights = []
        technical_insights = []

        for post in self.timeline:
            for insight in post["insights"]:
                if self._is_accessible_to_pms(insight):
                    accessible_insights.append(
                        {"insight": insight, "source_post": post["title"], "date": post["date"]}
                    )
                else:
                    technical_insights.append(
                        {"insight": insight, "source_post": post["title"], "date": post["date"]}
                    )

        return {
            "universal_principles": dict(principle_frequency.most_common(10)),
            "accessible_insights": accessible_insights[:20],
            "technical_insights_for_translation": technical_insights[:20],
            "transformation_strategies": [
                "Convert technical debugging stories to problem-solving frameworks",
                "Transform architecture decisions into decision-making principles",
                "Extract team coordination patterns from technical handoffs",
                "Translate testing strategies into quality assurance principles",
                "Convert infrastructure challenges into scaling insights",
            ],
        }

    def _is_accessible_to_pms(self, insight: str) -> bool:
        """Determine if an insight is accessible to non-technical PMs"""
        technical_terms = [
            "python",
            "git",
            "docker",
            "api",
            "database",
            "sql",
            "import",
            "class",
            "function",
            "deployment",
            "infrastructure",
            "monitoring",
            "scaling",
        ]

        insight_lower = insight.lower()
        technical_count = sum(1 for term in technical_terms if term in insight_lower)

        return technical_count < 2  # Less than 2 technical terms = accessible

    def run_complete_analysis(self) -> Dict[str, Any]:
        """Run complete analysis pipeline"""
        logger.info("Starting complete blog analysis")

        # Load posts
        self.load_all_posts()

        # Analyze spiral learning
        spiral_analysis = self.analyze_spiral_learning()

        # Generate transformation guide
        transformation_guide = self.generate_content_transformation_guide()

        # Compile results
        results = {
            "summary": {
                "total_posts": len(self.posts),
                "date_range": f"{self.timeline[0]['date']} to {self.timeline[-1]['date']}",
                "total_word_count": sum(post["word_count"] for post in self.timeline),
                "average_post_length": sum(post["word_count"] for post in self.timeline)
                // len(self.timeline),
            },
            "spiral_learning_analysis": spiral_analysis,
            "content_transformation_guide": transformation_guide,
            "timeline_analysis": {
                "posts_by_date": [
                    {"date": post["date"], "title": post["title"], "themes": post["themes"]}
                    for post in self.timeline
                ],
                "theme_frequency": Counter(
                    theme for post in self.timeline for theme in post["themes"]
                ),
                "technical_depth_distribution": Counter(
                    post["technical_depth"] for post in self.timeline
                ),
            },
        }

        return results


def main():
    """Main analysis execution"""
    analyzer = BlogSpiralAnalyzer()
    results = analyzer.run_complete_analysis()

    # Print summary
    print("=" * 80)
    print("BLOG SPIRAL LEARNING ANALYSIS RESULTS")
    print("=" * 80)

    print(f"\n📊 SUMMARY:")
    print(f"Total Posts: {results['summary']['total_posts']}")
    print(f"Date Range: {results['summary']['date_range']}")
    print(f"Total Words: {results['summary']['total_word_count']:,}")
    print(f"Average Post Length: {results['summary']['average_post_length']:,} words")

    print(f"\n🎯 SPIRAL LEARNING PATTERNS:")
    print(f"Total Themes Identified: {results['spiral_learning_analysis']['total_themes']}")
    print(f"Themes with Spiral Patterns: {results['spiral_learning_analysis']['spiral_themes']}")

    print(f"\n🔄 STRONGEST SPIRAL PATTERNS:")
    for pattern in sorted(
        results["spiral_learning_analysis"]["spiral_patterns"],
        key=lambda x: x["spiral_strength"],
        reverse=True,
    )[:5]:
        print(f"  • {pattern['theme']}: {pattern['spiral_strength']:.1f} abstraction increase")
        print(f"    Posts: {len(pattern['posts'])} over time")

    print(f"\n📚 TOP UNIVERSAL PRINCIPLES:")
    for principle, count in list(
        results["content_transformation_guide"]["universal_principles"].items()
    )[:5]:
        print(f"  • {principle}: {count} mentions")

    print(f"\n💡 ACCESSIBLE INSIGHTS FOR PMs:")
    for insight in results["content_transformation_guide"]["accessible_insights"][:3]:
        print(f"  • {insight['insight'][:100]}...")
        print(f"    From: {insight['source_post']}")

    # Save detailed results
    output_file = "blog_spiral_analysis_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n💾 Detailed results saved to: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
