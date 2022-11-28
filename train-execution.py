#@markdown ---
import os
from subprocess import getoutput
from IPython.display import HTML

fp16 = True #@param {type:"boolean"}
if fp16:
  prec="fp16"
else:
  prec="no"

#@markdown  - fp16 or half precision meaning slightly lower quality but double the speed.
s = getoutput('nvidia-smi')
if 'A100' in s:
  precision="no"
else:
  precision=prec

Training_Steps="2000" #@param{type: 'string'}
#@markdown - Keep it around 1600 to avoid overtraining.

Seed=75576 #@param{type: 'number'}

#@markdown ---------------------------
Save_Checkpoint_Every_n_Steps = False #@param {type:"boolean"}
Save_Checkpoint_Every=500 #@param{type: 'number'}
if Save_Checkpoint_Every==None:
  Save_Checkpoint_Every=1
#@markdown - Minimum 200 steps between each save.
stp=0
Start_saving_from_the_step=500 #@param{type: 'number'}
if Start_saving_from_the_step==None:
  Start_saving_from_the_step=0
if (Start_saving_from_the_step < 200):
  Start_saving_from_the_step=Save_Checkpoint_Every
stpsv=Start_saving_from_the_step
if Save_Checkpoint_Every_n_Steps:
  stp=Save_Checkpoint_Every
#@markdown - Start saving intermediary checkpoints from this step.

Caption=''
if Captionned_instance_images:
  Caption='--image_captions_filename'

if With_Prior_Preservation=='No':
  !accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
    $Caption \
    --save_starting_step=$stpsv \
    --save_n_steps=$stp \
    --train_text_encoder \
    --pretrained_model_name_or_path="$MODEL_NAME" \
    --instance_data_dir="$INSTANCE_DIR" \
    --output_dir="$OUTPUT_DIR" \
    --instance_prompt="$PT" \
    --seed=$Seed \
    --resolution=512 \
    --mixed_precision=$precision \
    --train_batch_size=1 \
    --gradient_accumulation_steps=1 \
    --use_8bit_adam \
    --learning_rate=1e-6 \
    --lr_scheduler="constant" \
    --center_crop \
    --lr_warmup_steps=0 \
    --max_train_steps=$Training_Steps 

else:

  !accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
    $Caption \
    --save_starting_step=$stpsv \
    --save_n_steps=$stp \
    --train_text_encoder \
    --pretrained_model_name_or_path="$MODEL_NAME" \
    --instance_data_dir="$INSTANCE_DIR" \
    --class_data_dir="$CLASS_DIR" \
    --output_dir="$OUTPUT_DIR" \
    --with_prior_preservation --prior_loss_weight=1.0 \
    --instance_prompt="$PT"\
    --class_prompt="$CPT" \
    --seed=$Seed \
    --resolution=512 \
    --mixed_precision=$precision \
    --train_batch_size=1 \
    --gradient_accumulation_steps=1 --gradient_checkpointing \
    --use_8bit_adam \
    --learning_rate=1e-6 \
    --lr_scheduler="constant" \
    --lr_warmup_steps=0 \
    --center_crop \
    --max_train_steps=$Training_Steps \
    --num_class_images=$SUBJECT_IMAGES

if Save_class_images_to_gdrive:
  if os.path.exists(str(CLASS_DIR)):
    if not os.path.exists('/content/gdrive/MyDrive/Class_images'):
      !mkdir /content/gdrive/MyDrive/Class_images
    Class_gdir= '/content/gdrive/MyDrive/Class_images/'+SUBJECT_TYPE
    if not os.path.exists(str(Class_gdir)):
      !cp -r "$CLASS_DIR" /content/gdrive/MyDrive/Class_images

if os.path.exists('/content/models/'+INSTANCE_NAME+'/unet/diffusion_pytorch_model.bin'):
  print("Almost done ...")
  %cd /content    
  !wget -O convertosd.py https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/convertosd.py
  clear_output()
  if precision=="no":
    !sed -i '226s@.*@@' /content/convertosd.py
  !sed -i '201s@.*@    model_path = "{OUTPUT_DIR}"@' /content/convertosd.py
  !sed -i '202s@.*@    checkpoint_path= "/content/gdrive/MyDrive/{INSTANCE_NAME}.ckpt"@' /content/convertosd.py
  !python /content/convertosd.py
  clear_output()
  if os.path.exists('/content/gdrive/MyDrive/'+INSTANCE_NAME+'.ckpt'):
    print("[1;32mDONE, the CKPT model is in your Gdrive")
  else:
    print("[1;31mSomething went wrong")
else:
  print("[1;31mSomething went wrong")