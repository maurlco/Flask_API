
### API Workflow (Draft)
Client => Flutter Ipad App
Backend => Flask API Server

1- Client send a portrait picture to Backend
2- Backend process image and classify face (rounded, squared,...)
3- Backend Generate Hair style
4- Backend concat Hair style + Portrait picture received
5- Backend send the resulting 3D model to client

_if client want to modify result_
1. Client send the previously received result + annotations (i.e, drawings) to Backend
2. Backend PROCESS result + annotations to add/remove hairs
3. Backend sent the resulting 3D model to client

### Current POC Workflow

1. Client send a dog jpeg to Backend
2. Backend process jpeg to classify dog breed
3. Backend generate an url based on this class (correspond to fake result of processing)
4. Backend send result url to client
4. Client use url to load an image (url contains class name)
5. Backend use the class name received, to provide the client a static mock result jpeg.
6. Client display the jpeg.

This POC just validate:
- We know how to receive an image
- We know how to use the received image to process smth (here, dog breed)
- We know how to send an image

### Next step POC
- Voir comment creer uuid en python (pour client call backend for update)

1. Backend Track model "smth" inference status in numerical values 
2. Client ask Backend status of model inference in %