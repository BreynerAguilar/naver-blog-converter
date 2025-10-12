# CLAUDE.md

This file provides guidance to Claude Code when working with the Naver Blog Converter project.

## Project Overview

**naver-blog** is a markdown-to-HTML conversion tool specifically designed to transform Obsidian vault markdown files into Naver blog-compatible format.

### Purpose

Naver Blog does not natively support markdown. This tool solves the compatibility issues by:
1. Converting mermaid diagrams to PNG images
2. Transforming tables to HTML
3. Stripping YAML frontmatter
4. Converting WikiLinks to plain text
5. Generating clean HTML that works with Naver's SmartEditor

### Key Constraints

**Naver Blog Limitations:**
- No native markdown support (uses SmartEditor ONE)
- No JavaScript execution (`<script>` tags blocked)
- No iframe/embed support
- Mermaid diagrams require image conversion
- Code syntax highlighting limited (requires Color Scripter)
- HTML editing not officially supported (requires DevTools workaround)

## Project Structure

```
/Users/julius/Documents/naver_blog/
├── md2naver.py          # Main conversion script
├── pyproject.toml       # uv project configuration
├── CLAUDE.md            # This file
├── README.md            # User documentation
└── .gitignore          # Git ignore patterns
```

### Output Structure (Generated)

When users run the converter, it creates:
```
naver_output_TIMESTAMP/
├── output.html          # Naver-ready HTML
├── INSTRUCTIONS.md      # Manual steps guide
├── images/              # Mermaid diagrams as PNG
│   ├── mermaid_1.png
│   └── mermaid_2.png
└── mermaid_code.txt     # Backup of mermaid source
```

## Technology Stack

**Runtime:** Python 3.11+, managed with `uv`

**Dependencies:**
- `markdown` - Markdown to HTML conversion
- `beautifulsoup4` - HTML parsing and cleaning

**Optional External Tool:**
- `mmdc` (mermaid-cli) - For automatic mermaid diagram rendering
- If not installed, users can manually render using Mermaid Live Editor

## Usage Patterns

### Command Line
```bash
# Standard usage
uv run md2naver input.md

# Custom output directory
uv run md2naver input.md -o my_output

# After installation
uv run md2naver
```

### From Obsidian Vault (via slash command)
Users can create a slash command in their vault:
```bash
/naver <filename>
```

## Conversion Pipeline

The `md2naver.py` script processes files in this order:

