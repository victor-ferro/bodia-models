import os
import shutil
from google.colab import files
from IPython.display import clear_output
from IPython.utils import capture
#@markdown ---
Training_Subject = "Character" #@param ["Character", "Object", "Style", "Artist", "Movie", "TV Show"] 

With_Prior_Preservation = "Yes" #@param ["Yes", "No"] 
#@markdown - With the prior reservation method, the results are better, you will either have to upload around 200 pictures of the class you're training (dog, person, car, house ...) or let Dreambooth generate them.

MODEL_NAME="/content/stable-diffusion-2"

Captionned_instance_images = False #@param {type:"boolean"}

#@markdown - Use the keywords included in each instance images as unique instance prompt, this allows to train on multiple subjects at the same time, example : 
#@markdown - An instance image named fat_dog_doginstancename_in_a_pool.jpg
#@markdown - another instance image named a_cat_catinstancename_in_the_woods.png
#@markdown - the unique training instance prompts would be : fat dog doginstancename in a pool, a cat doginstancename in the woods
#@markdown - at inference you can generate the dog by simply using doginstancename (a random unique identifier) or the cat by catinstancename

#@markdown - Also you can enhance the training of a simple subject by simply describing the image using keywords like : smiling, outdoor, sad, lether jacket ...etc

#@markdown - If you enable this feature, and want to train on multiple subjects, use the AUTOMATIC1111 colab to generate good quality 512x512 100-200 Class images for each subject (dog and a cat and a cow), then put them all in the same folder and entrer the folder's path in the cell below.

#@markdown - If you enable this feature, you must add an instance name and a subject type (dog, man, car) to all the images, separate keywords by an underscore (_).



SUBJECT_TYPE = "woman" #@param{type: 'string'}
while SUBJECT_TYPE=="":
   SUBJECT_TYPE=input('Input the subject type:')

#@markdown - If you're training on a character or an object, the subject type would be : Man, Woman, Shirt, Car, Dog, Baby ...etc
#@markdown - If you're training on a Style, the subject type would be : impressionist, brutalist, abstract, use "beautiful" for a general style...etc
#@markdown - If you're training on a Movie/Show, the subject type would be : Action, Drama, Science-fiction, Comedy ...etc
#@markdown - If you're training on an Artist, the subject type would be : Painting, sketch, drawing, photography, art ...etc


INSTANCE_NAME= "sks njrrt" #@param{type: 'string'}
while INSTANCE_NAME=="":
   INSTANCE_NAME=input('Input the instance name (identifier) :')

#@markdown - The instance is an identifier, choose a unique identifier unknown by stable diffusion. 

INSTANCE_DIR_OPTIONAL="" #@param{type: 'string'}
INSTANCE_DIR=INSTANCE_DIR_OPTIONAL
while INSTANCE_DIR_OPTIONAL!="" and not os.path.exists(str(INSTANCE_DIR)):
    INSTANCE_DIR=input('[1;31mThe instance folder specified does not exist, use the colab file explorer to copy the path :')

#@markdown - If the number of instance pictures is large, it is preferable to specify directly the folder instead of uploading, leave EMPTY to upload.

CLASS_DIR="/content/data/"+ SUBJECT_TYPE
Number_of_subject_images=500#@param{type: 'number'}
while Number_of_subject_images==None:
     Number_of_subject_images=input('Input the number of subject images :')
SUBJECT_IMAGES=Number_of_subject_images

Save_class_images_to_gdrive = False #@param {type:"boolean"}
#@markdown - Save time in case you're training multiple instances of the same class

if Training_Subject=="Character" or Training_Subject=="Object":
  PT="photo of "+INSTANCE_NAME+" "+SUBJECT_TYPE
  CPT="a photo of a "+SUBJECT_TYPE+", ultra detailed"
  if Captionned_instance_images:
    PT="photo of"
elif Training_Subject=="Style":
  With_Prior_Preservation = "No"
  PT="in the "+SUBJECT_TYPE+" style of "+INSTANCE_NAME
  if Captionned_instance_images:
    PT="in the style of"  
elif Training_Subject=="Artist":
  With_Prior_Preservation = "No"
  PT=SUBJECT_TYPE+" By "+INSTANCE_NAME
  if Captionned_instance_images:
    PT="by the artist"  
elif Training_Subject=="Movie":
  PT="from the "+SUBJECT_TYPE+" movie "+ INSTANCE_NAME
  CPT="still frame from "+SUBJECT_TYPE+" movie, ultra detailed, 4k uhd"
  if Captionned_instance_images:
    PT="from the movie"  
elif Training_Subject=="TV Show":
  CPT="still frame from "+SUBJECT_TYPE+" tv show, ultra detailed, 4k uhd"
  PT="from the "+SUBJECT_TYPE+" tv show "+ INSTANCE_NAME
  if Captionned_instance_images:
    PT="from the tv show"    
  
OUTPUT_DIR="/content/models/"+ INSTANCE_NAME

if INSTANCE_DIR_OPTIONAL=="":
  INSTANCE_DIR="/content/data/"+INSTANCE_NAME
  !mkdir -p "$INSTANCE_DIR"
  uploaded = files.upload()
  for filename in uploaded.keys():
    shutil.move(filename, INSTANCE_DIR)
    clear_output()

with capture.capture_output() as cap:
   %cd "$INSTANCE_DIR"
   !find . -name "* *" -type f | rename 's/ /_/g'
   %cd /content
print('[1;32mOK')