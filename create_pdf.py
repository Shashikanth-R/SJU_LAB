"""
Simple Markdown to HTML converter - No external dependencies
"""
import re
import os

def simple_md_to_html(md_text):
    """Convert markdown to HTML without external libraries"""
    html = md_text
    
    # Escape HTML
    # html = html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # Italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Code blocks
    html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # Horizontal rules
    html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)
    
    # Tables
    lines = html.split('\n')
    in_table = False
    new_lines = []
    
    for i, line in enumerate(lines):
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                new_lines.append('<table>')
            
            # Skip separator line
            if re.match(r'^\|[\s\-:|]+\|$', line.strip()):
                continue
            
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            
            # Check if header (first row of table)
            if i + 1 < len(lines) and '---' in lines[i + 1]:
                row = '<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>'
            else:
                row = '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'
            new_lines.append(row)
        else:
            if in_table:
                new_lines.append('</table>')
                in_table = False
            new_lines.append(line)
    
    if in_table:
        new_lines.append('</table>')
    
    html = '\n'.join(new_lines)
    
    # Paragraphs (lines with content)
    html = re.sub(r'^(?!<[hptulod]|</?t|<hr|<pre|<code)(.+)$', r'<p>\1</p>', html, flags=re.MULTILINE)
    
    # Clean up empty paragraphs
    html = re.sub(r'<p>\s*</p>', '', html)
    
    return html

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 850px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #ecf0f1; padding-bottom: 8px; margin-top: 30px; }}
        h3 {{ color: #7f8c8d; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-family: Consolas, monospace; }}
        pre {{ background-color: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 8px; overflow-x: auto; }}
        pre code {{ background-color: transparent; color: inherit; }}
        hr {{ border: none; border-top: 2px solid #ecf0f1; margin: 30px 0; }}
        p {{ margin: 10px 0; }}
        @media print {{ body {{ margin: 0; padding: 20px; }} pre {{ white-space: pre-wrap; }} }}
    </style>
</head>
<body>
{content}
</body>
</html>"""

def convert_file(md_path, html_path, title):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_content = simple_md_to_html(md_content)
    full_html = HTML_TEMPLATE.format(title=title, content=html_content)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ Created: {html_path}")

# Convert files
convert_file('PROJECT_REPORT.md', 'PROJECT_REPORT.html', 'Project Report')
convert_file('INSTALLATION_GUIDE.md', 'INSTALLATION_GUIDE.html', 'Installation Guide')

print("\n🎉 Done! HTML files created.")
print("\n📄 To create PDFs:")
print("   1. Double-click PROJECT_REPORT.html to open in browser")
print("   2. Press Ctrl+P → Save as PDF")
print("   3. Repeat for INSTALLATION_GUIDE.html")
