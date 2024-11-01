from flask import Flask, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)

BLOG_FILE = 'blog_posts.json'


def get_blog_posts():
    """Load and return all blog posts from the JSON file."""
    with open(BLOG_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_data(blog_posts):
    """Save the blog posts data to the JSON file.

    Args:
        blog_posts (list): List of blog posts to save.
    """
    with open(BLOG_FILE, 'w', encoding='utf-8') as file:
        json.dump(blog_posts, file, indent=4)


def initialize_default_posts():
    """Initialize the JSON file with default blog posts if it doesn't exist."""
    if not os.path.exists(BLOG_FILE):
        blog_posts = [
            {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
            {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'}
        ]
        save_data(blog_posts)


def add_blog_post(author, title, content):
    """Add a new blog post and save it to the JSON file.

    Args:
        author (str): The author of the blog post.
        title (str): The title of the blog post.
        content (str): The content of the blog post.
    """
    blog_posts = get_blog_posts()
    new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1
    new_post = {'id': new_id, 'author': author, 'title': title, 'content': content}
    blog_posts.append(new_post)
    save_data(blog_posts)


@app.route('/')
def index():
    """Render the index page with all blog posts."""
    blog_posts = get_blog_posts()
    return render_template('index.html', blog_posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Display the add post form or handle form submission to add a post."""
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        add_blog_post(author, title, content)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Delete a blog post and redirect to the index.

    Args:
        post_id (int): The ID of the post to be deleted.
    """
    blog_posts = get_blog_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_data(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Display the update form for a specific post or handle form submission to update the post.

    Args:
        post_id (int): The ID of the post to be updated.
    """
    blog_posts = get_blog_posts()
    post = next((p for p in blog_posts if p['id'] == post_id), None)

    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']
        save_data(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


# Initialize default blog posts if needed
initialize_default_posts()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
