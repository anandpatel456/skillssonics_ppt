"""
Layout Optimizer
Adjusts slide layout dynamically based on content length and structure.

Fixed:
  - Was overriding template_selector decisions for slides with 4-6 bullets
    that were better served by a single_content layout with dynamic font sizing.
  - Now only promotes to multi-column when content genuinely benefits from it.
  - Respects already-assigned special templates (title, end, statistics, etc.)
"""

# Templates that should never be overridden by the optimizer
PROTECTED_TEMPLATES = {
    "title", "title_only", "section_header",
    "statistics_big_num", "quote_testimonial",
    "process_steps", "timeline", "comparison",
    "team_people", "end_contact", "chart_data",
}


class LayoutOptimizer:

    def optimize(self, slide_data: dict) -> dict:
        """
        Inspect bullet-point count and adjust the auto_template if needed.
        Protected templates are left untouched.
        """
        current = slide_data.get("auto_template", "single_content")

        # Never touch special templates
        if current in PROTECTED_TEMPLATES:
            return slide_data

        content = slide_data.get("content", [])
        n = len(content)

        if n == 0:
            slide_data["auto_template"] = "single_content"

        elif n <= 5:
            # single_content handles ≤5 bullets well with dynamic font sizing
            slide_data["auto_template"] = "single_content"

        elif n <= 8:
            # two columns keeps text readable
            slide_data["auto_template"] = "two_column"
            # split content evenly if not already split
            if not slide_data.get("left_content"):
                mid = n // 2
                slide_data["left_content"]  = content[:mid]
                slide_data["right_content"] = content[mid:]

        else:
            # three columns for very long lists; cap at 9 total points
            slide_data["auto_template"] = "three_column"
            slide_data["content"]       = content[:9]

        return slide_data