import streamlit as pd  # Diimport sebagai cadangan jika diperlukan, tapi kita gunakan streamlit standard
import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. KONFIGURASI HALAMAN & DESAIN (NUANSA BIRU)
# ==========================================
st.set_page_config(
    page_title="Baytul Kalam - Aplikasi Maharah Kalam",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan modern, elegan, dan ramah remaja (MTs)
st.markdown("""
    <style>
    /* Mengubah warna font utama dan background */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Desain Header Utama */
    .main-title {
        color: #1E3A8A; /* Biru Gelap Islami */
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #3B82F6; /* Biru Muda Modern */
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    /* Styling untuk Chat Box Persona */
    .persona-card {
        background-color: #EFF6FF;
        border-left: 5px solid #2563EB;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INISIALISASI SESSION STATE (RIWAYAT)
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""
if "current_persona" not in st.session_state:
    st.session_state.current_persona = ""

# ==========================================
# 3. HALAMAN LOGIN (USERNAME & API KEY)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 class='main-title'>🕌 بَيْتُ الكَلَامِ (Baytul Kalam)</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Aplikasi Interaktif Pembelajaran Maharah Kalam Kelas IX MTs</p>", unsafe_allow_html=True)
    
    # Kolom tengah untuk form login agar terlihat rapi
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("Silakan masukkan Username dan Google AI Studio API Key Anda untuk memulai.")
        username = st.text_input("Username", placeholder="Masukkan nama Anda...")
        api_key = st.text_input("Google AI Studio API Key", type="password", placeholder="AIzaSy...")
        
        login_btn = st.button("Masuk Aplikasi 🚀", use_container_width=True)
        
        if login_btn:
            if username.strip() == "":
                st.error("Username tidak boleh kosong!")
            elif api_key.strip() == "":
                st.error("API Key tidak boleh kosong!")
            else:
                try:
                    # Validasi singkat API Key ke Google GenAI
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # Test call ringan untuk memastikan key valid
                    model.generate_content("Hi", generation_config={"max_output_tokens": 5})
                    
                    # Jika berhasil, simpan ke session state
                    st.session_state.username = username
                    st.session_state.api_key = api_key
                    st.session_state.logged_in = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal menghubungkan ke Google AI Studio. Pastikan API Key benar. Error: {e}")

# ==========================================
# 4. HALAMAN UTAMA (SETELAH LOGIN)
# ==========================================
else:
    # Konfigurasi ulang API Key yang valid
    genai.configure(api_key=st.session_state.api_key)
    
    # --- SIDEBAR: PENGATURAN PERSONA & MATERI ---
    with st.sidebar:
        st.markdown("### 👤 Profil Pengguna")
        st.success(f"Selamat Datang, **{st.session_state.username}**!")
        
        st.markdown("---")
        st.markdown("### ⚙️ Pengaturan Pembelajaran")
        
        # Pilihan Guru/Persona
        persona = st.radio(
            "Pilih Ustadz / Ustadzah:",
            ("Ustadz Miftah", "Ustadzah Shifa")
        )
        
        # Pilihan Materi Kelas IX MTs
        materi = st.radio(
            "Pilih Materi (Maharah Kalam):",
            ("Al-Usrah (العُصْرَة / Keluarga)", "Al-Hiwayah (الهِوَايَة / Hobi)", "Al-Mihnah (المِهْنَة / Profesi)")
        )
        
        st.markdown("---")
        # Tombol Keluar / Exit
        if st.button("🚪 Keluar dari Aplikasi (Exit)", use_container_width=True, type="secondary"):
            # Reset semua session state
            st.session_state.logged_in = False
            st.session_state.messages = []
            st.session_state.current_topic = ""
            st.session_state.current_persona = ""
            st.rerun()

    # --- DETEKSI PERUBAHAN MATERI ATAU PERSONA ---
    # Jika user mengganti topik atau guru di tengah jalan, percakapan di-reset agar nyambung
    if st.session_state.current_topic != materi or st.session_state.current_persona != persona:
        st.session_state.current_topic = materi
        st.session_state.current_persona = persona
        st.session_state.messages = [] # Reset riwayat untuk topik baru
        
        # Tentukan pesan greeting awal berdasarkan persona dan materi
        panggilan = "Ustadz Miftah" if persona == "Ustadz Miftah" else "Ustadzah Shifa"
        karakter = "seorang guru laki-laki yang sabar, interaktif, dan komunikatif" if persona == "Ustadz Miftah" else "seorang guru perempuan yang ramah, hangat, dan sangat memotivasi"
        
        greeting_text = (
            f"السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ، {st.session_state.username}! 👋\n\n"
            f"Saya **{panggilan}**, tutor bahasa Arab virtualmu hari ini. "
            f"Mari kita melatih kelancaran berbicara (*Maharah Kalam*) pada tema **{materi}**. "
            f"Ustadz/Ustadzah akan memberikan pertanyaan, koreksi, atau stimulus percakapan pendek. "
            f"Silakan balas menggunakan bahasa Arab (atau campuran jika belum tahu kosa katanya). "
            f"Mari kita mulai! Silakan sapa balik atau langsung mulai percakapan kita! 😊"
        )
        
        st.session_state.messages.append({"role": "assistant", "content": greeting_text})

    # --- TAMPILAN UTAMA DAERAH CHAT ---
    st.markdown("<h1 style='color: #1E3A8A; font-family: sans-serif;'>🕌 Baytul Kalam</h1>", unsafe_allow_html=True)
    st.markdown(f"#### Mode Pembelajaran Kelas IX MTs: `{materi}` bersama `{persona}`")
    
    # Banner Petunjuk Pembelajaran Berbahasa Arab
    st.markdown(
        f"""
        <div class='persona-card'>
            <strong>Karakter Pengajar:</strong> {persona} ({ "Laki-laki, Tegas & Edukatif" if persona == "Ustadz Miftah" else "Perempuan, Lembut & Apresiatif" }).<br>
            <strong>Fokus:</strong> Maharah Kalam (Keterampilan Berbicara). Jawablah stimulus dengan percaya diri!
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Menampilkan riwayat percakapan yang ada di dalam session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- PROSES INPUT PERCAKAPAN BARU ---
    if user_input := st.chat_input("Tulis jawaban atau pesan bahasa Arab Anda di sini..."):
        
        # 1. Tampilkan pesan user ke layar
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 2. Definisikan System Prompt yang ketat agar AI bertindak sesuai pesanan
        system_instruction = (
            f"Anda adalah {persona}, { 'seorang Ustadz' if persona == 'Ustadz Miftah' else 'seorang Ustadzah' } "
            f"ahli bahasa Arab yang mengajar siswa kelas IX Madrasah Tsanawiyah (MTs) di Indonesia. "
            f"Fokus pembelajaran saat ini adalah Maharah Kalam (Keterampilan Berbicara/Percakapan) dengan tema: {materi}.\n\n"
            f"Aturan Berkomunikasi:\n"
            f"1. Gunakan bahasa Arab yang sederhana, jelas, dan sesuai tingkat kemampuan anak kelas IX MTs (berikan harakat pada kata-kata penting jika memungkinkan).\n"
            f"2. Berikan terjemahan bahasa Indonesia atau penjelasan singkat di bawah baris bahasa Arab agar siswa paham.\n"
            f"3. Jika siswa membuat kesalahan tata bahasa (Nahwu/Sharaf) atau pilihan kata dalam bahasa Arab, koreksilah dengan lembut dan berikan contoh yang benar.\n"
            f"4. Selalu akhiri respon Anda dengan memberikan pertanyaan pendek atau stimulus baru agar percakapan terus berlanjut (interaktif).\n"
            f"5. Panggil siswa dengan namanya: {st.session_state.username}.\n"
            f"6. Gaya bahasa harus mencerminkan seorang pendidik muslim yang sopan, memotivasi, modern, dan hangat."
        )
        
        # 3. Panggil API Gemini dengan menyertakan context history
        try:
            with st.spinner(f"{persona} sedang mengetik tanggapan..."):
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    system_instruction=system_instruction
                )
                
                # Format ulang riwayat untuk dikirim ke API Gemini
                formatted_history = []
                for msg in st.session_state.messages[:-1]: # exclude input terakhir yang baru saja dimasukkan
                    role_name = "model" if msg["role"] == "assistant" else "user"
                    formatted_history.append({"role": role_name, "parts": [msg["content"]]})
                
                # Memulai chat dengan history eksternal
                chat_session = model.start_chat(history=formatted_history)
                response = chat_session.send_message(user_input)
                ai_response = response.text
                
            # 4. Tampilkan respon AI ke layar
            with st.chat_message("assistant"):
                st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"Terjadi kesalahan koneksi API: {e}. Pastikan kuota API Key Anda aktif.")