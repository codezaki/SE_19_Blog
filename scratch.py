from index import db, Post

posts = Post.query.all()
for post in posts:
    print(post.id)