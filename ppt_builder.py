"""
SkillSonics PPT Builder — routes slide data to templates with unique images.
"""
from pptx import Presentation
from pptx.util import Inches

from templates import SlideTemplate
from template_selector import SlideType
from config import BRAND_COLORS
from visual_enhancer import VisualEnhancer


class PPTBuilder:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(10)
        self.prs.slide_height = Inches(7.5)
        self.template = SlideTemplate(self.prs)
        self.colors = BRAND_COLORS
        self.visual = VisualEnhancer()
        self.slide_counter = 0  # Track slide index for unique images

    def build_slide(self, slide_data):
        tmpl = slide_data.get("auto_template", SlideType.SINGLE_CONTENT.value)
        dispatch = {
            SlideType.TITLE.value:              self._build_title,
            SlideType.TITLE_ONLY.value:         self._build_title,
            SlideType.SECTION_HEADER.value:     self._build_section,
            SlideType.SINGLE_CONTENT.value:     self._build_content,
            SlideType.TWO_COLUMN.value:         self._build_two_col,
            SlideType.THREE_COLUMN.value:       self._build_content,
            SlideType.COMPARISON.value:         self._build_comparison,
            SlideType.PROCESS_STEPS.value:      self._build_process,
            SlideType.TIMELINE.value:           self._build_process,
            SlideType.STATISTICS_BIG_NUM.value: self._build_stats,
            SlideType.QUOTE_TESTIMONIAL.value:  self._build_content,
            SlideType.ICON_GRID.value:          self._build_content,
            SlideType.CHART_DATA.value:         self._build_content,
            SlideType.TEAM_PEOPLE.value:        self._build_content,
            SlideType.END_CONTACT.value:        self._build_end,
        }
        builder = dispatch.get(tmpl, self._build_content)
        result = builder(slide_data)
        self.slide_counter += 1  # Increment after each slide
        return result

    def _build_title(self, data):
        return self.template.create_title_slide(
            title=data.get("title", ""),
            subtitle=data.get("subtitle", ""),
            topic=data.get("title", ""),
            visual=self.visual,
            slide_idx=self.slide_counter,
        )

    def _build_section(self, data):
        return self.template.create_section_slide(
            title=data.get("title", ""),
            subtitle=data.get("subtitle", ""),
            visual=self.visual,
            topic=data.get("title", ""),
            slide_idx=self.slide_counter,
        )

    def _build_content(self, data):
        return self.template.create_content_slide(
            title=data.get("title", ""),
            points=data.get("content", [])[:6],
            visual=self.visual,
            topic=data.get("title", ""),
            slide_idx=self.slide_counter,
        )

    def _build_two_col(self, data):
        lc = data.get("left_content", [])
        rc = data.get("right_content", [])
        if not lc or not rc:
            items = data.get("content", [])
            mid = max(len(items)//2, 1)
            lc, rc = items[:mid], items[mid:]
        return self.template.create_two_column_slide(
            title=data.get("title", ""),
            left_content=lc[:6],
            right_content=rc[:6],
            left_title=data.get("left_title", ""),
            right_title=data.get("right_title", ""),
        )

    def _build_comparison(self, data):
        lc = data.get("left_content", [])
        rc = data.get("right_content", [])
        if not lc or not rc:
            items = data.get("content", [])
            mid = max(len(items)//2, 1)
            lc, rc = items[:mid], items[mid:]
        return self.template.create_comparison_slide(
            title=data.get("title", ""),
            left_title=data.get("left_title", "Traditional"),
            left_content=lc[:5],
            right_title=data.get("right_title", "Modern"),
            right_content=rc[:5],
        )

    def _build_process(self, data):
        return self.template.create_process_slide(
            title=data.get("title", ""),
            steps=data.get("content", [])[:5],
        )

    def _build_stats(self, data):
        stats = data.get("statistics", [])
        if not stats:
            for item in data.get("content", [])[:4]:
                for sep in [" — ", " - ", ": "]:
                    if sep in item:
                        p = item.split(sep, 1)
                        stats.append({"number": p[0].strip(), "context": p[1].strip()})
                        break
                else:
                    w = item.split()
                    stats.append({"number": w[0] if w else "—",
                                  "context": " ".join(w[1:]) if len(w)>1 else item})
        return self.template.create_stats_slide(
            title=data.get("title", ""),
            statistics=stats[:4],
        )

    def _build_end(self, data):
        return self.template.create_end_slide(
            title=data.get("title", "Start Your Journey"),
        )

    def build_presentation(self, content_data, **kwargs):
        self.slide_counter = 0  # Reset counter
        for slide in content_data.get("slides", []):
            self.build_slide(slide)

    def save(self, filename="SkillSonics_Presentation.pptx"):
        import os
        out_dir = "/tmp/skillsonics_output"
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, filename)
        self.prs.save(path)
        return path