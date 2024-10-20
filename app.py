from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

BLOG_FILE = 'blog_posts.json'

def get_blog_posts():
    """Load and return all blog posts from the JSON file."""
    with open(BLOG_FILE, 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    """Render the index page with all blog posts."""
    blog_posts = get_blog_posts()  # Get posts from your JSON file
    return render_template('index.html', blog_posts=blog_posts)

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
    with open(BLOG_FILE, 'w') as file:
        json.dump(blog_posts, file, indent=4)


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
    with open(BLOG_FILE, 'w') as file:
        json.dump(blog_posts, file, indent=4)
    return redirect(url_for('index'))


def save_blog_posts(blog_posts):
    """Save the updated blog posts to the JSON file."""
    with open('posts.json', 'w') as f:
        json.dump(blog_posts, f, indent=4)


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Display the update form for a specific post or handle form submission to update the post.

    Args:
        post_id (int): The ID of the post to be updated.
    """
    blog_posts = get_blog_posts()  # Fetch the list of blog posts
    post = next((p for p in blog_posts if p['id'] == post_id), None)

    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        print(request.form)  # Debugging: print all the form data
        print("Title:", request.form.get('title'))
        print("Author:", request.form.get('author'))
        print("Content:", request.form.get('content'))

        # Check if the expected keys are in the form data
        if 'title' not in request.form or 'author' not in request.form or 'content' not in request.form:
            return "Form data is incomplete", 400

        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']
        save_blog_posts(blog_posts)  # Save the updated blog posts back to the file
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


# Initialize blog posts if the JSON file doesn't exist
try:
    get_blog_posts()
except FileNotFoundError:
    # Blog post data
    blog_posts = [
        {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
        {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'}
    ]

    # Save the blog posts to a JSON file
    with open(BLOG_FILE, 'w') as file:
        json.dump(blog_posts, file, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
