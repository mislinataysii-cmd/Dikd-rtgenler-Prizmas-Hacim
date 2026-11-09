dik-prizma-hacim-simulasyonu/
├── .streamlit/
│   └── config.toml
├── app.py
├── requirements.txt
└── README.md
streamlit>=1.30.0
streamlit-embedcode
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="MAT.7.4.4.ç - Dik Prizmalarda Hacim Bağıntısı",
    page_icon="🧊",
    layout="wide"
)

st.title("🧊 MAT.7.4.4.ç - Dik Prizmaların Hacmi ve Katman Simülasyonu")
st.caption("Taban Alanı (TA) × Yükseklik (h) Bağıntısının Birim Küpler ve Katmanlar Aracılığıyla Keşfi")

# Yan Panel - Kontroller
with st.sidebar:
    st.header("1. Kutu ve Boyut Seçimi")
    box_preset = st.radio(
        "Hazır Kutu Türü Seçin:",
        ["1. Kutu: 2×2×4 (Kare Prizma)", "2. Kutu: 2×4×4 (Dik Konum)", "2. Kutu: 4×4×2 (Yan Yatırılmış)", "3. Kutu: 4×4×4 (Küp Kiler)", "Özel Boyut"]
    )

    if box_preset == "1. Kutu: 2×2×4 (Kare Prizma)":
        dim_x, dim_y, dim_z = 2, 2, 4
    elif box_preset == "2. Kutu: 2×4×4 (Dik Konum)":
        dim_x, dim_y, dim_z = 2, 4, 4
    elif box_preset == "2. Kutu: 4×4×2 (Yan Yatırılmış)":
        dim_x, dim_y, dim_z = 4, 4, 2
    elif box_preset == "3. Kutu: 4×4×4 (Küp Kiler)":
        dim_x, dim_y, dim_z = 4, 4, 4
    else:
        dim_x = st.slider("Genişlik (X - a)", 1, 6, 3)
        dim_y = st.slider("Derinlik (Y - b)", 1, 6, 3)
        dim_z = st.slider("Yükseklik (Z - h)", 1, 6, 3)

    st.divider()
    st.header("2. Taban Kabul Edilen Yüz")
    direction = st.selectbox(
        "Taban Yönü:",
        options=[1, 2, 3],
        format_func=lambda x: {
            1: "Alt Yüz Taban (Z Yönünde Katmanlaşma)",
            2: "Ön Yüz Taban (Y Yönünde Katmanlaşma)",
            3: "Yan Yüz Taban (X Yönünde Katmanlaşma)"
        }[x]
    )

    # Katman Sınırı Belirleme
    max_kat = dim_z if direction == 1 else (dim_y if direction == 2 else dim_x)
    kat = st.slider("Dolu Katman Sayısı:", 0, max_kat, min(1, max_kat))
    
    show_skeleton = st.checkbox("L-İskelet Göster", value=True)

# Matematiksel Hesaplamalar
if direction == 1:
    ta = dim_x * dim_y
    h = dim_z
    yon_adi = "Alt Taban (a × b)"
elif direction == 2:
    ta = dim_x * dim_z
    h = dim_y
    yon_adi = "Ön Yüz (a × h)"
else:
    ta = dim_y * dim_z
    h = dim_x
    yon_adi = "Yan Yüz (b × h)"

total_volume = dim_x * dim_y * dim_z
current_cubes = ta * kat