1. **Strip Frontmatter** - Remove YAML between `---` markers
2. **Extract Mermaid** - Find ```mermaid blocks, save code, replace with placeholders
3. **Convert WikiLinks** - Transform `[[link]]` → `link`
4. **Extract Code Blocks** - Identify for Color Scripter reference
5. **Markdown → HTML** - Use `markdown` library with table/fenced_code extensions
6. **Clean HTML** - Remove prohibited tags (script, iframe, embed)
7. **Render Mermaid** - Generate PNG files (if mmdc available)
8. **Generate Instructions** - Create step-by-step upload guide

## Common User Workflows

### Workflow 1: Simple Markdown (No Diagrams)
```
User writes markdown → Run converter → Get HTML → Paste to Naver
```

### Workflow 2: With Mermaid Diagrams
```
User writes markdown with mermaid
↓
Run converter
↓
Get HTML + PNG images + Instructions
↓
Upload PNGs to Naver
↓
Replace MERMAID_IMAGE_N placeholders with CDN URLs
↓
Paste HTML via DevTools
```

### Workflow 3: With Code Highlighting
```
User writes markdown with code blocks
↓
Run converter
↓
Get HTML + Instructions
↓
Copy code from INSTRUCTIONS.md
↓
Use Color Scripter (https://colorscripter.com/)
↓
Replace <!-- CODE_BLOCK_N --> markers
↓
Paste HTML to Naver
```

## Development Guidelines

### When Modifying the Converter

**Always Preserve:**
- Bilingual content (Korean/English) - do not translate
- Original markdown structure
- User's writing voice and style

**Key Conversion Rules:**
- Strip frontmatter completely (Naver doesn't use it)
- Convert mermaid to images (no exceptions - Naver can't render)
- Keep tables as HTML tables (markdown tables don't work)
- Preserve code blocks but mark for optional Color Scripter enhancement
- WikiLinks become plain text (no internal linking in blog)

### Testing Changes

Always test with these file types from the Obsidian vault:
1. **Simple markdown** - Headers, lists, bold/italic
2. **With mermaid** - `글감/1011 산일전기와 전력 시장 공급망 분석.md`
3. **With code blocks** - `글감/1011 클로드 자동화 치트키 10개.md`
4. **With tables** - Files in `글감/` containing pipe tables

### Error Handling

**Common Issues:**
- `mmdc not found` - Not an error, just means manual mermaid rendering needed
- `FileNotFoundError` - User provided wrong path
- `UnicodeDecodeError` - File encoding issue (should handle UTF-8)

### Code Style

- Use type hints for function parameters
- Keep functions focused and single-purpose
- Print progress updates for long operations
- Generate helpful instructions for manual steps
- Fail gracefully when optional tools (mmdc) unavailable

## Integration with User's Obsidian Vault

The user's vault is located at:
```
/Users/julius/Documents/Obsidian Vault/base/
```

**Target Content:**
- `글감/` (Writing Ideas) - Personal articles and blog posts
- Contains bilingual Korean/English content
- Heavy use of mermaid diagrams (mindmap, pie, gantt, flow)
- Technical and business analysis content

**Slash Command Integration:**
The user wants a `/naver` command in their vault that:
1. Takes a filename from `글감/` folder
2. Runs this converter
3. Outputs to a convenient location
4. Provides next-step instructions

## Important Notes

### DO NOT:
- Translate Korean to English or vice versa (preserve original language)
- Skip mermaid conversion (diagrams won't render in Naver)
- Generate complex nested HTML (Naver may strip it)
- Use `<script>`, `<iframe>`, `<embed>` tags (always blocked)
- Modify user's original markdown files

### ALWAYS:
- Test with actual files from user's `글감/` folder
- Preserve bilingual content exactly as written
- Generate clear instructions for manual steps
- Handle missing mmdc gracefully
- Keep HTML simple and Naver-compatible
- Output helpful error messages

## Dependencies and Installation

### Required
```bash
uv sync
```
Installs: markdown, beautifulsoup4

### Optional
```bash
# For automatic mermaid rendering
npm install -g @mermaid-js/mermaid-cli
```

Without mmdc:
- Users can manually render at https://mermaid.live/
- Converter still works, just skips automatic PNG generation
- Instructions file will note this

## Future Enhancements

**Potential Features:**
- Direct upload to Naver blog via API (if available)
- Batch conversion of multiple files
- Custom mermaid themes
- Automatic Color Scripter integration (if API exists)
- Preview mode before conversion
- Template support for consistent styling

**Not Planned:**
- Real-time sync (Naver doesn't support)
- WYSIWYG editor (defeats purpose)
- Automatic translation (preserve user's language)

## Troubleshooting

### "Module not found: markdown"
```bash
cd /Users/julius/Documents/naver_blog
uv sync
```

### "mmdc command not found"
Not critical - mermaid diagrams can be rendered manually.
Instructions file will guide user to https://mermaid.live/

### "HTML looks broken in Naver"
- Check if user edited in WYSIWYG mode (corrupts HTML)
- Verify all image URLs are replaced (no MERMAID_IMAGE_N placeholders)
- Ensure DevTools method was used (not direct paste)

### "Code has no syntax highlighting"
- Expected behavior - Naver doesn't support it natively
- User needs to use Color Scripter (see INSTRUCTIONS.md)
- Or accept plain code formatting

## Contact and Support

This is a personal tool for the user's Obsidian vault.
For issues, check:
1. README.md for usage instructions
2. Generated INSTRUCTIONS.md for manual steps
3. Original markdown file for source of truth

---

**Remember:** This tool bridges the gap between Obsidian's rich markdown (with mermaid) and Naver blog's limited HTML support. The goal is maximum automation while providing clear guidance for necessary manual steps.
