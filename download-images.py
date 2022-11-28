#@markdown We’ve created the following image sets
#@markdown - `young_man` - provided by me
#@markdown - `young_woman`

dataset="young_man" #@param ["young_man", "young_woman"]
!git clone https://github.com/djbielejeski/Stable-Diffusion-Regularization-Images-{dataset}.git

!mkdir -p regularization_images/{dataset}
!mv -v regularization_images/{dataset}/*.* regularization_images/{dataset}
CLASS_DIR="/content/regularization_images/" + dataset