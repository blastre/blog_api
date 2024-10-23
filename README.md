# Blog API

A simple RESTful API for managing blog posts, built with FastAPI in Python. This API supports basic CRUD operations for blog posts and includes user authentication using JWT (JSON Web Tokens).

## Features

- User Registration
- User Login with JWT authentication
- Create, Read, Update, and Delete blog posts
- Add comments to blog posts
- Like blog posts

## Technologies Used

- **FastAPI**: For building the API
- **SQLAlchemy**: For database management
- **SQLite**: For local development (can be switched to a cloud database)
- **python-jose**: For handling JWT tokens
- **Passlib**: For password hashing

## API Endpoints

### Authentication

- `POST /register`: Register a new user
- `POST /token`: Log in and receive a JWT token

### Blog Posts

- `POST /blogs`: Create a new blog post
- `GET /blogs`: Retrieve a list of blog posts
- `GET /blogs/{id}`: Retrieve a single blog post by its ID
- `PUT /blogs/{id}`: Update an existing blog post
- `DELETE /blogs/{id}`: Delete a blog post

### Comments

- `POST /blogs/{id}/comments`: Add a comment on a blog post

### Likes

- `PUT /blogs/{id}/like`: Add a like to a blog post

## Installation

1. Clone the repository:
   - `git clone https://github.com/YOUR_GITHUB_USERNAME/blog_api.git`
   - `cd blog_api`

2. Create a virtual environment:
   - For Windows: `python -m venv venv`
   - For macOS/Linux: `python3 -m venv venv`

3. Activate the virtual environment:
   - For Windows: `.\\venv\\Scripts\\activate`
   - For macOS/Linux: `source venv/bin/activate`

4. Install the required packages: `pip install -r requirements.txt`

## Running the API

To start the FastAPI application, run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

You can access the API at `http://localhost:8000`.

## Deployment

This API can be deployed on platforms like [Render](https://render.com) or [Vercel](https://vercel.com).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
