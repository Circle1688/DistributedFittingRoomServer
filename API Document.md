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
image/jpeg
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
   "message": "string"
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
              {"key": "b_{main}_overweight", "value": 1},
              {"key": "b_{main}_skinny", "value": 0},
              {"key": "b_{Head}_Neck Thickness", "value": 0},
              {"key": "b_{Head}_Neck Length", "value": 1},
              {"key": "b_{Torso}_Shoulder Width", "value": 0.3},
              {"key": "b_{Torso}_Chest Width", "value": 0},
              {"key": "b_{Torso}_Breast Size", "value": 2},
              {"key": "b_{Torso}_Waist Thickness", "value": 0},
              {"key": "b_{Torso}_Belly Size", "value": 2},
              {"key": "b_{Torso}_Hips Size", "value": 0},
              {"key": "b_{Arms}_Upper Arm Length", "value": 0},
              {"key": "b_{Arms}_Upper Arm Thickness", "value": 0},
              {"key": "b_{Arms}_Forearm Length", "value": 1},
              {"key": "b_{Arms}_Forearm Thickness", "value": 0},
              {"key": "b_{Legs}_Thigh Length", "value": 0},
              {"key": "b_{Legs}_Thigh Thickness", "value": 1},
              {"key": "b_{Legs}_Shin Length", "value": 0},
              {"key": "b_{Legs}_Shin Thickness", "value": 0},
              {"key": "b_{Arms}_Hand Width", "value": 0},
              {"key": "b_{Arms}_Hand Thickness", "value": 0},
              {"key": "b_{Legs}_Foot Length", "value": 1}
          ],
          "body_dimension_lengths": [
              {"key": "spine", "value": {"x":1.1, "y":1.2, "z":1.1}}
          ],
          "hairstyle": "10",
          "hair_color": "6B4F30FF",
          "camera_view": "Front",
          "view_mode": 0,
          "expression": "Kiss",
          "background_color_hex": "FFE4DBFF",
          "gender": "Female"
      },
      "apparel_details": {
          "brand": "brand",
          "item_id": "LongSleeve",
          "color": "Black",
          "size": "M",
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
              {"key": "b_{main}_overweight", "value": 1},
              {"key": "b_{main}_skinny", "value": 0},
              {"key": "b_{Head}_Neck Thickness", "value": 0},
              {"key": "b_{Head}_Neck Length", "value": 1},
              {"key": "b_{Torso}_Shoulder Width", "value": 0.3},
              {"key": "b_{Torso}_Chest Width", "value": 0},
              {"key": "b_{Torso}_Breast Size", "value": 2},
              {"key": "b_{Torso}_Waist Thickness", "value": 0},
              {"key": "b_{Torso}_Belly Size", "value": 2},
              {"key": "b_{Torso}_Hips Size", "value": 0},
              {"key": "b_{Arms}_Upper Arm Length", "value": 0},
              {"key": "b_{Arms}_Upper Arm Thickness", "value": 0},
              {"key": "b_{Arms}_Forearm Length", "value": 1},
              {"key": "b_{Arms}_Forearm Thickness", "value": 0},
              {"key": "b_{Legs}_Thigh Length", "value": 0},
              {"key": "b_{Legs}_Thigh Thickness", "value": 1},
              {"key": "b_{Legs}_Shin Length", "value": 0},
              {"key": "b_{Legs}_Shin Thickness", "value": 0},
              {"key": "b_{Arms}_Hand Width", "value": 0},
              {"key": "b_{Arms}_Hand Thickness", "value": 0},
              {"key": "b_{Legs}_Foot Length", "value": 1}
          ],
          "body_dimension_lengths": [
              {"key": "spine", "value": {"x":1.1, "y":1.2, "z":1.1}}
          ],
          "hairstyle": "10",
          "hair_color": "6B4F30FF",
          "camera_view": "Front",
          "view_mode": 0,
          "expression": "Kiss",
          "background_color_hex": "FFE4DBFF",
          "gender": "Female"
      },
      "apparel_details": {
          "brand": "brand",
          "item_id": "LongSleeve",
          "color": "Black",
          "size": "M",
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
           "type":"image",
           "url":"1738860389536"
       },
       {
           "type":"video",
           "url":"1738860592428"
       }
   ]
}
```



### /get_gallery_image/{url}

**GET**

**Authorization**

ex：/get_gallery_image/1736386913456-1



#### Responses

```json
jpg file
```



### /get_gallery_video/{url}

**GET**

**Authorization**

ex：/get_gallery_video/1738860592428



#### Responses

```json
mp4 file
```



### /get_thumbnail/{url}

**GET**

**Authorization**

ex：/get_thumbnail/1736386913456-1



#### Responses

```json
jpg file
```



### /get_avatar_thumbnail

**GET**

**Authorization**



#### Responses

```json
image/jpeg
```



### /remove_gallery_image/{url}

**DELETE**

**Authorization**



#### Responses

```json
{
   "message": "string"
}
```



### /remove_gallery_video/{url}

**DELETE**

**Authorization**



#### Responses

```json
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

