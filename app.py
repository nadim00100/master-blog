from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_posts():
    with open('blog_posts.json', 'r') as f:
        return json.load(f)

def save_posts(posts):
    with open('blog_posts.json', 'w') as f:
        json.dump(posts, f, indent=4)

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        blog_posts = load_posts()

        new_post = {
            "id": blog_posts[-1]["id"] + 1 if blog_posts else 1,
            "title": title,
            "author": author,
            "content": content
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_posts()
    # Filter out the post with matching id
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_posts()
    post = next((p for p in blog_posts if p['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Get updated data from the form
        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']

        save_posts(blog_posts)
        return redirect(url_for('index'))

    # GET request — render form with current post data
    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
