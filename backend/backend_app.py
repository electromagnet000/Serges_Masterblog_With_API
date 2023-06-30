from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


def generate_id(data):
    return len(data) + 1


@app.route('/api/posts', methods=['POST'])
def add_posts():
    # creates new id

    title = request.json.get("title")
    content = request.json.get("content")
    new_id = generate_id(POSTS)

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    new_post = {
        "id": int(new_id),
        "title": title,
        "content": content
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201


# deletes a chosen post
@app.route('/api/posts/<int:post_id>', methods=["DELETE"])
def delete_post(post_id):
    # gets the post that needs to be deleted by checking the post id on all available posts
    check_posts = [post for post in POSTS if post["id"] == post_id]

    # if no post is found matching the id it then returns an error
    if not check_posts:
        return jsonify({"error": "page not found"}), 404

    success = {"message": f"Post with id {post_id} has been deleted successfully."}

    # removes the chosen post from POSTS
    POSTS.remove(check_posts[0])
    return jsonify(success), 200


# updates a chosen posts information
@app.route('/api/posts/<int:post_id>', methods=["PUT"])
def update(post_id):
    # gets the correct post matching the post_id
    chosen_post = [post for post in POSTS if post["id"] == post_id]

    # checks the post validation
    if not chosen_post:
        return jsonify({"error": "page not found"}), 404

    #We want to assign new values to the old values so we create a variable
    new_title = request.json.get("title", chosen_post[0]["title"])
    new_content = request.json.get("content", chosen_post[0]["content"])
    update_post = {"id": post_id, "title": new_title, "content": new_content}

    return jsonify(update_post), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
    print()
