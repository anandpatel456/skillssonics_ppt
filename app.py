"""
SkillSonics PPT Agent
Pure Streamlit native components — enhanced with beautiful native styling.
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from content_generator import ContentGenerator
from ppt_builder import PPTBuilder
from config import TRAINING_DOMAINS, ORG_INFO, BRAND_COLORS

st.set_page_config(
    page_title="SkillSonics — PPT Generator",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="auto"
)

# ── API key ───────────────────────────────────────────────────────────────────
API_KEY = os.getenv("GROQ_API_KEY", "")
if not API_KEY:
    st.error("⚠️ GROQ_API_KEY not found in .env file. Please add it and restart.")
    st.stop()

# ── Session state ─────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None

# ══════════════════════════════════════════════════════════
# BEAUTIFUL HEADER
# ══════════════════════════════════════════════════════════
st.markdown("""
# 🎓 **SkillSonics PPT Generator**

### *AI-powered presentation builder for vocational training excellence*
""")

# Add a beautiful separator with emoji
st.markdown("---")
st.markdown("✨ Create professional training presentations in seconds with AI ✨")
st.markdown("---")

# ══════════════════════════════════════════════════════════
# BEAUTIFUL INPUT FORM
# ══════════════════════════════════════════════════════════
st.markdown("## 📋 **Configure Your Presentation**")
st.markdown("*Fill in the details below to create your professional training presentation*")

# Add some spacing
st.markdown("")

# Enhanced topic input with better styling
st.markdown("### 🎯 **Training Topic**")
topic = st.text_input(
    label="Enter the main subject of your training presentation *",
    placeholder="e.g. Robotics in Automotive, EV Battery Systems, CNC Machine Operation",
    help="Be specific about the training topic for better AI-generated content",
)

# Two-column layout with better styling
st.markdown("### 👥 **Target Audience & Presentation Length**")
col1, col2 = st.columns(2)
with col1:
    audience = st.selectbox(
        label="**Who will be viewing this presentation?** *",
        options=[
            "🆕 New Trainees / Beginners",
            "🔧 Experienced Technicians", 
            "🏢 Corporate Teams",
            "🤝 Institutional Partners",
            "💼 Job Placement Officers",
            "🏛️ Government Officials",
        ],
        help="Select the primary audience for your training",
        index=None,
    )
with col2:
    num_slides = st.slider(
        label="**Number of Slides** (including title & closing)",
        min_value=5,
        max_value=15,
        value=8,
        step=1,
        help="Choose the length of your presentation",
    )

# Enhanced domain selection
st.markdown("### 🏭 **Training Domain (Optional)**")
domain = st.selectbox(
    label="Select an industry for more specific content",
    options=["— Not specified —"] + TRAINING_DOMAINS,
    help="This helps AI generate industry-specific examples and terminology",
)

# Beautiful separator
st.markdown("---")
st.markdown("### ✨ **What You'll Get**")
st.markdown("*Professional presentations with AI-powered content generation*")

# Beautiful features showcase with enhanced styling
st.markdown("")

# Create two beautiful columns for features
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### 📝 **Rich Content**
    - ✅ 5–7 detailed bullets per slide
    - 📊 Statistics slide with real data  
    - ⚖️ Traditional vs Modern comparison
    - 🔢 Step-by-step process diagram
    """)
with col2:
    st.markdown("""
    ### 🎨 **Professional Design**
    - 🖼️ Topic-relevant images on slides
    - 💰 Career outcomes & salary data
    - 🏷️ SkillSonics branded footer
    - 📥 Download-ready .pptx file
    """)

# Beautiful separator
st.markdown("---")

# Enhanced generate button with better styling
st.markdown("### 🚀 **Ready to Create Your Presentation?**")
st.markdown("*Click the button below to generate your professional training presentation*")

generate = st.button(
    "⚡ **Generate Presentation**",
    type="primary",
    use_container_width=True,
)

# Add some helpful tips
st.markdown("---")
st.markdown("💡 **Tip**: Be specific with your topic and select the right audience for better results!")

# ══════════════════════════════════════════════════════════
# GENERATION
# ══════════════════════════════════════════════════════════
if generate:
    if not topic.strip():
        st.error("❌ Please enter a Training Topic.")
        st.stop()

    st.session_state.result = None
    selected_domain = None if domain == "— Not specified —" else domain

    st.divider()
    st.subheader("⏳ Generating your presentation…")

    progress = st.progress(0, text="Starting…")

    try:
        progress.progress(10, text="🤖 AI is writing slide content…")
        gen = ContentGenerator(API_KEY)
        content_data = gen.generate_ppt_content(
            topic      = topic.strip(),
            audience   = audience,
            num_slides = num_slides,
            domain     = selected_domain,
            tone       = "professional",
            style      = "Training",
        )

        progress.progress(50, text="🖼️ Fetching images & building slides…")
        builder = PPTBuilder()
        builder.build_presentation(content_data)

        progress.progress(85, text="💾 Saving file…")
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe     = "".join(c if c.isalnum() else "_" for c in topic.strip()[:30])
        filepath = builder.save(f"{safe}_{ts}.pptx")

        progress.progress(100, text="✅ Done!")
        st.session_state.result = (filepath, content_data, topic.strip())
        st.rerun()

    except Exception as e:
        progress.empty()
        st.error(f"❌ Generation failed: {e}")
        with st.expander("Error details"):
            st.exception(e)

