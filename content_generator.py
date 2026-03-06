"""
SkillSonics Content Generator — Rich, presenter-ready content.
"""

import json
from groq import Groq
from config import TRAINING_DOMAINS, ORG_INFO
from template_selector import TemplateSelector, SlideType


class ContentGenerator:

    def __init__(self, api_key):
        self.client   = Groq(api_key=api_key)
        self.model    = "llama-3.3-70b-versatile"
        self.selector = TemplateSelector()

    # ─────────────────────────────────────────────────────────────────────────
    def generate_ppt_content(self, topic, audience, num_slides,
                              domain=None, tone="professional", style=None):

        domain_ctx = f"in the {domain} sector" if domain else ""

        system_prompt = f"""You are a senior vocational training content designer for {ORG_INFO['name']}.

ABSOLUTE RULES — violating these will make the presentation useless:

1. EVERY bullet point must be ONE complete, informative sentence of 15–25 words.
   BAD:  "Understand robotics basics"
   GOOD: "Program ABB IRB 1200 robotic arms using RAPID language for pick-and-place tasks in automotive assembly"

2. EVERY slide must have 5–6 bullets. Never fewer than 5.

3. Statistics slides MUST return a "statistics" array (NOT a content array) with:
   - "number": short stat like "90%", "₹28K", "3.2L+"
   - "context": one sentence of 12–15 words explaining what it means

4. Comparison slides MUST return "left_content" and "right_content" arrays with 4–5 items each.

5. Process slides MUST have 4–5 steps, each step described in 15–20 words.

6. Always use real brand names, tools, Indian salary figures (₹), certification names, company names.

7. NEVER truncate, shorten or compress bullet points. Full sentences only.

Tone: {tone}. Audience: {audience}.
"""

        example_stats = json.dumps([
            {"number": "90%", "context": "Placement rate for trained robotics technicians across Pune and Chennai automotive clusters"},
            {"number": "₹28K", "context": "Average starting monthly salary at Maruti Suzuki, Tata Motors and Bosch manufacturing plants"},
            {"number": "3.2L+", "context": "New robotics and automation jobs projected in India by 2026 across auto and electronics manufacturing"},
            {"number": "₹8.4T", "context": "Indian automotive sector market size by 2026 driving large-scale robotics and automation investment"}
        ], indent=2)

        user_prompt = f"""Create a complete vocational training PowerPoint for:

TOPIC: {topic} {domain_ctx}
AUDIENCE: {audience}
SLIDES: {num_slides}

Return ONLY valid JSON — no markdown, no extra text. Use this exact structure:

{{
  "presentation_title": "compelling full title",
  "slides": [

    {{
      "title": "{topic} — Career Transformation",
      "subtitle": "Build a future-proof career in India's fastest-growing industry sector",
      "slide_type": "title",
      "content": []
    }},

    {{
      "title": "What You Will Learn in This Program",
      "slide_type": "single_content",
      "content": [
        "Program 6-axis robotic arms using ABB RAPID and FANUC TP languages for precision assembly tasks",
        "Read and interpret PLC ladder diagrams to diagnose and fix faults within 30 minutes on production lines",
        "Calibrate collaborative robots (cobots) and set safety zones per ISO 10218 robotic safety standard",
        "Integrate IoT sensors with SCADA systems for real-time production monitoring on factory dashboards",
        "Operate teach pendants to create, test and optimise robot programs for pick-and-place operations",
        "Apply IS 15885 safety lockout/tagout procedures before servicing any robotic workstation equipment"
      ]
    }},

    {{
      "title": "Industry Insights & Market Data",
      "slide_type": "statistics_big_num",
      "statistics": {example_stats},
      "content": []
    }},

    {{
      "title": "Core Technical Concepts",
      "slide_type": "single_content",
      "content": [
        "6-Axis Kinematics: joint angles computed using Denavit-Hartenberg parameters for accurate 3D path planning",
        "End-Effectors: pneumatic grippers, welding torches and vision cameras mounted at the robot wrist joint",
        "Servo Drive Systems: brushless DC motors with absolute encoders deliver ±0.02mm positioning repeatability",
        "Machine Vision: 2D and 3D cameras detect part position and orientation for adaptive robotic gripping",
        "Safety PLCs: Pilz PNOZ and Siemens F-CPU monitor light curtains, e-stops and door interlock circuits",
        "Offline Programming: RobotStudio and ROBOGUIDE simulate full cell layout before physical robot commissioning"
      ]
    }},

    {{
      "title": "Traditional vs Modern {topic}",
      "slide_type": "comparison",
      "left_title": "Traditional (Manual) Approach",
      "right_title": "Modern (Robotic) Approach",
      "left_content": [
        "Manual process requires 3–5 years of apprenticeship training before reaching full industry proficiency",
        "Human error rate of 2–5% causes costly rework exceeding ₹50,000 per production shift regularly",
        "Cycle times of 8–12 minutes per unit are typical due to operator fatigue on long shifts",
        "Night shift quality drops significantly as worker concentration and physical endurance decline over time",
        "Product changeover requires 4–6 hours of manual retooling, calibration and trial run before resuming"
      ],
      "right_content": [
        "Certification achievable in 3 months through SkillSonics structured hands-on training programme",
        "Robotic precision reduces error rate to under 0.1%, saving over ₹2 lakh monthly in rework costs",
        "Cycle time drops to under 90 seconds per unit with consistent 24/7 quality output on all shifts",
        "Robots maintain identical quality at 3 AM as at 9 AM — zero fatigue, zero variation in output",
        "Quick-change tooling allows full product changeover in under 20 minutes with zero manual calibration"
      ]
    }},

    {{
      "title": "Hands-On Training Curriculum",
      "slide_type": "process_steps",
      "content": [
        "Module 1 — Safety Induction: Lockout/tagout procedures, PPE selection and IS 15885 robotic safety standards training",
        "Module 2 — Robot Anatomy: Study servo motors, harmonic drives, encoders and end-effector mounting interface systems",
        "Module 3 — Teach Pendant: Program basic pick-and-place and palletising cycles on live ABB IRC5 FlexPendant controller",
        "Module 4 — Offline Programming: Design, simulate and validate welding paths in RobotStudio before physical cell deployment",
        "Module 5 — Maintenance: Diagnose servo fault codes, replace lubrication, recalibrate axes and update controller firmware"
      ]
    }},

    {{
      "title": "Career Outcomes & Salary Progression",
      "slide_type": "single_content",
      "content": [
        "Robotic Cell Operator at Maruti Suzuki or Tata Motors: ₹25,000–35,000 per month as starting package",
        "Automation Technician at Bosch, ABB India or Siemens India: ₹30,000–45,000 per month after one year",
        "PLC and Robotics Programmer with ABB/FANUC certification: ₹40,000–65,000 per month within three years",
        "FANUC Certified Robot Technician: globally recognised credential opening Gulf, Europe and Southeast Asia markets",
        "SkillSonics Placement Cell partners with 150+ companies across Pune, Chennai, Bengaluru, NCR and Ahmedabad",
        "Average time from course completion to confirmed job offer: 6–8 weeks with active placement desk support"
      ]
    }},

    {{
      "title": "Begin Your Journey with SkillSonics",
      "slide_type": "end_contact",
      "content": []
    }}

  ]
}}

CRITICAL: Replace ALL example content above with content SPECIFIC to the topic "{topic}".
Keep the exact same structure, slide_type values and array names.
Every bullet must be 15–25 words. Every stat must have a number and a context.
Generate exactly {num_slides} slides total.
"""

        try:
            response = self.client.chat.completions.create(
                model       = self.model,
                temperature = 0.25,
                max_tokens  = 7000,
                messages    = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
            )

            raw  = response.choices[0].message.content.strip()
            raw  = self._clean_json(raw)
            data = json.loads(raw)

            slides = data.get("slides", [])[:num_slides]

            for i, slide in enumerate(slides):
                st = slide.get("slide_type", "")

                # ── Auto-detect missing slide_type ────────────────────────────
                if not st:
                    tl = slide.get("title", "").lower()
                    if i == 0:
                        st = "title"
                    elif i == len(slides) - 1:
                        st = "end_contact"
                    elif any(w in tl for w in ["vs", "versus", "comparison", "traditional", "modern"]):
                        st = "comparison"
                    elif any(w in tl for w in ["step", "process", "module", "curriculum", "how to"]):
                        st = "process_steps"
                    elif any(w in tl for w in ["statistic", "insight", "market", "data", "figure"]):
                        st = "statistics_big_num"
                    else:
                        st = "single_content"

                # ── Fix stats slide that came back with content[] ──────────────
                if st == "statistics_big_num" and not slide.get("statistics"):
                    raw_pts  = slide.get("content", [])
                    slide["statistics"] = self._parse_stats(raw_pts)
                    slide["content"]    = []

                # ── Fix comparison slide missing left/right ────────────────────
                if st == "comparison" and not slide.get("left_content"):
                    items = slide.get("content", [])
                    mid   = max(len(items) // 2, 1)
                    slide["left_content"]  = items[:mid]
                    slide["right_content"] = items[mid:]
                    slide["content"]       = []
                if st == "comparison" and not slide.get("left_title"):
                    slide["left_title"]  = "Traditional"
                    slide["right_title"] = "Modern"

                slide["auto_template"] = self._map_slide_type(st)

            data["slides"] = slides
            return data

        except Exception as e:
            raise Exception(f"Content generation failed: {str(e)}")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _parse_stats(self, items):
        result = []
        for item in items[:4]:
            for sep in [" — ", " - ", ": ", " – "]:
                if sep in item:
                    parts = item.split(sep, 1)
                    result.append({"number": parts[0].strip(), "context": parts[1].strip()})
                    break
            else:
                words = item.split()
                result.append({
                    "number":  words[0] if words else "—",
                    "context": " ".join(words[1:]) if len(words) > 1 else item,
                })
        return result

    def _map_slide_type(self, st):
        mapping = {
            "title":              SlideType.TITLE.value,
            "single_content":     SlideType.SINGLE_CONTENT.value,
            "two_column":         SlideType.TWO_COLUMN.value,
            "three_column":       SlideType.THREE_COLUMN.value,
            "comparison":         SlideType.COMPARISON.value,
            "process_steps":      SlideType.PROCESS_STEPS.value,
            "timeline":           SlideType.TIMELINE.value,
            "statistics_big_num": SlideType.STATISTICS_BIG_NUM.value,
            "quote_testimonial":  SlideType.QUOTE_TESTIMONIAL.value,
            "icon_grid":          SlideType.ICON_GRID.value,
            "chart_data":         SlideType.CHART_DATA.value,
            "team_people":        SlideType.TEAM_PEOPLE.value,
            "end_contact":        SlideType.END_CONTACT.value,
            "section_header":     SlideType.SECTION_HEADER.value,
        }
        return mapping.get(st.lower(), SlideType.SINGLE_CONTENT.value)

    def _clean_json(self, text):
        for fence in ("```json", "```"):
            if text.startswith(fence):
                text = text[len(fence):]
        if text.endswith("```"):
            text = text[:-3]
        start = text.find("{")
        end   = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start:end+1]
        return text.strip()