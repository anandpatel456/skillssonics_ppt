"""
Smart Template Selector - Automatically chooses optimal layouts based on content analysis
"""

from enum import Enum
from typing import List, Dict, Any
import re

class SlideType(Enum):
    TITLE = "title"
    TITLE_ONLY = "title_only"
    SECTION_HEADER = "section_header"
    SINGLE_CONTENT = "single_content"
    TWO_COLUMN = "two_column"
    THREE_COLUMN = "three_column"
    COMPARISON = "comparison"
    IMAGE_FOCUS = "image_focus"
    CHART_DATA = "chart_data"
    PROCESS_STEPS = "process_steps"
    TIMELINE = "timeline"
    QUOTE_TESTIMONIAL = "quote_testimonial"
    TEAM_PEOPLE = "team_people"
    STATISTICS_BIG_NUM = "statistics_big_num"
    ICON_GRID = "icon_grid"
    END_CONTACT = "end_contact"

class TemplateSelector:
    """Intelligently selects templates based on content characteristics"""
    
    # Keywords that trigger specific templates
    TEMPLATE_TRIGGERS = {
        SlideType.COMPARISON: [
            "vs", "versus", "comparison", "difference", "pros and cons", 
            "advantages", "disadvantages", "before and after", "old vs new",
            "traditional vs modern", "theory vs practice"
        ],
        SlideType.PROCESS_STEPS: [
            "step", "process", "workflow", "procedure", "how to", "stages",
            "phases", "methodology", "approach", "implementation", "execution",
            "step-by-step", "sequence", "order", "flow"
        ],
        SlideType.TIMELINE: [
            "timeline", "history", "evolution", "schedule", "roadmap", 
            "milestones", "phases over time", "journey", "progression",
            "2010", "2020", "year", "month", "week", "day", "future"
        ],
        SlideType.STATISTICS_BIG_NUM: [
            "percent", "%", "statistics", "numbers", "growth", "increase",
            "90%", "80%", "market share", "success rate", "placement rate",
            "salary", "package", "stipend", "revenue", "trained", "students"
        ],
        SlideType.QUOTE_TESTIMONIAL: [
            "quote", "testimonial", "review", "feedback", "says", "said",
            "student says", "employer says", "graduate", "success story",
            "\"", "'", "remark", "comment", "experience"
        ],
        SlideType.TEAM_PEOPLE: [
            "team", "faculty", "instructors", "trainers", "staff", "mentors",
            "experts", "professionals", "who we are", "our people", "leadership"
        ],
        SlideType.CHART_DATA: [
            "chart", "graph", "data", "survey", "results", "analysis",
            "pie chart", "bar graph", "trends", "metrics", "kpi", "figures"
        ],
        SlideType.SECTION_HEADER: [
            "module", "unit", "chapter", "section", "part", "introduction to",
            "overview of", "learning outcomes", "objectives", "goals"
        ],
        SlideType.ICON_GRID: [
            "features", "benefits", "services", "skills", "tools", "technologies",
            "modules", "components", "elements", "key points", "highlights"
        ]
    }
    
    def __init__(self):
        self.content_analyzer = ContentAnalyzer()
    
    def analyze_and_select(self, slide_content: Dict[str, Any], slide_index: int, total_slides: int) -> SlideType:
        """
        Analyze content and automatically select best template
        
        Args:
            slide_content: Dictionary with title, points, etc.
            slide_index: Position in presentation (0-based)
            total_slides: Total number of slides
        """
        title = slide_content.get("title", "").lower()
        points = slide_content.get("content", []) or []
        points_text = " ".join(points).lower()
        combined_text = f"{title} {points_text}"
        
        # Rule 1: First slide is always Title
        if slide_index == 0:
            return SlideType.TITLE
            
        # Rule 2: Last slide is always End/Contact
        if slide_index == total_slides - 1:
            return SlideType.END_CONTACT
            
        # Rule 3: Check for section headers (short title, no points or "introduction/overview")
        if len(points) <= 1 or any(keyword in title for keyword in ["introduction", "overview", "module", "unit"]):
            if self._is_section_header(title, points):
                return SlideType.SECTION_HEADER
        
        # Rule 4: Analyze content patterns
        template_scores = self._score_templates(combined_text, points)
        
        # Rule 5: Check point structure for specific layouts
        if self._has_comparison_structure(points):
            return SlideType.COMPARISON
            
        if self._has_process_structure(points):
            return SlideType.PROCESS_STEPS
            
        if self._has_timeline_structure(points):
            return SlideType.TIMELINE
            
        # Rule 6: Check for statistics/numbers
        if self._contains_big_numbers(points):
            return SlideType.STATISTICS_BIG_NUM
            
        # Rule 7: Check for testimonials
        if self._contains_quotes(points):
            return SlideType.QUOTE_TESTIMONIAL
            
        # Rule 8: Check for list of features/benefits (short items)
        if self._is_feature_list(points):
            return SlideType.ICON_GRID
            
        # Rule 9: Check content length for column layout
        point_lengths = [len(p) for p in points]
        avg_length = sum(point_lengths) / len(point_lengths) if point_lengths else 0
        
        if len(points) >= 6 and avg_length > 80:
            # Long content - split into two columns
            return SlideType.TWO_COLUMN
            
        if len(points) >= 3 and any("vs" in p.lower() or "compare" in p.lower() for p in points):
            return SlideType.TWO_COLUMN
            
        # Rule 10: Default based on content density
        if len(points) <= 2 and avg_length > 150:
            return SlideType.SINGLE_CONTENT  # Heavy text, single focus
            
        return SlideType.SINGLE_CONTENT
    
    def _score_templates(self, text: str, points: List[str]) -> Dict[SlideType, int]:
        """Score each template type based on keyword matches"""
        scores = {template: 0 for template in SlideType}
        
        for template, keywords in self.TEMPLATE_TRIGGERS.items():
            for keyword in keywords:
                if keyword in text:
                    scores[template] += 1
                    
        return scores
    
    def _is_section_header(self, title: str, points: List[str]) -> bool:
        """Determine if this is a section divider slide"""
        header_indicators = ["module", "unit", "chapter", "part", "section", "introduction", "overview"]
        return any(indicator in title.lower() for indicator in header_indicators) or len(points) == 0
    
    def _has_comparison_structure(self, points: List[str]) -> bool:
        """Detect comparison patterns in bullet points"""
        comparison_markers = ["vs", "versus", "difference", "while", "whereas", "compared to", "on the other hand"]
        return any(marker in " ".join(points).lower() for marker in comparison_markers)
    
    def _has_process_structure(self, points: List[str]) -> bool:
        """Detect sequential/step patterns"""
        step_patterns = [
            r"^\d+\.",  # Starts with number
            r"^step\s+\d",  # "Step 1"
            r"^phase\s+\d",  # "Phase 1"
            r"^stage\s+\d",  # "Stage 1"
            r"first", r"second", r"third", r"next", r"then", r"finally"
        ]
        
        text = " ".join(points).lower()
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in step_patterns)
    
    def _has_timeline_structure(self, points: List[str]) -> bool:
        """Detect timeline/date patterns"""
        date_patterns = [
            r"\b20\d\d\b",  # Years 2000-2099
            r"\b\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)",
            r"month\s+\d", r"week\s+\d", r"day\s+\d",
            r"timeline", r"roadmap", r"milestone"
        ]
        
        text = " ".join(points)
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in date_patterns)
    
    def _contains_big_numbers(self, points: List[str]) -> bool:
        """Check for statistics/big numbers worthy of highlight"""
        number_patterns = [
            r"\b\d+%",  # Percentages
            r"\b\d+\s*(k|thousand|lac|lakh|million|cr|crore)",  # Large numbers
            r"\b\d{2,3}\s*(students|trainees|placements|companies)",  # Counts
            r"₹\s*\d+", r"\$\s*\d+",  # Currency
            r"(increase|decrease|growth|rise|fall).*?\d+%"  # Growth stats
        ]
        
        text = " ".join(points)
        matches = sum(1 for pattern in number_patterns if re.search(pattern, text, re.IGNORECASE))
        return matches >= 2  # At least 2 statistical references
    
    def _contains_quotes(self, points: List[str]) -> bool:
        """Detect quoted text or testimonials"""
        quote_marks = ['''', "'", '"', ''', '"', '"']
        text = " ".join(points)
        return any(mark in text for mark in quote_marks) or "says" in text.lower() or "testimonial" in text.lower()
    
    def _is_feature_list(self, points: List[str]) -> bool:
        """Check if points are short feature/benefit items"""
        if not points:
            return False
            
        # Short items (under 60 chars) with similar structure
        short_count = sum(1 for p in points if len(p) < 60)
        return short_count >= 3 and len(points) >= 4


