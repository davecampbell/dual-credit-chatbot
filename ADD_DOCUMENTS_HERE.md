# 📁 Adding Documents to the Chatbot

## Quick Start

**Just copy any `.md` file to the `knowledge/` folder:**
```bash
cp your-document.md knowledge/
```

The chatbot automatically loads ALL `.md` files from the `knowledge/` folder.

## After Adding Files

Restart the Streamlit app:
```bash
streamlit run app.py
```

The sidebar will show all loaded files.

## Supported Format

- **File type:** Markdown (`.md`)
- **Encoding:** UTF-8
- **Size:** No strict limit, but keep individual files under 100KB for best performance

## Tips

✅ **DO:**
- Use clear, descriptive filenames
- Structure content with markdown headers
- Keep related info in separate files for easier updates

❌ **DON'T:**
- Don't use other file formats (PDF, DOCX, etc.) - convert to Markdown first
- Don't duplicate information across multiple files
- Don't add README.md from root (it won't be loaded)

## Example

If you have grant request information:
```bash
# Copy the file
cp ~/Documents/grant-templates.md knowledge/

# Restart the app
streamlit run app.py

# Ask the chatbot: "What are the grant requirements?"
```
