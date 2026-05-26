document.addEventListener('DOMContentLoaded', () => {
    // Lógica para garantir que jogadores de linha não sejam repetidos na escalação
    const escalacaoForm = document.querySelector('form[action="/update-escalacao"]');
    
    if (escalacaoForm) {
        const selects = Array.from(escalacaoForm.querySelectorAll('select[name="jogadores_linha"]'));

        const updateSelectOptions = () => {
            const selectedValues = new Set();
            // Primeiro, coleta todos os valores selecionados
            selects.forEach(s => {
                if (s.value) {
                    selectedValues.add(s.value);
                }
            });

            // Depois, itera sobre cada select para desabilitar as opções
            selects.forEach(currentSelect => {
                Array.from(currentSelect.options).forEach(option => {
                    // Desabilita a opção se ela foi selecionada em OUTRO select
                    // mas não no select atual (para permitir que a seleção atual permaneça visível)
                    if (option.value && selectedValues.has(option.value) && option.value !== currentSelect.value) {
                        option.disabled = true;
                    } else {
                        option.disabled = false;
                    }
                });
            });
        };

        // Adiciona o listener a todos os selects
        selects.forEach(s => {
            s.addEventListener('change', updateSelectOptions);
        });

        // Roda a função uma vez no carregamento da página para o caso de o formulário já vir preenchido
        updateSelectOptions();
    }
});
