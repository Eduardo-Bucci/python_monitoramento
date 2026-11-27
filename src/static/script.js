
function atualizarVaga(id, ocupada) {
    const bolinha = document.getElementById(`vaga-${id}`);

    if (!bolinha) {
        console.warn(`Vaga ${id} não encontrada no HTML.`);
        return;
    }

    bolinha.classList.remove(
        "livre",
        "ocupada",
        "indisponivel"
    );

    bolinha.classList.add(ocupada ? "ocupada" : "livre");
}

const statusArduino = document.getElementById("statusArduino");

async function buscarDados(){
    try{
        const response = await fetch("/status")
        const dados = await response.json()
        if(dados.status === "aguardando dados"){
            statusArduino.textContent = "Aguardando dados do Arduino..."
            return dados.status
        }
        atualizarVaga(1, dados.vaga_1 === "Ocupada")
        atualizarVaga(2, dados.vaga_2 === "Ocupada")
        atualizarVaga(3, dados.vaga_3 === "Ocupada")

        statusArduino.textContent = "Sistema no ar - Último leitura: " + dados.ultima_coleta

        document.getElementById("vagas_livres").textContent = 'Vagas Livres: ' + dados.vagas_livres
        document.getElementById("fluxo_dia").textContent = 'Fluxo de hoje: ' + dados.entrada_dia
        document.getElementById("porcentagem").textContent =  dados.lotado ? 'Estacionamento Lotado!' : 'Vagas ainda disponíveis'
        document.getElementById("alerta_lotado").textContent = 'Lotado: ' + dados.lotado

    }
    catch(error){
        statusArduino.textContent = "Erro na conexão com servidor"
    }
}

buscarDados()
setInterval(buscarDados, 1000)