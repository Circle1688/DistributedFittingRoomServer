# API Document

## Account

### /register

**POST**

Call when an account is created.

#### Request body

```json
{
  "email": "string",
  "full_name": "string",
  "date_of_birth": 1731754271,
  "ethnicity": "string",
  "gender": "string"
}
```

#### Responses

```json
{
   "message": "string"
}
```



### /login

**POST**

Call when the user logs in.

Please save the token for authorization access.

#### Request body

```json
{
  "email": "string"
}
```

#### Responses

```json
{
   "token": "string"
}
```



### /get_user_info

**GET**

**Authorization**



#### Responses

```json
{
  "email": "string",
  "full_name": "string",
  "date_of_birth": 1731754271,
  "ethnicity": "string",
  "gender": "string"
}
```



### /update_user_info

**POST**

**Authorization**



#### Request body

```json
{
  "full_name": "string",
  "date_of_birth": 1731754271,
  "ethnicity": "string",
  "gender": "string"
}
```

#### Responses

```json
{
   "message": "string"
}
```



### /get_avatar

**GET**

**Authorization**



#### Responses

```json
{
    "avatar_url": "https://media.kungcorp.io/33/avatar/avatar_1738860389536.png",
    "avatar_thumbnail_url": "https://media.kungcorp.io/33/avatar/avatar_1738860389536_thumbnail.jpg"
}
```



### /upload_avatar

**POST**

**Authorization**



#### Request body

```json
Image file
```



#### Responses

```json
{
    "avatar_url": "https://media.kungcorp.io/33/avatar/avatar_1738860389536.png",
    "avatar_thumbnail_url": "https://media.kungcorp.io/33/avatar/avatar_1738860389536_thumbnail.jpg"
}
```



## User Detail

### /get_user_details

**GET**

**Authorization**



#### Responses

```json
{
  "face_shape": "string",
  "skin_tone": 0,
  "body_dimensions": "string",
  "real_world_measurements": "string",
  "hair_style": "string",
  "hair_color": "string"
}
```



### /update_user_details

**POST**

**Authorization**



#### Request body

```json
{
  "face_shape": "string",
  "skin_tone": 0,
  "body_dimensions": "string",
  "real_world_measurements": "string",
  "hair_style": "string",
  "hair_color": "string"
}
```



#### Responses

```json
{
   "message": "string"
}
```



## Generate

### /generate

**POST**

**Authorization**



#### Request body

```json
{
  	"user_details": {
          "face_shape": "long",
          "skin_tone": 2,
          "pose":"I-Pose",
          "real_world_measurements": {
                "Height": 180,
                "Thigh Length": 45.84773,
                "Calf Length": 46.71822,
                "Feet Length": 24.95818,
                "Neck Length": 11.30822,
                "Shoulder Width": 43.42514,
                "Upper Arm Length": 25.20014,
                "Forearm Length": 24.77694,
                "Hand Length": 18.56700,
                "Muscle": 0.25,
                "Body Fat": 0.20,
                "Neck Thickness": 32.21194,
                "Bust": 96.75247,
                "Cup": 15.09754,
                "Waist": 69.90949,
                "Belly": 80.75730,
                "Hips": 102.57145,
                "Thigh Size": 55.89947,
                "Calf Size": 36.81380,
                "Upper Arm Size": 25.16563,
                "Forearm Size": 22.76084,
                "Hand Size": 20.51066
          },
          "hairstyle": "30",
          "hair_color": "6B4F30FF",
          "camera_view": "front",
          "view_mode": 0,
          "expression": "Smile",
          "background_color_hex": "FFE4DBFF",
          "gender": "Female"
      },
      "apparel_details": {
          "brand": "gymshark",
          "item_id": "Hoodie",
          "color": "Red",
          "size": "L",
          "size2": "L"
      },
      "image_options":{
          "quality": 100,
          "thumbnail_width": 128
      },
      "task_options":{
          "vip": true,
          "limit": 5
      },
      "render_mode": "2D_Kling"
}
```



#### Responses

```json
{
   "task_id": "string"
}
```



### /generate_video

**POST**

**Authorization**



#### Request body

```json
{
  	"user_details": {
          "face_shape": "long",
          "skin_tone": 2,
          "pose":"I-Pose",
          "real_world_measurements": {
                "Height": 180,
                "Thigh Length": 45.84773,
                "Calf Length": 46.71822,
                "Feet Length": 24.95818,
                "Neck Length": 11.30822,
                "Shoulder Width": 43.42514,
                "Upper Arm Length": 25.20014,
                "Forearm Length": 24.77694,
                "Hand Length": 18.56700,
                "Muscle": 0.25,
                "Body Fat": 0.20,
                "Neck Thickness": 32.21194,
                "Bust": 96.75247,
                "Cup": 15.09754,
                "Waist": 69.90949,
                "Belly": 80.75730,
                "Hips": 102.57145,
                "Thigh Size": 55.89947,
                "Calf Size": 36.81380,
                "Upper Arm Size": 25.16563,
                "Forearm Size": 22.76084,
                "Hand Size": 20.51066
          },
          "hairstyle": "30",
          "hair_color": "6B4F30FF",
          "camera_view": "front",
          "view_mode": 0,
          "expression": "Smile",
          "background_color_hex": "FFE4DBFF",
          "gender": "Female"
      },
      "apparel_details": {
          "brand": "gymshark",
          "item_id": "Hoodie",
          "color": "Red",
          "size": "L",
          "size2": "L"
      },
      "video_options":{
          "video_live": false,
          "duration": 5,
          "negative_prompt": "",
          "prompt": "",
          "seed": 0
      },
      "task_options":{
          "vip": true,
          "limit": 5
      },
      "render_mode": "2D_Kling"
}
```



