import streamlit as st
from streamlit.components.v1 import html


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

        // Zoom functionality
        function imageZoom(imgID1, resultID1, imgID2, resultID2) {
            var img1, img2, lens1, lens2, result1, result2, cx, cy;
            img1 = document.getElementById(imgID1);
            img2 = document.getElementById(imgID2);
            result1 = document.getElementById(resultID1);
            result2 = document.getElementById(resultID2);
            /*create lens:*/
            lens1 = document.createElement("DIV");
            lens1.setAttribute("class", "img-zoom-lens");
            lens2 = document.createElement("DIV");
            lens2.setAttribute("class", "img-zoom-lens");
            /*insert lens:*/
            img1.parentElement.insertBefore(lens1, img1);
            img2.parentElement.insertBefore(lens2, img2);
            /*calculate the ratio between result DIV and lens:*/
            cx = result1.offsetWidth / lens1.offsetWidth;
            cy = result1.offsetHeight / lens1.offsetHeight;
            /*set background properties for the result DIVs:*/
            result1.style.backgroundImage = "url('" + img1.src + "')";
            result1.style.backgroundSize = (img1.width * cx) + "px " + (img1.height * cy) + "px";
            result2.style.backgroundImage = "url('" + img2.src + "')";
            result2.style.backgroundSize = (img2.width * cx) + "px " + (img2.height * cy) + "px";
            /*execute a function when someone moves the cursor over the images, or the lenses:*/
            lens1.addEventListener("mousemove", moveLens);
            img1.addEventListener("mousemove", moveLens);
            lens2.addEventListener("mousemove", moveLens);
            img2.addEventListener("mousemove", moveLens);
            /*and also for touch screens:*/
            lens1.addEventListener("touchmove", moveLens);
            img1.addEventListener("touchmove", moveLens);
            lens2.addEventListener("touchmove", moveLens);
            img2.addEventListener("touchmove", moveLens);

            function moveLens(e) {
                var pos, x, y;
                /*prevent any other actions that may occur when moving over the image:*/
                e.preventDefault();
                /*get the cursor's x and y positions:*/
                pos = getCursorPos(e);
                /*calculate the position of the lenses:*/
                x = pos.x - (lens1.offsetWidth / 2);
                y = pos.y - (lens1.offsetHeight / 2);
                /*prevent the lens from being positioned outside the images:*/
                if (x > img1.width - lens1.offsetWidth) {x = img1.width - lens1.offsetWidth;}
                if (x < 0) {x = 0;}
                if (y > img1.height - lens1.offsetHeight) {y = img1.height - lens1.offsetHeight;}
                if (y < 0) {y = 0;}
                /*set the position of the lenses:*/
                lens1.style.left = x + "px";
                lens1.style.top = y + "px";
                lens2.style.left = x + "px";
                lens2.style.top = y + "px";
                /*display what the lens "sees":*/
                result1.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
                result2.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
            }

            function getCursorPos(e) {
                var a, x = 0, y = 0;
                e = e || window.event;
                /*get the x and y positions of the images:*/
                a = img1.getBoundingClientRect();
                /*calculate the cursor's x and y coordinates, relative to the image:*/
                x = e.pageX - a.left;
                y = e.pageY - a.top;
                /*consider any page scrolling:*/
                x = x - window.pageXOffset;
                y = y - window.pageYOffset;
                return {x : x, y : y};
            }
        }

        // Initiate zoom effect:
        imageZoom("img1", "myresult1", "img2", "myresult2");
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

            .img-zoom-lens {{
                position: absolute;
                border: 1px solid #d4d4d4;
                /*set the size of the lens:*/
                width: 40px;
                height: 40px;
            }}

            .img-zoom-result {{
                border: 1px solid #d4d4d4;
                /*set the size of the result div:*/
                width: 300px;
                height: 300px;
            }}
        </style>

        <div id="container">
            <img id="img1" src="{st.session_state["default_image"]}" alt="Image 1">
            <img id="img2" src="{st.session_state["default_image"]}" alt="Image 2">
            <div id="divider"></div>
        </div>

        <div id="myresult1" class="img-zoom-result"></div>
        <div id="myresult2" class="img-zoom-result"></div>

        <input id="slider" type="range" min="0" max="100" value="50">
    """

    html(my_html, height=600)

    img = st.selectbox(
        label="",
        options=[
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
