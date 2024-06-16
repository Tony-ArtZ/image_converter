# Image Converter API

A robust and efficient image conversion API built with FastAPI. This API allows users to upload images, convert them to various supported formats, and download the converted files. 

## Features

- **Image Upload**: Upload images for conversion.
- **Format Conversion**: Convert images to various supported formats.
- **Status Check**: Check the status of image conversion tasks.
- **Download Converted Images**: Download the converted images.
- **Automatic Cleanup**: Periodic cleanup of old files to save space.

## Tech Stack

- **FastAPI**: The web framework for building the API.
- **Uvicorn**: ASGI server for running the FastAPI application.
- **APScheduler**: For scheduling periodic tasks.
- **CORS Middleware**: To handle Cross-Origin Resource Sharing.
- **Background Tasks**: To handle image conversion asynchronously.
- **Static Files**: Serving static files and the main interface.

## Getting Started

1. Clone the repository.
2. Install the dependencies.
3. Run the server.

## Running the Server

```sh
uvicorn main:app --host 0.0.0.0 --port 5000
```

This will start the server, and you can interact with the API at `http://localhost:5000`.

## Directory Structure

- `constants.py`: Contains constant values used across the application.
- `converter.py`: Handles image conversion logic.
- `cleaner.py`: Contains functions for cleaning up old files.
- `static/`: Directory for static files like the main HTML interface.

## Contributions

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

---

Enjoy converting your images seamlessly with our API!
