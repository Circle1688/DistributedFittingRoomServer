# 虚拟试穿如何新增服务

假设是新增**kling**的服务

转到**virtual_try_on**文件夹下

1. 创建 kling.py

2. 实现函数

   ```python
   def process(human_image_path, cloth_image_path) -> bool
   ```

3. 打开 **plugin_server/try_on.py**

4. 在文件开头引入

   ```python
   from virtual_try_on.kling import process as kling_process
   ```

5. 在**virtual_try_on**函数下加入

   ```python
   def virtual_try_on(render_mode, human_image_path, request_data):
       cloth_image_path = get_cloth_image(request_data)
       
       ## 加入的部分
       if render_mode == '2D_Kling':
           return kling_process(human_image_path, cloth_image_path)
    	# 举例   
       elif render_mode == '2D_****':
           return ****_process(human_image_path, cloth_image_path)
       ## 加入的部分
   
       return False
   ```