import time
import base64
import jwt
import requests

access_key_id = "3e83cccb357c4e36bffceda7b9ff53c7"
access_key_secret = "806cfcff57274463a83bea41995f9039"


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate_jwt(ak, sk):
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,
        "nbf": int(time.time()) - 5
    }
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    return jwt.encode(payload, sk, algorithm="HS256", headers=headers)


def send_to_kling(human_b64, cloth_b64, token):
    url = "https://api.klingai.com/v1/images/kolors-virtual-try-on"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model_name": "kolors-virtual-try-on-v1-5",
        "human_image": human_b64,
        "cloth_image": cloth_b64
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    if "data" in data and "task_id" in data["data"]:
        task_id = data["data"]["task_id"]
        print(f"Task submitted! ID: {task_id}")
        return task_id
    else:
        print("Failed to submit task:", data)
        return None


def poll_for_result(task_id, token):
    url = f"https://api.klingai.com/v1/images/kolors-virtual-try-on/{task_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("⏳ Polling for result...")
    while True:
        response = requests.get(url, headers=headers)
        data = response.json()
        status = data.get("data", {}).get("task_status")

        if status == "succeed":
            image_url = data["data"]["task_result"]["images"][0]["url"]
            print(f"Task complete! Image URL:\n{image_url}")
            return image_url
        elif status == "failed":
            reason = data["data"].get("task_status_msg", "Unknown reason")
            print(f"Task failed: {reason}")
            return None
        else:
            print("Still processing... Waiting 3s")
            time.sleep(3)


def download_file(url, download_path):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            with open(download_path, "wb") as file:
                file.write(response.content)
            print("Download successfully")
            return True
        else:
            print("Download failed")
            return False
    except Exception as e:
        print(f"Download error: {e}")
        return False


def process(human_image_path, cloth_image_path):
    cloth_b64 = encode_image_to_base64(cloth_image_path)
    human_b64 = encode_image_to_base64(human_image_path)
    token = generate_jwt(access_key_id, access_key_secret)
    task_id = send_to_kling(human_b64, cloth_b64, token)

    if task_id:
        image_url = poll_for_result(task_id, token)
        if image_url:
            return download_file(image_url, human_image_path)

    return False