#### Responses

```json
{
   "task_id": "string"
}
```



### /upscale

**POST**

**Authorization**



#### Request body

```json
{
   "video_url": "string",
   "task_options":{
      "vip": true,
      "limit": 5
   }
}
```



#### Responses

```json
{
   "task_id": "string"
}
```



### /image_to_video

**POST**

**Authorization**



#### Request body

```json
{
  	  "image":"",
      "video_options":{
          "video_live": false,
          "duration": 5,
          "negative_prompt": "",
          "prompt": "",
          "seed": 0
      },
      "task_options":{
          "vip": true,
          "limit": 5
      }
}
```



#### Responses

```json
{
   "task_id": "string"
}
```





### /generate/{task_id}

**GET**

**Authorization**



#### Responses

```json
{
   "status": str,
   "type": "vip",
   "position": int
}
```



```python
status="PENDING"

status="STARTED"

status="SUCCESS"

status="FAILED"


# In process
position = 0

# There's one more task ahead
position = 1

# There are two more tasks ahead
position = 2

# There are n tasks ahead
position = n
```



## Gallery

### /get_gallery

**GET**

**Authorization**



/get_gallery?limit=10

/get_gallery?limit=10&cursor=1739678350



#### Responses

```json
{
    "gallery_urls": [
        {
            "source_url": "https://media.kungcorp.io/33/gallery/3aa38a43-631e-44f4-ae1a-de16d9843cad_upscale.mp4",
            "thumbnail_url": "https://media.kungcorp.io/33/gallery/3aa38a43-631e-44f4-ae1a-de16d9843cad_upscale_thumbnail.jpg",
            "last_modified": 1739678557
        },
        {
            "source_url": "https://media.kungcorp.io/33/gallery/fa398b2c-d6c4-4e81-b58e-8585b37cbebc.mp4",
            "thumbnail_url": "https://media.kungcorp.io/33/gallery/fa398b2c-d6c4-4e81-b58e-8585b37cbebc_thumbnail.jpg",
            "last_modified": 1739678440
        },
        {
            "source_url": "https://media.kungcorp.io/33/gallery/fa398b2c-d6c4-4e81-b58e-8585b37cbebc.jpg",
            "thumbnail_url": "https://media.kungcorp.io/33/gallery/fa398b2c-d6c4-4e81-b58e-8585b37cbebc_thumbnail.jpg",
            "last_modified": 1739678350
        }
    ],
    "pagination": {
        "limit": 10,
        "next_cursor": 1739678350,
        "has_next": true
    }
}
```



### /remove_gallery_file/{file_name}

**DELETE**

**Authorization**

 

#### Responses

```
{
   "message": "string"
}
```

 

## Task

### /get_tasks

**GET**

**Authorization**



#### Responses

```json
{
    "tasks": [
        {
            "taskid": "df812521-fb0f-4347-be72-f2d0771b1c2f",
            "status": "PENDING"
        },
        {
            "taskid": "2e6bf30f-6a0f-4e49-a674-70886b66f2b8",
            "status": "STARTED"
        }
    ]
}
```



## Clothes

### /upload_clothes

**POST**



#### Excel Example

| URL                   | Brand  | Gender | Name   | Render Mode | Colors         | Colors Hex              | Sizes       |
| --------------------- | ------ | ------ | ------ | ----------- | -------------- | ----------------------- | ----------- |
| https://example.com/1 | BrandA | Male   | Cloth1 | 2D_Kling    | Red,Blue,Green | #FF0000,#0000FF,#008000 | S,M,L       |
| https://example.com/2 | BrandB | Female | Cloth2 | 3D          | Black,White    | #000000,#FFFFFF         | XS,S,M,L,XL |
| https://example.com/3 | BrandC | Female | Cloth3 | 3D          | Yellow,Purple  | #FFFF00,#800080         | M,L,XL,XXL  |



#### Request body

```json
*.xls *.xlsx
```



#### Responses

```json
{
   "message": "string"
}
```



### /get_clothes

**POST**



#### Request body

```json
{
    "url":"https://example.com/1",
    "brand":"",
    "name":"cloth1"
}
```



#### Responses

```json
{
    "gender": "Male",
    "colors": [
        "Red",
        "Blue",
        "Green"
    ],
    "sizes": [
        "S",
        "M",
        "L"
    ],
    "name": "Cloth1",
    "render_mode": "3D",
    "brand": "BrandA",
    "colors_hex": [
        "#FF0000",
        "#0000FF",
        "#008000 "
    ]
}
```

