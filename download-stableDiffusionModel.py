import os
import time
from IPython.display import clear_output
from IPython.utils import capture

with capture.capture_output() as cap: 
  %cd /content/
#@markdown ---
Huggingface_Token = "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" #@param {type:"string"}
token=Huggingface_Token

#@markdown *(Make sure you've accepted the terms in https://huggingface.co/stabilityai/stable-diffusion-2)*

#@markdown ---

CKPT_Path = "" #@param {type:"string"}

#@markdown Or

CKPT_gdrive_Link = "" #@param {type:"string"}


if CKPT_Path !="":
  if os.path.exists('/content/stable-diffusion-2'):
    !rm -r /content/stable-diffusion-2
  if os.path.exists(str(CKPT_Path)):
    !mkdir /content/stable-diffusion-2
    with capture.capture_output() as cap: 
      !wget https://raw.githubusercontent.com/huggingface/diffusers/main/scripts/convert_original_stable_diffusion_to_diffusers.py
    !python /content/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path "$CKPT_Path" --dump_path /content/stable-diffusion-2
    if os.path.exists('/content/stable-diffusion-2/unet/diffusion_pytorch_model.bin'):
      !rm /content/convert_original_stable_diffusion_to_diffusers.py
      !rm /content/v1-inference.yaml
      clear_output()
      print('[1;32mDONE !')
    else:
      !rm /content/convert_original_stable_diffusion_to_diffusers.py
      !rm /content/v1-inference.yaml
      !rm -r /content/stable-diffusion-2
      while not os.path.exists('/content/stable-diffusion-2/unet/diffusion_pytorch_model.bin'):
        print('[1;31mConversion error, check your CKPT and try again')
        time.sleep(5)
  else:
    while not os.path.exists(str(CKPT_Path)):
       print('[1;31mWrong path, use the colab file explorer to copy the path')
       time.sleep(5)


elif CKPT_gdrive_Link !="":   
    if os.path.exists('/content/stable-diffusion-2'):
      !rm -r /content/stable-diffusion-2     
    !gdown --fuzzy $CKPT_gdrive_Link -O model.ckpt    
    if os.path.exists('/content/model.ckpt'):
      if os.path.getsize("/content/model.ckpt") > 1810671599:
        !mkdir /content/stable-diffusion-2
        with capture.capture_output() as cap: 
          !wget https://raw.githubusercontent.com/huggingface/diffusers/main/scripts/convert_original_stable_diffusion_to_diffusers.py
        !python /content/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path /content/model.ckpt --dump_path /content/stable-diffusion-2
        if os.path.exists('/content/stable-diffusion-2/unet/diffusion_pytorch_model.bin'):
          clear_output()
          print('[1;32mDONE !')
          !rm /content/convert_original_stable_diffusion_to_diffusers.py
          !rm /content/v1-inference.yaml
          !rm /content/model.ckpt
        else:
          if os.path.exists('/content/v1-inference.yaml'):
            !rm /content/v1-inference.yaml
          !rm /content/convert_original_stable_diffusion_to_diffusers.py
          !rm -r /content/stable-diffusion-2
          !rm /content/model.ckpt
          while not os.path.exists('/content/stable-diffusion-2/unet/diffusion_pytorch_model.bin'):
            print('[1;31mConversion error, check your CKPT and try again')
            time.sleep(5)
      else:
        while os.path.getsize('/content/model.ckpt') < 1810671599:
           print('[1;31mWrong link, check that the link is valid')
           time.sleep(5)


elif token =="":
  if os.path.exists('/content/stable-diffusion-2'):
    !rm -r /content/stable-diffusion-2
  clear_output()
  token=input("Insert your huggingface token :")
  %cd /content/
  clear_output()
  !mkdir /content/stable-diffusion-2
  %cd /content/stable-diffusion-2
  !git init
  !git lfs install --system --skip-repo
  !git remote add -f origin  "https://USER:{token}@huggingface.co/stabilityai/stable-diffusion-2"
  !git config core.sparsecheckout true
  !echo -e "feature_extractor\nsafety_checker\nscheduler\ntext_encoder\ntokenizer\nunet\nmodel_index.json" > .git/info/sparse-checkout
  !git pull origin main
  if os.path.exists('/content/stable-diffusion-2/unet/diffusion_pytorch_model.bin'):
    !git clone "https://USER:{token}@huggingface.co/stabilityai/sd-vae-ft-mse"
    !mv /content/stable-diffusion-2/sd-vae-ft-mse /content/stable-diffusion-2/vae
    !rm -r /content/stable-diffusion-2/.git
    %cd /content/    
    clear_output()
    print('[1;32mDONE !')
  else:
    while not os.path.exists('/content/stable-diffusion-2'):
         print('[1;31mMake sure you accepted the terms in https://huggingface.co/stabilityai/stable-diffusion-2')
         time.sleep(5)
         
elif token !="":
  if os.path.exists('/content/stable-diffusion-2'):
    !rm -r /content/stable-diffusion-2   
  clear_output()
  %cd /content/
  clear_output()
  !mkdir /content/stable-diffusion-2
  %cd /content/stable-diffusion-2
  !git init
  !git lfs install --system --skip-repo
  !git remote add -f origin  "https://USER:{token}@huggingface.co/stabilityai/stable-diffusion-2"
  !git config core.sparsecheckout true
  !echo -e "feature_extractor\nsafety_checker\nscheduler\ntext_encoder\ntokenizer\nunet\nmodel_index.json" > .git/info/sparse-checkout
  !git pull origin main
  if os.path.exists('/content/stable-diffusion-2/unet/diffusion_pytorch_model.bin'):
    !git clone "https://USER:{token}@huggingface.co/stabilityai/sd-vae-ft-mse"
    !mv /content/stable-diffusion-2/sd-vae-ft-mse /content/stable-diffusion-2/vae
    !rm -r /content/stable-diffusion-2/.git
    %cd /content/    
    clear_output()
    print('[1;32mDONE !')
  else:
    while not os.path.exists('/content/stable-diffusion-2'):
         print('[1;31mMake sure you accepted the terms in https://huggingface.co/stabilityai/stable-diffusion-2')
         time.sleep(5)