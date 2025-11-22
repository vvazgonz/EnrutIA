from flask import Flask, render_template_string, request
import pandas as pd
from enrutador import enrutador

app = Flask(__name__)

HTML = '''
<!doctype html>
<title>¿Cuál sería el mejor modelo?</title>
<style>
body {
  background: #000;
  color: #fff;
  font-family: 'Segoe UI', 'Arial', sans-serif;
  margin: 0; padding: 0;
  min-height: 100vh;
}
h1 {
  text-align: center;
  margin-top: 40px;
  letter-spacing: 1px;
}
p {
  text-align: center;
  max-width: 650px; margin: 0 auto 25px auto;
}
form {
  max-width: 420px;
  margin: 32px auto 0 auto;
  padding: 32px 24px 25px 24px;
  border: 1px;
  display: flex; flex-direction: column;
  gap: 18px;
}
label {
  font-weight: 500;
}
input[type=range] {
  width: 140px;
  accent-color: #3085d6;
  background: transparent;
}
#slider_val {
  margin-left: 12px;
  font-size: 1em;
  font-family: "Segoe UI Mono", monospace;
}
input[type=text] {
  width: 100%;
  background-color: #000;
  color: #fff;
  font-size: 1em;
  padding: 6px 8px;
  border-radius: 7px;
  border: 1px solid #fff;
  margin-top: 4px;
}
button[type=submit] {
  margin-top: 16px;
  background: #3085d6;
  border: none;
  color: #fff;
  border-radius: 7px;
  font-size: 1.07em;
  font-family: inherit;
  padding: 9px 0;
  font-weight: 500;
  letter-spacing: 1px;
  box-shadow: 0 0 8px #3085d655;
  cursor: pointer;
  transition: background 0.18s, transform 0.15s;
}
div.respuesta {
  margin: 24px auto 0 auto;
  padding: 19px 17px;
  text-align: center;
  background: #242933;
  border-radius: 10px;
  border: 1px solid #3085d6aa;
  color: #f3f6fb;
  font-size: 1.15em;
  box-shadow: 0 0 12px #3085d640;
  max-width: 500px;
}
input[type=range] {
  width: 100%;
  background: transparent;
}

::-webkit-scrollbar { width: 8px; background: #31353c; }
::-webkit-scrollbar-thumb { background: #3085d680; border-radius: 6px;}
</style>
<h1>¿Cuál sería el mejor modelo?</h1>
<p>Entre o4-mini, GPT-4o-mini y Llama-3.1-8B, nuestro enrutador decidirá cuál es el mejor modelo, según tus preferencias, para obtener una respuesta y ser lo más sostenibles posibles.</p>
<form method="post">
  <label>k (0-2):</label>
  <input type="range" name="k" min="0" max="2" value="{{ k or 1 }}">
  <span id="slider_val">{{ k or 1 }}</span>
  <script>
    document.addEventListener('DOMContentLoaded', function () {
      let slider = document.querySelector('input[type="range"]');
      let output = document.getElementById('slider_val');
      slider.oninput = function() {
        output.textContent = this.value;
      }
    });
  </script>
  <br>
  <label>¿Qué pregunta tienes hoy?:</label>
  <input type="text" name="pregunta" value="{{ pregunta or '' }}"><br><br>
  <button type="submit" name="accion" value="Preguntar">Preguntar</button>
</form>

{% if resultado is not none %}
  <div style="margin-top:20px;">
    <b>Respuesta del enrutador:</b><br>
    {{ resultado | safe }}
  </div>
{% endif %}
'''

@app.route("/", methods=["GET", "POST"])
def main():
    resultado = None
    k = 1
    pregunta = ""
    if request.method == "POST":
        k = int(request.form["k"])
        pregunta = request.form["pregunta"]
        resultado = enrutador(k, pregunta)
    return render_template_string(HTML, resultado=resultado, k=k, pregunta=pregunta)

if __name__ == "__main__":
    app.run(debug=True)
