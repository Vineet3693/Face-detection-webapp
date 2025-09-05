
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Page config
st.set_page_config(
    page_title="Face Detection App",
    page_icon="🔍",
    layout="wide"
)

# Load the face classifier
@st.cache_resource
def load_classifier():
    return cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_faces(image):
    face_classifier = load_classifier()
    
    # Convert PIL image to OpenCV format
    img_array = np.array(image)
    
    # Convert RGB to BGR (OpenCV uses BGR)
    if len(img_array.shape) == 3:
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    else:
        img_bgr = img_array
    
    # Convert to grayscale
    gray_image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_classifier.detectMultiScale(
        gray_image, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(40, 40)
    )
    
    # Draw bounding boxes
    for (x, y, w, h) in faces:
        cv2.rectangle(img_bgr, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # Add face number
        cv2.putText(img_bgr, f'Face {len([f for f in faces if f[0] <= x])}', 
                   (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Convert back to RGB for display
    result_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    return result_img, len(faces)

def main():
    # Header
    st.title("🔍 AI Face Detection App")
    st.markdown("### Upload an image and let AI detect faces automatically!")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        st.info("This app uses OpenCV's Haar Cascade classifier for face detection.")
        
        # Detection parameters
        scale_factor = st.slider("Scale Factor", 1.05, 1.3, 1.1, 0.05)
        min_neighbors = st.slider("Min Neighbors", 3, 10, 5)
        min_size = st.slider("Min Face Size", 20, 100, 40)
        
        st.markdown("---")
        st.markdown("**How it works:**")
        st.markdown("1. Upload an image")
        st.markdown("2. AI scans for face patterns")
        st.markdown("3. Green boxes highlight detected faces")
    
    # Main content
    uploaded_file = st.file_uploader(
        "📁 Choose an image file", 
        type=['jpg', 'jpeg', 'png', 'bmp'],
        help="Supported formats: JPG, JPEG, PNG, BMP"
    )
    
    if uploaded_file is not None:
        # Create columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Original Image")
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Image info
            st.info(f"📊 Image Size: {image.size[0]} x {image.size[1]} pixels")
        
        # Detect faces button
        if st.button("🚀 Detect Faces", type="primary", use_container_width=True):
            with st.spinner("🔍 Analyzing image for faces..."):
                try:
                    result_img, face_count = detect_faces(image)
                    
                    with col2:
                        st.subheader("🎯 Detection Result")
                        st.image(result_img, caption=f"Found {face_count} face(s)", use_column_width=True)
                    
                    # Results summary
                    if face_count > 0:
                        st.success(f"✅ Successfully detected **{face_count}** face(s)!")
                        
                        # Additional stats
                        col_stats1, col_stats2, col_stats3 = st.columns(3)
                        with col_stats1:
                            st.metric("Faces Found", face_count)
                        with col_stats2:
                            st.metric("Processing Time", "< 1 sec")
                        with col_stats3:
                            confidence = "High" if face_count > 0 else "Low"
                            st.metric("Confidence", confidence)
                    else:
                        st.warning("⚠️ No faces detected. Try:")
                        st.markdown("- A clearer image with better lighting")
                        st.markdown("- Frontal face poses work best")
                        st.markdown("- Ensure faces are not too small")
                        
                except Exception as e:
                    st.error(f"❌ Error processing image: {str(e)}")
    
    else:
        # Sample images section
        st.markdown("---")
        st.subheader("📸 Try with sample images")
        st.markdown("Don't have an image? Try these sample photos:")
        
        # Sample image URLs (using placeholder service)
        sample_info = [
            ("Single Person", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face"),
            ("Group Photo", "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=400&h=400&fit=crop"),
            ("Family", "https://images.unsplash.com/photo-1581833971358-2c8b550f87b3?w=400&h=400&fit=crop")
        ]
        
        cols = st.columns(len(sample_info))
        for i, (name, url) in enumerate(sample_info):
            with cols[i]:
                st.markdown(f"**{name}**")
                st.markdown(f"[🔗 Try this image]({url})")
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit and OpenCV")

if __name__ == "__main__":
    main()
