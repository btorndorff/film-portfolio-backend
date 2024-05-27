import os

import cloudinary
import cloudinary.api
import cloudinary.uploader
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

app = Flask(__name__)

CORS(
    app, resources={r"/images": {"origins": "http://localhost:3000"}}
)  # Adjust origin to match your frontend's URL


def fetch_all_images_from_folder(folder, max_results=100):
    all_images = []
    next_cursor = None

    while True:
        resources = cloudinary.api.resources(
            type="upload",
            prefix=folder,
            max_results=max_results,
            next_cursor=next_cursor,
        )

        images = resources.get("resources", [])
        all_images.extend(images)

        next_cursor = resources.get("next_cursor")
        if not next_cursor:
            break

    return all_images


@app.route("/images", methods=["GET"])
def get_images():
    try:
        # Fetch all resources from the specified folder
        folder = "film-portfolio"
        all_images = fetch_all_images_from_folder(folder)

        # Extract relevant information
        image_info = [
            {
                "url": image["secure_url"],
                "width": image["width"],
                "height": image["height"],
                "public_id": image["public_id"],
            }
            for image in all_images
        ]

        return jsonify({"images": image_info})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
