from flask import Flask, render_template, g, redirect, request

app = Flask(__name__)

@app.before_request
def load_toc():
    with open("book_viewer/data/toc.txt", "r") as file:
        g.toc = file.readlines()

@app.template_filter('in_paragraphs')
def in_paragraphs(text):
    if not text:
        return ''

    paragraphs = text.split('\n\n')
    
    formatted_paragraphs = ''
    for idx, paragraph in enumerate(paragraphs):
        formatted_paragraphs += f'<p id={idx}>{paragraph}</p>'

    return formatted_paragraphs

@app.template_filter('bold_findings')
def bold_findings(text, query):
    text = text.replace(query, f'<strong>{query}</strong>')
    return text


@app.route("/")
def index():
    return render_template('home.html', toc=g.toc)

@app.route("/chapters/<page_num>")
def chapters(page_num):
    if not page_num.isdigit() or 1 > int(page_num) or int(page_num) > len(g.toc):
        return redirect("/")

    with open(f"book_viewer/data/chp{page_num}.txt", "r") as file:
        chapter = file.read()
    
    chapter_title = g.toc[int(page_num) - 1] 

    return render_template('chapter.html', 
                            toc=g.toc,
                            chapter=chapter,
                            chapter_num=page_num,
                            chapter_title=chapter_title)

@app.route("/search")
def search():
    query = request.args.get('query', '')
    chapter_nums, paragraphs = [], []
    if query:
        chapter_nums, paragraphs = find_in_chapters(query) 
    
    print('In search:')
    print(chapter_nums)
    print(paragraphs)
    return render_template('search.html',
                            toc=g.toc,
                            query=query,
                            chapter_nums=chapter_nums,
                            paragraphs=paragraphs)

def find_in_chapters(query):
    chapter_nums = []
    paragraphs = []
    
    for chapter_num in range(1, len(g.toc) + 1):
    # for chapter_num in range(1, 2):
        with open(f"book_viewer/data/chp{chapter_num}.txt", "r") as file:
            chapter = file.read()

        if query in chapter:
            chapter_nums.append(chapter_num)
            paragraphs.append(find_paragraphs(chapter, query))

    print('In find_in_chapters:')
    print(chapter_nums)
    print(paragraphs)

    return chapter_nums, paragraphs

def find_paragraphs(chapter, query):
    formatted_paragraphs = in_paragraphs(chapter)
    paragraphs = formatted_paragraphs.split('<p id=')
    result = []

    for paragraph in paragraphs:
        if query in paragraph:
            p_id = paragraph[: paragraph.index('>')]
            paragraph = paragraph[paragraph.index('>') + 1: paragraph.index('<')]
            result.append({'id': p_id, 'paragraph': paragraph})

    print('In find_paragraphs:')
    print(result)
    return result
    
@app.errorhandler(404)
def page_not_found(error):
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5003)
    