# ══════════════════════════════════════════════════════════
# BEAUTIFUL RESULTS
# ══════════════════════════════════════════════════════════
if st.session_state.result:
    filepath, content_data, orig_topic = st.session_state.result
    slides   = content_data.get("slides", [])
    n_slides = len(slides)

    # Beautiful success celebration
    st.markdown("---")
    st.markdown("""
    # 🎉 **Presentation Successfully Created!**
    
    ### *Your professional training presentation is ready for download*
    """)
    
    # Enhanced metrics with beautiful styling
    st.markdown("## 📊 **Presentation Summary**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Topic", orig_topic[:25] + ("…" if len(orig_topic) > 25 else ""))
    with col2:
        st.metric("📑 Slides", n_slides)
    with col3:
        st.metric("✅ Status", "Ready")

    # Beautiful success message
    st.success(f"🎯 **Excellent!** Your presentation contains {n_slides} professional slides with images, diagrams & SkillSonics branding.")

    # Enhanced download section
    st.markdown("---")
    st.markdown("## 📥 **Download Your Presentation**")
    st.markdown("*Click below to download your PowerPoint file*")
    
    try:
        with open(filepath, "rb") as f:
            st.download_button(
                label               = "📥 **Download PowerPoint (.pptx)**",
                data                = f.read(),
                file_name           = os.path.basename(filepath),
                mime                = "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width = True,
                type                = "primary",
            )
    except FileNotFoundError:
        st.error("❌ File not found — please regenerate.")

    # Beautiful slide preview section
    st.markdown("---")
    st.markdown(f"## 📑 **Slide Outline ({n_slides} slides)**")
    st.markdown("*Preview your presentation - expand any slide to see detailed content*")

    TEMPLATE_LABELS = {
        "title":              "🏠 Title",
        "single_content":     "📝 Content",
        "statistics_big_num": "📊 Statistics",
        "process_steps":      "🔢 Process",
        "comparison":         "⚖️ Comparison",
        "two_column":         "📰 Two Column",
        "three_column":       "📰 Three Column",
        "end_contact":        "📞 Contact",
        "section_header":     "📌 Section",
        "quote_testimonial":  "💬 Quote",
        "icon_grid":          "🔷 Grid",
    }

    for i, slide in enumerate(slides, 1):
        tmpl  = slide.get("auto_template", "single_content")
        title = slide.get("title", f"Slide {i}")
        label = TEMPLATE_LABELS.get(tmpl, "📄 Slide")

        with st.expander(f"**Slide {i}** · {label} · {title}"):

            # Statistics slide with enhanced styling
            if slide.get("statistics"):
                st.markdown("### 📊 **Key Statistics**")
                for s in slide["statistics"]:
                    num = s.get("number", "")
                    ctx = s.get("context", "")
                    st.markdown(f"- **{num}** — {ctx}")

            # Comparison slide with enhanced layout
            elif slide.get("left_content") or slide.get("right_content"):
                lc = slide.get("left_content", [])
                rc = slide.get("right_content", [])
                lt = slide.get("left_title",  "Traditional")
                rt = slide.get("right_title", "Modern")
                
                st.markdown(f"### ⚖️ **{lt} vs {rt}**")
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"#### {lt}")
                    for pt in lc[:6]:
                        st.markdown(f"- {pt}")
                with c2:
                    st.markdown(f"#### {rt}")
                    for pt in rc[:6]:
                        st.markdown(f"- {pt}")

            # Normal content with enhanced styling
            else:
                pts = slide.get("content", [])
                if slide.get("subtitle"):
                    st.markdown(f"### {slide['subtitle']}")
                if pts:
                    for pt in pts[:7]:
                        st.markdown(f"- {pt}")
                elif not slide.get("subtitle"):
                    st.caption("📞 Closing / contact slide")

    # Beautiful regenerate option
    st.markdown("---")
    st.markdown("### 🔄 **Create Another Presentation?**")
    st.markdown("*Ready to create more professional training content?*")
    
    if st.button("🔄 **Generate Another Presentation**", use_container_width=True):
        st.session_state.result = None
        st.rerun()