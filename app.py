import streamlit as st
from streamlit.components.v1 import html


def main():
    movie = st.sidebar.selectbox("movie:", ["humanoid"])
    player = st.sidebar.selectbox("player:", ["Panasonic LX-900"])
    deinterlacer = st.sidebar.selectbox("de-interlacer:", ["Kramer VP-730AMP"])
    scaler = st.sidebar.selectbox("scaler:", ["DVDO VP-50Pro"])

    line_visibility = st.sidebar.checkbox("line divider", value=True)

    screencap_url = "http://localhost:8000"

    if not line_visibility:
        line_color = "transparent"
    else:
        line_color = st.sidebar.color_picker(
            "divider color", label_visibility="collapsed"
        )

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

    updateImages();

    function imageZoom(imgID, resultID) {
        var img, lens, result, cx, cy;
        img = document.getElementById(imgID);
        result = document.getElementById(resultID);
        lens = document.createElement("DIV");
        lens.setAttribute("class", "img-zoom-lens");
        img.parentElement.insertBefore(lens, img);
        cx = result.offsetWidth / lens.offsetWidth;
        cy = result.offsetHeight / lens.offsetHeight;
        result.style.backgroundImage = "url('" + img.src + "')";
        result.style.backgroundSize = (img.width * cx) + "px " + (img.height * cy) + "px";
        lens.addEventListener("mousemove", moveLens);
        img.addEventListener("mousemove", moveLens);
        lens.addEventListener("touchmove", moveLens);
        img.addEventListener("touchmove", moveLens);
        function moveLens(e) {
            var pos, x, y;
            e.preventDefault();
            pos = getCursorPos(e);
            x = pos.x - (lens.offsetWidth / 2);
            y = pos.y - (lens.offsetHeight / 2);
            if (x > img.width - lens.offsetWidth) {x = img.width - lens.offsetWidth;}
            if (x < 0) {x = 0;}
            if (y > img.height - lens.offsetHeight) {y = img.height - lens.offsetHeight;}
            if (y < 0) {y = 0;}
            lens.style.left = x + "px";
            lens.style.top = y + "px";
            result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
        }
        function getCursorPos(e) {
            var a, x = 0, y = 0;
            e = e || window.event;
            a = img.getBoundingClientRect();
            x = e.pageX - a.left;
            y = e.pageY - a.top;
            x = x - window.pageXOffset;
            y = y - window.pageYOffset;
            return {x : x, y : y};
        }
    }

    imageZoom('img1', 'zoomResult1');
    imageZoom('img2', 'zoomResult2');
    """

    my_html = f"""
    <style>
        #container {{
            position: relative;
            height: 300px;
            width: 600px;
            overflow: hidden;
        }}

        #img1, #img2 {{
            position: absolute;
            height: 300px;
            width: 600px;
        }}

        #divider {{
            position: absolute;
            height: 300px;
            width: 2px;
            background-color: {line_color};
        }}

        .img-zoom-lens {{
            position: absolute;
            border: 1px solid #d4d4d4;
            border-radius: 50%;
            cursor: zoom-in;
            width: 50px;
            height: 50px;
        }}

        .img-zoom-result {{
            border: 1px solid #d4d4d4;
            width: 200px;
            height: 200px;
            background-repeat: no-repeat;
            position: fixed;
            right: 30px;
            top: 30px;
        }}
    </style>
    <div id="container">
        <div>
            <img id="img1" src="{screencap_url}/humanoid/lx-900.png" />
            <div id="zoomResult1" class="img-zoom-result"></div>
        </div>
        <div>
            <img id="img2" src="{screencap_url}/humanoid/nr.png" />
            <div id="zoomResult2" class="img-zoom-result"></div>
        </div>
        <div id="divider"></div>
    </div>
    <input id="slider" type="range" min="0" max="100" value="50" style="width: 100%;">
    <script>{my_js}</script>
    """
    html(my_html, height=600)


if __name__ == "__main__":
    main()
