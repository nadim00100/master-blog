from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


def load_posts():
    """
    Load blog posts from a JSON file.

    Returns:
        list: A list of blog post dictionaries.
    """
    if not os.path.exists('blog_posts.json'):
        return []

    with open('blog_posts.json', 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_posts(posts):
    """
    Save blog posts to a JSON file.

    Args:
        posts (list): A list of blog post dictionaries to be saved.
    """
    with open('blog_posts.json', 'w') as f:
        json.dump(posts, f, indent=4)


@app.route('/')
def index():
    """
    Display the index page with all blog posts.
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add a new blog post via form submission.
    GET: Show the add post form.
    POST: Save the new post and redirect to index.
    """
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        blog_posts = load_posts()
        new_id = blog_posts[-1]["id"] + 1 if blog_posts else 1

        new_post = {
            "id": new_id,
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
    """
    Delete a blog post by its ID.

    Args:
        post_id (int): The ID of the post to delete.
    """
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update a blog post by its ID.
    GET: Show the update form with current data.
    POST: Save updated data and redirect to index.

    Args:
        post_id (int): The ID of the post to update.
    """
    blog_posts = load_posts()
    post = next((p for p in blog_posts if p['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']

        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
