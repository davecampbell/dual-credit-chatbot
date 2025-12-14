import streamlit as st
import anthropic
import os

# ============================================================================
# CONFIGURATION - Edit these to customize the chatbot
# ============================================================================

# Page settings
PAGE_TITLE = "WHSAA Sophomore Scholars Program Q&A"
PAGE_ICON = "🎓"

# Header text
MAIN_TITLE = "🎓 WHSAA Sophomore Scholars Program Q&A"
MAIN_SUBTITLE = "Ask questions about the Sophomore Scholars Program and Kentucky's Dual Credit program."
# Chat settings
CHAT_INPUT_PLACEHOLDER = "Ask a question about the Sophomore Scholars Program..."

# System prompt - describes the chatbot's role and behavior
SYSTEM_PROMPT_INTRO = """You are a helpful assistant answering questions about the Waggener High School Alumni Association (WHSAA) Sophomore Scholars Program and Kentucky's Dual Credit program.

IMPORTANT: Only use information from the following documents to answer questions. If the answer is not in the documents, say "I don't have that information in the provided documents."

Instructions:
- Be concise and helpful
- Cite specific sections or data points from the documents when relevant
- If asked about something not in the documents, politely say you don't have that information
- Focus on factual information from the documents
- When information comes from a specific source file, mention it"""

# Sidebar content
SIDEBAR_ABOUT_TITLE = "### About"
SIDEBAR_ABOUT_TEXT = "This chatbot answers questions about WHSAA Sophomore Scholars Program and Kentucky's Dual Credit program."

SIDEBAR_EXAMPLES_TITLE = "### Example Questions"
SIDEBAR_EXAMPLES = """
- What is the Sophomore Scholars Program?
- Why were sophomores chosen?
- What is dual credit?
- How much does dual credit cost?
"""

# Model configuration - set via environment variable
# Run test_models.py to find which model works with your API key
DEFAULT_MODEL = "claude-sonnet-4-20250514"  # Latest Claude 4 Sonnet (Dec 2025)
MODEL = os.environ.get("CLAUDE_MODEL", DEFAULT_MODEL)

# ============================================================================
# END CONFIGURATION
# ============================================================================

# Page config (uses settings from above)
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="centered"
)

# Load all knowledge base documents
@st.cache_data
def load_documents():
    """Load all markdown and PDF files from the knowledge folder."""
    import glob
    from pypdf import PdfReader

    # Get all markdown and PDF files from the knowledge folder
    md_files = glob.glob('knowledge/*.md')
    pdf_files = glob.glob('knowledge/*.pdf')
    all_files = sorted(md_files + pdf_files)

    if not all_files:
        st.error("⚠️ No knowledge base files found in the 'knowledge/' folder!")
        st.info("Add .md or .pdf files to the 'knowledge/' folder and restart the app.")
        return ""

    combined_content = []

    for file_path in all_files:
        try:
            filename = file_path.replace('knowledge/', '')

            # Add a header to separate documents
            combined_content.append(f"\n\n{'='*80}\n")
            combined_content.append(f"SOURCE: {filename}\n")
            combined_content.append(f"{'='*80}\n\n")

            # Read based on file type
            if file_path.endswith('.pdf'):
                # Extract text from PDF
                reader = PdfReader(file_path)
                pdf_text = []
                for page_num, page in enumerate(reader.pages, 1):
                    text = page.extract_text()
                    if text.strip():
                        pdf_text.append(f"[Page {page_num}]\n{text}")

                content = '\n\n'.join(pdf_text)
                if not content.strip():
                    content = "[PDF file contains no extractable text]"

            else:  # .md file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

            combined_content.append(content)

        except Exception as e:
            st.warning(f"Could not load {file_path}: {e}")

    return '\n'.join(combined_content)

# Header
st.title(MAIN_TITLE)
st.markdown(MAIN_SUBTITLE)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get document content
doc_content = load_documents()

# Chat input
if prompt := st.chat_input(CHAT_INPUT_PLACEHOLDER):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        try:
            # Get API key from environment
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                st.error("⚠️ API key not configured. Please add ANTHROPIC_API_KEY to your secrets.")
                st.stop()

            client = anthropic.Anthropic(api_key=api_key)

            # Create system prompt with document content
            system_prompt = f"""{SYSTEM_PROMPT_INTRO}

DOCUMENTS:
{doc_content}"""

            # Show spinner while generating
            with st.spinner("Thinking..."):
                # Create messages for API (exclude system prompt from messages)
                api_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                # Call Claude API
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=2048,
                    system=system_prompt,
                    messages=api_messages
                )

            # Extract answer
            answer = response.content[0].text

            # Display answer
            st.markdown(answer)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please make sure your ANTHROPIC_API_KEY is set correctly in the Streamlit secrets.")

# Sidebar with info
with st.sidebar:
    st.markdown(SIDEBAR_ABOUT_TITLE)
    st.markdown(SIDEBAR_ABOUT_TEXT)

    # Show loaded files
    import glob
    md_files = glob.glob('knowledge/*.md')
    pdf_files = glob.glob('knowledge/*.pdf')
    all_files = sorted(md_files + pdf_files)

    if all_files:
        st.markdown("#### 📚 Knowledge Base:")
        for f in all_files:
            filename = f.replace('knowledge/', '')
            icon = "📄" if f.endswith('.pdf') else "📝"
            st.markdown(f"- {icon} {filename}")
    else:
        st.warning("No files in knowledge/ folder")

    st.markdown(SIDEBAR_EXAMPLES_TITLE)
    st.markdown(SIDEBAR_EXAMPLES)

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("*Powered by Claude AI*")