# 3D Sahne için HTML/Three.js Şablonu
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; overflow: hidden; background-color: #f4f6f9; }}
        #canvas-container {{ width: 100vw; height: 500px; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="canvas-container"></div>
    <script>
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf4f6f9);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        
        // Işıklandırma
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(10, 20, 15);
        scene.add(dirLight);

        // Ana Dış Kutu (Şeffaf Prizma)
        const a = {dim_x}, b = {dim_y}, h = {dim_z};
        const boxGeo = new THREE.BoxGeometry(a, h, b);
        const boxMat = new THREE.MeshPhongMaterial({{
            color: 0x1976d2,
            transparent: true,
            opacity: 0.15,
            wireframe: false
        }});
        const outerBox = new THREE.Mesh(boxGeo, boxMat);
        outerBox.position.set(a/2, h/2, b/2);
        scene.add(outerBox);

        // Kutu Çerçevesi
        const edges = new THREE.EdgesGeometry(boxGeo);
        const lineMat = new THREE.LineBasicMaterial({{ color: 0x0d47a1, linewidth: 2 }});
        const wireframe = new THREE.LineSegments(edges, lineMat);
        wireframe.position.set(a/2, h/2, b/2);
        scene.add(wireframe);

        // Katman Küplerini Çizme
        const direction = {direction};
        const kat = {kat};
        const showSkeleton = {str(show_skeleton).lower()};

        const cubeGeo = new THREE.BoxGeometry(0.96, 0.96, 0.96);
        const cubeMat = new THREE.MeshPhongMaterial({{ color: direction === 1 ? 0x43a047 : (direction === 2 ? 0x8e24aa : 0xfb8c00) }});

        for(let x = 0; x < a; x++) {{
            for(let y = 0; y < b; y++) {{
                for(let z = 0; z < h; z++) {{
                    let shouldDraw = false;
                    
                    if (direction === 1 && z < kat) shouldDraw = true;
                    if (direction === 2 && y < kat) shouldDraw = true;
                    if (direction === 3 && x < kat) shouldDraw = true;

                    if (shouldDraw) {{
                        const mesh = new THREE.Mesh(cubeGeo, cubeMat);
                        mesh.position.set(x + 0.5, z + 0.5, y + 0.5);
                        scene.add(mesh);
                    }}
                }}
            }}
        }}

        // L-İskelet Gösterimi
        if (showSkeleton) {{
            const skelMat = new THREE.MeshPhongMaterial({{ color: 0xd32f2f, transparent: true, opacity: 0.4 }});
            for(let i=0; i<a; i++) {{
                const m = new THREE.Mesh(cubeGeo, skelMat);
                m.position.set(i+0.5, 0.5, 0.5);
                scene.add(m);
            }}
            for(let j=1; j<b; j++) {{
                const m = new THREE.Mesh(cubeGeo, skelMat);
                m.position.set(0.5, 0.5, j+0.5);
                scene.add(m);
            }}
            for(let k=1; k<h; k++) {{
                const m = new THREE.Mesh(cubeGeo, skelMat);
                m.position.set(0.5, k+0.5, 0.5);
                scene.add(m);
            }}
        }}

        // Kamera Konumu
        camera.position.set(a * 2.5, h * 2.5, b * 3);
        controls.target.set(a/2, h/2, b/2);
        controls.update();

        function animate() {{
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""

# Sol ve Sağ Kolon Düzeni
col_vis, col_info = st.columns([2, 1])

with col_vis:
    components.html(html_code, height=520)

with col_info:
    st.subheader("📐 Hacim Bağıntısı (V = TA × h)")
    
    st.info(f"""
    **Seçilen Taban:** {yon_adi}  
    **1. Katmandaki Küp Sayısı (Taban Alanı - TA):** `{ta}` br²  
    **Kat Sayısı (Yükseklik - h):** `{h}` br  
    """)

    st.metric("Toplam Prizma Hacmi (V)", f"{total_volume} br³")
    st.metric("Şu Anki Dolu Hacim", f"{current_cubes} br³", delta=f"%{round((current_cubes/total_volume)*100)} Doluluk")

    st.markdown("""
    ---
    **Kazanım Notu:**
    Prizmanın hacmi, tabanı oluşturan 1 birimküp katmanındaki küp sayısının (**Taban Alanı**), üst üste koyulan katman sayısı (**Yükseklik**) ile çarpılmasıyla hesaplanır.
    $$V = \\text{Taban Alanı} \\times \\text{Yükseklik} = TA \\cdot h$$
    """)
