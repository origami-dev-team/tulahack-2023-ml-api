import os
import io
from torch import save
from kandinsky2 import get_kandinsky2
from translate import Translator
from rembg.bg import remove

IMAGE_HEGHT = 450
IMAGE_WIDTH = 350

def download_pretrained_model():
    os.system("pip install 'git+https://github.com/ai-forever/Kandinsky-2.git'")
    os.system("pip install git+https://github.com/openai/CLIP.git")

    model = get_kandinsky2(
        "cuda",
        task_type="text2img",
        cache_dir="/tmp/kandinsky2",
        model_version="2.1",
        use_flash_attention=False,
    )
    save(model, 'generate_model.pth')

def translate_query(query: str) -> str:
    translator= Translator(from_lang='ru', to_lang="en")
    translation = translator.translate(query)
    return translation

def generate_image(query: str, model, generate_emotions: bool, delete_background: bool):
    if generate_emotions:
        # это характерно для персонажа
        query = "в полный рост "+query
    else:
        # это для задних фонов
        query = "пусто без людей "+query
    query = translate_query(query) + " anime"
    images = model.generate_text2img(
        query,
        num_steps=100,
        batch_size=1,
        guidance_scale=4,
        h=IMAGE_HEGHT,
        w=IMAGE_WIDTH,
        sampler="p_sampler",
        prior_cf_scale=4,
        prior_steps="5",
    )
    
    if generate_emotions:
        emotions = ['happy', 'sad', 'angry']
        for emotion in emotions:
            images.append(model.generate_img2img(
                prompt=emotion+' '+query,
                pil_img=images[0],
                num_steps=100,
                batch_size=1,
                sampler="p_sampler"
            )[0].resize((IMAGE_WIDTH, IMAGE_HEGHT)))
        
    imgs_byte = []

    for i, _ in enumerate(images):
        if delete_background:
            images[i] = remove(images[i])
        img_byte = io.BytesIO()
        images[i].save(img_byte, format='PNG')
        imgs_byte.append(img_byte.getvalue())

    return imgs_byte