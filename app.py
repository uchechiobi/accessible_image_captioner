import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model     = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
device    = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Streamlit UI
st.title("📸 Accessible Image Captioner")
st.markdown(
    "Upload an image and get a descriptive caption (alt-text) for accessibility. "
    "All inference runs locally—no external API calls."
)

uploaded_file = st.file_uploader("Choose an image…", type=["jpg", "jpeg", "png"])
if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Generate caption
    with st.spinner("Generating caption…"):
        inputs  = processor(images=image, return_tensors="pt").to(device)
        output  = model.generate(**inputs, max_length=50)
        caption = processor.decode(output[0], skip_special_tokens=True)

    st.success("Caption generated!")
    st.write(f"**Caption:** {caption}")
    st.caption("Model: Salesforce/blip-image-captioning-base")
