document.addEventListener("DOMContentLoaded", () => {
  const calendar = document.getElementById("calendar");

  const meses = [
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro"
  ];

  const anoAtual = new Date().getFullYear();

  meses.forEach((mes, index) => {
    const mesDiv = document.createElement("div");
    mesDiv.classList.add("mes");

    const titulo = document.createElement("h2");
    titulo.textContent = mes;

    const diasContainer = document.createElement("div");
    diasContainer.classList.add("dias");

    const diasSemana = ["D", "S", "T", "Q", "Q", "S", "S"];
    diasSemana.forEach(dia => {
      const diaSemana = document.createElement("div");
      diaSemana.classList.add("dia-semana");
      diaSemana.textContent = dia;
      diasContainer.appendChild(diaSemana);
    });

    const primeiroDia = new Date(anoAtual, index, 1).getDay();
    const ultimoDia = new Date(anoAtual, index + 1, 0).getDate();

    for (let i = 0; i < primeiroDia; i++) {
      const vazio = document.createElement("div");
      vazio.classList.add("dia", "vazio");
      diasContainer.appendChild(vazio);
    }

    for (let dia = 1; dia <= ultimoDia; dia++) {
      const diaDiv = document.createElement("div");
      diaDiv.classList.add("dia");
      diaDiv.textContent = dia;

      const dataId = `${anoAtual}-${(index + 1).toString().padStart(2, "0")}-${dia.toString().padStart(2, "0")}`;
      diaDiv.dataset.data = dataId;

      diaDiv.addEventListener("click", () => {
        abrirModal(diaDiv);
      });

      diasContainer.appendChild(diaDiv);
    }

    mesDiv.appendChild(titulo);
    mesDiv.appendChild(diasContainer);
    calendar.appendChild(mesDiv);
  });

  carregarEventos();
});

function abrirModal(diaElemento) {
  removerModal();

  const data = diaElemento.dataset.data;

  const modal = document.createElement("div");
  modal.id = "modal";
  modal.className = "modal";

  modal.innerHTML = `
    <div class="modal-content">
      <h2>Adicionar Evento</h2>
      <form id="eventoForm">
        <input type="hidden" id="dataSelecionada" value="${data}" />
        
        <label for="tipo">Tipo:</label>
        <select id="tipo" required>
          <option value="">Selecione</option>
          <option value="feriado">Feriado</option>
          <option value="compromisso">Compromisso</option>
          <option value="tarefa">Tarefa</option>
        </select>

        <label for="descricao">Descrição:</label>
        <input type="text" id="descricao" required />

        <div class="botoes">
          <button type="submit">Salvar</button>
          <button type="button" id="cancelar">Cancelar</button>
        </div>
      </form>
    </div>
  `;

  document.body.appendChild(modal);

  document.getElementById("cancelar").addEventListener("click", removerModal);

  document.getElementById("eventoForm").addEventListener("submit", (e) => {
    e.preventDefault();

    const tipo = document.getElementById("tipo").value;
    const descricao = document.getElementById("descricao").value;

    if (!tipo || !descricao) return;

    const data = document.getElementById("dataSelecionada").value;
    const diaElemento = document.querySelector(`[data-data='${data}']`);
    if (diaElemento) {
      diaElemento.classList.remove("feriado", "compromisso", "tarefa");
      diaElemento.classList.add(tipo);
      diaElemento.title = descricao;
    }

    salvarEvento(data, tipo, descricao);
    removerModal();
  });
}

function removerModal() {
  const modalExistente = document.getElementById("modal");
  if (modalExistente) {
    modalExistente.remove();
  }
}

function salvarEvento(data, tipo, descricao) {
  const eventos = JSON.parse(localStorage.getItem("eventos")) || {};
  eventos[data] = { tipo, descricao };
  localStorage.setItem("eventos", JSON.stringify(eventos));
}

function carregarEventos() {
  const eventos = JSON.parse(localStorage.getItem("eventos")) || {};
  Object.entries(eventos).forEach(([data, evento]) => {
    const diaElemento = document.querySelector(`[data-data='${data}']`);
    if (diaElemento) {
      diaElemento.classList.add(evento.tipo);
      diaElemento.title = evento.descricao;
    }
  });
}
