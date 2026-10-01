import streamlit as st
from PIL import Image
import os
import io
from datetime import datetime

# ==============================================
st.set_page_config(
    page_title="KreaVision AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Folder penyimpanan
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDERS = {
    "images": os.path.join(BASE_DIR, "hasil_gambar"),
    "videos": os.path.join(BASE_DIR, "hasil_video"),
    "storyboards": os.path.join(BASE_DIR, "hasil_storyboard"),
    "prompts": os.path.join(BASE_DIR, "hasil_prompt"),
}
for f in FOLDERS.values():
    os.makedirs(f, exist_ok=True)

# Tampilan
st.markdown("""
<style>
    .main-title {font-size: 2.8rem; font-weight: 900; 
    background: linear-gradient(90deg, #6366F1, #EC4899, #F59E0B);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .stButton>button {border-radius: 12px; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🤖 KreaVision AI</h1>', unsafe_allow_html=True)
st.subheader("Buat Gambar • Video 30 Detik • Storyboard • Prompt Otomatis")

# Menu
menu = st.sidebar.radio("Pilih Fitur", [
    "✨ Ekstrak Prompt dari Gambar",
    "🎨 Buat Gambar AI",
    "🎬 Buat Video AI (maks 30 detik)",
    "📖 Buat Storyboard"
])

def buat_prompt(deskripsi, gaya="detail"):
    if gaya == "pendek":
        return deskripsi
    elif gaya == "sedang":
        return f"{deskripsi}, jernih, warna alami, komposisi bagus, resolusi tinggi"
    else:
        return f"""{deskripsi}, foto realistis 8K, sangat detail, pencahayaan sinematik, 
warna hidup, komposisi profesional, kualitas studio"""

def prompt_negatif():
    return "buram, cacat, tidak simetris, jelek, terdistorsi"

# 1. Ekstrak Prompt
if menu == "✨ Ekstrak Prompt dari Gambar":
    st.header("🖼️ Ubah Gambar Jadi Prompt")
    upload = st.file_uploader("Unggah gambar", type=["png","jpg","jpeg","webp"])
    
    if upload:
        col1, col2 = st.columns(2)
        with col1:
            st.image(upload, caption="Gambar Asli", use_column_width=True)
        with col2:
            deskripsi = st.text_area("Deskripsi Gambar", 
                "Pemandangan gunung saat matahari terbenam, langit oranye keunguan, kabut tipis di lembah, hutan pinus, suasana tenang",
                height=150)
            gaya = st.selectbox("Jenis Prompt", ["pendek", "sedang", "detail"])
            
            if st.button("✨ Hasilkan Prompt", type="primary"):
                p_positif = buat_prompt(deskripsi, gaya)
                p_neg = prompt_negatif()
                st.success("Prompt siap dipakai!")
                st.text_area("✅ Prompt Positif", p_positif, height=150)
                st.text_area("❌ Prompt Negatif", p_neg, height=100)
                gabungan = f"POSITIF:\n{p_positif}\n\nNEGATIF:\n{p_neg}"
                st.download_button("📥 Unduh Prompt", gabungan, 
                    file_name=f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# 2. Buat Gambar
elif menu == "🎨 Buat Gambar AI":
    st.header("🎨 Buat Gambar dari Deskripsi")
    teks = st.text_area("Tulis deskripsi gambar", height=120,
        placeholder="Contoh: kucing berbulu oranye duduk di jendela, hujan di luar, lampu jalan menyala...")
    ukuran = st.selectbox("Ukuran", ["1024x1024", "1792x1024", "1024x1792"])
    gaya = st.selectbox("Gaya", ["Foto Realistis", "Lukisan", "Anime", "Ilustrasi"])
    
    if st.button("🎨 Buat Gambar", type="primary") and teks:
        st.info("🔄 Sedang memproses...")
        st.success("✅ Selesai! (Sambungkan API untuk hasil asli)")
        st.image("https://picsum.photos/1024/1024", caption=f"Contoh: {gaya} | {ukuran}")

# 3. Buat Video
elif menu == "🎬 Buat Video AI (maks 30 detik)":
    st.header("🎬 Buat Video — Maksimal 30 Detik")
    sumber = st.radio("Sumber Video", ["Dari Teks", "Dari Gambar"])
    durasi = st.slider("Durasi (detik)", 5, 30, 15)
    
    if sumber == "Dari Teks":
        skenario = st.text_area("Cerita/Alur Video", height=120,
            placeholder="Contoh: Matahari terbit dari balik bukit, cahaya perlahan menyinari lembah berkabut...")
    else:
        st.file_uploader("Unggah gambar referensi", type=["png","jpg","jpeg"])
        st.text_area("Deskripsi gerakan & suasana", height=100)
    
    musik = st.selectbox("Musik Latar", ["Tenang", "Semangat", "Sinematik", "Tidak Ada"])
    if st.button("🎬 Buat Video", type="primary"):
        st.info(f"🔄 Membuat video {durasi} detik...")
        st.success("✅ Selesai! (Sambungkan API untuk hasil video)")

# 4. Storyboard
elif menu == "📖 Buat Storyboard":
    st.header("📖 Buat Storyboard Otomatis")
    judul = st.text_input("Judul Cerita")
    naskah = st.text_area("Naskah / Alur Cerita", height=200,
        placeholder="Bagian 1: Pemandangan pagi...\nBagian 2: Tokoh berjalan...")
    jumlah = st.slider("Jumlah Adegan", 3, 12, 6)
    
    if st.button("📖 Buat Storyboard", type="primary") and naskah:
        st.success(f"✅ {jumlah} adegan dibuat!")
        st.text_area("Storyboard", naskah, height=300)
        st.download_button("📥 Unduh Storyboard", naskah,
            file_name=f"storyboard_{judul or 'cerita'}.txt")

st.caption("---\nKreaVision AI — Sambungkan API penyedia AI untuk hasil gambar & video sesungguhnya")
