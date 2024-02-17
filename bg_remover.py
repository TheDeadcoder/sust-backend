from rembg import remove, new_session
import requests
from pathlib import Path

image_url = 'https://dxpcgmtdvyvcxbaffqmt.supabase.co/storage/v1/object/public/demo/427910728_779020504130427_8566049262563333412_n.jpg'

response = requests.get(image_url)
input_image_bytes = response.content

output_image_bytes = remove(input_image_bytes)

output_filename = Path("output").name
output_filename = output_filename.split('.')[0] + ".png"  # Change extension to .png
output_path =  output_filename

with open(output_path, 'wb') as output_file:
    output_file.write(output_image_bytes)