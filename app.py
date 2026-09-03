import streamlit as st
from google import genai
from PIL import Image

SECRET_PASSWORD = "Thavish"

st.set_page_config(page_title="Hardware Diagnostic System", page_icon="🔬")
st.title("🔬 Phone Board IC Diagnostic System")
st.write("Motherboard photo එකක් upload කර පද්ධතිය මගින් Storage IC විස්තර පරීක්ෂා කරන්න.")

st.sidebar.header("System Settings")
user_pass = st.sidebar.text_input("Enter Access Passcode:", type="password")

if user_pass == SECRET_PASSWORD:
    st.sidebar.success("Access Granted!")
    api_key = st.sidebar.text_input("System License Key:", type="password")
    language = st.sidebar.selectbox("Language / භාෂාව", ["English", "සිංහල"])
    
    uploaded_file = st.file_uploader("Board photo එකක් තෝරන්න...", type=["jpg", "jpeg", "png"])

    if uploaded_file and api_key:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Board Photo", use_container_width=True)
        
        btn_label = "Scan IC Details" if language == "English" else "IC විස්තර පරීක්ෂා කරන්න"
        
        if st.button(btn_label):
            try:
                client = genai.Client(api_key=api_key)
                
                if language == "English":
                    prompt = """
                    You are an automated hardware diagnostic database tool. Analyze the motherboard photo with these strict rules:
                    1. Do NOT use any conversational AI phrases (e.g., 'Based on the image', 'Here are the details', 'As an AI model').
                    2. If NO NAND/eMMC/UFS storage chip is present in the photo, output ONLY this text: "[CRITICAL] Storage Chip is NOT present on this board."
                    3. If the storage chip IS present but the IC part number/text is blurry or unreadable, output ONLY this text: "[WARNING] Storage Chip detected, but IC Part Number is NOT clearly visible."
                    4. If the chip and part number are clearly visible, output a clean, technical diagnostic report listing:
                       - IC Part Number
                       - Manufacturer
                       - Storage Capacity (in GB)
                       - RAM Details (only if visible)
                    """
                else:
                    prompt = """
                    ඔබ ස්වයංක්‍රීය හාඩ්වෙයාර් පරීක්ෂණ දත්ත පද්ධතියකි. මෙම motherboard ඡායාරූපය පරීක්ෂා කර පහත රීති අකුරටම අනුගමනය කරන්න:
                    1. කිසිදු AI හෝ සංවාද ශෛලියේ වාක්‍ය (උදා: 'ඡායාරූපයට අනුව', 'මම AI එකක් ලෙස', 'මෙන්න විස්තර') භාවිතා නොකරන්න.
                    2. ඡායාරූපය තුළ NAND/eMMC/UFS storage chip එක නොමැති නම්, මෙම වාක්‍යය පමණක් ලබාදෙන්න: "[දෝෂයයි] Storage Chip එක මෙහි නොමැත."
                    3. Storage chip එක තිබුණද එහි IC අංකය/අකුරු පැහැදිලි නැතිනම් හෝ කියවිය නොහැකි නම්, මෙම වාක්‍යය පමණක් ලබාදෙන්න: "[අවධානයට] Storage Chip එක පෙනෙන්නට ඇත, නමුත් IC අංකය පැහැදිලිව පෙනෙන්නට නොමැත."
                    4. Chip එක සහ අංකය පැහැදිලිව පෙනේ නම්, පහත විස්තර පමණක් තාක්ෂණික වාර්තාවක් ලෙස ලබාදෙන්න:
                       - IC Part Number
                       - නිෂ්පාදකයා (Manufacturer)
                       - ධාරිතාව (Storage Capacity in GB)
                       - RAM විස්තර (පෙනේ නම් පමණක්)
                    """
                
                sp_text = "Scanning IC Database..." if language == "English" else "IC දත්ත පරීක්ෂා කරමින් පවතී..."
                with st.spinner(sp_text):
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[prompt, image]
                    )
                    st.success("Scan Complete!" if language == "English" else "පරික්ෂාව සාර්ථකයි!")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"System Error: {e}")
elif user_pass != "":
    st.sidebar.error("Invalid Access Passcode!")
else:
    st.warning("Please enter Access Passcode from the sidebar.")