class ContentAnalyzer:
    """Analyzes content structure and suggests optimizations"""
    
    def optimize_for_template(self, content: Dict[str, Any], template_type: SlideType) -> Dict[str, Any]:
        """
        Reformat content to best fit the selected template
        """
        optimized = content.copy()
        
        if template_type == SlideType.COMPARISON:
            optimized = self._format_comparison(content)
        elif template_type == SlideType.PROCESS_STEPS:
            optimized = self._format_process(content)
        elif template_type == SlideType.TWO_COLUMN:
            optimized = self._split_two_columns(content)
        elif template_type == SlideType.STATISTICS_BIG_NUM:
            optimized = self._extract_statistics(content)
        elif template_type == SlideType.ICON_GRID:
            optimized = self._format_icon_grid(content)
            
        return optimized
    
    def _format_comparison(self, content: Dict) -> Dict:
        """Split content into left/right comparison columns"""
        points = content.get("content", [])
        
        left_items = []
        right_items = []
        
        for point in points:
            lower = point.lower()
            if any(word in lower for word in ["traditional", "theory", "old", "before", "disadvantage", "con"]):
                left_items.append(point)
            elif any(word in lower for word in ["modern", "practice", "new", "after", "advantage", "pro"]):
                right_items.append(point)
            else:
                # Alternate distribution
                if len(left_items) <= len(right_items):
                    left_items.append(point)
                else:
                    right_items.append(point)
        
        return {
            **content,
            "left_content": left_items,
            "right_content": right_items,
            "left_title": "Traditional Approach",
            "right_title": "Modern Approach"
        }
    
    def _format_process(self, content: Dict) -> Dict:
        """Format content as numbered steps"""
        points = content.get("content", [])
        steps = []
        
        for i, point in enumerate(points, 1):
            # Clean up existing numbers
            clean = re.sub(r'^\d+[\.\)]\s*', '', point)
            steps.append(f"Step {i}: {clean}")
            
        return {
            **content,
            "content": steps,
            "diagram_type": "process",
            "diagram_data": steps
        }
    
    def _split_two_columns(self, content: Dict) -> Dict:
        """Split long content into two balanced columns"""
        points = content.get("content", [])
        mid = len(points) // 2
        
        return {
            **content,
            "left_content": points[:mid],
            "right_content": points[mid:],
            "left_title": "Key Points",
            "right_title": "Details"
        }
    
    def _extract_statistics(self, content: Dict) -> Dict:
        """Extract and highlight statistics"""
        points = content.get("content", [])
        stats = []
        
        for point in points:
            # Extract numbers and percentages
            numbers = re.findall(r'\d+%|\d+\s*(k|thousand|lac|lakh|million|cr|crore)|₹\s*\d+|\$\s*\d+', point)
            if numbers:
                stats.append({
                    "number": numbers[0],
                    "context": point
                })
                
        return {
            **content,
            "statistics": stats,
            "highlight_stats": True
        }
    
    def _format_icon_grid(self, content: Dict) -> Dict:
        """Format short points as icon grid items"""
        points = content.get("content", [])
        
        # Assign icons based on content keywords
        icon_map = {
            "skill": "🔧", "tool": "🛠️", "software": "💻", "hardware": "🔌",
            "safety": "🦺", "certificate": "📜", "job": "💼", "career": "🚀",
            "money": "💰", "salary": "💵", "learn": "📚", "practice": "🏋️",
            "test": "📝", "exam": "✅", "industry": "🏭", "company": "🏢"
        }
        
        items = []
        for point in points:
            icon = "⭐"  # default
            for keyword, icon_char in icon_map.items():
                if keyword in point.lower():
                    icon = icon_char
                    break
            items.append({"icon": icon, "text": point})
            
        return {
            **content,
            "icon_grid_items": items
        }