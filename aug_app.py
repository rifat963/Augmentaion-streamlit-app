import streamlit as st
from PIL import Image
import torchvision.transforms as transforms
import io

# Set page configuration
st.set_page_config(
    page_title="Image Augmentation Explorer",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for header and footer
st.markdown(
    """
    <style>
    .header {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .footer {
        font-size: 14px;
        text-align: center;
        margin-top: 20px;
        color: gray;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="header">Image Augmentation Explorer</div>', unsafe_allow_html=True)

# Sidebar for augmentation selection
st.sidebar.header("Select Augmentation")
augmentation = st.sidebar.selectbox(
    "Choose an augmentation technique:",
    (
        "Horizontal Flip",
        "Vertical Flip",
        "Random Rotation",
        "Color Jitter",
        "Grayscale",
        "Center Crop",
        "Random Resized Crop",
        "Gaussian Blur",
    )
)

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load image
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    # Define augmentation transformations and corresponding PyTorch code
    if augmentation == "Horizontal Flip":
        transform = transforms.RandomHorizontalFlip(p=1.0)
        code = "transforms.RandomHorizontalFlip(p=1.0)"
    elif augmentation == "Vertical Flip":
        transform = transforms.RandomVerticalFlip(p=1.0)
        code = "transforms.RandomVerticalFlip(p=1.0)"
    elif augmentation == "Random Rotation":
        degrees = st.sidebar.slider("Rotation Degrees", 0, 360, 45)
        transform = transforms.RandomRotation(degrees=degrees)
        code = f"transforms.RandomRotation(degrees={degrees})"
    elif augmentation == "Color Jitter":
        brightness = st.sidebar.slider("Brightness", 0.0, 2.0, 1.0)
        contrast = st.sidebar.slider("Contrast", 0.0, 2.0, 1.0)
        saturation = st.sidebar.slider("Saturation", 0.0, 2.0, 1.0)
        hue = st.sidebar.slider("Hue", -0.5, 0.5, 0.0)
        transform = transforms.ColorJitter(
            brightness=brightness, contrast=contrast, saturation=saturation, hue=hue
        )
        code = (
            f"transforms.ColorJitter(brightness={brightness}, contrast={contrast}, "
            f"saturation={saturation}, hue={hue})"
        )
    elif augmentation == "Grayscale":
        num_output_channels = st.sidebar.radio("Number of Output Channels", [1, 3], index=0)
        transform = transforms.Grayscale(num_output_channels=num_output_channels)
        code = f"transforms.Grayscale(num_output_channels={num_output_channels})"
    elif augmentation == "Center Crop":
        size = st.sidebar.slider("Crop Size", 50, min(image.size), 100)
        transform = transforms.CenterCrop(size)
        code = f"transforms.CenterCrop(size={size})"
    elif augmentation == "Random Resized Crop":
        size = st.sidebar.slider("Output Size", 50, min(image.size), 100)
        scale = st.sidebar.slider("Scale", 0.1, 1.0, (0.5, 1.0))
        ratio = st.sidebar.slider("Ratio", 0.5, 2.0, (0.75, 1.33))
        transform = transforms.RandomResizedCrop(size=size, scale=scale, ratio=ratio)
        code = (
            f"transforms.RandomResizedCrop(size={size}, scale={scale}, ratio={ratio})"
        )
    elif augmentation == "Gaussian Blur":
        kernel_size = st.sidebar.slider("Kernel Size", 3, 21, 5, step=2)
        sigma = st.sidebar.slider("Sigma", 0.1, 5.0, 1.0)
        transform = transforms.GaussianBlur(kernel_size=kernel_size, sigma=sigma)
        code = f"transforms.GaussianBlur(kernel_size={kernel_size}, sigma={sigma})"

    # Apply transformation
    transformed_image = transform(image)
    st.image(transformed_image, caption=f"Image after {augmentation}", use_column_width=True)

    # Display PyTorch code
    st.code(code, language="python")

# Footer
st.markdown(
    """
    <div class="footer">
    Created for CSE 366<br>
    Faculty: Mohammad Rifat Ahmmad Rashid<br>
    Associate Professor<br>
    East West University
    </div>
    """,
    unsafe_allow_html=True
)
