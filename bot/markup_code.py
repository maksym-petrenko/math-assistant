import html


def generate_code(code: str, language: str | None) -> str:
    escaped_code = html.escape(code)
    if language is None:
        return f'<pre>{escaped_code}</pre>'
    return f'<pre><code class="language-{language}">{escaped_code}</code></pre>'
