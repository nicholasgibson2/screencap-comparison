import streamlit as st
from streamlit.components.v1 import html
from streamlit_image_select import image_select


def main():
    movie = st.sidebar.selectbox("movie:", ["humanoid"])
    player = st.sidebar.selectbox("player:", ["Panasonic LX-900"])
    deinterlacer = st.sidebar.selectbox("de-interlacer:", ["Kramer VP-730AMP"])
    scaler = st.sidebar.selectbox("scaler:", ["DVDO VP-50Pro"])

    line_visibility = st.sidebar.checkbox("line divider", value=True)

    # screencap_url = "https://screencaps.blob.core.windows.net"
    screencap_url = "http://localhost:8000"

    if not line_visibility:
        line_color = "transparent"
    else:
        line_color = st.sidebar.color_picker(
            "divider color", label_visibility="collapsed"
        )

    # Define your javascript
    my_js = """
        let img1 = document.getElementById('img1');
        let img2 = document.getElementById('img2');
        let container = document.getElementById('container');
        let divider = document.getElementById('divider');

        let slider = document.getElementById('slider');

        function updateImages() {
            let slideValue = (slider.value / 100) * container.offsetWidth;
            img2.style.clip = 'rect(0, ' + slideValue + 'px, ' + container.offsetHeight + 'px, 0)';
            divider.style.left = slideValue + 'px';
        }

        slider.oninput = updateImages;

        // Call the function when the page loads
        updateImages();
    """

    if "default_image" not in st.session_state:
        st.session_state["default_image"] = f"{screencap_url}/humanoid/default.png"

    # Prepare html code
    my_html = f"""
        <style>
            body {{
                margin: 0;
                padding: 0;
            }}

            #container {{
                position: relative;
                height: 90vh;
                width: 100%;
                overflow: hidden;
            }}

            #img1, #img2 {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}

            #divider {{
                position: absolute;
                top: 0;
                height: 100%;
                width: 1px;
                background: {line_color};
            }}

            #img2 {{
                clip: rect(0, 50%, 100%, 0);
            }}
        </style>
        <div id="container">
            <img id="img1" src="{st.session_state['default_image']}" />
            <img id="img2" src="{screencap_url}/humanoid/nr.png" />
            <div id="divider"></div>
        </div>
        <input id="slider" type="range" min="0" max="100" value="50" style="width: 100%;">
        <script>{my_js}</script>
    """

    html(my_html, height=600)
    img = image_select(
        label="",
        images=[
            f"{screencap_url}/humanoid/default.png",
            f"{screencap_url}/humanoid/nr.png",
            f"{screencap_url}/humanoid/other.png",
        ],
    )

    if st.session_state["default_image"] != img:
        st.session_state["default_image"] = img
        st.experimental_rerun()


if __name__ == "__main__":
    main()
