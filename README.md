# 3dmodel_human
human 3d model for body measures

### Work
- This repo contains code to create 3D model of a persons body based on input weight
- 3D model is created using Mayavi

### Steps
    - Install requirements.txt
    - Start server by running server_api python file
    - Using sample post call to get updated model for 3d body model
    - api/post endpoint will download updated 3d model object file based on weight provided

### Sample call
```
curl --header "Content-Type: application/json"   --request POST   --data '{"weight":"26"}'   http://localhost:5000/api/post
```
