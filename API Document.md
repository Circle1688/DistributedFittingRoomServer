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



body_dimensions is a list, you need to add the key-value pairs.



#### Request body

```json
{
  	"user_details": {
      "face_shape": "long",
      "skin_tone": 2,
      "pose":"I-Pose",
      "body_dimensions": [
              {"key": "b_{main}_muscular", "value": 0.5},
              {"key": "b_{main}_overweight", "value": 0.5}
          ],
          "body_dimension_lengths": [
              {"key": "spine", "value": {"x":1.05, "y":1.05, "z":1.05}},
              {"key": "thigh_R", "value": {"x":1.0, "y":1.05, "z":1.0}},
              {"key": "thigh_L", "value": {"x":1.0, "y":1.05, "z":1.0}},
              {"key": "shin_R", "value": {"x":1.0, "y":1.05, "z":1.0}},
              {"key": "shin_L", "value": {"x":1.0, "y":1.05, "z":1.0}},
              {"key": "shoulder_R", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "shoulder_L", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "upper_arm_R", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "upper_arm_L", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "forearm_R", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "forearm_L", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "neck", "value": {"x":1.0, "y":1.0, "z":1.0}}
            //   {"key": "head", "value": {"x":1.6, "y":1.6, "z":1.6}}
          ],
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
      "vip":true
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



body_dimensions is a list, you need to add the key-value pairs.



#### Request body

```json
{
  	"user_details": {
      "face_shape": "long",
      "skin_tone": 2,
      "pose":"I-Pose",
      "body_dimensions": [
              {"key": "b_{main}_muscular", "value": 0.5},
              {"key": "b_{main}_overweight", "value": 0.5}
          ],
          "body_dimension_lengths": [
              {"key": "spine", "value": {"x":1.05, "y":1.05, "z":1.05}},
              {"key": "thigh_R", "value": {"x":1.0, "y":1.05, "z":1.0}},
              {"key": "thigh_L", "value": {"x":1.0, "y":1.05, "z":1.0}},
              {"key": "shin_R", "value": {"x":1.0, "y":1.05, "z":1.0}},
              {"key": "shin_L", "value": {"x":1.0, "y":1.05, "z":1.0}},
              {"key": "shoulder_R", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "shoulder_L", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "upper_arm_R", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "upper_arm_L", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "forearm_R", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "forearm_L", "value": {"x":1.0, "y":1.0, "z":1.0}},
              {"key": "neck", "value": {"x":1.0, "y":1.0, "z":1.0}}
            //   {"key": "head", "value": {"x":1.6, "y":1.6, "z":1.6}}
          ],
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
          "duration": 5,
          "negative_prompt": "",
          "prompt": "",
          "seed": 0
      },
      "vip":true
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
   "vip":true
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
    ]
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

| URL                   | Brand  | Gender | Name   | Colors         | Colors Hex              | Sizes       |
| --------------------- | ------ | ------ | ------ | -------------- | ----------------------- | ----------- |
| https://example.com/1 | BrandA | Male   | Cloth1 | Red,Blue,Green | #FF0000,#0000FF,#008000 | S,M,L       |
| https://example.com/2 | BrandB | Female | Cloth2 | Black,White    | #000000,#FFFFFF         | XS,S,M,L,XL |
| https://example.com/3 | BrandC | Female | Cloth3 | Yellow,Purple  | #FFFF00,#800080         | M,L,XL,XXL  |



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
    "brand": "BrandA",
    "colors_hex": [
        "#FF0000",
        "#0000FF",
        "#008000 "
    ]
}
```



# API Call Example

1. /register
2. /login
3. /update_user_details
4. /upload_avatar
5. /generate
6. Poll the **/generate/{taskid}** every 5 seconds using the task id
7. When status is SUCCESS, go next step
8. /get_gallery
9. Use task id to match the image
10. /get_gallery_image/{url}

