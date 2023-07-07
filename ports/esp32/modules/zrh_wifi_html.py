from micropython import const

html = const('''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0,user-scalable=no"
    />
    <title>WiFi配置</title>
    <style>
      :root {
        --bg-color: #fff;
        --main-color: #3388ff;
      }
      html,
      body {
        padding: 10px;
        margin: 0;
        background-color: var(--bg-color);
        font-size: 16px;
        overflow: hidden;
      }
      * {
        box-sizing: border-box;
      }
      #ssid,
      #password {
        height: 45px;
        line-height: 45px;
        outline-color: var(--main-color);
        padding: 4px;
        font-size: 16px;
        border-style: solid;
        border-color: #dfdfdf;
        outline: none;
      }
      input:focus {
        border-color: var(--main-color);
      }
      .btn-send {
        width: 150px;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
        padding: 0;
        border: none;
        background-color: var(--main-color);
        margin: 0 auto;
      }
      .btn-send span {
        display: flex;
        width: 146px;
        height: 46px;
        justify-content: center;
        align-items: center;
        color: #fff;
        position: relative;
        z-index: 1;
        background-color: var(--main-color);

        font-size: 16px;
      }
      .btn-loading::after {
        content: "";
        width: 40px;
        height: 200px;
        background: linear-gradient(
          90deg,
          transparent,
          #ff9966,
          #ff9966,
          #ff9966,
          #ff9966,
          transparent
        );
        position: absolute;
        z-index: 0;
        animation: is-loading 3s linear infinite;
      }
      .item {
        display: flex;
        flex-direction: column;
        row-gap: 6px;
        margin-bottom: 6px;
      }
      .item-inline {
        display: flex;
        row-gap: 8px;
        margin-bottom: 20px;
        align-items: center;
      }
      #input-show-password {
        cursor: pointer;
        width: 20px;
        height: 20px;
      }
      .label-show-password {
        cursor: pointer;
        user-select: none;
        outline: none;
      }
      .error-text {
        font-size: 12px;
        color: red;
        opacity: 0;
        transition: opacity 0.4s;
      }
      #toast {
        width: 66vw;
        height: 100px;
        background-color: #171717;
        color: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 25%;
        z-index: 999;
        left: calc(50vw - 33vw);
        border-radius: 4px;
        box-shadow: 0 2px 20px 6px rgba(0, 0, 0, 0.2);
        user-select: none;
      }
      #mask-layer {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        backdrop-filter: blur(2px);
        z-index: 999;
        display: none;
      }
      @keyframes is-loading {
        from {
          transform: rotateZ(0);
        }
        to {
          transform: rotateZ(360deg);
        }
      }
    </style>
  </head>
  <body>
    <div class="item ssid">
      <label for="ssid">SSID</label>
      <input type="text" id="ssid" oninput="onInputChange(event)" />
      <div class="error-text">请输入SSID</div>
    </div>
    <div class="item password">
      <label for="password">密码</label>
      <input type="password" id="password" oninput="onInputChange(event)" />
      <div class="error-text">请输入密码</div>
    </div>
    <div class="item-inline">
      <input
        type="checkbox"
        id="input-show-password"
        onclick="onShowPassword(this.checked)"
      />
      <label class="label-show-password" for="input-show-password"
        >显示密码</label
      >
    </div>
    <button id="btn-send" class="btn-send" onclick="onSend(event)">
      <span id="btn-text">确认</span>
    </button>

    <div id="mask-layer">
      <div id="toast">配置成功</div>
    </div>

    <script>
      async function onSend(e) {
        const ssid = document.getElementById("ssid");
        const password = document.getElementById("password");

        const ssidValue = ssid.value;
        const passwordValue = password.value;

        if (!ssidValue) {
          document.querySelector(".ssid .error-text").style.opacity = 1;
          return;
        }
        if (!passwordValue) {
          document.querySelector(".password .error-text").style.opacity = 1;
          return;
        }

        const btnSend = document.getElementById("btn-send");
        const btnText = document.getElementById("btn-text");
        if (btnSend.classList.contains("btn-loading")) {
          console.log("请求中...");
          return;
        }

        ssid.setAttribute("disabled", "disabled");
        password.setAttribute("disabled", "disabled");
        btnText.innerText = "正在提交";
        btnSend.classList.toggle("btn-loading");
        console.log(ssidValue, passwordValue);
        
        const res = await fetch(`/cmd`, {
          method: "POST",
          body: JSON.stringify({
            cmd: "SET_WIFI",
            data: {
              ssid: ssidValue,
              password: passwordValue,
            },
          }),
        });
        const json = await res.json();

        console.log("res:", json);
        btnSend.classList.toggle("btn-loading");
        ssid.removeAttribute("disabled");
        password.removeAttribute("disabled");
        btnText.innerText = "确认";
      }

      function onInputChange(event) {
        const target = event.target;
        if (target.value) {
          if (target.nextElementSibling.style.opacity === 0) return;
          target.nextElementSibling.style.opacity = 0;
        } else {
          if (target.nextElementSibling.style.opacity === 1) return;
          target.nextElementSibling.style.opacity = 1;
        }
      }

      function onShowPassword(e) {
        document
          .getElementById("password")
          .setAttribute("type", e ? "text" : "password");
      }

      function onToast(text) {
        const eleMaskLayer = document.getElementById("mask-layer");
        const eleToast = document.getElementById("toast");
        eleMaskLayer.style.display = "flex";
        eleToast.innerText = text;
        setTimeout(() => {
          eleToast.innerText = "成功";
          eleMaskLayer.style.display = "none";
        }, 3000);
      }
    </script>
  </body>
</html>

''')
